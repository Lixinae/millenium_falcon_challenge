import json
import os

from flask import jsonify, request, redirect, flash, url_for
from flask_restx import Resource
from werkzeug.utils import secure_filename

from backend_millenium_falcon_computer.api import api_bp_api
from backend_millenium_falcon_computer.configuration.configuration import allowed_file_extensions_upload, web_upload_dir
from backend_millenium_falcon_computer.odds_success_calculator.calculator import calculate_odds_of_success


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_file_extensions_upload


@api_bp_api.route("/upload_and_compute")
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

            # Todo -> Faire ça dans une thread pool
            odds_of_success = calculate_odds_of_success(json_data)

            return jsonify({"odds_of_success": odds_of_success,
                            "upload_file_json_answer": json_data})

# @api_bp_api.route("/askToComputeData")
# class ComputeDataApi(Resource):
#     def get(self):
#         return redirect(url_for('index_bp.index'))
#
#     def post(self):
#         computed_data = 0
#         if not os.path.exists(file_save_path):
#             return jsonify("Error, no file uploaded")
#
#
#         computed_data = compute_data()
#         # Todo -> Do task
#
#         return computed_data
