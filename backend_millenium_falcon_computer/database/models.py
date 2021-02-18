from sqlalchemy import Column, Integer, String
from backend_millenium_falcon_computer import db


class Routes(db.Model):
    __tablename__ = "routes"
    origin = Column(String(128), primary_key=True)
    destination = Column(String(128), primary_key=True)
    travel_time = Column(Integer, primary_key=True)

    # ORIGIN (TEXT): Name of the origin planet. Cannot be null or empty.
    # DESTINATION (TEXT): Name of the destination planet. Cannot be null or empty.
    # TRAVEL_TIME (INTEGER): Number days needed to travel from one planet to the other. Must be strictly positive.

    #
    def __repr__(self):
        return 'Origin: {}\n' \
               'Destination: {}\n' \
               'travel_time: {}\n\n'.format(self.origin,
                                            self.destination,
                                            self.travel_time, )

    #
    # def to_dict(self):
    #     return jsonify({"Id": self.id,
    #                     'name': self.name,
    #                     'quick_description': self.quick_description,
    #                     'miniature': url_for('static', filename=self.miniature_path),
    #                     'url': url_for(self.url)})
