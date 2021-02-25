import json
import os
import random
from typing import Dict

from backend_millenium_falcon_computer.configuration.configuration import generated_data_dir
from backend_millenium_falcon_computer.mass_data_generator.generator import get_list_planets


####################################
###### Empire Generation Data ######
####################################
def generate_e_data(numb_of_bounty_hunters: int) -> json:
    """

    :param numb_of_bounty_hunters:
    :return:
    """
    planets = get_list_planets()
    max_countdown = 100
    empire_data = {
        "countdown": random.randint(5, max_countdown),
        "bounty_hunters": []
    }
    for i in range(0, numb_of_bounty_hunters):
        bh = {
            "planet": random.choice(planets),
            "day": random.randint(1, max_countdown - 1)
        }
        # Pour eviter les doublons
        if bh not in empire_data["bounty_hunters"]:
            empire_data["bounty_hunters"].append(bh)
    return empire_data


def generate_empire_data(numb_of_bounty_hunters: int, save_to_file: bool = True) -> Dict:
    """

    :param numb_of_bounty_hunters:
    :param save_to_file: Indique si l'on veut sauvegarder les données dans un fichier ou non
    :return:
    """
    empire_data = generate_e_data(numb_of_bounty_hunters)

    if save_to_file:
        save_empire_json_to_file(empire_data, "empire.json")
    return empire_data


def save_empire_json_to_file(empire_data: json, filename: str) -> None:
    """
    Sauvegarde le json dans un fichier
    :param filename: Nom de fichier à sauvegarder
    :param empire_data: Le json à sauvegarder
    """
    path = os.path.join(generated_data_dir, filename)
    with open(path, 'w', encoding='utf-8') as output_file:
        json.dump(empire_data, output_file, ensure_ascii=False, indent=4)
        output_file.write("\n")
