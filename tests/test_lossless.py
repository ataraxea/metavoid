from pathlib import Path
from io import BytesIO

from metavoid.handlers.jpeg_lossless import clean_jpeg_lossless

from PIL import Image, ExifTags

from metavoid.handlers.jpeg_segments import (
    inspect_jpeg_segments,
    strip_exif_bytes,
)


def test_lossless_exif_removal(tmp_path: Path):
    file = tmp_path / "photo.jpg"

    image = Image.new("RGB", (20, 20), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Metavoid Labs"

    image.save(file, format="JPEG", exif=exif)

    original = file.read_bytes()
    segments = inspect_jpeg_segments(file)

    exif_segments = [
        segment for segment in segments
        if segment["exif"]
    ]

    assert len(exif_segments) == 1

    cleaned = strip_exif_bytes(file)

    segment = exif_segments[0]

    expected = (
        original[:segment["offset"]]
        + original[segment["end"]:]
    )

    assert cleaned == expected

    assert file.read_bytes() == original

    with Image.open(BytesIO(cleaned)) as result:
        result.load()
        assert result.getexif() == {}

    with Image.open(BytesIO(original)) as before:
        with Image.open(BytesIO(cleaned)) as after:
            assert before.convert("RGB").tobytes() == (
                after.convert("RGB").tobytes()
            )


def test_lossless_without_exif(tmp_path: Path):
    file = tmp_path / "plain.jpg"

    Image.new("RGB", (20, 20), "blue").save(
        file,
        format="JPEG",
    )

    original = file.read_bytes()
    cleaned = strip_exif_bytes(file)

    assert cleaned == original

def test_lossless_file_output(tmp_path):
    original = tmp_path / "photo.jpg"

    image = Image.new("RGB", (20, 20), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Metavoid Labs"

    image.save(original, format="JPEG", exif=exif)

    original_bytes = original.read_bytes()

    output = clean_jpeg_lossless(original)

    assert output.exists()
    assert original.read_bytes() == original_bytes
    assert output.read_bytes() == strip_exif_bytes(original)

    with Image.open(output) as cleaned:
        cleaned.load()
        assert cleaned.getexif() == {}