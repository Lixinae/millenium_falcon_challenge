import json
import os
import random
from typing import List, Dict

from backend_millenium_falcon_computer.configuration.configuration import generated_data_dir
from backend_millenium_falcon_computer.mass_data_generator.generator import get_list_planets


def generate_p_data(generate_planets_parameters: Dict) -> List:
    """
    Generate la liste des planetes au format json
    :param generate_planets_parameters: Dictionnaire avec toutes les informations de paramétrage
    :return:
    """
    planets_list = get_list_planets()
    planets_list_json = []
    previous_planets = [planets_list[0]]
    travel_time = random.randint(1, 10)
    planet_json = {
        "origin": planets_list[0],
        "destination": planets_list[1],
        "travel_time": travel_time,
    }
    planets_list_json.append(planet_json)

    number_planets = generate_planets_parameters["number_planets"]
    min_destinations = generate_planets_parameters["min_destinations"]
    max_destinations = generate_planets_parameters["max_destinations"]
    min_travel_time = generate_planets_parameters["min_travel_time"]
    max_travel_time = generate_planets_parameters["max_travel_time"]

    max_iterate = min(number_planets, len(planets_list))

    for origin in planets_list[1:max_iterate]:
        # Pour avoir de multiple destination par planete
        for i in range(min_destinations, max_destinations):
            travel_time = random.randint(min_travel_time, max_travel_time)
            destination = random.choice(previous_planets)
            planet_json = {
                "origin": origin,
                "destination": destination,
                "travel_time": travel_time,
            }
            combi_already_in_list = any(
                filter(lambda x: x["origin"] == origin and x["destination"] == destination, planets_list_json))
            if not combi_already_in_list:
                planets_list_json.append(planet_json)
        previous_planets.append(origin)
    return planets_list_json


def generate_planets_data(generate_planets_parameters: Dict, save_to_file: bool = False) -> List:
    planets_list = generate_p_data(generate_planets_parameters)

    if save_to_file:
        save_list_json_to_file(planets_list, "planets_json.json")
    return planets_list


def save_list_json_to_file(planets_list: List, filename: str) -> None:
    """
    Sauvegarde la liste json dans un fichier
    :param filename: Nom de fichier à sauvegarder
    :param planets_list: La liste des planètes
    """
    path = os.path.join(generated_data_dir, filename)
    with open(path, 'w', encoding='utf-8') as output_file:
        output_file.write("[\n")
        for json_elem in planets_list:
            json.dump(json_elem, output_file, ensure_ascii=False, indent=4)
            output_file.write(",\n")
        output_file.write("]")


def save_list_to_db(planets_list:List, db_session) -> None:
    pass