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

    # Todo -> Remplacer par arguments ligne de commande
    millenium_json_config_file = os.path.join(resource_dir, "example4/millenium-falcon.json")
    empire_json_file = os.path.join(resource_dir, "example2/empire.json")

    config.init_from_json_file(millenium_json_config_file)
    json_empire = read_json_file(empire_json_file)

    odds_of_success_info = calculator.calculate_best_odds_of_success(json_empire)
    if not odds_of_success_info:
        print(0)
    else:
        print(odds_of_success_info["odds_of_success"])
