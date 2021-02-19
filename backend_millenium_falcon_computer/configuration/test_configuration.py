import os
from unittest import TestCase

from backend_millenium_falcon_computer.configuration.configuration import ConfigurationApp, resource_dir


class TestConfigurationApp(TestCase):
    def test_init_from_json_all_ok(self):
        json_data = {
            "autonomy": 10,
            "departure": "Tatooine",
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
        config = ConfigurationApp()
        config._init_from_json(json_data)
        self.assertTrue(config.autonomy == 10)
        self.assertTrue(config.departure == "Tatooine")
        self.assertTrue(config.arrival == "Endor")
        self.assertTrue(config._routes_db == "universe.db")

    def test_init_from_json_all_wrong_values(self):
        json_data = {
            "autonomy": 15,
            "departure": "Coruscant",
            "arrival": "Mandalor",
            "routes_db": "universe.db"
        }
        config = ConfigurationApp()
        config._init_from_json(json_data)
        self.assertFalse(config.autonomy == 10)
        self.assertFalse(config.departure == "Tatooine")
        self.assertFalse(config.arrival == "Endor")
        self.assertTrue(config._routes_db == "universe.db")

    def test_init_from_json_file_all_ok(self):
        json_config_file_location = os.path.join(resource_dir, "test_data/millenium-falcon.json")
        json_config_file_location_folder = os.path.dirname(json_config_file_location)
        config = ConfigurationApp()
        config.init_from_json_file(json_config_file_location)
        self.assertTrue(config.autonomy == 12)
        self.assertTrue(config.departure == "Dagobah")
        self.assertTrue(config.arrival == "Hoth")
        self.assertTrue(config._routes_db == "universe.db")
        self.assertTrue(config._json_config_file_path_folder == json_config_file_location_folder)
        self.assertTrue(
            config.full_route_db == os.path.join(resource_dir, json_config_file_location_folder, "universe.db"))

    def test_to_json_data(self):
        json_data = {
            "autonomy": 10,
            "departure": "Tatooine",
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
        config = ConfigurationApp()
        config._init_from_json(json_data)
        json_data_from_config = config.to_json_data()
        self.assertTrue(json_data_from_config["autonomy"] == 10)
        self.assertTrue(json_data_from_config["departure"] == "Tatooine")
        self.assertTrue(json_data_from_config["arrival"] == "Endor")
