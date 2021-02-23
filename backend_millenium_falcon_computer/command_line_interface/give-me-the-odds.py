import json
import os
import sys

from backend_millenium_falcon_computer.configuration.configuration import config, resource_dir
from backend_millenium_falcon_computer.odds_success_calculator import calculator


def read_json_file(empire_json_file_: json):
    with open(empire_json_file_, 'r') as jsonfile:
        json_empire_ = json.load(jsonfile)
    return json_empire_


# Todo -> Cli
# Prend 2 fichier en entrée (les 2 json) give-me-the-odds example1/millenium-falcon.json example1/empire.json
if __name__ == '__main__':

    # Default values
    millenium_json_config_file = os.path.join(resource_dir, "example1/millenium-falcon.json")
    empire_json_file = os.path.join(resource_dir, "example1/empire.json")

    if len(sys.argv) == 3:
        millenium_json_config_file = sys.argv[1]
        empire_json_file = sys.argv[2]
    else:
        print("No files provided in input, it should be in the format:")
        print("give-me-the-odds example1/millenium-falcon.json example1/empire.json")
        print("Now using the default values provided")
        print("Default files are: \n" + millenium_json_config_file + "\n" + empire_json_file)

    config.init_from_json_file(millenium_json_config_file)
    json_empire = read_json_file(empire_json_file)

    odds_of_success_info = calculator.calculate_best_odds_of_success(json_empire)
    if not odds_of_success_info:
        print(0)
    else:
        print(odds_of_success_info["odds_of_success"])
