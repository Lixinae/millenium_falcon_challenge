from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from backend_millenium_falcon_computer.configuration.configuration import ConfigurationFlask, ConfigurationApp, \
    web_static_dir, \
    web_templates_dir, resource_dir

db = SQLAlchemy()


# bootstrap = Bootstrap()
#
#
#
def blueprint_registrations(current_app):
    from backend_millenium_falcon_computer.index import index_bp
    current_app.register_blueprint(index_bp)


#
# # Creation de l'app
def create_app() -> Flask:
    global db
    from backend_millenium_falcon_computer.configuration.configuration import json_config_file_location
    configuration_app = ConfigurationApp()
    configuration_app.init_from_json_file(json_config_file_location)
    db_path = configuration_app.full_route_db
    configuration_flask = ConfigurationFlask(db_path)

    app = Flask(__name__,
                static_folder=web_static_dir + '/',
                template_folder=web_templates_dir + '/')

    app.config.from_object(configuration_flask)
    db.init_app(app)

    #     """
    #     Creation de l'application
    #     :param config_class: Classe de configuration -> Default is DevelopmentConfig
    #     :return: The created app with all the information
    #     """
    #     app.logger.debug("Logging set up finished ")
    #     db.init_app(app)
    #
    app.app_context().push()  # this does the binding
    #
    #     # We need those import for the metadata for the database
    #     # Todo -> Here add import for each model for the database
    #     import application.apps.app_model
    #     import application.portfolio.project_model
    import backend_millenium_falcon_computer.database.models
    db.create_all()
    #     app.logger.debug("Database init finished")
    #
    #     bootstrap.init_app(app)
    #     app.logger.debug("Bootstrap init finished")
    #
    blueprint_registrations(app)
    # app.logger.debug("Blueprint_registrations finished")
    #
    #     # add_functions_to_jinja2(app)
    #     # app.logger.debug("add_functions_to_jinja2 finished")
    #
    #     # assets_from_env = Environment(app)
    #     # create_static_bundles_assets(assets_from_env)
    #     # app.logger.debug("create_static_bundles_assets finished")
    #
    #     # if not config_class == TestingConfig:
    #     #     # Do not load the stats if we are in unit test mod
    #     #     from application.statistics.Request import Request
    #     #     statistics = Statistics(app, db, Request)
    #     #     app.logger.debug("Init of app finished")
    #     # if config_class == DevelopmentConfig:
    #     #     set_all_logger_to_level(logging.DEBUG)
    return app
