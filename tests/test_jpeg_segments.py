from pathlib import Path

import pytest
from PIL import Image, ExifTags

from metavoid.handlers.jpeg_segments import inspect_jpeg_segments


def test_detect_exif_segment(tmp_path: Path):
    file = tmp_path / "test.jpg"

    image = Image.new("RGB", (20, 20), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Metavoid Labs"

    image.save(file, format="JPEG", exif=exif)

    segments = inspect_jpeg_segments(file)

    assert any(segment["exif"] for segment in segments)
    assert segments[-1]["marker"] == "FFDA"


def test_jpeg_without_exif(tmp_path: Path):
    file = tmp_path / "clean.jpg"

    Image.new("RGB", (20, 20)).save(file, "JPEG")

    segments = inspect_jpeg_segments(file)

    assert not any(segment["exif"] for segment in segments)


def test_invalid_jpeg(tmp_path: Path):
    file = tmp_path / "invalid.jpg"
    file.write_bytes(b"Not a real JPEG")

    with pytest.raises(ValueError):
        inspect_jpeg_segments(file)


def test_truncated_segment(tmp_path: Path):
    file = tmp_path / "broken.jpg"

    # APP1 claims a length larger than available data.
    file.write_bytes(
        b"\xff\xd8\xff\xe1\x00\x20Exif\x00\x00"
    )

    with pytest.raises(ValueError):
        inspect_jpeg_segments(file)
