from flask import Flask
from backend_millenium_falcon_computer.database import Session, engine
from backend_millenium_falcon_computer.configuration.configuration import ConfigurationFlask, ConfigurationApp, \
    web_static_dir, \
    web_templates_dir, resource_dir


# bootstrap = Bootstrap()
#
#
#
def blueprint_registrations(current_app):
    from backend_millenium_falcon_computer.index import index_bp
    current_app.register_blueprint(index_bp)

    from backend_millenium_falcon_computer.api import api_bp
    current_app.register_blueprint(api_bp)


#
# # Creation de l'app
def init_db():
    from backend_millenium_falcon_computer.database import models
    models.Base.metadata.create_all(bind=engine)


def create_app() -> Flask:
    configuration_flask = ConfigurationFlask()

    current_app = Flask(__name__,
                        static_folder=web_static_dir + '/',
                        template_folder=web_templates_dir + '/')

    current_app.config.from_object(configuration_flask)
    init_db()

    #     """
    #     Creation de l'application
    #     :param config_class: Classe de configuration -> Default is DevelopmentConfig
    #     :return: The created app with all the information
    #     """
    #     app.logger.debug("Logging set up finished ")
    #     db.init_app(app)
    #
    current_app.app_context().push()  # this does the binding
    #
    #     # We need those import for the metadata for the database
    #     app.logger.debug("Database init finished")
    #
    #     bootstrap.init_app(app)
    #     app.logger.debug("Bootstrap init finished")
    #
    blueprint_registrations(current_app)

    # So we can upload files
    import secrets
    secret = secrets.token_urlsafe(32)
    current_app.secret_key = secret

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
    return current_app


app = create_app()
