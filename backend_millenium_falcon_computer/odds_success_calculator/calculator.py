import json
from typing import List, Dict

from backend_millenium_falcon_computer.configuration.configuration import config
from backend_millenium_falcon_computer.database.query_wrappers import QueryWrappers


def fetch_data_from_db() -> json:
    """
    Récupère les informations des routes au format json
    :return: Les informations des routes au format json
    """
    query_wrappers = QueryWrappers()
    return query_wrappers.query_all_routes()


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
    odds_info = calculte_odds(json_config=json_config,
                              json_from_empire=json_from_empire,
                              trajectories=trajectories,
                              json_database=json_from_db)
    return odds_info


def calculte_odds(json_config: json, json_from_empire: json, trajectories: List, json_database) -> Dict:
    """
    Calcule les chances de succès de chacune des routes
    :param json_database: Le json qui contient les données de la base de données
    :param trajectories: Tous les routes sur lesquels iterer pour les calculs
    :param json_config: Les données de configuration au format json
    :param json_from_empire: Les données lié à l'empire au format json
    :return: Un dictionnaire avec la trajectoire effectué, les arrêts pour refuel, les chances de succès
    """

    autonomy = json_config["autonomy"]
    empire_countdown = json_from_empire["countdown"]
    bounty_hunters = json_from_empire["bounty_hunters"]
    trajectories_time_and_caught_proba = []
    nb_planets = len(set([x.origin for x in json_database]))
    # Car on ne peut pas avoir de bount_hunters sur le départ et l'arrivé
    caught_probability_values_max_size = empire_countdown + nb_planets
    caught_probability_values = [caught_probability(x) for x in range(0, caught_probability_values_max_size)]
    unique_trajectories = [list(i) for i in set(map(tuple, trajectories))]
    for trajectory in unique_trajectories:
        total_travel_time_without_refuel = compute_total_time_travel_without_refuel(trajectory, json_database)

        count_refuel_times_needed = 0
        if total_travel_time_without_refuel >= autonomy:
            count_refuel_times_needed = total_travel_time_without_refuel // autonomy

        # Si le temps de trajet théorique + le nombre de refuel necessaire dépasse le countdown,
        # On ne calcule pas les chances d'être pris
        if count_refuel_times_needed + total_travel_time_without_refuel > empire_countdown:
            continue

        # On ne prendra en compte le refuel que dans les trajets où l'on peut arriver à temps
        maximum_possible_refuel_to_be_in_time = min(len(trajectory) - 2,
                                                    empire_countdown - total_travel_time_without_refuel)
        if maximum_possible_refuel_to_be_in_time < 0:
            continue

        # Calculer toutes les routes possibles avec count_refuel arret maximum, avec leur chance d'être capturé
        for count_refuel in range(count_refuel_times_needed, maximum_possible_refuel_to_be_in_time + 1):
            # Si on a un chemin à 0% d'être pris, on arrête le calcul directement pour éviter trop de calcul inutile
            if any([x for x in trajectories_time_and_caught_proba if x["caught_proba"] == 0]):
                return find_best_proba_success(trajectories_time_and_caught_proba)
            # Cas où l'on a pas besoin de refuel du tout et on fait le trajet d'un coup
            if count_refuel == 0:
                calculate_trajectorie_odds_no_refuel(bounty_hunters,
                                                     empire_countdown,
                                                     trajectories_time_and_caught_proba,
                                                     trajectory,
                                                     json_database,
                                                     caught_probability_values)
            else:
                combinations_falcon_data(trajectory,
                                         count_refuel,
                                         bounty_hunters,
                                         caught_probability_values,
                                         autonomy,
                                         empire_countdown,
                                         json_database,
                                         trajectories_time_and_caught_proba)
    if not trajectories_time_and_caught_proba:
        return {}
    return find_best_proba_success(trajectories_time_and_caught_proba)


