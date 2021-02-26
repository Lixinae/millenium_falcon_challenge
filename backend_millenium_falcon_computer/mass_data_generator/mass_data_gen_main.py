import json
import os

from backend_millenium_falcon_computer import init_db
from backend_millenium_falcon_computer.configuration.configuration import generated_data_dir, config
from backend_millenium_falcon_computer.mass_data_generator.empire_data_generator import generate_empire_data
from backend_millenium_falcon_computer.mass_data_generator.millenium_falcon_generator import generate_falcon_data
from backend_millenium_falcon_computer.mass_data_generator.planets_data_generator import generate_planets_data, \
    export_list_to_db

if __name__ == '__main__':

    generate_planets_parameters = {
        "number_planets": 60,
        "min_destinations": 1,
        "max_destinations": 5,
        "min_travel_time": 1,
        "max_travel_time": 6
    }
    generated_falcon = generate_falcon_data(5, 10, generate_planets_parameters["number_planets"])
    generated_planets = generate_planets_data(generate_planets_parameters)

    millenium_json_config_file = os.path.join(generated_data_dir, "millenium-falcon.json")

    config.init_from_json_file(millenium_json_config_file)
    init_db()
    export_list_to_db(generated_planets)
    numb_of_bounty_hunters = generate_planets_parameters["number_planets"]
    generated_empire = generate_empire_data(numb_of_bounty_hunters)


