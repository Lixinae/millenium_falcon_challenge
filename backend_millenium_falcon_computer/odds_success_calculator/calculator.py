import json
from itertools import combinations
from typing import List, Dict

from backend_millenium_falcon_computer.configuration.configuration import config
from backend_millenium_falcon_computer.database.query_wrappers import query_all_routes, \
    query_specific_origin_destination


def fetch_data_from_db() -> json:
    """
    Récupère les informations des routes au format json
    :return: Les informations des routes au format json
    """
    return query_all_routes()


def fetch_data_from_config(config_informations):
    """
    Recupère les informations de configurations
    :param config_informations: Les informations de configuration
    :return: Un json des informations de configuration
    """
    json_config = config_informations.to_json_data()
    return json_config


def calculate_best_odds_of_success(json_from_empire: json, config_informations=config) -> Dict:
    """
    Calcul tous les trajets possible à partir des données
    Puis calcul les meilleurs chances de succès des différentes routes
    :param json_from_empire: Les données json des informations sur les éléments de l'empire
    :param config_informations: La configuration utilisé, soit celle par defaut, soit à partir d'un fichier lu en entrée
    :return: Les chances de succès
    """
    json_from_db = fetch_data_from_db()
    json_config = fetch_data_from_config(config_informations)
    # On calcul toute les routes possible à partir des informations de la base de données et de la configuration
    trajectories = calculate_all_possible_trajectories(json_config, json_from_db)
    odds_info = calculte_odds(json_config=json_config, json_from_empire=json_from_empire, trajectories=trajectories)
    return odds_info


def calculte_odds(json_config: json, json_from_empire: json, trajectories: List, ) -> Dict:
    """
    Calcule les chances de succès de chacune des routes
    :param trajectories: Tous les routes sur lesquels iterer pour les calculs
    :param json_config: Les données de configuration au format json
    :param json_from_empire: Les données lié à l'empire au format json
    :return: Un dictionnaire avec la trajectoire effectué, les arrêts pour refuel, les chances de succès
    """

    autonomy = json_config["autonomy"]
    empire_countdown = json_from_empire["countdown"]
    bounty_hunters = json_from_empire["bounty_hunters"]
    trajectories_time_and_caught_proba = []
    for trajectory in trajectories:
        total_travel_time_without_refuel = compute_total_time_travel_withou_refuel(trajectory)

        count_refuel_times_needed = 0
        if total_travel_time_without_refuel >= autonomy:
            count_refuel_times_needed = total_travel_time_without_refuel // autonomy

        # Si le temps de trajet théorique + le nombre de refuel necessaire dépasse le countdown,
        # On ne calcule pas les chances d'être pris
        if count_refuel_times_needed + total_travel_time_without_refuel > empire_countdown:
            continue

        # On ne prendra en compte le refuel que dans les trajets où l'on peut arriver à temps
        maximum_possible_refuel_to_be_in_time = empire_countdown - total_travel_time_without_refuel
        if maximum_possible_refuel_to_be_in_time < 0:
            continue
        print("total_travel_time_without_refuel:" + str(total_travel_time_without_refuel))
        print("maximum_possible_refuel_to_be_in_time:" + str(maximum_possible_refuel_to_be_in_time))
        print("count_refuel_times_needed:" + str(count_refuel_times_needed))
        print("len(trajectory):" + str(len(trajectory)))

        # Todo -> Split en plusieurs fonctions
        # Calculer toutes les routes possibles avec n arret maximum, avec leur chance d'être capturé
        for count_refuel in range(0, maximum_possible_refuel_to_be_in_time + 1):
            # Cas où l'on a pas besoin de refuel du tout et on fait le trajet d'un coup
            if count_refuel == 0:
                if count_refuel_times_needed == 0:
                    total_travel_time_no_refuel_needed = 0
                    count_time_encounter_bounty_hunters = 0
                    caught_proba = 0
                    for i in range(0, len(trajectory) - 1):
                        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1])
                        current_planet = {
                            "planet": trajectory[i],
                            "day": total_travel_time_no_refuel_needed
                        }
                        count_time_encounter_bounty_hunters = increase_count_time_bounty_hunters(bounty_hunters,
                                                                                                 count_time_encounter_bounty_hunters,
                                                                                                 current_planet)
                        total_travel_time_no_refuel_needed += travel_between
                    caught_proba = update_caught_probability(caught_proba, count_time_encounter_bounty_hunters)
                    # Il est inutile de créer l'objet et de l'ajouter à la liste si on excède le temps
                    if total_travel_time_no_refuel_needed <= empire_countdown:
                        trajectory_time_and_caught_proba = {
                            "trajectory": trajectory,
                            "total_time": total_travel_time_no_refuel_needed,
                            "caught_proba": caught_proba,
                            "refueled_on": []  # Champs inutile dans ce cas, mais nécessaire pour garder la cohérence
                        }
                        trajectories_time_and_caught_proba.append(trajectory_time_and_caught_proba)
            else:
                combinaisons_planets_refuel = combinations(trajectory[:len(trajectory) - 1], count_refuel)
                list_combinaisons_planets_refuel = list(combinaisons_planets_refuel)
                for combinaisons_planet_refuel in list_combinaisons_planets_refuel:
                    print("-------------- Refuel ON:")
                    print(combinaisons_planet_refuel)
                    print("-------------- ")

                    total_travel_time_with_refuel = 0
                    count_time_encounter_bounty_hunters = 0
                    current_fuel = autonomy
                    caught_proba = 0
                    refueled_on = []
                    for i in range(0, len(trajectory) - 1):
                        print(trajectory[i] + " -> " + trajectory[i + 1])
                        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1])
                        current_planet = {
                            "planet": trajectory[i],
                            "day": total_travel_time_with_refuel
                        }
                        print(current_planet)

                        if current_planet in bounty_hunters:
                            count_time_encounter_bounty_hunters += 1
                        for planet in combinaisons_planet_refuel:
                            if current_planet["planet"] == planet:
                                refueled_on.append(planet)
                                total_travel_time_with_refuel += 1
                                current_planet["day"] = total_travel_time_with_refuel
                                current_fuel = autonomy
                                if current_planet in bounty_hunters:
                                    count_time_encounter_bounty_hunters += 1

                        predicted_fuel = current_fuel - travel_between
                        if predicted_fuel < 0:  # On a besoin de refuel
                            total_travel_time_with_refuel += 1
                            current_planet["day"] = total_travel_time_with_refuel
                            current_fuel = autonomy
                            refueled_on.append(current_planet["planet"])
                            if current_planet in bounty_hunters:
                                count_time_encounter_bounty_hunters += 1
                        current_fuel -= travel_between
                        total_travel_time_with_refuel += travel_between
                    caught_proba = update_caught_probability(caught_proba, count_time_encounter_bounty_hunters)
                    # Il est inutile de créer l'objet et de l'ajouter à la liste si on excède le temps
                    if total_travel_time_with_refuel <= empire_countdown:
                        trajectory_time_and_caught_proba = {
                            "trajectory": trajectory,
                            "total_time": total_travel_time_with_refuel,
                            "caught_proba": caught_proba,
                            "refueled_on": refueled_on
                        }
                        trajectories_time_and_caught_proba.append(trajectory_time_and_caught_proba)

            # Cette méthode est très lourde
            # Si count_refuel == 0 et count_refuel_times_needed == 0
            #   On ne compte pas le refuel car non necessaire mais juste le trajet
            # Si count_refuel == 1
            #   On test tous les trajets possibe avec 1 refuel (chaque planète peut être un point de refuel
            # Si count_refuel == 2
            #   On test tous les trajets possible pour chaque combinaison de planète possible pour refuel
            # Etc....

    if not trajectories_time_and_caught_proba:
        return {}
    return find_best_proba_success(trajectories_time_and_caught_proba)


