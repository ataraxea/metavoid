from pathlib import Path

import pytest

from PIL import Image, ExifTags

from metavoid.handlers.jpeg import clean_jpeg


def make_test_jpeg(path: Path) -> None:
    """Create a JPEG with fake EXIF metadata."""

    image = Image.new("RGB", (20, 20), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Metavoid Labs"

    image.save(path, format="JPEG", exif=exif)


def test_safe_clean(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    make_test_jpeg(original)

    original_bytes = original.read_bytes()

    output = clean_jpeg(original)

    assert output.exists()
    assert original.read_bytes() == original_bytes

    with Image.open(output) as image:
        image.load()
        assert image.getexif() == {}

    assert list(tmp_path.glob(".metavoid-*.tmp")) == []


def test_no_overwrite(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    output = tmp_path / "photo_clean.jpg"

    make_test_jpeg(original)
    output.write_bytes(b"IMPORTANT DATA")

    with pytest.raises(FileExistsError):
        clean_jpeg(original)

    assert output.read_bytes() == b"IMPORTANT DATA"


def test_cleanup_on_error(tmp_path: Path, monkeypatch):
    original = tmp_path / "photo.jpg"
    make_test_jpeg(original)

    def broken_link(*args, **kwargs):
        raise OSError("Simulated filesystem error")

    monkeypatch.setattr(
        "metavoid.handlers.jpeg.os.link",
        broken_link,
    )

    with pytest.raises(OSError):
        clean_jpeg(original)

    assert not (tmp_path / "photo_clean.jpg").exists()
    assert list(tmp_path.glob(".metavoid-*.tmp")) == []
