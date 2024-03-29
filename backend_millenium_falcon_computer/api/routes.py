import concurrent.futures
import json
import os

from flask import jsonify, request, redirect, flash, url_for
from flask_restx import Resource
from werkzeug.utils import secure_filename

from backend_millenium_falcon_computer.api import api_bp_api
from backend_millenium_falcon_computer.configuration.configuration import allowed_file_extensions_upload, web_upload_dir
from backend_millenium_falcon_computer.odds_success_calculator.calculator import calculate_best_odds_of_success


def allowed_file(filename):
    """
    Indique si un fichier avec une extension
    :param filename: Nom du fichier qu'il faut verifier
    :return: True si l'extension de fichier est autorisé, False sinon
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_extensions_upload


@api_bp_api.route("/upload_and_compute")
class UploadFileApi(Resource):
    def get(self):
        """
        En cas de get : redirection sur la page d'index
        :return: On redirige sur la page d'index
        """
        return redirect(url_for('index_bp.index'))

    def post(self):
        """
        Method post sur l'api "UploadFileApi"

        :return: Si tout va bien on renvoie un json avec les données de réponse, sinon on redirige sur l'url qui appel l'api
        """
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_save_path = os.path.join(web_upload_dir, filename)
            file.save(file_save_path)
            with open(file_save_path, 'r') as jsonfile:
                json_data_empire = json.load(jsonfile)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(calculate_best_odds_of_success, json_data_empire)
                odds_of_success_info = future.result()

            odds_of_success = 0
            trajectory = []
            refueled_on = []
            if odds_of_success_info:
                if "odds_of_success" in odds_of_success_info:
                    odds_of_success = odds_of_success_info["odds_of_success"]
                if "trajectory" in odds_of_success_info:
                    trajectory = odds_of_success_info["trajectory"]
                if "refueled_on" in odds_of_success_info:
                    refueled_on = odds_of_success_info["refueled_on"]

            return jsonify({"odds_of_success": odds_of_success,
                            "upload_file_json_answer": json_data_empire,
                            "trajectory": trajectory,
                            "refueled_on": refueled_on
                            })