def increase_count_time_bounty_hunters(bounty_hunters, count_time_encounter_bounty_hunters, current_planet):
    if current_planet in bounty_hunters:
        count_time_encounter_bounty_hunters += 1
    return count_time_encounter_bounty_hunters


def update_caught_probability(caught_proba, count_time_encounter_bounty_hunters):
    for i in range(0, count_time_encounter_bounty_hunters):
        num = pow(9, i)
        denom = pow(10, i + 1)
        caught_proba += num / denom
    return caught_proba


def find_best_proba_success(trajectories_time_and_caught_proba) -> Dict:
    def take_caught_proba(elem):
        return elem["caught_proba"]

    trajectories_time_and_caught_proba.sort(key=take_caught_proba)
    lowest_caught_proba = trajectories_time_and_caught_proba[0]["caught_proba"]
    trajectories_time_and_caught_proba[0]["odds_of_success"] = (1 - lowest_caught_proba) * 100
    return trajectories_time_and_caught_proba[0]
    # return (1 - lowest_caught_proba) * 100


def compute_total_time_travel_withou_refuel(trajectory):
    total_travel_time_without_refuel = 0
    for i in range(0, len(trajectory) - 1):
        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1])
        total_travel_time_without_refuel += travel_between
    return total_travel_time_without_refuel


def get_travel_time_between(origin, destination):
    result = query_specific_origin_destination(origin, destination)
    if result:
        return result[0].travel_time
    else:
        return 0


def transform_json_to_usable_data(json_from_db):
    planets_output = {}
    for dict_db_Routes in json_from_db:
        planet_name = dict_db_Routes.origin
        destination = dict_db_Routes.destination
        if planet_name not in planets_output:
            planets_output[planet_name] = [destination]
        else:
            planets_output[planet_name].append(destination)
    return planets_output


def calculate_all_possible_trajectories(json_config: json, json_from_db: json) -> List:
    departure = json_config["departure"]
    arrival = json_config["arrival"]
    planets = transform_json_to_usable_data(json_from_db)
    trajectories = []
    for planet in planets[departure]:
        visited = [departure]
        trajectory = [departure]
        explore(planets, planet, arrival, trajectory, trajectories, visited)
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
