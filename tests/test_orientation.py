from pathlib import Path

import pytest
from PIL import Image

from metavoid.core import clean_file
from metavoid.handlers.jpeg_segments import strip_exif_bytes


def make_jpeg_with_orientation(
    path: Path,
    orientation: int,
) -> None:
    """Create a JPEG with a chosen EXIF Orientation."""

    image = Image.new("RGB", (40, 20), "blue")

    exif = Image.Exif()
    exif[274] = orientation

    image.save(
        path,
        format="JPEG",
        exif=exif,
    )


def test_lossless_accepts_normal_orientation(
    tmp_path: Path,
):
    original = tmp_path / "normal.jpg"
    output = tmp_path / "normal_lossless.jpg"

    make_jpeg_with_orientation(original, 1)

    expected = strip_exif_bytes(original)
    original_bytes = original.read_bytes()

    clean_file(original, lossless=True)

    assert output.exists()
    assert output.read_bytes() == expected
    assert original.read_bytes() == original_bytes

    with Image.open(output) as image:
        image.load()
        assert image.size == (40, 20)
        assert image.getexif().get(274, 1) == 1


def test_lossless_rejects_rotated_orientation(
    tmp_path: Path,
):
    original = tmp_path / "rotated.jpg"
    output = tmp_path / "rotated_lossless.jpg"

    make_jpeg_with_orientation(original, 6)

    original_bytes = original.read_bytes()

    with pytest.raises(ValueError):
        clean_file(original, lossless=True)

    assert original.read_bytes() == original_bytes
    assert not output.exists()
