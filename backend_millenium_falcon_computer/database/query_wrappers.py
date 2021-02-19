from backend_millenium_falcon_computer.database.models import Routes
from backend_millenium_falcon_computer.database import session


def query_all_routes():
    return session.query(Routes).all()


def query_specific_origin(origin_str: str):
    return session.query(Routes).filter_by(origin=origin_str).all()


def query_specific_destination(destination_str: str):
    return session.query(Routes).filter_by(destination=destination_str).all()


def query_specific_travel_time(travel_time: int):
    return session.query(Routes).filter_by(travel_time=travel_time).all()
