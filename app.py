from flask import Flask

from backend_millenium_falcon_computer import create_app
from backend_millenium_falcon_computer.configuration import configuration


def create_server():
    return create_app()


if __name__ == '__main__':
    app = create_server()
    app.run(host="0.0.0.0", port='80')
