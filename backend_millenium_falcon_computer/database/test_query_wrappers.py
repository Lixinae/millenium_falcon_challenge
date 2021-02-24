import os
from unittest import TestCase

from backend_millenium_falcon_computer import resource_dir
from backend_millenium_falcon_computer.configuration.configuration import config
from backend_millenium_falcon_computer.database import init_db
from backend_millenium_falcon_computer.database.query_wrappers import *


class TestQueriesDatabase(TestCase):
    def test_query_all_routes(self):
        all_routes = self.query_wrappers.query_all_routes()
        self.assertEqual(len(all_routes), 5)
        for route in all_routes:
            route_json = route.to_json()
            self.assertTrue("origin" in route_json)
            self.assertTrue("destination" in route_json)
            self.assertTrue("travel_time" in route_json)

    def test_query_specific_origin_ok(self):
        all_routes = self.query_wrappers.query_specific_origin("Tatooine")
        self.assertEqual(len(all_routes), 2)
        for route in all_routes:
            route_json = route.to_json()
            self.assertEqual(route_json["origin"], "Tatooine")

    def test_query_specific_origin_nok(self):
        all_routes = self.query_wrappers.query_specific_origin("Randomness")
        self.assertEqual(len(all_routes), 0)

    def test_query_specific_destination_ok(self):
        all_routes = self.query_wrappers.query_specific_destination("Dagobah")
        self.assertEqual(len(all_routes), 1)
        self.assertEqual(all_routes[0].destination, "Dagobah")

    def test_query_specific_destination_nok(self):
        all_routes = self.query_wrappers.query_specific_destination("Randomness")
        self.assertEqual(len(all_routes), 0)

    def test_query_specific_origin_destination_ok(self):
        all_routes = self.query_wrappers.query_specific_origin_destination("Tatooine", "Dagobah")
        self.assertEqual(len(all_routes), 1)
        self.assertEqual(all_routes[0].destination, "Dagobah")

    def test_query_specific_origin_destination_nok(self):
        all_routes = self.query_wrappers.query_specific_origin_destination("Endor", "Dagobah")
        self.assertEqual(len(all_routes), 0)

    def test_query_specific_travel_time_ok(self):
        all_routes = self.query_wrappers.query_specific_travel_time(1)
        self.assertEqual(len(all_routes), 2)

    def test_query_specific_travel_time_nok(self):
        all_routes = self.query_wrappers.query_specific_travel_time(100)
        self.assertEqual(len(all_routes), 0)

    def setUp(self) -> None:
        self.test_data_folder = os.path.join(resource_dir, "test_data")
        self.millenium_json_config_file = os.path.join(self.test_data_folder, "example1/millenium-falcon.json")
        config.init_from_json_file(self.millenium_json_config_file)
        init_db()
        self.query_wrappers = QueryWrappers()
