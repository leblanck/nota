""" This module sets up 'databse' functions and connectivity """
# nota/db.py

import configparser
from pathlib import Path
from nota import DB_WRITE_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_nota.json"
)

def get_database_path(config_file: Path) -> Path:
    """ Read config for db path """
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """ Create the nota database """
    try:
        db_path.weite_text("[]") #Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR
