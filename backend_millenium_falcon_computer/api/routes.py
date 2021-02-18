from flask import jsonify
from flask_restx import Resource

from backend_millenium_falcon_computer.api import api_bp_api


# Todo -> Change the name to something correct
# Todo -> Add new classes for each api routes : Envoie de fichier / recupération des informations etc....
@api_bp_api.route("")
class Api(Resource):
    def get(self):
        return jsonify("This is a dummy get")
        pass

    def post(self):
        return jsonify("This is a dummy post")
        pass
