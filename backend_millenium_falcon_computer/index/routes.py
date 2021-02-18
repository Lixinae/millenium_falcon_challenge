from flask import make_response, render_template

from backend_millenium_falcon_computer.index import index_bp


@index_bp.route("/")
def index():
    return make_response(render_template('index.html', title="Millenium falcon challenge"), 200)
