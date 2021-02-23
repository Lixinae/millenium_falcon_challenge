import os
import unittest

from backend_millenium_falcon_computer import resource_dir
from backend_millenium_falcon_computer.configuration.configuration import config
from backend_millenium_falcon_computer.database import init_db
from backend_millenium_falcon_computer.odds_success_calculator import calculator
from backend_millenium_falcon_computer.command_line_interface.give_me_the_odds import read_json_file


class GiveMeTheOddsTests(unittest.TestCase):
    def test_example_1(self):
        millenium_json_config_file = os.path.join(self.test_data_folder, "example1/millenium-falcon.json")
        empire_json_file = os.path.join(self.test_data_folder, "example1/empire.json")
        config.init_from_json_file(millenium_json_config_file)
        init_db()
        json_empire = read_json_file(empire_json_file)
        odds_of_success_info = calculator.calculate_best_odds_of_success(json_empire)
        odds_of_success = 0
        if odds_of_success_info:
            odds_of_success = odds_of_success_info["odds_of_success"]
            self.assertEqual(odds_of_success, 0)
        else:
            self.assertEqual(odds_of_success, 0)

    def test_example_2(self):
        millenium_json_config_file = os.path.join(self.test_data_folder, "example2/millenium-falcon.json")
        empire_json_file = os.path.join(self.test_data_folder, "example2/empire.json")
        config.init_from_json_file(millenium_json_config_file)
        init_db()
        json_empire = read_json_file(empire_json_file)
        odds_of_success_info = calculator.calculate_best_odds_of_success(json_empire)
        odds_of_success = 0
        if odds_of_success_info:
            odds_of_success = odds_of_success_info["odds_of_success"]
            self.assertEqual(odds_of_success, 81)
        else:
            self.assertEqual(odds_of_success, 0)

    def test_example_3(self):
        millenium_json_config_file = os.path.join(self.test_data_folder, "example3/millenium-falcon.json")
        empire_json_file = os.path.join(self.test_data_folder, "example3/empire.json")
        config.init_from_json_file(millenium_json_config_file)
        init_db()
        json_empire = read_json_file(empire_json_file)
        odds_of_success_info = calculator.calculate_best_odds_of_success(json_empire)
        odds_of_success = 0
        if odds_of_success_info:
            odds_of_success = odds_of_success_info["odds_of_success"]
            self.assertEqual(odds_of_success, 90)
        else:
            self.assertEqual(odds_of_success, 0)

    def test_example_4(self):
        millenium_json_config_file = os.path.join(self.test_data_folder, "example4/millenium-falcon.json")
        empire_json_file = os.path.join(self.test_data_folder, "example4/empire.json")
        config.init_from_json_file(millenium_json_config_file)
        init_db()
        json_empire = read_json_file(empire_json_file)
        odds_of_success_info = calculator.calculate_best_odds_of_success(json_empire)
        odds_of_success = 0
        if odds_of_success_info:
            odds_of_success = odds_of_success_info["odds_of_success"]
            self.assertEqual(odds_of_success, 100)
        else:
            self.assertEqual(odds_of_success, 0)

    def setUp(self) -> None:
        self.test_data_folder = os.path.join(resource_dir, "test_data")


if __name__ == '__main__':
    unittest.main()
