from backend_millenium_falcon_computer.database.models import Routes


def query_all_routes():
    return Routes.query.all()


def query_specific_origin(origin_str: str):
    return Routes.query.filter_by(origin=origin_str).all()


def query_specific_destination(destination_str: str):
    return Routes.query.filter_by(destination=destination_str).all()


def query_specific_travel_time(travel_time: int):
    return Routes.query.filter_by(travel_time=travel_time).all()
