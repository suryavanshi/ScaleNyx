# isort: skip_file
from infra_agent.api import cli
from typer.testing import CliRunner


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