def combinations_falcon_data(trajectory,
                             taille_combi,
                             bounty_hunters,
                             caught_probability_values,
                             autonomy,
                             empire_countdown,
                             json_database,
                             trajectories_time_and_caught_proba) -> None:
    """
    Calcul toutes les combinaisons possible pour le nombre d'arrêts / refuel souhaité et
    injecte les informations dans la liste "trajectories_time_and_caught_proba"

    :param trajectory: La trajectoire actuelle sur laquelle test la combinaison
    :param taille_combi: Taille de la combinaison voulu
    :param bounty_hunters: Les planètes où se trouve les chasseurs de primes et à quel moment
    :param caught_probability_values: Tableau des probabilité possible de capture
    :param autonomy: autonomy: L'autonomie du faucon millenium
    :param empire_countdown: Le timer à partir duquel la missions est considéré comme un echec
    :param json_database: La base de donnée au format json pour eviter les appels à la base de données
    :param trajectories_time_and_caught_proba: La liste avec toutes les informations sur tous les trajets possible
    """
    pool = tuple(trajectory[:len(trajectory) - 1])
    size_pool = len(pool)
    if taille_combi > size_pool:
        return
    indices = [x for x in range(taille_combi)]

    combinaison = tuple(pool[i] for i in indices)

    data = calculate_total_time_odds_for_combination(combinaison,
                                                     bounty_hunters,
                                                     caught_probability_values,
                                                     autonomy,
                                                     json_database,
                                                     trajectory)
    if data not in trajectories_time_and_caught_proba:
        if data["total_time"] <= empire_countdown:
            trajectories_time_and_caught_proba.append(data)
    while True:
        for i in reversed(range(taille_combi)):
            if indices[i] != i + size_pool - taille_combi:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, taille_combi):
            indices[j] = indices[j - 1] + 1
        combinaison = tuple(pool[i] for i in indices)
        data = calculate_total_time_odds_for_combination(combinaison,
                                                         bounty_hunters,
                                                         caught_probability_values,
                                                         autonomy,
                                                         json_database,
                                                         trajectory)
        if data not in trajectories_time_and_caught_proba:
            if data["total_time"] <= empire_countdown:
                trajectories_time_and_caught_proba.append(data)


def calculate_total_time_odds_for_combination(combinaisons_planet_refuel,
                                              bounty_hunters,
                                              caught_probability_values,
                                              autonomy,
                                              json_database,
                                              trajectory):
    """
    Calcul le temps mis et les chances d'être pris pour la combinaison donné
    :param combinaisons_planet_refuel: La combinaison à tester
    :param bounty_hunters: Les planètes où se trouve les chasseurs de primes et à quel moment
    :param caught_probability_values: Tableau des probabilité possible de capture
    :param autonomy: L'autonomie du faucon millenium
    :param json_database: La base de donnée au format json pour eviter les appels à la DB
    :param trajectory: La trajectoire actuelle
    :return: Les informations sur la combinaison
    """
    current_day = 0
    count_time_encounter_bounty_hunters = 0
    current_fuel = autonomy
    refuel_on = combinaisons_planet_refuel[:len(combinaisons_planet_refuel)]
    for i in range(0, len(trajectory) - 1):
        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1], json_database)
        current_planet = trajectory[i]
        current_planet_day = {
            "planet": trajectory[i],
            "day": current_day
        }
        if current_planet_day in bounty_hunters:
            count_time_encounter_bounty_hunters += 1
        if current_planet in refuel_on:
            # Si la planète actuel est dans la liste des combinaions, on doit refuel
            # On met à jour le current_planet_day pour check si on est sur une planète avec les bounty hunters
            current_day += 1
            current_planet_day["day"] = current_day
            current_fuel = autonomy
            if current_planet_day in bounty_hunters:
                count_time_encounter_bounty_hunters += 1
        predicted_fuel = current_fuel - travel_between
        # Si on doit refuel sur d'autres planète que celle dans la combinaison, on ajoute 1 jour de refuel
        # On ne doit refuel QUE sur les planètes de la combinaison
        if predicted_fuel < 0:
            current_day += 1
        current_fuel -= travel_between
        current_day += travel_between
    if count_time_encounter_bounty_hunters > len(caught_probability_values):
        caught_proba = caught_probability(caught_probability_values)
    else:
        caught_proba = caught_probability_values[count_time_encounter_bounty_hunters]
    trajectory_time_and_caught_proba = {
        "trajectory": trajectory,
        "total_time": current_day,
        "caught_proba": caught_proba,
        "refueled_on": refuel_on
    }
    return trajectory_time_and_caught_proba


