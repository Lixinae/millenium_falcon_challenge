import json
from typing import List

from backend_millenium_falcon_computer.configuration.configuration import config
from backend_millenium_falcon_computer.database.query_wrappers import query_all_routes, \
    query_specific_origin_destination, query_specific_origin
from backend_millenium_falcon_computer.trajectory.trajectory import Trajectory


def fetch_data_from_db() -> json:
    return query_all_routes()


def fetch_data_from_config(config_informations):
    """

    :param config_informations: Les informations de configuration
    :return: Un json des informations de configuration
    """
    json_config = config_informations.to_json_data()
    # json_config = {
    #     "autonomy": config_informations.autonomy,
    #     "departure": config_informations.departure,
    #     "arrival": config_informations.arrival,
    # }
    return json_config


def calculate_odds_of_success(json_from_empire: json, config_informations=config) -> int:
    """

    :param json_from_empire:
    :param config_informations: La configuration utilisé, soit celle par defaut, soit à partir d'un fichier lu en entrée
    :return: Les chances de succès
    """
    json_from_db = fetch_data_from_db()
    json_config = fetch_data_from_config(config_informations)
    return calculte_odds(json_config, json_from_db, json_from_empire)


# json_config
# {
#   "autonomy": 6,
#   "departure": "Tatooine",
#   "arrival": "Endor",
# }

# json_from_db
# [{
# origin: "Tatooine",
# destination: "Dagobah",
# travel_time: 6
# }
# , {
# origin: "Dagobah",
# destination: "Endor",
# travel_time: 4
# }
# , {
# origin: "Dagobah",
# destination: "Hoth",
# travel_time: 1
# }
# , {
# origin: "Hoth",
# destination: "Endor",
# travel_time: 1
# }
# , {
# origin: "Tatooine",
# destination: "Hoth",
# travel_time: 6
# }
# ]


# json_from_empire example
# {
#   "countdown": 7,
#   "bounty_hunters": [
#     {
#       "planet": "Hoth",
#       "day": 6
#     },
#     {
#       "planet": "Hoth",
#       "day": 7
#     },
#     {
#       "planet": "Hoth",
#       "day": 8
#     }
#   ]
# }
def calculte_odds(json_config: json, json_from_db: json, json_from_empire: json) -> int:
    # Todo -> calculte_odds
    trajectories = calculate_all_possible_trajectories(json_config, json_from_db, json_from_empire)
    # Si aucun trajet n'est possible alors on a 0% de chance se succès
    if not trajectories:
        return 0
    # Prendre tous les trajectoire possible, choisir celui qui a les meilleurs chance de succès, renvoyer ses chances de succès
    pass


def get_travel_time_between(origin, destination):
    result = query_specific_origin_destination(origin, destination)
    if result:
        return result[0].travel_time
    else:
        return 0


def calculate_all_possible_trajectories(json_config: json, json_from_db: json, json_from_empire: json) -> List:
    trajectories = []
    departure = json_config["departure"][0]
    arrival = json_config["arrival"][0]
    initial_fuel = json_config["autonomy"][0]
    empire_countdown = json_from_empire["countdown"]
    bounty_hunters = json_from_empire["bounty_hunters"]
    # trajectory = Trajectory(departure=departure,
    #                         arrival=arrival,
    #                         initial_fuel=initial_fuel,
    #                         empire_countdown=empire_countdown,
    #                         bounty_hunters=bounty_hunters)
    reachable_planets = query_specific_origin(departure)
    # print(reachable_planets)
    # current_trajectory = [
    #     {
    #         "planet": departure,
    #         "isVisited": True,
    #     }
    # ]

    # [{
    #   Origin: Tatooine
    #   Destination: Dagobah
    #   travel_time: 6
    # },
    # {
    #   Origin: Tatooine
    #   Destination: Hoth
    #   travel_time: 6
    # }
    # ]
    # visited_planets = [departure]
    # print(json_from_db)
    # print(planets)

    # planets = [
    #     {
    #         "planet": "Tatooine",
    #         "visited": False,
    #         "reachable": ["Dagobah", "Hoth"]
    #     },
    #     {
    #         "planet": "Dagobah",
    #         "visited": False,
    #         "reachable": ["Hoth", "Endor"]
    #     },
    #     {
    #         "planet": "Endor",
    #         "visited": False,
    #         "reachable": []
    #     },
    #     {
    #         "planet": "Hoth",
    #         "visited": False,
    #         "reachable": ["Endor"]
    #     },
    # ]
    planets = {
        "Tatooine": ["Dagobah", "Hoth"],
        "Dagobah": ["Endor", "Hoth"],
        "Endor": [],
        "Hoth": ["Endor"]
    }
    #
    trajectories = []
    for planet in planets["Tatooine"]:
        visited = ["Tatooine"]
        trajectory = ["Tatooine"]
        explore(departure, planets, planet, arrival, trajectory, trajectories, visited)

    print(trajectories)
    # for target_planet in reachable_planets:
    # for planet in planets:
    #     trajectory = []
    #     visited = []
    #     explore_all_routes(planets, planet, trajectory, visited)
    #     print(trajectory)
    # planets = {
    #     "Tatooine": ["Dagobah", "Hoth"],
    #     "Dagobah": ["Hoth", "Endor"],
    #     "Hoth": ["Endor"],
    #     "Endor": []
    # }

    # for target_planet in reachable_planets:
    # for target_planet in planets:
    #     current_trajectory = []
    #     visited = []
    #     explore_all_routes(planets, target_planet, visited)

    # print(trajectories)

    # trajectories_times = []
    # for trajectory in trajectories:
    #     total_travel_time = 0
    #     current_fuel = initial_fuel
    #     caught_proba = 0
    #     for i in range(0, len(trajectory) - 1):
    #         travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1])
    #         print("initial_fuel: " + str(initial_fuel))
    #         print("travel_between: " + str(travel_between))
    #         if initial_fuel < travel_between:
    #             break
    #         if trajectory[i] == arrival:
    #             break
    #         predicted_fuel = current_fuel - travel_between
    #         if predicted_fuel < 0:  # We need to refuel
    #             total_travel_time += 1
    #             current_fuel = initial_fuel
    #         current_fuel -= travel_between
    #         total_travel_time += travel_between
    #     trajectory_total_time = {
    #         "trajectory": trajectory,
    #         "total_time": total_travel_time,
    #         "caught_proba": caught_proba
    #     }
    #     trajectories_times.append(trajectory_total_time)
    #     print(total_travel_time)
    # print(trajectories_times)

