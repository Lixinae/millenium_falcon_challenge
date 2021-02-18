from flask import Blueprint
from flask_restx import Api

from backend_millenium_falcon_computer.configuration.configuration import web_static_dir, web_templates_dir

api_bp = Blueprint('api_bp', __name__,
                   static_folder=web_static_dir,
                   template_folder=web_templates_dir)

api_bp_api = Api(api_bp, version="1.0", title="API", description="The API for the millenium falcon challenge app", prefix="/api")

from backend_millenium_falcon_computer.api import routes
