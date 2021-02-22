import os
import pathlib
import json

basedir = pathlib.Path(__file__).parent.parent.parent
web_dir = os.path.join(basedir, "web_C3PO")
web_templates_dir = os.path.join(web_dir, "templates")
web_static_dir = os.path.join(web_dir, "static")
web_upload_dir = os.path.join(web_dir, "uploads")
resource_dir = os.path.join(basedir, "resources")

allowed_file_extensions_upload = {'json'}


# Configuration for the app

class ConfigurationApp:

    def __init__(self):
        self.autonomy = 6
        self.departure = "Tatooine"
        self.arrival = "Endor"
        self._routes_db = "universe.db"
        self.json_config_file_location = os.path.join(resource_dir, "configuration/millenium-falcon.json")
        self._json_config_file_path_folder = os.path.dirname(self.json_config_file_location)
        self.full_route_db = os.path.join(resource_dir, self._json_config_file_path_folder, self._routes_db)
        self.sql_alchemy_database_url = 'sqlite:///' + os.path.join(basedir, self.full_route_db)

    def _init_from_json(self, json_data):
        # Todo -> Add security to check if values exist or not
        self.autonomy = json_data["autonomy"]
        self.departure = json_data["departure"]
        self.arrival = json_data["arrival"]
        self._routes_db = json_data["routes_db"]
        self.full_route_db = os.path.join(resource_dir, self._json_config_file_path_folder, self._routes_db)
        self.sql_alchemy_database_url = 'sqlite:///' + os.path.join(basedir, self.full_route_db)

    def init_from_json_file(self, json_file_location):
        with open(json_file_location, 'r') as jsonfile:
            json_data = json.load(jsonfile)
            self._json_config_file_path_folder = os.path.dirname(json_file_location)
            self._init_from_json(json_data)

    def __repr__(self):
        return 'autonomy: {}\n' \
               'departure: {}\n' \
               'arrival: {}\n' \
               'full_route_db: {}\n\n'.format(self.autonomy,
                                              self.departure,
                                              self.arrival,
                                              self.full_route_db)

    def to_json_data(self):
        return {
            'autonomy': self.autonomy,
            'departure': self.departure,
            'arrival': self.arrival,
        }


class ConfigurationAppTest(ConfigurationApp):
    def __init__(self):
        super().__init__()
        self.json_config_file_location = os.path.join(resource_dir, "test_data/millenium-falcon.json")
        self._json_config_file_path_folder = os.path.dirname(self.json_config_file_location)
        self.full_route_db = os.path.join(resource_dir, self._json_config_file_path_folder, self._routes_db)
        self.sql_alchemy_database_url = 'sqlite:///' + os.path.join(basedir, self.full_route_db)


# Use for most cases
config = ConfigurationApp()
config.init_from_json_file(os.path.join(resource_dir, "configuration/millenium-falcon.json"))

# Only use for testing purpose
config_test = ConfigurationAppTest()


class ConfigurationFlask:
    def __init__(self):
        self.ALLOWED_EXTENSIONS = allowed_file_extensions_upload
        self.UPLOAD_FOLDER = web_upload_dir
