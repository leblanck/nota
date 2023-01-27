""" Testing for Nota """
# tests/test_nota.py
import json
import pytest
from typer.testing import CliRunner
from nota import DB_READ_ERROR, SUCCESS, __app_name__, __version__, cli, nota

runner = CliRunner()

test_data_1 = {
    "description": ["Clean", "the", "bathroom"],
    "priority": 1,
    "todo": {
        "Description": "Clean the bathroom",
        "Priority": 1,
        "Done": False,
    }
}

test_data_2 = {
    "description": ["Do the laundry"],
    "priority": 2,
    "todo": {
        "Description": ["Do the laundry"],
        "Priority": 2,
        "Done": False,
    }
}

def test_version():
    """ Tests the '--version' command """
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

@pytest.fixture
def mock_json_file(tmp_path):
    """ Create Mock JSON db file """
    todo = [{"Description": "Get Some Milk", "Priority": 2, "Done": False}]
    db_file = tmp_path / "todo.json"
    with db_file.open("w") as db:
        json.dump(todo, db, indent=4)
    return db_file

@pytest.mark.parametrize(
    "description, priority, expected",
    [
        pytest.param(
            test_data_1["description"],
            test_data_1["priority"],
            (test_data_1["todo"], SUCCESS),
        ),
        pytest.param(
            test_data_2["description"],
            test_data_2["priority"],
            (test_data_2["todo"], SUCCESS),
        )
    ],
)

def test_add(mock_json_file, description, priority, expected):
    todoer = nota.Todoer(mock_json_file)
    assert todoer.add(description, priority) ==  expected
    read = todoer._db_handler.read_todos()
    assert len(read.todo_list) == 2