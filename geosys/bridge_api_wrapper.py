# coding=utf-8
"""Implementation of Bridge API Wrapper.
"""
from geosys.bridge_api.api_abstract import ApiClient
from geosys.bridge_api.connection import ConnectionAPIClient
from geosys.bridge_api.default import IDENTITY_URLS, BRIDGE_URLS, ALL_REGIONS
from geosys.bridge_api.definitions import CROPS, SAMZ, OM
from geosys.bridge_api.field_level_maps import FieldLevelMapsAPIClient
from geosys.bridge_api.utilities import get_definition

from geosys.bridge_api.definitions import (
    SAMPLE_MAP,
    INSEASONFIELD_AVERAGE_NDVI,
    INSEASONFIELD_AVERAGE_LAI,
    INSEASONFIELD_AVERAGE_REVERSE_NDVI,
    INSEASONFIELD_AVERAGE_REVERSE_LAI
)

from geosys.utilities.utilities import log

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class AuthenticationError(BaseException):
    """Error when oauth token is missing for an authenticated request.
    """


class MapProduct(object):
    """Wrapper instance of Bridge API Coverage map product"""

    def __init__(self, map_data):
        """BRIDGE API Coverage map product wrapper class.

        :param map_data: Dictionary of API response from Bridge API Coverage
            call. example: {
                "type": "NDVI",
                "_links": {
                    "self": url_to_product,
                    "worldFile": url_to_product,
                    "thumbnail": url_to_product,
                    "legend": url_to_product,
                    "image:image/png": url_to_product,
                    "image:image/tiff+zip": url_to_product,
                    "image:application/shp+zip": url_to_product,
                    "image:application/vnd.google-earth.kmz": url_to_product,
                }
            }
        :type map_data: dict
        """
        self.map_data = map_data

    def map_type(self):
        """Get the type of the map product.

        :return: Map type (NDVI, NDVI, etc).
        :rtype: str
        """
        return self.map_data.get('type', '')

    def get_output_url(self, output_format):
        """Get the url of map product based on output format.

        :param output_format: Map output format.
        :type output_format: str

        :return: The url of map product.
        :rtype: str
        """
        return self.map_data.get('_links', {}).get(output_format, {})


class BridgeAPI(ApiClient):
    """Wrapper client for bridge api."""

    def __init__(
            self,
            username,
            password,
            region,
            client_id,
            client_secret,
            use_testing_service=False,
            identity_url=None,
            server_url=None,
            proxies=None):
        """Wrapper implementation for bridge api.

        :param username: Bridge API username.
        :type username: str

        :param password: Bridge API password.
        :type password: str

        :param region: Region of fields.
        :type region: str

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client Secret
        :type client_secret: str

        :param use_testing_service: Testing service flag.
        :type use_testing_service: bool

        :param proxies: Tuple of proxy definition.
            (proxy_host, proxy_port, proxy_user, proxy_password)
        :type proxies: tuple
        """
        super(BridgeAPI, self).__init__()
        self.username = username
        self.password = password
        self.region = region
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_testing_service = use_testing_service
        self.access_token = None
        if proxies:
            self.set_proxy(*proxies)

        # create server url
        self.identity_server = (IDENTITY_URLS[self.region]['test']
                                if self.use_testing_service
                                else identity_url or IDENTITY_URLS[self.region]['prod'])
        self.bridge_server = (server_url or BRIDGE_URLS[self.region]['test']
                              if self.use_testing_service
                              else server_url or BRIDGE_URLS[self.region]['prod'])

        # authenticate user
        self.authenticated, self.authentication_message = self.authenticate()

        if self.authenticated:
            super(BridgeAPI, self).__init__(access_token=self.access_token)
        else:
            raise AuthenticationError(self.authentication_message)

    @staticmethod
    def get_crops():
        """Get default crops.

        :return: List of crops available.
        :rtype: list
        """
        return CROPS.values()

    @staticmethod
    def get_regions():
        """Get default regions.

        :return: List of tuple of regions available.
        :rtype: list
        """
        regions = []
        for region in ALL_REGIONS:
            regions.append((region['key'], region['description']))
        return regions

    def authenticate(self):
        """Authenticate user using given credentials.

        :return: Authentication status and message.
        :rtype: tuple
        """
        try:
            api_client = ConnectionAPIClient(self.identity_server)
            response = api_client.get_access_token(
                self.username,
                self.password,
                self.client_id,
                self.client_secret)
            if response.get('access_token'):
                self.access_token = response['access_token']
                message = 'Authentication succeeded.'
                return True, message
            else:
                message = (
                    'Ensure your username, password, client id, and client '
                    'secret are valid for the selected region service and then'
                    'try again.')
                return False, message
        except KeyError:
            message = 'Please enter a correct region (NA or EU)'
            return False, message

    def get_catalog_imagery(self, geometry, crop, sowing_date, filters=None):
        """Get catalog imagery for given parameters.

        :param geometry: A geometry in WKT format.
        :type geometry: str

        :param crop: Crop type.
        :type crop: str

        :param sowing_date: Sowing date. YYYY-MM-DD
        :type sowing_date: str

        :param filters: Filter coverage results.
            example: {
                "Image.Date": "$gte:2010-01-01",
                "coverageType": "CLEAR"
            }
        :type filters: dict

        :return: JSON response.
            List of maps data specification based on given criteria.
        :rtype: list
        """
        # Construct parameter

        request_data = {
            "seasonFields": [
                {
                    "geometry": geometry,
                    "crop": crop,
                    "sowingDate": sowing_date,
                }
            ]
        }

        api_client = FieldLevelMapsAPIClient(
            self.access_token, self.bridge_server)
        coverages_json = api_client.get_catalog_imagery(
            request_data, filters=filters)

        return coverages_json

    def _get_field_map(
            self,
            map_type_key,
            request_data,
            n_planned=None,
            yield_val=None,
            min_yield_val=None,
            max_yield_val=None,
            sample_field_id=None,
            params=None,
            zone_count=None
    ):
        """Actual method to call field map creation request.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param request_data: Request data.
        :type request_data: dict

        :param params: Request parameters.
        :type params: dict

        :param n_planned: Value used for nitrogen maps
        :type n_planned: float

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        api_client = FieldLevelMapsAPIClient(
            self.access_token, self.bridge_server)
        field_map_json = api_client.get_field_map(
            map_type_key,
            request_data,
            n_planned,
            yield_val,
            min_yield_val,
            max_yield_val,
            sample_field_id,
            params,
            zone_count=zone_count)

        return field_map_json

    def get_hotspot(self, url):
        """Get zone hotspots.

        :return: JSON response.
            Map data specification based on given parameters.
        :rtype: dict
        """
        api_client = FieldLevelMapsAPIClient(
            self.access_token, self.bridge_server)
        map_json = api_client.get_hotspot(
            url)

        return map_json

    def get_hotspot(self, url, params, data):
        """Get zone hotspots.

        :return: JSON response.
            Map data specification based on given parameters.
        :rtype: dict
        """
        api_client = FieldLevelMapsAPIClient(
            self.access_token, self.bridge_server)
        map_json = api_client.get_hotspot(
            url, params, data)

        return map_json

    def get_field_map(
            self,
            map_type_key,
            season_field_id,
            season_field_geom,
            image_date,
            image_id=None,
            n_planned=1.0,
            yield_val=0,
            min_yield_val=0,
            max_yield_val=0,
            sample_map_data=None,
            sample_map_id=None,
            zone_count=None,
            **kwargs):
        """Get requested field map.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param season_field_id: ID of the season field.
        :param season_field_id: str

        :param image_date: Date of the image. yyyy-MM-dd
        :type image_date: str

        :param image_id: ID of the sensor image
        :type image_id: str

        :param n_planned: Value used for nitrogen maps
        :type n_planned: float

        :param yield_val: Average yield
        :type yield_val: float

        :param min_yield_val: Minimum yield
        :type min_yield_val: float

        :param max_yield_val: Maximum yield
        :type max_yield_val: float

        :param sample_map_data: Sample map request data
        :type sample_map_data: dict

        :param sample_map_id: Sample map ID from API call
        :type sample_map_id: str

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        nitrogen_maps = [
            INSEASONFIELD_AVERAGE_NDVI['key'],
            INSEASONFIELD_AVERAGE_LAI['key'],
            INSEASONFIELD_AVERAGE_REVERSE_NDVI['key'],
            INSEASONFIELD_AVERAGE_REVERSE_LAI['key']
        ]
        # Construct map creation parameters
        if map_type_key == SAMPLE_MAP['key']:
            # Only for Sample maps
            if sample_map_id is None:
                request_data = sample_map_data
                request_data.update(kwargs)
            else:
                request_data = None
        elif map_type_key == OM['key']:
            request_data = {
                'Image': {
                    "Id": image_id
                },
                "AverageOrganicMatter": 100,
                'SeasonField': {
                    'Id': season_field_id,
                    'geometry': season_field_geom
                }
            }
        elif map_type_key in nitrogen_maps:
            request_data = {
                'Image': {
                    "Id": image_id
                },
                'SeasonField': {
                    'Id': season_field_id,
                    'geometry': season_field_geom
                },
                "offset": 0,
                "gain": 0,
                "nPlanned": n_planned,
            }
        else:
            request_data = {
                'Image': {
                    "Id": image_id
                },
                'SeasonField': {
                    'Id': season_field_id,
                    'geometry': season_field_geom
                },
                "offset": 0,
                "gain": 0,
            }
        if 'data' in kwargs:
            request_data.update(kwargs.pop('data'))
        else:
            request_data.update(kwargs)

        # Get request parameters
        params = kwargs.get('params')

        return self._get_field_map(
            map_type_key,
            request_data,
            n_planned,
            yield_val,
            min_yield_val,
            max_yield_val,
            sample_map_id,
            params, zone_count=zone_count)

    def get_difference_map(
            self, map_type_key, season_field_geometry,
            earliest_image_date, latest_image_date, **kwargs):
        """Get requested difference map.

        Currently this only support NDVI and EVI map.

        :param map_type_key: Map type key.
        :type map_type_key: str

        :param season_field_id: ID of the season field.
        :param season_field_id: str

        :param earliest_image_date: Earliest date of the image. yyyy-MM-dd
        :type earliest_image_date: str

        :param latest_image_date: Latest date of the image. yyyy-MM-dd
        :type latest_image_date: str

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        # Construct map creation parameters
        request_data = {
            "SeasonField": {
                "Id": None,
                "geometry": season_field_geometry
            },
            "EarliestImage": {
                "Date": earliest_image_date
            },
            "LatestImage": {
                "Date": latest_image_date
            }
        }
        request_data.update(kwargs)

        # Get request parameters
        params = kwargs.get('params')

        map_type_definition = get_definition(map_type_key)
        difference_map_definition = map_type_definition['difference_map']

        return self._get_field_map(
            difference_map_definition['key'], request_data, params=params)

    def get_samz_map(
            self,
            geometry,
            list_of_image_ids,
            list_of_image_date=None,
            zone_count=0,
            **kwargs):
        """Get requested SAMZ map.

        :param season_field_id: ID of the season field.
        :param season_field_id: str

        :param list_of_image_ids: IDs of selected images.
        :param list_of_image_ids: list

        :param list_of_image_date: List of image date indicating the maps
            which are going to be compiled.
        :type list_of_image_date: list

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        # Construct map creation parameters
        request_data = {
            "SeasonField": {
                "Id": None,
                "geometry": geometry
            },
            "Images": [
                {"id": image_id} for image_id in list_of_image_ids
            ],
            "zoneCount": zone_count
        }

        return self._get_field_map(SAMZ['key'], request_data)

    def get_rx_map(
            self,
            url,
            source_map_id,
            zone_count=0,
            **kwargs):
        """Get requested RX map.

        :param source_map_id: ID of the season field.
        :param source_map_id: str

        :param list_of_image_ids: IDs of selected images.
        :param list_of_image_ids: list

        :param list_of_image_date: List of image date indicating the maps
            which are going to be compiled.
        :type list_of_image_date: list

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        # Construct map creation parameters
        api_client = FieldLevelMapsAPIClient(
            self.access_token, self.bridge_server)
        request_data = {
            "SourceMapId": source_map_id,
            "zoneCount": zone_count
        }
        request_data.update(kwargs)

        rx_json = api_client.get_rx_map(url, request_data)

        return rx_json
    
    def patch_rx_map(
            self,
            source_map_id,
            patch_data=None,
            **kwargs):
        """Patch requested RX map.

        :param source_map_id: ID of the season field.
        :param source_map_id: str

        :param patch_data: Patch data.
        :type patch_data: dict

        :param kwargs: Other map creation and request parameters.

        :return: JSON response.
            Map data specification based on given criteria.
        :rtype: dict
        """
        # Construct map creation parameters
        api_client = FieldLevelMapsAPIClient(
            self.access_token, self.bridge_server)
        rx_patch = api_client.patch_rx_map(source_map_id, patch_data)
        
        return rx_patch
    
