from pathlib import Path

import typer

from metavoid.core import get_file_info

app = typer.Typer(
    name="metavoid",
    help="Inspect and remove metadata from files.",
    no_args_is_help=True,
)


@app.command()
def inspect(file: Path):
    """Inspect metadata in a file."""
    try:
        info = get_file_info(file)
    except (ValueError, OSError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"File: {info['name']}")
    typer.echo(f"Size: {info['size']} bytes")
    typer.echo(f"Path: {info['path']}")
    typer.echo(f"Format: {info['format']}")

    metadata = info["metadata"]

    if metadata:
        typer.echo("\nEXIF metadata:")

        for key, value in metadata.items():
            typer.echo(f"  {key}: {value}")

    elif info["format"] == "JPEG":
        typer.echo("\nNo top-level EXIF metadata found.")
    else:
        typer.echo("\nMetadata inspection is not supported for this format yet.")



@app.command()
def clean(file: Path):
    """Remove metadata from a file."""
    typer.echo("Metadata cleaning is not implemented yet.")
