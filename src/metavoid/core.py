import os
import shutil
import tempfile

from pathlib import Path

from metavoid.detector import detect_format
from metavoid.handlers.jpeg import read_exif, clean_jpeg
from metavoid.handlers.jpeg_lossless import clean_jpeg_lossless


def get_file_info(file: Path) -> dict:
    """Get file information and supported metadata."""

    if not file.is_file():
        raise ValueError(f"Not a valid file: {file}")

    file_format = detect_format(file)

    metadata = {}

    if file_format == "JPEG":
        metadata = read_exif(file)

    return {
        "name": file.name,
        "size": file.stat().st_size,
        "path": str(file.resolve()),
        "format": file_format,
        "metadata": metadata,
    }


def clean_file(
    file: Path,
    lossless: bool = False,
    output: Path | None = None,
    in_place: bool = False,
) -> Path:
    """Clean JPEG metadata with configurable output behavior."""

    if not file.is_file():
        raise ValueError(f"Not a valid file: {file}")

    if in_place and output is not None:
        raise ValueError(
            "--in-place and --output cannot be used together"
        )

    if in_place and file.is_symlink():
        raise ValueError(
            "In-place cleaning of symbolic links is not supported"
        )

    source = file.resolve()
    file_format = detect_format(source)

    if file_format != "JPEG":
        raise ValueError(
            f"Cleaning is not supported for {file_format}"
        )

    if output is not None:
        destination = output.resolve()
        if destination == source:
            raise ValueError(
                "Use --in-place to replace the original file"
            )
        if destination.exists():
            raise FileExistsError(
                f"Output already exists: {destination}"
            )
        working_parent = destination.parent
    else:
        destination = None
        working_parent = source.parent

    if not working_parent.is_dir():
        raise ValueError(
            f"Output directory does not exist: {working_parent}"
        )

    with tempfile.TemporaryDirectory(
        prefix=".metavoid-",
        dir=working_parent,
    ) as directory:
        workdir = Path(directory)
        staged_source = workdir / source.name

        shutil.copyfile(source, staged_source)

        if lossless:
            staged_result = clean_jpeg_lossless(staged_source)
        else:
            staged_result = clean_jpeg(staged_source)

        if not staged_result.is_file():
            raise ValueError("Cleaning produced no output file")

        if in_place:
            os.replace(staged_result, source)
            return file

        if destination is None:
            destination = source.parent / staged_result.name

        os.link(staged_result, destination)

    return destination
