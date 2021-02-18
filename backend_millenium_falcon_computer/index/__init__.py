from flask import Blueprint
from backend_millenium_falcon_computer import web_static_dir, web_templates_dir

index_bp = Blueprint('index_bp', __name__,
                     static_folder=web_static_dir + "/",
                     template_folder=web_templates_dir + "/")

from backend_millenium_falcon_computer.index import routes
