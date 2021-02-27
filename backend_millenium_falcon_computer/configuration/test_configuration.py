import os
from unittest import TestCase

from backend_millenium_falcon_computer.configuration.configuration import resource_dir, ConfigurationAppTest


class TestConfigurationApp(TestCase):
    def test_init_from_json_all_ok(self):
        json_data = {
            "autonomy": 10,
            "departure": "Tatooine",
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
        self.config._init_from_json(json_data)
        self.assertTrue(self.config.autonomy == 10)
        self.assertTrue(self.config.departure == "Tatooine")
        self.assertTrue(self.config.arrival == "Endor")
        self.assertTrue(self.config._routes_db == "universe.db")

    def test_init_from_json_all_wrong_values(self):
        json_data = {
            "autonomy": 15,
            "departure": "Coruscant",
            "arrival": "Mandalor",
            "routes_db": "universe.db"
        }
        self.config._init_from_json(json_data)
        self.assertFalse(self.config.autonomy == 10)
        self.assertFalse(self.config.departure == "Tatooine")
        self.assertFalse(self.config.arrival == "Endor")
        self.assertTrue(self.config._routes_db == "universe.db")

    def test_init_from_json_file_all_ok(self):
        json_config_file_location = os.path.join(resource_dir, "test_data/anything_can_go/millenium-falcon.json")
        json_config_file_location_folder = os.path.dirname(json_config_file_location)
        self.config.init_from_json_file(json_config_file_location)
        self.assertTrue(self.config.autonomy == 12)
        self.assertTrue(self.config.departure == "Dagobah")
        self.assertTrue(self.config.arrival == "Hoth")
        self.assertTrue(self.config._routes_db == "universe.db")
        self.assertTrue(self.config._json_config_file_path_folder == json_config_file_location_folder)
        self.assertTrue(
            self.config.full_route_db == os.path.join(resource_dir, json_config_file_location_folder, "universe.db"))

    def test_to_json_data(self):
        json_data = {
            "autonomy": 10,
            "departure": "Tatooine",
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
        self.config._init_from_json(json_data)
        json_data_from_config = self.config.to_json_data()
        self.assertTrue(json_data_from_config["autonomy"] == 10)
        self.assertTrue(json_data_from_config["departure"] == "Tatooine")
        self.assertTrue(json_data_from_config["arrival"] == "Endor")

    def setUp(self) -> None:
        self.config = ConfigurationAppTest()
