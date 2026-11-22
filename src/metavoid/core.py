from pathlib import Path

from metavoid.detector import detect_format
from metavoid.handlers.jpeg import read_exif
from metavoid.handlers.jpeg import clean_jpeg


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

def clean_file(file: Path) -> Path:
    """Clean metadata from a supported file."""

    if not file.is_file():
        raise ValueError(f"Not a valid file: {file}")

    file_format = detect_format(file)

    if file_format == "JPEG":
        return clean_jpeg(file)

    raise ValueError(
        f"Cleaning is not supported for {file_format}"
    )
