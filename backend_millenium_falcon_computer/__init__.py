from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#
db = SQLAlchemy()


# bootstrap = Bootstrap()
#
#
#
# def blueprint_registrations(current_app):
#     pass
#
# # Creation de l'app
def create_app():
    global db
    #     global statistics
    #     """
    #     Creation de l'application
    #     :param config_class: Classe de configuration -> Default is DevelopmentConfig
    #     :return: The created app with all the information
    #     """
    #     # Doit être global pour permettre d'avoir accès au logger dans l'application
    app = Flask(__name__)
    #                 static_folder=web_static_dir + '/general',
    #                 template_folder=web_templates_dir + '/')
    #     app.config.from_object(config_class)
    #     setup_logging(config_class)
    #     app.logger.debug("Logging set up finished ")
    #     db.init_app(app)
    #
    #     app.app_context().push()  # this does the bindind
    #
    #     # We need those import for the metadata for the database
    #     # Todo -> Here add import for each model for the database
    #     import application.apps.app_model
    #     import application.portfolio.project_model
    db.create_all()
    #     app.logger.debug("Database init finished")
    #
    #     bootstrap.init_app(app)
    #     app.logger.debug("Bootstrap init finished")
    #
    #     blueprint_registrations(app)
    #     app.logger.debug("Blueprint_registrations finished")
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
