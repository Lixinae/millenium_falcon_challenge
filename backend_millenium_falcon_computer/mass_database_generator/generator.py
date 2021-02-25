import json
import os
import random
from typing import List

from backend_millenium_falcon_computer.configuration.configuration import generated_data_dir


# Orm model
# class Routes(Base):
#     __tablename__ = "routes"
#     origin = Column(String(128), primary_key=True)
#     destination = Column(String(128), primary_key=True)
#     travel_time = Column(Integer, primary_key=True)

# Quand tu crée un élément il est forcément connecté a un ou plusieurs élément précédent, n'importe lequel
# Partir de ce moment là, si tu crée une infinité d'éléments, ton graphe sera toujours connexe
# Du coup t'as juste a faire un algo qui pour chaque élément créé, tu lui donne comme destination une planète déjà existant aléatoirement


def pick_random_name_not_picked_from_list() -> str:
    # Pioche un nom dans un liste de nom
    pass


def generate_list_of_planets(quantity) -> List[str]:
    planets_list = []
    for i in range(0, quantity):
        name = pick_random_name_not_picked_from_list()
        planets_list.append(name)
    # Todo ->
    return planets_list


def pick_random_from_previous_planets(previous_planets):
    return random.choice(previous_planets)


def generate_data(quantity) -> List[json]:
    # Ensemble de "quantity" planets
    planets_list = generate_list_of_planets(quantity)
    planets_list_json = []
    previous_planets = [planets_list[0]]
    travel_time = random.randint(1, 10)
    planet_json = {
        "origin": planets_list[0],
        "destination": planets_list[1],
        "travel_time": travel_time,
    }
    planets_list_json.append(planet_json)
    for origin in planets_list[1:]:
        travel_time = random.randint(1, 10)
        destination = pick_random_from_previous_planets(previous_planets)
        planet_json = {
            "origin": origin,
            "destination": destination,
            "travel_time": travel_time,
        }
        planets_list_json.append(planet_json)

    return planets_list_json


def generate(quantity: int, save_to_file: bool = False) -> List[json]:
    planets_list = generate_data(quantity)

    if save_to_file:
        save_json_to_file(planets_list)
    return planets_list


def save_json_to_file(planets_list: List[json]) -> None:
    """
    Sauvegarde la liste json dans un fichier
    :param planets_list: La liste des planètes
    """
    path = os.path.join(generated_data_dir, "big_db.json")
    with open(path, 'w', encoding='utf-8') as file:
        for planet_db in planets_list:
            json.dump(planet_db, file, ensure_ascii=False, indent=4)
            file.write("\n")


if __name__ == '__main__':
    generated_planets = generate(100)
