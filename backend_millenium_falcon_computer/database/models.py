from sqlalchemy import Column, Integer, String
from backend_millenium_falcon_computer import db


# Todo -> Corriger le modèle
class Apps(db.Model):
    __tablename__ = "Routes"
    origin = Column(String(128))
    destination = Column(String(128))
    travel_time = Column(Integer)
    # ORIGIN (TEXT): Name of the origin planet. Cannot be null or empty.
    # DESTINATION (TEXT): Name of the destination planet. Cannot be null or empty.
    # TRAVEL_TIME (INTEGER): Number days needed to travel from one planet to the other. Must be strictly positive.

    # def __init__(self, name: str, quick_description: str, url: str):
    #     self.name = name
    #     self.quick_description = quick_description
    #     self.url = url
    #
    # def __repr__(self):
    #     return '<Id:{}\n' \
    #            'Nom projet: {}\n' \
    #            'Description rapide:{}\n' \
    #            'Miniature:{}\n' \
    #            'Url:{}>\n'.format(self.id,
    #                               self.name,
    #                               self.quick_description,
    #                               url_for('static', filename=self.miniature_path),
    #                               url_for(self.url))
    #
    # def to_dict(self):
    #     return jsonify({"Id": self.id,
    #                     'name': self.name,
    #                     'quick_description': self.quick_description,
    #                     'miniature': url_for('static', filename=self.miniature_path),
    #                     'url': url_for(self.url)})
