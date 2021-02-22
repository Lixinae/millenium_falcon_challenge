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
    odds = calculte_odds(json_config, json_from_db, json_from_empire)
    print("Odds: " + str(odds))
    return odds


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
    initial_fuel = json_config["autonomy"]
    arrival = json_config["arrival"]
    empire_countdown = json_from_empire["countdown"]
    bounty_hunters = json_from_empire["bounty_hunters"]
    print(bounty_hunters)
    trajectories_time_and_caught_proba = []
    for trajectory in trajectories:
        wait_time = 0
        total_travel_time = compute_trajectory_time_caught(arrival,
                                                           bounty_hunters,
                                                           initial_fuel,
                                                           trajectories_time_and_caught_proba,
                                                           trajectory,
                                                           wait_time)

        if total_travel_time < empire_countdown:
            wait_time = 1
            total_travel_time = compute_trajectory_time_caught(arrival,
                                                               bounty_hunters,
                                                               initial_fuel,
                                                               trajectories_time_and_caught_proba,
                                                               trajectory,
                                                               wait_time)
    print(trajectories_time_and_caught_proba)
    # S'il n'y a aucun chemin dans les temps on renvoie 0
    filtered_time = [x for x in trajectories_time_and_caught_proba if x["total_time"] <= empire_countdown]
    if not filtered_time:
        return 0

    print(filtered_time)


def compute_trajectory_time_caught(arrival, bounty_hunters, initial_fuel, trajectories_times, trajectory,wait_time):
    total_travel_time = 0
    current_fuel = initial_fuel
    caught_proba = 0
    count_time_encounter_bounty_hunters = 0
    for i in range(0, len(trajectory) - 1):
        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1])
        if initial_fuel < travel_between:  # On a pas assez de carburant pour aller sur la 1ere planète
            break
        if trajectory[i] == arrival:  # On est arrivé à la fin du trajet
            break
        current_planet = {
            "planet": trajectory[i],
            "day": total_travel_time
        }
        if current_planet in bounty_hunters:
            count_time_encounter_bounty_hunters += 1
        predicted_fuel = current_fuel - travel_between
        if predicted_fuel < 0:  # On a besoin de refuel
            total_travel_time += 1
            current_fuel = initial_fuel

        current_fuel -= travel_between
        total_travel_time += travel_between
        total_travel_time += wait_time
    for i in range(0, count_time_encounter_bounty_hunters + 1):
        num = pow(9, i)
        denom = pow(10, i + 1)
        caught_proba += num / denom
    trajectory_total_time = {
        "trajectory": trajectory,
        "total_time": total_travel_time,
        "caught_proba": caught_proba
    }
    trajectories_times.append(trajectory_total_time)
    return total_travel_time


def get_travel_time_between(origin, destination):
    result = query_specific_origin_destination(origin, destination)
    if result:
        return result[0].travel_time
    else:
        return 0


def calculate_all_possible_trajectories(json_config: json, json_from_db: json, json_from_empire: json) -> List:
    departure = json_config["departure"]
    arrival = json_config["arrival"]
    print(json_from_db)
    # planets = transform_json_to_usable_data(json_from_db)
    # print(planets)
    planets = {
        "Tatooine": ["Dagobah", "Hoth"],
        "Dagobah": ["Endor", "Hoth"],
        "Endor": [],
        "Hoth": ["Endor"]
    }
    #
    trajectories = []
    for planet in planets[departure]:
        visited = [departure]
        trajectory = [departure]
        explore(planets, planet, arrival, trajectory, trajectories, visited)
    print(trajectories)
    return trajectories


def explore(dict_path_planets, current_planet, arrival, trajectory, trajectories, visited):
    if current_planet == arrival:
        new_trajectory = list(trajectory)
        new_trajectory.append(current_planet)
        trajectories.append(new_trajectory)
        return
    if current_planet in visited:
        return
    if dict_path_planets[current_planet].count == 0:
        return
    visited.append(current_planet)
    trajectory.append(current_planet)
    for planet in dict_path_planets[current_planet]:
        if planet not in visited:
            explore(dict_path_planets, planet, arrival, trajectory, trajectories, visited)
