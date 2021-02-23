from flask import Flask

from backend_millenium_falcon_computer.configuration.configuration import ConfigurationFlask, ConfigurationApp, \
    web_static_dir, \
    web_templates_dir, resource_dir
import secrets


def blueprint_registrations(current_app):
    """
    Enregistre tous les blueprint de l'application
    :param current_app: L'application flask courante
    """
    from backend_millenium_falcon_computer.index import index_bp
    current_app.register_blueprint(index_bp)

    from backend_millenium_falcon_computer.api import api_bp
    current_app.register_blueprint(api_bp)


#
# # Creation de l'app
def create_app() -> Flask:
    """
    Factory pour la création de l'application Flask
    :return: L'application flask créé
    """
    # Ici on peut rajouter une initialisation de la configuration par un fichier json,
    # Si l'on en veut un autre que celui par defaut
    # config_app.init_from_json_file(json_file)
    # Puis rajouter
    # init_db()
    # Pour override les valeurs par défauts

    configuration_flask = ConfigurationFlask()

    current_app = Flask(__name__,
                        static_folder=web_static_dir + '/',
                        template_folder=web_templates_dir + '/')

    current_app.config.from_object(configuration_flask)

    current_app.app_context().push()  # this does the binding

    blueprint_registrations(current_app)

    # So we can upload files
    # We need to do
    secret = secrets.token_urlsafe(32)
    current_app.secret_key = secret
    return current_app


app = create_app()
