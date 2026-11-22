from pathlib import Path

SIGNATURES = {
    b"\xff\xd8\xff": "JPEG",
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"%PDF-": "PDF",
    b"GIF87a": "GIF",
    b"GIF89a": "GIF",
}


def detect_format(file: Path) -> str:
    """Detect file format using magic bytes."""

    with file.open("rb") as stream:
        header = stream.read(8)

    for signature, format_name in SIGNATURES.items():
        if header.startswith(signature):
            return format_name

    return "UNKNOWN"
