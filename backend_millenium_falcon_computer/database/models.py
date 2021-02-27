from sqlalchemy import Column, Integer, String
from backend_millenium_falcon_computer.database import base


# Idéalement on ne devrait qu'une clé primaire comme un ID ou autre
# Ici les champs sur marqué en tant que clé primaire, sinon SQL alchemy rale
class Routes(base):
    __tablename__ = "routes"
    origin = Column(String(128), primary_key=True)
    destination = Column(String(128), primary_key=True)
    travel_time = Column(Integer, primary_key=True)

    # ORIGIN (TEXT): Name of the origin planet. Cannot be null or empty.
    # DESTINATION (TEXT): Name of the destination planet. Cannot be null or empty.
    # TRAVEL_TIME (INTEGER): Number days needed to travel from one planet to the other. Must be strictly positive.

    def __init__(self, origin, destination, travel_time):
        self.origin = origin
        self.destination = destination
        self.travel_time = travel_time

    def __repr__(self):
        return '{\norigin: \"' + self.origin + '\",\n' + \
               'destination: \"' + self.destination + '\",\n' + \
               'travel_time: ' + str(self.travel_time) + '\n}\n'

    #
    def to_json(self):
        return {"origin": self.origin,
                'destination': self.destination,
                'travel_time': self.travel_time,
                }
