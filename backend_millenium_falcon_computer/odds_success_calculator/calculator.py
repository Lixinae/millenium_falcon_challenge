import json

from backend_millenium_falcon_computer.configuration.configuration import config
from backend_millenium_falcon_computer.database.query_wrappers import query_all_routes


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

#json_from_db
# [Origin: Tatooine
# Destination: Dagobah
# travel_time: 6
#
# , Origin: Dagobah
# Destination: Endor
# travel_time: 4
#
# , Origin: Dagobah
# Destination: Hoth
# travel_time: 1
#
# , Origin: Hoth
# Destination: Endor
# travel_time: 1
#
# , Origin: Tatooine
# Destination: Hoth
# travel_time: 6
#
# ]

# json_from_empire
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
    return -1
    pass
