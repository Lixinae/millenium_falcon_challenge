from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend_millenium_falcon_computer.configuration.configuration import config

# Default values
Session = sessionmaker(autocommit=False, autoflush=False)
Base = declarative_base()


def init_db():
    """
    On doit lancer ça après l'initialisation de la configuration pour
    :return:
    """
    global Session, Base
    engine = create_engine(config.sql_alchemy_database_url, connect_args={"check_same_thread": False})
    Session.configure(bind=engine)
    Base = declarative_base()

    # Initialisation des tables de la BDD
    Base.metadata.create_all(bind=engine)
