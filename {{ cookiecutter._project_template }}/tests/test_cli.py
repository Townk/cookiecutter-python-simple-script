"""Test cases for the cli module."""
import pytest
from click.testing import CliRunner

from {{ cookiecutter.project.package }} import cli


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_run_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli.{{ cookiecutter.project.package }})
    assert result.exit_code == 0
