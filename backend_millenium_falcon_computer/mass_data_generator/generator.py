import os

from backend_millenium_falcon_computer.configuration.configuration import generated_data_dir, resource_dir


# Orm model
# class Routes(Base):
#     __tablename__ = "routes"
#     origin = Column(String(128), primary_key=True)
#     destination = Column(String(128), primary_key=True)
#     travel_time = Column(Integer, primary_key=True)

# Quand tu crée un élément il est forcément connecté a un ou plusieurs élément précédent, n'importe lequel
# Partir de ce moment là, si tu crée une infinité d'éléments, ton graphe sera toujours connexe
# Du coup t'as juste a faire un algo qui pour chaque élément créé, tu lui donne comme destination une planète déjà existant aléatoirement


def get_list_planets():
    path = os.path.join(resource_dir, "planets.txt")
    with open(path, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()
        planets = [x.strip() for x in lines]  # Todo -> lire un fichier avec les entrées
    return list(set(planets))
