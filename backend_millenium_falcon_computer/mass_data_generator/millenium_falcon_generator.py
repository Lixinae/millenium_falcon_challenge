import json
import os
import random
from typing import Dict

# {
#     "autonomy": 6,
#     "departure": "Tatooine",
#     "arrival": "Endor",
#     "routes_db": "universe.db"
# }
from backend_millenium_falcon_computer.configuration.configuration import generated_data_dir
from backend_millenium_falcon_computer.mass_data_generator.generator import get_list_planets


def generate_falcon_data(min_autonomy: int,
                         max_autonomy: int,
                         number_planets: int,
                         save_to_file: bool = True,
                         filename: str = "millenium-falcon.json") -> Dict:
    planets = get_list_planets()
    max_iterate = min(number_planets, len(planets))
    planets_choices = planets[:max_iterate]
    falcon = {
        "autonomy": random.randint(min_autonomy, max_autonomy),
        "departure": random.choice(planets_choices),
        "arrival": random.choice(planets_choices),
        "routes_db": "universe.db"
    }
    if save_to_file:
        path = os.path.join(generated_data_dir, filename)
        with open(path, 'w', encoding='utf-8') as output_file:
            json.dump(falcon, output_file, ensure_ascii=False, indent=4)

    return falcon