def calculate_trajectorie_odds_no_refuel(bounty_hunters,
                                         empire_countdown,
                                         trajectories_time_and_caught_proba,
                                         trajectory,
                                         json_database,
                                         caught_probability_values):
    """
    Et calcule la probabilité d'echec pour le trajet donné, où il n'y pas besoin de remettre du carburant
    :param bounty_hunters: Les planètes où se trouve les chasseurs de primes et à quel moment
    :param empire_countdown: Le timer à partir duquel la missions est considérer comme un echec
    :param trajectories_time_and_caught_proba: La liste de toute les trajectoires, avec
                                                les différentes combinaisons d'arrêt,
                                                leur taux d'echec et le temps total mis
    :param trajectory: La trajectoire actuelle
    :param json_database: Les données json des planètes
    :param caught_probability_values: Tableau des probabilité possible de capture
    """
    total_travel_time_no_refuel_needed = 0
    count_time_encounter_bounty_hunters = 0
    # Calculer de la probabilité d'être capturer pour le trajet donné
    for i in range(0, len(trajectory) - 1):
        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1], json_database)
        # La planète sur laquelle on se trouve actuellement avec le moment où on y est
        current_planet = {
            "planet": trajectory[i],
            "day": total_travel_time_no_refuel_needed
        }
        # Si on se trouve sur une planète où sont les chasseurs de primes à ce moment
        # On augmente les chances d'être pris
        if current_planet in bounty_hunters:
            count_time_encounter_bounty_hunters += 1
        total_travel_time_no_refuel_needed += travel_between
    if count_time_encounter_bounty_hunters > len(caught_probability_values):
        caught_proba = caught_probability(caught_probability_values)
    else:
        caught_proba = caught_probability_values[count_time_encounter_bounty_hunters]
    # Il est inutile de créer l'objet et de l'ajouter à la liste si on excède le temps
    if total_travel_time_no_refuel_needed <= empire_countdown:
        trajectory_time_and_caught_proba = {
            "trajectory": trajectory,
            "total_time": total_travel_time_no_refuel_needed,
            "caught_proba": caught_proba,
            "refueled_on": []  # Champs inutile dans ce cas, mais nécessaire pour garder la cohérence
        }
        trajectories_time_and_caught_proba.append(trajectory_time_and_caught_proba)


def caught_probability(count_time_encounter_bounty_hunters):
    """
    Calcule la probabilité d'être pris
    :param count_time_encounter_bounty_hunters: Le nombre de fois où l'on rencontre des chasseurs de primes
    :return: La probabilité d'être capturé
    """
    caught_proba = 0
    for i in range(0, count_time_encounter_bounty_hunters):
        num = pow(9, i)
        denom = pow(10, i + 1)
        caught_proba += num / denom
    return caught_proba


