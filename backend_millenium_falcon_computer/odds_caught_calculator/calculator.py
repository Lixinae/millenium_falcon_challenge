import json

from backend_millenium_falcon_computer.database.query_wrappers import query_all_routes


def fetch_data_from_db() -> json:
    return query_all_routes()


def calculate_odds_of_success(json_from_file: json) -> int:
    json_from_db = fetch_data_from_db()
    return calculte_odds(json_from_db, json_from_file)


def calculte_odds(json_from_db: json, json_from_file: json) -> int:
    # Todo -> calculte_odds
    pass
