from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from metavoid.cli import app
from metavoid.handlers.jpeg_metadata import (
    classify_segment,
    get_jpeg_segment_report,
)


def test_classify_segments():
    assert classify_segment("APP1", b"Exif\x00\x00data") == "EXIF"
    assert classify_segment(
        "APP1",
        b"http://ns.adobe.com/xap/1.0/\x00data",
    ) == "XMP"
    assert classify_segment("APP2", b"ICC_PROFILE\x00data") == "ICC"
    assert classify_segment("APP13", b"Photoshop 3.0\x00") == "Photoshop"
    assert classify_segment("FFFE", b"Comment") == "Comment"
    assert classify_segment("APP1", b"Unknown") == "Other"


def test_jpeg_segment_report(tmp_path: Path):
    file = tmp_path / "image.jpg"

    Image.new("RGB", (20, 20), "blue").save(
        file,
        format="JPEG",
    )

    report = get_jpeg_segment_report(file)

    assert len(report) > 0
    assert report[-1]["type"] == "Start of Scan"
    assert any(item["type"] == "JFIF" for item in report)


def test_verbose_cli(tmp_path: Path):
    file = tmp_path / "image.jpg"

    Image.new("RGB", (20, 20), "blue").save(
        file,
        format="JPEG",
    )

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["inspect", str(file), "--verbose"],
    )

    assert result.exit_code == 0
    assert "JPEG segments:" in result.output
    assert "JFIF" in result.output
    assert "Detected:" in result.output
