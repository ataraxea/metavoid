from pathlib import Path

from typer.testing import CliRunner
from PIL import Image, ExifTags

from metavoid.cli import app
from metavoid.core import get_file_info

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

def test_jpeg_gps_integration(tmp_path):
    """Test GPS extraction from a real JPEG file."""

    file = tmp_path / "photo.jpg"

    image = Image.new("RGB", (20, 20), "blue")
    exif = Image.Exif()

    gps = exif.get_ifd(ExifTags.IFD.GPSInfo)

    gps[ExifTags.GPS.GPSLatitudeRef] = "N"
    gps[ExifTags.GPS.GPSLatitude] = (56, 57, 0)
    gps[ExifTags.GPS.GPSLongitudeRef] = "E"
    gps[ExifTags.GPS.GPSLongitude] = (24, 6, 0)

    image.save(file, format="JPEG", exif=exif)

    # Test the core logic
    info = get_file_info(file)

    assert info["format"] == "JPEG"
    assert info["metadata"]["GPSLatitude"] == "56.950000"
    assert info["metadata"]["GPSLongitude"] == "24.100000"

    # Test the actual CLI
    runner = CliRunner()
    result = runner.invoke(app, ["inspect", str(file)])

    assert result.exit_code == 0
    assert "GPSLatitude: 56.950000" in result.output
    assert "GPSLongitude: 24.100000" in result.output