def find_best_proba_success(trajectories_time_and_caught_proba) -> Dict:
    """
    Trie la liste des trajectoires, par rapport à leur taux d'echec
    Et renvoie le 1er élement, celui qui a le taux d'echec le plus faible
    Ajoute également un champs "odds_of_success" au résultat pour indiquer les chances de succès
    :param trajectories_time_and_caught_proba: La liste de toute les trajectoires avec les différentes combinaisons d'arrêt et leur taux d'echec
    :return: La trajectoire ayant le taux d'echec le plus bas
    """

    def take_caught_proba(elem):
        """
        Fonction pour sort la liste d'entrée
        :param elem: Element à comparer
        :return: La valeur de "caught_proba"
        """
        return elem["caught_proba"]

    trajectories_time_and_caught_proba.sort(key=take_caught_proba)
    lowest_caught_proba = trajectories_time_and_caught_proba[0]["caught_proba"]
    # Ajoute un champs "odds_of_success" au résultat
    # On ne l'ajoute qu'a ce moment pour éviter plein de calcul inutile pendant les parcours
    trajectories_time_and_caught_proba[0]["odds_of_success"] = (1 - lowest_caught_proba) * 100
    return trajectories_time_and_caught_proba[0]


def compute_total_time_travel_without_refuel(trajectory, json_database) -> int:
    """
    Calcule le temps de trajet total d'une trajectoire sans prendre en compte le refuel
    :param json_database: La bdd sous forme json pour être plus rapide qu'un appelle à la BDD
    :param trajectory: La trajectoire sur laquelle calculer le temps de trajet
    :return: Le temps de trajet total d'une trajectoire sans prendre en compte le refuel
    """
    total_travel_time_without_refuel = 0
    for i in range(0, len(trajectory) - 1):
        travel_between = get_travel_time_between(trajectory[i], trajectory[i + 1], json_database)
        total_travel_time_without_refuel += travel_between
    return total_travel_time_without_refuel


def get_travel_time_between(origin, destination, json_database) -> int:
    """
    Va interroger la BDD pour récupérer le temps de trajet entre les planètes "origin" et destination
    Puis renvoie cette valeur.
    Renvoie 0 en cas de non existence
    :param json_database: La bdd sous forme json pour être plus rapide qu'un appelle à la BDD
    :param origin: La planète d'origin
    :param destination: La planète destination
    :return: Le temps de trajet entre origin et destination
    """
    val = next((planet for planet in json_database if planet.origin == origin and planet.destination == destination),
               None)
    if val:
        return val.travel_time
    return 0


def transform_json_to_usable_data(json_from_db) -> json:
    """
    Prend le json de la base de données et le transforme en un jeu plus utilisable
    :param json_from_db: Les données json de la base de données
    :return: Un json formatté correctement
    """
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
    """
    Calcule tous les trajets possible le depart et l'arrivé en fonction des données de la BDD
    On considère les données comme un graphe et on effectue un parcours en profondeur à l'aide d'une fonction récursive
    :param json_config: Les données json de la configuration
    :param json_from_db: Les données json de la base de données
    :return: Tous les trajets possible entre le depart et l'arrivé configuré dans le json de configuration
    """
    # Valeur par defaut au cas où il y aurais un soucis avec le json à ce moment
    departure = "Tatooine"
    arrival = "Endor"
    if "departure" in json_config:
        departure = json_config["departure"]
    if "arrival" in json_config:
        arrival = json_config["arrival"]
    dict_path_planets = transform_json_to_usable_data(json_from_db)

    trajectories = []
    for planet in dict_path_planets[departure]:
        visited = [departure]
        trajectory = [departure]
        explore(dict_path_planets, planet, arrival, trajectory, trajectories, visited)
    return trajectories


def explore(dict_path_planets, current_planet, arrival, trajectory, trajectories, visited):
    """
    Fonction recursive pour effectuer un parcours en profondeur du graph avec les planètes
    :param dict_path_planets: Le graph contenant les planètes avec les trajets possible entre chacune
    :param current_planet: Planète sur laquelle on est actuellement
    :param arrival: Planète cible
    :param trajectory: Trajectoire actuelle
    :param trajectories: List de toutes les trajectoires possible
    :param visited: Liste des planètes visité
    """
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
