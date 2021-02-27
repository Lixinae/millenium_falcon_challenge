import os

from backend_millenium_falcon_computer.configuration.configuration import resource_dir


def get_list_planets():
    """
    Lit le fichier "planets.txt" et stock le contenu dans une liste
    :return: La liste des planets
    """
    path = os.path.join(resource_dir, "planets.txt")
    with open(path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()
        planets = [x.strip() for x in lines]
    return list(set(planets))
