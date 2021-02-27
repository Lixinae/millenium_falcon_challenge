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
    Génère les données de l'empire
    :param numb_of_bounty_hunters: Nombre de chasseur de primes que l'on veut dans le système
    :return: Le json de l'empire avec toutes les informations
    """
    planets = get_list_planets()
    min_coutdown = int(len(planets)/5)
    max_countdown = min_coutdown*2
    countdown = random.randint(min_coutdown, max_countdown)
    empire_data = {
        "countdown": countdown,
        "bounty_hunters": []
    }
    for i in range(0, numb_of_bounty_hunters):
        bounty_hunter = {
            "planet": random.choice(planets),
            "day": random.randint(1, countdown - 1)
        }
        # Pour eviter les doublons
        if bounty_hunter not in empire_data["bounty_hunters"]:
            empire_data["bounty_hunters"].append(bounty_hunter)
    return empire_data


def generate_empire_data(numb_of_bounty_hunters: int,
                         save_to_file: bool = True,
                         filename: str = "empire.json") -> Dict:
    """
    Génère les données de l'empire et les sauvegarde dans le fichier "empire.json" dans le dossier "generated_data"
    :param filename: Nom du fichier de sauvegarde
    :param numb_of_bounty_hunters:
    :param save_to_file: Indique si l'on veut sauvegarder les données dans un fichier ou non
    :return: Le json de l'empire généré
    """
    empire_data = generate_e_data(numb_of_bounty_hunters)

    if save_to_file:
        save_empire_json_to_file(empire_data, filename)
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
