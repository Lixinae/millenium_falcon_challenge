from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend_millenium_falcon_computer.configuration.configuration import config

# Default values
Session = sessionmaker(autocommit=False, autoflush=False)
base = declarative_base()


def init_db():
    """
    On doit lancer ça après l'initialisation de la configuration pour être sur que la valeur config.sql_alchemy_database_url est bien set
    :return:
    """
    global Session, base
    engine = create_engine(config.sql_alchemy_database_url, connect_args={"check_same_thread": False})
    Session.configure(bind=engine)
    base.metadata.bind = engine

    # Initialisation des tables de la BDD
    from backend_millenium_falcon_computer.database.models import Routes
    base.metadata.create_all()
