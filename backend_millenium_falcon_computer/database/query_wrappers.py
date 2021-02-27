from backend_millenium_falcon_computer.database.models import Routes
from backend_millenium_falcon_computer.database import Session


class QueryWrappers:

    def __init__(self):
        self._session = Session()

    def query_all_routes(self):
        """
        Permet de query toutes les routes dans la BDD pour la session
        :return: La liste des routes dans la BDD
        """
        return self._session.query(Routes).all()

    def query_specific_origin(self, origin_str: str):
        """
        Query toutes les routes ayant pour champ origin "origin_str"
        :param origin_str: L'origin sur laquelle on veut faire la requête
        :return: La liste des routes correspondant à ce champs
        """
        return self._session.query(Routes).filter_by(origin=origin_str).all()

    def query_specific_destination(self, destination_str: str):
        """
        Query toutes les routes ayant pour champ destination "destination_str"
        :param destination_str: La destination sur laquelle on veut faire la requête
        :return: La liste des routes correspondant à ce champs
        """
        return self._session.query(Routes).filter_by(destination=destination_str).all()

    def query_specific_origin_destination(self, origin_str: str, destination_str: str):
        """
        Query toutes les routes ayant pour champs origin "origin_str" et pour champ destination "destination_str"
        :param origin_str: L'origin sur laquelle on veut faire la requête
        :param destination_str: La destination sur laquelle on veut faire la requête
        :return: La liste des routes correspondant à ces champs
        """
        return self._session.query(Routes).filter_by(origin=origin_str).filter_by(destination=destination_str).all()

    def query_specific_travel_time(self, travel_time: int):
        """
        Query toutes les routes ayant pour champ travel_time "travel_time"
        :param travel_time: Le temps que l'on veut check
        :return: La liste des routes dans la BDD avec pour temps de voyage "travel_time"
        """
        return self._session.query(Routes).filter_by(travel_time=travel_time).all()

