from pathlib import Path

import pytest

from metavoid.detector import detect_format


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        (b"\xff\xd8\xff\xe0", "JPEG"),
        (b"\x89PNG\r\n\x1a\n", "PNG"),
        (b"%PDF-1.7", "PDF"),
        (b"GIF89a", "GIF"),
        (b"GIF87a", "GIF"),
        (b"Hello World", "UNKNOWN"),
    ],
)
def test_detect_format(
    tmp_path: Path,
    header: bytes,
    expected: str,
):
    file = tmp_path / "sample.bin"
    file.write_bytes(header)

    assert detect_format(file) == expected


def test_detect_format_ignores_extension(tmp_path: Path):
    file = tmp_path / "not_an_image.txt"
    file.write_bytes(b"\xff\xd8\xff\xe0")

    assert detect_format(file) == "JPEG"
