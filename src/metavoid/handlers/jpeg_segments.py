
from pathlib import Path


def inspect_jpeg_segments(file: Path) -> list[dict]:
    """Inspect JPEG segments before the first SOS marker."""

    data = file.read_bytes()

    if not data.startswith(b"\xff\xd8"):
        raise ValueError("Not a JPEG file")

    segments = []
    position = 2

    while position < len(data):
        start = position

        if data[position] != 0xFF:
            raise ValueError("Invalid JPEG marker")

        while position < len(data) and data[position] == 0xFF:
            position += 1

        if position >= len(data):
            raise ValueError("Truncated JPEG marker")

        marker = data[position]
        position += 1

        if marker == 0x00:
            raise ValueError("Unexpected stuffed byte")

        if marker == 0xD9:
            raise ValueError("JPEG ended before SOS")

        if marker == 0x01 or 0xD0 <= marker <= 0xD7:
            continue

        if position + 2 > len(data):
            raise ValueError("Truncated segment length")

        length = int.from_bytes(
            data[position:position + 2],
            "big",
        )

        if length < 2 or position + length > len(data):
            raise ValueError("Invalid segment length")

        payload = data[position + 2:position + length]

        name = (
            f"APP{marker - 0xE0}"
            if 0xE0 <= marker <= 0xEF
            else f"FF{marker:02X}"
        )

        segments.append({
            "marker": name,
            "offset": start,
            "length": length,
            "exif": (
                marker == 0xE1
                and payload.startswith(b"Exif\x00\x00")
            ),
        })

        position += length

        if marker == 0xDA:
            return segments

    raise ValueError("Missing JPEG SOS marker")
