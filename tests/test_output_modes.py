from pathlib import Path

from PIL import Image
from typer.testing import CliRunner

from metavoid.cli import app


runner = CliRunner()


def make_jpeg(path: Path, orientation: int = 1):
    exif = Image.Exif()
    exif[274] = orientation
    exif[271] = "Metavoid Labs"

    Image.new("RGB", (40, 20), "blue").save(
        path,
        format="JPEG",
        exif=exif,
    )


def test_in_place_removes_exif(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    make_jpeg(original)

    result = runner.invoke(
        app,
        ["clean", str(original), "--in-place"],
    )

    assert result.exit_code == 0, result.output
    assert original.exists()

    with Image.open(original) as image:
        image.load()
        assert not image.getexif()


def test_lossless_in_place(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    make_jpeg(original)

    result = runner.invoke(
        app,
        ["clean", str(original), "--lossless", "--in-place"],
    )

    assert result.exit_code == 0, result.output

    with Image.open(original) as image:
        image.load()
        assert not image.getexif()


def test_custom_output(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    output = tmp_path / "public.jpg"
    make_jpeg(original)

    before = original.read_bytes()

    result = runner.invoke(
        app,
        ["clean", str(original), "-o", str(output)],
    )

    assert result.exit_code == 0, result.output
    assert output.exists()
    assert original.read_bytes() == before


def test_existing_output_is_not_overwritten(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    output = tmp_path / "public.jpg"
    make_jpeg(original)
    output.write_bytes(b"keep this")

    result = runner.invoke(
        app,
        ["clean", str(original), "-o", str(output)],
    )

    assert result.exit_code != 0
    assert output.read_bytes() == b"keep this"


def test_conflicting_options(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    make_jpeg(original)

    before = original.read_bytes()

    result = runner.invoke(
        app,
        [
            "clean",
            str(original),
            "--in-place",
            "-o",
            str(tmp_path / "public.jpg"),
        ],
    )

    assert result.exit_code != 0
    assert original.read_bytes() == before


def test_failed_lossless_preserves_original(tmp_path: Path):
    original = tmp_path / "photo.jpg"
    make_jpeg(original, orientation=6)

    before = original.read_bytes()

    result = runner.invoke(
        app,
        [
            "clean",
            str(original),
            "--lossless",
            "--in-place",
        ],
    )

    assert result.exit_code != 0
    assert original.read_bytes() == before
    assert not list(tmp_path.glob(".metavoid-*"))
