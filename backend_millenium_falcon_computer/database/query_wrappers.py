from backend_millenium_falcon_computer.database.models import Routes
from backend_millenium_falcon_computer.database import Session


class QueryWrappers:

    def __init__(self):
        self._session = Session()

    def query_all_routes(self):
        return self._session.query(Routes).all()

    def query_specific_origin(self, origin_str: str):
        return self._session.query(Routes).filter_by(origin=origin_str).all()

    def query_specific_destination(self, destination_str: str):
        return self._session.query(Routes).filter_by(destination=destination_str).all()

    def query_specific_origin_destination(self, origin_str: str, destination_str: str):
        return self._session.query(Routes).filter_by(origin=origin_str).filter_by(destination=destination_str).all()

    def query_specific_travel_time(self, travel_time: int):
        return self._session.query(Routes).filter_by(travel_time=travel_time).all()

