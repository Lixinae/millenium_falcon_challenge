from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from backend_millenium_falcon_computer.configuration.configuration import config


engine = create_engine(config.sql_alchemy_database_url, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

session = Session()

# Initialisation des tables de la BDD
# On laisse le from ici pour eviter les import circulaire
from backend_millenium_falcon_computer.database import models
models.Base.metadata.create_all(bind=engine)

