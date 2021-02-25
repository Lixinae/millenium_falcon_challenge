import random
from typing import Dict

# {
#     "autonomy": 6,
#     "departure": "Tatooine",
#     "arrival": "Endor",
#     "routes_db": "universe.db"
# }


def generate_falcon_data(min_autonomy: int, max_autonomy: int) -> Dict:
    planets = []
    falcon = {
        "autonomy": random.randint(min_autonomy, max_autonomy),
        "departure": random.choice(planets),
        "arrival": random.choice(planets),
        "routes_db": "universe.db"
    }
    return falcon
