from pathlib import Path

from metavoid.detector import detect_format


def get_file_info(file: Path) -> dict:
    """Get basic file information."""

    if not file.is_file():
        raise ValueError(f"Not a valid file: {file}")

    return {
        "name": file.name,
        "size": file.stat().st_size,
        "path": str(file.resolve()),
        "format": detect_format(file),
    }
