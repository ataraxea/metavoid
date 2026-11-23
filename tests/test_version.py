from importlib.metadata import version

from typer.testing import CliRunner

from metavoid.cli import app


def test_version_option():
    runner = CliRunner()

    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.output.strip() == (
        f"Metavoid {version('metavoid')}"
    )
