from pathlib import Path

from PIL import Image, ExifTags

from metavoid.handlers.jpeg import read_exif


def test_read_exif(tmp_path: Path):
    file = tmp_path / "test.jpg"

    image = Image.new("RGB", (10, 10), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Metavoid Labs"
    exif[ExifTags.Base.Model] = "Test Camera"

    image.save(file, format="JPEG", exif=exif)

    metadata = read_exif(file)

    assert metadata["Make"] == "Metavoid Labs"
    assert metadata["Model"] == "Test Camera"


def test_read_exif_empty(tmp_path: Path):
    file = tmp_path / "empty.jpg"

    image = Image.new("RGB", (10, 10), "blue")
    image.save(file, format="JPEG")

    assert read_exif(file) == {}