# Test en cours
# Todo explore
def explore(departure, planets, current_planet: str, arrival, trajectory, trajectories, visited):
    # print("Visited")
    # print(visited)
    if current_planet == arrival:
        trajectory.append(current_planet)
        trajectories.append(trajectory)
        return
    if current_planet in visited:
        return

    visited.append(current_planet)
    trajectory.append(current_planet)
    # trajectory = [departure]
    for planet in planets[current_planet]:
        if planet not in visited:
            explore(departure, planets, planet, arrival, trajectory, trajectories, visited)


def build_reachables(planets, reachables):
    reachable_planets = []
    for planet in planets:
        if planet["planet"] in reachables:
            reachable_planets.append(planet)
    return reachable_planets


# def parcours_en_profondeur(graphe, sommet_en_cours: str, sommets_visites: []):
#     print('Essai d explorer le sommet :' + str(sommet_en_cours))
#     if sommet_en_cours not in sommets_visites:
#         sommets_visites.append(sommet_en_cours)  # Ajoute le sommet en cours au noeud visité
#         print('Exploration du sommet :' + str(sommet_en_cours))
#     sommets_voisins_non_visites = []
#     for sommet_voisin in graphe[sommet_en_cours]:
#         if sommet_voisin not in sommets_visites:
#             sommets_voisins_non_visites.append(
#                 sommet_voisin)  # Constitue la liste des sommets voisins non encore visité
#
#     for sommet in sommets_voisins_non_visites:
#         # pour tout les sommets voisins non visités on effectue un parcours en profondeur
#         parcours_en_profondeur(graphe, sommet, sommets_visites)


# def explore_all_routes(planets, current_planet: str, trajectory, visited):
#     if current_planet not in visited:
#         visited.append(current_planet)
#         trajectory.append(current_planet)
#         print(current_planet)
#     reachables_neighbours_non_explored = []
#     for reachable in planets[current_planet]:
#         if reachable not in visited:
#             reachables_neighbours_non_explored.append(reachable)
#     for reachable in reachables_neighbours_non_explored:
#         explore_all_routes(planets, reachable, trajectory, visited)


# def explore_all_routes(planets, current_planet: str, trajectory, visited):
#     if current_planet in visited:
#         return
#     visited.append(current_planet)
#     trajectory.append(current_planet)
#     print(current_planet)
#     reachables_neighbours_non_explored = []
#     for reachable in planets[current_planet]:
#         if reachable not in visited:
#             reachables_neighbours_non_explored.append(reachable)
#     for reachable in reachables_neighbours_non_explored:
#         explore_all_routes(planets, reachable, trajectory, visited)


def check_if_planet_is_in_visited_planets(current_planet, visited_planets):
    return current_planet in visited_planets
    # return any([True for x in current_trajectory if x["planet"] == current_planet])


# Ne fonctionne pas
def calculate_all_possible_trajectories_aux(current_planet,
                                            arrival,
                                            trajectories,
                                            visited_planets,
                                            current_trajectory
                                            ):
    print("Target:" + current_planet)
    print("Visited:" + " ".join(visited_planets))
    print("Current trajectory: " + " ".join(current_trajectory))
    visited_planets.append(current_planet)
    print("")
    # if check_if_planet_is_in_visited_planets(current_planet, visited_planets):
    #     return
    # if arrival in visited_planets:
    #     return

    current_trajectory.append(current_planet)
    if current_planet == arrival:
        trajectories.append(current_trajectory)
        return

    # if current_planet == arrival:
    #     visited_planets.append(current_planet)
    #     trajectories.append(visited_planets)
    #     return
    # print(current_trajectory)
    # visited_planets.append(current_planet)
    # if current_planet not in current_trajectory:
    #     current_trajectory.append(current_planet)

    reachable_planets = query_specific_origin(current_planet)
    # if not reachable_planets:
    #     return
    # print("Hello")
    for target_planet in reachable_planets:
        # print(target_planet)
        destination = target_planet.destination
        if not check_if_planet_is_in_visited_planets(destination, visited_planets):
            calculate_all_possible_trajectories_aux(destination,
                                                    arrival,
                                                    trajectories,
                                                    visited_planets,
                                                    current_trajectory)
