import sys

# Todo -> Cli
# Prend 2 fichier en entrée (les 2 json) give-me-the-odds example1/millenium-falcon.json example1/empire.json
from backend_millenium_falcon_computer import ConfigurationApp

if __name__ == '__main__':
    argv = sys.argv[1]

    config = ConfigurationApp()
    config.init_from_json_file()
    # Todo -> Read files
    # example1/millenium-falcon.json -> Config file: need to read it
    # example1/empire.json
    # Todo -> Calculate proba -> This will be done in the backend part
    # Todo -> Print result
    pass