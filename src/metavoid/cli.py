from pathlib import Path

import typer

app = typer.Typer(
    name="metavoid",
    help="Inspect and remove metadata from files.",
    no_args_is_help=True,
)



@app.command()
def inspect(file: Path):
    """Inspect metadata in a file."""

    if not file.exists():
        typer.echo(f"Error: File '{file}' does not exist.")
        raise typer.Exit(code=1)

    if not file.is_file():
        typer.echo(f"Error: '{file}' is not a regular file.")
        raise typer.Exit(code=1)

    typer.echo(f"File: {file.name}")
    typer.echo(f"Size: {file.stat().st_size} bytes")
    typer.echo(f"Path: {file.resolve()}")



@app.command()
def clean(file: Path):
    """Remove metadata from a file."""
    typer.echo(f"Cleaning: {file}")
