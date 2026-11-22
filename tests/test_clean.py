from pathlib import Path

import pytest

from PIL import Image, ExifTags

from metavoid.core import clean_file


def test_clean_jpeg(tmp_path: Path):
    original = tmp_path / "photo.jpg"

    image = Image.new("RGB", (20, 20), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Test Camera"

    image.save(original, format="JPEG", exif=exif)

    original_bytes = original.read_bytes()

    output = clean_file(original)

    assert output.exists()
    assert output != original
    assert original.read_bytes() == original_bytes

    with Image.open(output) as cleaned:
        assert cleaned.getexif() == {}


def test_clean_jpeg_no_overwrite(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    output = tmp_path / "photo_clean.jpg"

    Image.new("RGB", (20, 20)).save(original)
    output.write_bytes(b"DO NOT DELETE")

    with pytest.raises(FileExistsError):
        clean_file(original)

    assert output.read_bytes() == b"DO NOT DELETE"


def test_clean_unsupported_format(tmp_path: Path):
    file = tmp_path / "document.txt"
    file.write_text("Hello, Metavoid!")

    with pytest.raises(ValueError):
        clean_file(file)
