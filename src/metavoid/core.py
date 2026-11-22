from pathlib import Path


def get_file_info(file: Path) -> dict:
    """Get basic filesystem information."""

    if not file.is_file():
        raise ValueError(f"Not a valid file: {file}")

    return {
        "name": file.name,
        "size": file.stat().st_size,
        "path": str(file.resolve()),
    }
