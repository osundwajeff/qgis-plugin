# coding=utf-8
"""This module contains default values used by Bridge API Interface.
"""

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"

DEFAULT_API_VER = 1

REGION_NA = {
    'key': 'na',
    'description': (
        'US Platform - Fields located in USA, Canada, and Australia.')
}
REGION_EU = {
    'key': 'eu',
    'description': (
        'Fields located in European Platform - Europe, South America and '
        'South Africa.')
}
ALL_REGIONS = [REGION_NA, REGION_EU]

IDENTITY_URLS = {
    'na': {
        'test': 'https://identity.preprod.geosys-na.com',
        'prod': 'https://identity.geosys-na.com'
    },
    'eu': {
        'test': 'https://identity.preprod.geosys-na.com',
        'prod': 'https://identity.geosys-eu.com'
    }
}
BRIDGE_URLS = {
    'na': {
        'test': 'https://api-pp.geosys-na.net',
        'prod': 'https://api.geosys-na.net'
    },
    'eu': {
        'test': 'https://api-pp.geosys-na.net',
        'prod': 'https://api.geosys-eu.net'
    }
}

HOTSPOT_URL = 'https://hotspots.aws.geosys.com/hotspots-processor'

VEGETATION_ENDPOINT = 'vegetation'
SAMZ_ENDPOINT = 'management-zones'
ELEVATION_ENDPOINT = 'topology-map'

CLIENT_ID = 'mapproduct_api'
CLIENT_SECRET = 'mapproduct_api.secret'
GRANT_TYPE = 'password'
SCOPE = 'openid offline_access'
MAX_FEATURE_NUMBERS = 10
DEFAULT_N_PLANNED = 0.01
DEFAULT_COVERAGE_PERCENT = 100

# Default parameters for map creation
DEFAULT_AVE_YIELD = 1.0
DEFAULT_MIN_YIELD = 1.0
DEFAULT_MAX_YIELD = 1.0
DEFAULT_ORGANIC_AVE = 0.0
DEFAULT_ZONE_COUNT = 0
DEFAULT_GAIN = 0.0
DEFAULT_OFFSET = 0.0

FIELD_MAPS_API_VERSION = 5

# Thumbnail URLs
COLOR_COMPOSITION_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/'
    'COLORCOMPOSITION/thumbnail.png')

NDVI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/NDVI/thumbnail.png'
)
NDWI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/NDWI/thumbnail.png'
)
NDMI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/NDMI/thumbnail.png'
)
GNDVI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/GNDVI/thumbnail.png'
)
EVI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/EVI/thumbnail.png'
)
CVI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/CVI/thumbnail.png'
)

NITROGEN_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/model-map/{nitrogen_map_type}/thumbnail.png')

S2REP_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/S2REP/thumbnail.png'
)
LAI_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/LAI/thumbnail.png'
)
CVIN_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/base-reference-map/CVIN/thumbnail.png'
)
YGM_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/yield-goal-map/YGM/thumbnail.png')

YPM_THUMBNAIL_URL = (
    '{bridge_url}/field-level-maps/v5/maps/yield-variability-map/YPM/thumbnail.png'
)

SAMZ_THUMBNAIL_URL = (
    '{bridge_url}/maps/management-zones-map/SAMZ/thumbnail.png'
)
SLOPE_THUMBNAIL_URL = (
    '{bridge_url}/maps/topology-map/SLOPE/thumbnail.png'
)

SAMPLEMAP_THUMBNAIL_URL = (
    '{bridge_url}/maps/sample/{mapType}/thumbnail.png')

OM_THUMBNAIL_URL = (
    '{bridge_url}/maps/organic-matter-map/OM/thumbnail.png')

# coverage filters
COVERAGE_TYPE = 'CoverageType'
COVERAGE_PERCENT = 'coveragePercent'
IMAGE_DATE = 'Image.Date'
IMAGE_SENSOR = 'Image.Sensor'
IMAGE_SOIL_MATERIAL = 'Image.SoilMaterial'
MASK = 'Mask'
MAPS_TYPE = 'Maps.Type'

# map creation parameters
YIELD_AVERAGE = 'HistoricalYieldAverage'
YIELD_MINIMUM = 'MinYieldGoal'
YIELD_MAXIMUM = 'MaxYieldGoal'
ORGANIC_AVERAGE = 'AverageOrganicMatter'
SAMZ_ZONE = 'zoneCount'
SAMZ_ZONING = 'zoning'
HOTSPOT = 'hotspot'
POSITION = 'position'
FILTER = 'filter'
ZONING_SEGMENTATION = 'zoningSegmentation'
GAIN = 'gain'
OFFSET = 'offset'

# map output format based on Bridge API

# file extension
PGW_EXT = '.pgw'
PNG_KMZ_EXT = '.png.kmz'
PNG_EXT = '.png'
TIFF_EXT = '.tiff'
SHP_EXT = '.shp'
KMZ_EXT = '.kmz'
KML_EXT = '.kml'
LEGEND_EXT = '.legend.png'

# API key
PNG_KMZ_KEY = 'image:application/vnd.google-earth.kmz+png'
PNG_KEY = 'image:image/png'
ZIPPED_TIFF_KEY = 'image:image/tiff+zip'
ZIPPED_SHP_KEY = 'image:application/shp+zip'
KMZ_KEY = 'image:application/vnd.google-earth.kmz'
KML_KEY = 'image:application/vnd.google-earth.kml'
THUMBNAIL_KEY = 'thumbnail'
LEGEND_KEY = 'legend'
WORLD_FILE_KEY = 'worldFile'
WORLD_FILE_KEY2 = 'worldfile'

PGW = {
    'api_key': WORLD_FILE_KEY,
    'extension': PGW_EXT
}
PGW2 = {
    'api_key': WORLD_FILE_KEY2,
    'extension': PGW_EXT
}
PNG = {
    'api_key': PNG_KEY,
    'extension': PNG_EXT
}
PNG_KMZ = {
    'api_key': PNG_KMZ_KEY,
    'extension': PNG_KMZ_EXT
}
ZIPPED_TIFF = {
    'api_key': ZIPPED_TIFF_KEY,
    'extension': TIFF_EXT
}
ZIPPED_SHP = {
    'api_key': ZIPPED_SHP_KEY,
    'extension': SHP_EXT
}
KMZ = {
    'api_key': KMZ_KEY,
    'extension': KML_EXT
}
KML = {
    'api_key': KML_KEY,
    'extension': KML_EXT
}
LEGEND = {
    'api_key': LEGEND_KEY,
    'extension': LEGEND_EXT
}

ZIPPED_FORMAT = [ZIPPED_TIFF, ZIPPED_SHP]
RASTER_FORMAT = [ZIPPED_TIFF, PNG, PNG_KMZ]
VECTOR_FORMAT = [ZIPPED_SHP, KML]
VALID_QGIS_FORMAT = [ZIPPED_TIFF, ZIPPED_SHP, KML, PNG, PNG_KMZ]
