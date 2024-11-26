# -*- coding: utf-8 -*-

"""
/***************************************************************************
 GeosysProcessingProvider
                                 A QGIS plugin
 GeosysProcessingProvider
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-03-30
        copyright            : (C) 2019 by Kartoza Pty. Ltd
        email                : rohmat@kartoza.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import tempfile

from PyQt5.QtCore import QCoreApplication, QDate, QSettings
from PyQt5.QtWidgets import QDateEdit
from processing.gui.wrappers import WidgetWrapper
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterRasterDestination,
    QgsProcessingParameterEnum,
    QgsProcessingParameterString,
    QgsCoordinateReferenceSystem,
    QgsProcessingParameterNumber)

from geosys.bridge_api.default import (
    ZIPPED_TIFF_KEY, TIFF_EXT, MAPS_TYPE, IMAGE_SENSOR, IMAGE_DATE, MAP_LIMIT,
    ZIPPED_TIFF, YIELD_AVERAGE, YIELD_MINIMUM, YIELD_MAXIMUM, ORGANIC_AVERAGE,
    SAMZ_ZONE)
from geosys.bridge_api.definitions import ARCHIVE_MAP_PRODUCTS, SENSORS, \
    ALL_SENSORS
from geosys.bridge_api_wrapper import BridgeAPI
from geosys.ui.widgets.geosys_coverage_downloader import (
    credentials_parameters_from_settings, create_map)
from geosys.utilities.downloader import fetch_data, extract_zip
from geosys.utilities.gui_utilities import reproject
from geosys.utilities.qgis_settings import QGISSettings
from geosys.utilities.settings import setting

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class DateWidgetWrapper(WidgetWrapper):
    """QDateEdit widget wrapper.

    WidgetWrapper for QgsProcessingParameterString that create and manage
    a QDateEdit widget.
    """
    def createWidget(self):
        """Override method."""
        self.date_edit = QDateEdit()
        self.date_edit.setDisplayFormat('yyyy-MM-dd')
        self.date_edit.setCalendarPopup(True)
        current_date = QDate.currentDate()
        self.date_edit.setDate(current_date)
        return self.date_edit

    def setValue(self, value):
        """Override method."""
        date = QDate.fromString(value, 'yyyy-MM-dd')
        self.date_edit.setDate(date)

    def value(self):
        """Override method."""
        return self.date_edit.date().toString('yyyy-MM-dd')


class MapCoverageDownloader(QgsProcessingAlgorithm):
    """Extended QgsProcessingAlgorithm class for GEOSYS coverage downloader.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT = 'INPUT'
    COVERAGE_DATE = 'COVERAGE_DATE'
    MAP_PRODUCT = 'MAP_PRODUCT'
    SENSOR = 'SENSOR'
    OUTPUT = 'OUTPUT'

    SENSOR_OPTIONS = [ALL_SENSORS] + SENSORS

    def tr(self, string):
        """Translate string on processing context."""
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        """MapCoverageDownloader instance."""
        return MapCoverageDownloader()

    def name(self):
        """Unique name of the algorithm.

        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'geosys_get_field_level_map'

    def displayName(self):
        """Display name of the algorithm.

        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Get field level map')

    def initAlgorithm(self, config=None):
        """Algorithm initialisation.

        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        # Coverage parameters from settings
        settings = QSettings()
        self.crop_type = setting(
            'crop_type', expected_type=str, qsettings=settings)
        self.sowing_date = setting(
            'sowing_date', expected_type=str, qsettings=settings)
        self.output_dir = setting(
            'output_directory', expected_type=str, qsettings=settings)

        # We add the input vector features source. It only allows polygon.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Coverage layer'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        # Coverage date. Will search the most recent map product prior to
        # the coverage date.
        date_param = QgsProcessingParameterString(
            self.COVERAGE_DATE, self.tr('Coverage date'))
        date_param.setMetadata({
            'widget_wrapper': {
                'class': DateWidgetWrapper
            }
        })
        self.addParameter(date_param)

        # Map products options.
        map_products = []
        for map_product in ARCHIVE_MAP_PRODUCTS:
            map_products.append(map_product['key'])
        self.addParameter(
            QgsProcessingParameterEnum(
                self.MAP_PRODUCT,
                self.tr('Map product'),
                options=map_products,
                defaultValue=0
            )
        )

        # Sensor options.
        sensors = []
        for sensor in self.SENSOR_OPTIONS:
            sensors.append(sensor['key'])
        self.addParameter(
            QgsProcessingParameterEnum(
                self.SENSOR,
                self.tr('Sensor'),
                options=sensors,
                defaultValue=0
            )
        )

        # Output directory where the map product of the coverage search will be
        # placed.
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT,
                self.tr('Output layer')
            ), createOutput=True
        )

    def processAlgorithm(self, parameters, context, feedback):
        """Here is where the processing itself takes place.
        """
        # Retrieve the feature source.
        source = self.parameterAsSource(parameters, self.INPUT, context)

        # Reproject layer to EPSG:4326
        if source.sourceCrs().authid() != 'EPSG:4326':
            source = reproject(
                source, QgsCoordinateReferenceSystem('EPSG:4326'))

        # Handle multi features
        # Merge features into multi-part polygon
        # TODO use Collect Geometries processing algorithm
        geom = None
        for index, feature in enumerate(source.getFeatures()):
            if not feature.hasGeometry() or not (
                    feature.geometry().isGeosValid()):
                continue
            if not geom:
                geom = feature.geometry()
            else:
                geom = geom.combine(feature.geometry())

        if geom:
            geom_wkt = geom.asWkt()
        else:
            # geometry is not valid
            return False, 'Geometry is not valid.'

        # Retrieve the coverage date.
        coverage_date = self.parameterAsString(
            parameters, self.COVERAGE_DATE, context)

        # Retrieve the selected map product.
        map_product_index = self.parameterAsEnum(
            parameters, self.MAP_PRODUCT, context)
        map_product = ARCHIVE_MAP_PRODUCTS[map_product_index]['key']

        # Retrieve the selected sensor type.
        sensor_index = self.parameterAsEnum(parameters, self.SENSOR, context)
        sensor_type = self.SENSOR_OPTIONS[sensor_index]['key']
        if sensor_type == ALL_SENSORS['key']:
            sensor_type = None

        # Retrieve output layer destination.
        self.output_destination = self.parameterAsOutputLayer(
            parameters, self.OUTPUT, context)

        filters = {
            MAPS_TYPE: map_product,
            IMAGE_DATE: '$lte:{}'.format(coverage_date),
            MAP_LIMIT: 1  # only get the recent one
        }
        sensor_type and filters.update({
            IMAGE_SENSOR: sensor_type
        })

        # Start coverage search
        bridge_api = BridgeAPI(
            *credentials_parameters_from_settings(),
            proxies=QGISSettings.get_qgis_proxy())

        results = bridge_api.get_catalog_imagery(
            geom_wkt, self.crop_type, self.sowing_date,
            filters=filters)

        if isinstance(results, dict) and results.get('message'):
            # TODO handle model_validation_error
            raise Exception(results['message'])

        if len(results) > 0:
            # Compute the number of steps to display within the progress bar
            total = 100.0 / len(results)
            for index, result in enumerate(results):
                # Stop the algorithm if cancel button has been clicked
                if feedback.isCanceled():
                    break

                # Update the progress bar
                progress_text = (
                    'Downloading {} of {} maps...'.format(
                        index+1, len(results)))
                feedback.setProgressText(progress_text)

                downloaded_path, message = self.download_map(result)

                feedback.pushInfo(downloaded_path)
                feedback.setProgress(int((index+1) * total))
        else:
            message = self.tr(
                'No coverage result available based on given parameters')

        return {
            self.OUTPUT: self.output_destination,
            'message': message
        }

    def download_map(self, coverage_map_json):
        """Download map directly from the coverage search result.

        :param coverage_map_json: Result of single map coverage.
            example: {
                "seasonField": {
                    "id": "zgzmbrm",
                    "customerExternalId": "..."
                },
                "image": {
                    "date": "2018-10-18",
                    "sensor": "SENTINEL_2",
                    "soilMaterial": "BARE"
                },
                "maps": [
                    {
                        "type": "NDVI",
                        "_links": {
                            "self": "the_url",
                            "worldFile": "the_url",
                            "thumbnail": "the_url",
                            "legend": "the_url",
                            "image:image/png": "the_url",
                            "image:image/tiff+zip": "the_url",
                            "image:application/shp+zip": "the_url",
                            "image:application/vnd.google-earth.kmz": "the_url"
                        }
                    }
                ],
                "coverageType": "CLEAR"
            }
        :type coverage_map_json: dict
        """
        bridge_api = BridgeAPI(
            *credentials_parameters_from_settings(),
            proxies=QGISSettings.get_qgis_proxy())

        # Get the requested map format. For now, use Raster (.tiff)
        map_format = ZIPPED_TIFF_KEY
        map_extension = TIFF_EXT

        map_urls = coverage_map_json['maps'][0]['_links']
        url = map_urls.get(map_format)

        message = self.tr(
            'Please check your output directory for the result.')

        if url:
            # Download zipped map and extract it in requested format.
            zip_path = tempfile.mktemp('{}.zip'.format(map_extension))

            fetch_data(url, zip_path, headers=bridge_api.headers)
            extract_zip(zip_path, self.output_destination)
        else:
            # download map using get field map request
            settings = QSettings()
            data = {
                YIELD_AVERAGE: setting(
                    YIELD_AVERAGE, expected_type=int, qsettings=settings),
                YIELD_MINIMUM: setting(
                    YIELD_MINIMUM, expected_type=int, qsettings=settings),
                YIELD_MAXIMUM: setting(
                    YIELD_MAXIMUM, expected_type=int, qsettings=settings),
                ORGANIC_AVERAGE: setting(
                    ORGANIC_AVERAGE,
                    expected_type=int, qsettings=settings),
                SAMZ_ZONE: setting(
                    SAMZ_ZONE, expected_type=int, qsettings=settings),
            }
            is_success, message = create_map(
                coverage_map_json,
                os.path.dirname(self.output_destination),
                os.path.basename(self.output_destination),
                ZIPPED_TIFF, data)
            if not is_success:
                message = self.tr('Error creating map. {}').format(message)

        return self.output_destination, message
