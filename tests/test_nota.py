""" Testing for Nota """
# tests/test_nota.py
from typer.testing import CliRunner
from nota import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    """ Tests the '--version' command """
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout
