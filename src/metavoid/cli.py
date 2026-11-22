from pathlib import Path

import typer

from metavoid.handlers.jpeg_metadata import get_jpeg_segment_report

from metavoid.core import get_file_info, clean_file

app = typer.Typer(
    name="metavoid",
    help="Inspect and remove metadata from files.",
    no_args_is_help=True,
)

@app.command()
def inspect(
    file: Path,
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed JPEG segment information.",
    ),
):
    """Inspect file metadata."""

    try:
        info = get_file_info(file)

        report = None

        if verbose and info["format"] == "JPEG":
            report = get_jpeg_segment_report(file)

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
        typer.echo("\nMetadata inspection is not supported yet.")

    if report is not None:
        typer.echo("\nJPEG segments:")

        for segment in report:
            typer.echo(
                f"  {segment['marker']:<6} "
                f"{segment['type']:<15} "
                f"{segment['size']} bytes"
            )

        detected = {segment["type"] for segment in report}

        typer.echo("\nDetected:")
        for kind in ("EXIF", "XMP", "ICC", "Photoshop", "Comment"):
            status = "Yes" if kind in detected else "No"
            typer.echo(f"  {kind}: {status}")

@app.command()
def clean(
    file: Path,
    lossless: bool = typer.Option(
        False,
        "--lossless",
        help="Remove JPEG EXIF without recompression.",
    ),
):
    """Create a cleaned copy of a supported file."""

    try:
        output = clean_file(file, lossless=lossless)

    except (ValueError, OSError) as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Original: {file}")
    typer.echo(f"Cleaned: {output}")
    typer.echo(f"Mode: {'lossless' if lossless else 'standard'}")
    typer.echo("EXIF verification: passed")
