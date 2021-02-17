import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Todo -> read configuration file

# {
#   "autonomy": 6,
#   "departure": "Tatooine",
#   "arrival": "Endor",
#   "routes_db": "universe.db"
# }
routes_db = "universe.db"

class Configuration:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, routes_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False