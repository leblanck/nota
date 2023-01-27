""" This module sets up 'databse' functions and connectivity """
# nota/db.py

import configparser
import json
from pathlib import Path
from typing import Any, Dict, List, NamedTuple
from nota import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

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
        db_path.write_text("[]") #Empty to-do list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    todo_list: List[Dict[str, Any]]
    error: int

class DatabaseHandler:
    def __int__(self, db_path: Path) -> None:
        self._db_path = db_path

    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.optn("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError: # Will Catch JSON Format Issues
                    return DBResponse([], JSON_ERROR)
        except OSError: # Will Catch File IO Issues
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        except OSError: # Will Cath File IO Issues
            return DBResponse([], DB_W)
