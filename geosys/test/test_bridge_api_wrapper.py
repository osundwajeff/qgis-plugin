# coding=utf-8
"""Bridge API wrapper client test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""
import os
import unittest
from dataclasses import field

from geosys.bridge_api_wrapper import BridgeAPI

from multiprocessing import Process

from .mock.mock_http_server import MockApiServer

__copyright__ = "Copyright 2019, Kartoza"
__license__ = "GPL version 3"
__email__ = "rohmat@kartoza.com"
__revision__ = "$Format:%H$"


class BridgeAPIWrapperTest(unittest.TestCase):
    """Test Bridge API wrapper class works."""

    def setUp(self):
        """Runs before each test."""
        # self.username = os.environ.get('BRIDGE_API_USERNAME', None)
        # self.password = os.environ.get('BRIDGE_API_PASSWORD', None)

        self.username = 'test'
        self.password = 'test'

        self.app_server = MockApiServer()

        self.server = Process(target=self.app_server.run)
        self.server.start()

        message = ('API test server and its url need to be defined and available')

        self.assertIsNotNone(self.app_server, message)
        self.assertIsNotNone(self.app_server.url, message)

    def test_get_crops(self):
        """Test we can get all available crops from definition"""
        crops = BridgeAPI.get_crops()
        expected_crops = [
            'SUGARCANE',
            'CORN',
            'MILLET',
            'GRAPES',
            'OTHERS',
            'COTTON',
            'SUNFLOWER',
            'PEANUT',
            'SOYBEANS',
            'ORANGE',
            'RICE',
            'SORGHUM',
            'WINTER_DURUM_WHEAT',
            'WINTER_SOFT_WHEAT',
            'SPRING_DURUM_WHEAT',
            'SOFT_WHITE_SPRING_WHEAT',
            'TRITICALE',
            'WINTER_BARLEY',
            'SPRING_BARLEY',
            'WINTER_OSR']
        self.assertEqual(sorted(crops), sorted(expected_crops))

    def test_get_regions(self):
        """Test we can get all available regions from definition"""
        regions = BridgeAPI.get_regions()
        expected_regions = [
            ('na',
             'US Platform - Fields located in USA, Canada, and Australia.'),
            ('eu',
             'Fields located in European Platform - Europe, South America '
             'and South Africa.')]
        self.assertEqual(regions, expected_regions)

    def test_get_coverage(self):
        """Test we can successfully get the coverage."""

        geom = ("POLYGON(("
                "1.5614669851321183 43.43877959480905,"
                "1.5720241598147355 43.43877959480905,"
                "1.5720241598147355 43.43323264029555,"
                "1.5614669851321183 43.43323264029555,"
                "1.5614669851321183 43.43877959480905))")

        crop_type = 'CORN'
        sowing_date = '2024-01-01'

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='test',
            client_secret='test.secret',
            use_testing_service=False,
            identity_url=self.app_server.url,
            server_url=self.app_server.url
        )

        coverages = bridge_api.get_catalog_imagery(
            geometry=geom, crop=crop_type, sowing_date=sowing_date)
        self.assertTrue(len(coverages) > 0)

    def test_get_field_map(self):
        """Test we can successfully get the field map."""
        map_type_key = 'NDVI'
        season_field_id = 'nja3zv9'
        image_date = '2024-10-21'
        image_id = 'IKc73hpUQ71zsw94i77UI1lwJh7dcYFoTFwjoPfYPAq'

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='test',
            client_secret='test.secret',
            use_testing_service=False,
            identity_url=self.app_server.url,
            server_url=self.app_server.url
        )
        field_map = bridge_api.get_field_map(
            map_type_key, season_field_id, image_date, image_id
        )
        self.assertTrue('seasonField' in field_map)

    def test_get_difference_map(self):
        """Test we can successfully get the difference map."""
        map_type_key = 'NDVI'
        season_field_id = 'nja3zv9'
        earliest_image_date = '2024-10-21'
        latest_image_date = '2024-11-02'

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='test',
            client_secret='test.secret',
            use_testing_service=False,
            identity_url=self.app_server.url,
            server_url=self.app_server.url
        )
        field_map = bridge_api.get_difference_map(
            map_type_key, season_field_id,
            earliest_image_date, latest_image_date
        )

        self.assertTrue('seasonField' in field_map)

    def test_get_samz_map(self):
        """Test we can successfully get the SAMZ map."""
        season_field_id = 'nja3zv9'
        params = {'zoneCount': 5}
        images_ids = [
            'IKc73hpUQ726BpoqhQpaU8SfYGFYTAL5hhyYZq4PwFY',
            'IKc73hpUQ7258rG71UeO1lSjNsyqKnIvs5u5uNwBDPw',
            'IKc73hpUQ724bvftcz8VwUcNIu0zZd3Uh0ipmckxKHk',
            'IKc73hpUQ7245vMfZRcmMZTisN0Oh5pObBmZzfW5D76'
        ]

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='test',
            client_secret='test.secret',
            use_testing_service=False,
            identity_url=self.app_server.url,
            server_url=self.app_server.url
        )

        # test SAMZ auto
        field_map = bridge_api.get_samz_map(
            season_field_id, [], params=params)

        self.assertTrue('seasonField' in field_map)

        # test SAMZ custom
        field_map = bridge_api.get_samz_map(
            season_field_id, images_ids, params=params)

        self.assertTrue('seasonField' in field_map)

    def test_get_content(self):
        """Test we can successfully get the content of png response."""
        image_id = 'IKc73hpUQ6t1tqdBqbWqEsD4IMwNnwN2zsF6EO4BM2e'
        season_field = 'nja3zv9'

        thumbnail_url = (
            f"https://api-pp.geosys-na.net:443/field-level-maps/v5/"
            f"season-fields/{season_field}/coverage/{image_id}"
            "/base-reference-map/NDVI/thumbnail.png"
        )

        bridge_api = BridgeAPI(
            username=self.username,
            password=self.password,
            region='na',
            client_id='test',
            client_secret='test.secret',
            use_testing_service=False,
            identity_url=self.app_server.url,
            server_url=self.app_server.url
        )

        content = bridge_api.get_content(thumbnail_url)

        self.assertTrue(isinstance(content, bytes))

    def tearDown(self):
        self.server.terminate()
        self.server.join()


if __name__ == "__main__":
    suite = unittest.makeSuite(BridgeAPIWrapperTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
