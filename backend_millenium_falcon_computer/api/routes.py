import json
import os

from flask import jsonify, request, redirect, flash, url_for
from flask_restx import Resource
from werkzeug.utils import secure_filename

from backend_millenium_falcon_computer.api import api_bp_api

# Todo -> Change the name to something correct
# Todo -> Add new classes for each api routes : Envoie de fichier / recupération des informations etc....
from backend_millenium_falcon_computer.configuration.configuration import allowed_file_extensions_upload, web_upload_dir


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_extensions_upload


@api_bp_api.route("/upload_empire")
class UploadFileApi(Resource):
    def get(self):
        return redirect(url_for('index_bp.index'))

    def post(self):
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
                json_data = json.load(jsonfile)
                print(json_data)
                # Todo -> Voir si on compute ici
            return json_data

