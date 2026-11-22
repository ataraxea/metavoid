from io import BytesIO
from pathlib import Path

from PIL import Image, ExifTags

from metavoid.handlers.jpeg_segments import (
    inspect_jpeg_segments,
    strip_exif_bytes,
)
from metavoid.handlers.jpeg_metadata import (
    get_jpeg_segment_report,
)


def make_segment(marker: int, payload: bytes) -> bytes:
    """Build a JPEG segment with a length field."""

    length = len(payload) + 2

    if length > 65535:
        raise ValueError("Segment is too large")

    return (
        b"\xff"
        + bytes([marker])
        + length.to_bytes(2, "big")
        + payload
    )


def test_preserve_other_segments(tmp_path: Path):
    file = tmp_path / "complex.jpg"

    image = Image.new("RGB", (20, 20), "blue")

    exif = Image.Exif()
    exif[ExifTags.Base.Make] = "Metavoid Labs"

    image.save(file, format="JPEG", exif=exif)

    original = file.read_bytes()

    xmp = make_segment(
        0xE1,
        b"http://ns.adobe.com/xap/1.0/\x00"
        b"<x:xmpmeta>Test</x:xmpmeta>",
    )

    icc = make_segment(
        0xE2,
        b"ICC_PROFILE\x00\x01\x01"
        + b"TEST_PROFILE",
    )

    comment = make_segment(
        0xFE,
        b"Metavoid test comment",
    )

    extra = xmp + icc + comment

    file.write_bytes(original[:2] + extra + original[2:])

    before = file.read_bytes()
    segments = inspect_jpeg_segments(file)

    exif_segments = [
        segment for segment in segments
        if segment["exif"]
    ]

    assert len(exif_segments) == 1

    exif_segment = exif_segments[0]

    cleaned = strip_exif_bytes(file)

    expected = (
        before[:exif_segment["offset"]]
        + before[exif_segment["end"]:]
    )

    assert cleaned == expected

    assert file.read_bytes() == before

    with Image.open(BytesIO(cleaned)) as result:
        result.load()
        assert result.getexif() == {}

    cleaned_file = tmp_path / "cleaned.jpg"
    cleaned_file.write_bytes(cleaned)

    report = get_jpeg_segment_report(cleaned_file)
    detected = {segment["type"] for segment in report}

    assert "EXIF" not in detected
    assert "XMP" in detected
    assert "ICC" in detected
    assert "Comment" in detected


def test_multiple_exif_segments(tmp_path: Path):
    file = tmp_path / "multiple_exif.jpg"

    Image.new("RGB", (20, 20), "blue").save(
        file,
        format="JPEG",
    )

    exif1 = make_segment(
        0xE1,
        b"Exif\x00\x00" + b"test-one",
    )

    exif2 = make_segment(
        0xE1,
        b"Exif\x00\x00" + b"test-two",
    )

    original = file.read_bytes()

    file.write_bytes(
        original[:2] + exif1 + exif2 + original[2:]
    )

    cleaned = strip_exif_bytes(file)

    assert cleaned == original
