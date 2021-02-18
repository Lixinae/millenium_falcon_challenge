import os
import pathlib
import json

basedir = pathlib.Path(__file__).parent.parent.parent
web_templates_dir = os.path.join(basedir, "web_C3PO/templates")
web_static_dir = os.path.join(basedir, "web_C3PO/static")
resource_dir = os.path.join(basedir, "resources")

# Todo -> Trouver comment le parametrer au moment de la creation de l'appli
json_config_file_location = os.path.join(resource_dir, "example1/millenium-falcon.json") # "./resources/example1/millenium-falcon.json"


# Configuration for the app

class ConfigurationApp:
    autonomy = 6,
    departure = "Tatooine",
    arrival = "Endor",
    _routes_db = "universe.db"
    full_route_db = os.path.join(resource_dir, "example1", _routes_db)

    def init_from_json(self, folder_of_db, json_data):
        # Todo -> Add security to check if values exist or not
        self.autonomy = json_data["autonomy"]
        self.departure = json_data["departure"]
        self.arrival = json_data["arrival"]
        self._routes_db = json_data["routes_db"]
        self.full_route_db = os.path.join(resource_dir, folder_of_db, self._routes_db)

    def init_from_json_file(self, location):
        with open(location, 'r') as jsonfile:
            json_data = json.load(jsonfile)
            folder_of_file = os.path.dirname(location)
            print(folder_of_file)

            self.init_from_json(folder_of_file, json_data)

    def __repr__(self):
        return 'Autonomy: {}\n' \
               'Departure: {}\n' \
               'Arrival: {}\n' \
               'Full_route_db: {}\n\n'.format(self.autonomy,
                                              self.departure,
                                              self.arrival,
                                              self.full_route_db)


class ConfigurationFlask:
    def __init__(self, db_path):
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, db_path)
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True
