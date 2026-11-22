from pathlib import Path

import pytest

from metavoid.handlers.jpeg_segments import (
    inspect_jpeg_segments,
    strip_exif_bytes,
)


@pytest.mark.parametrize(
    "content",
    [
        b"",
        b"Hello World",
        b"\xff\xd8",
        b"\xff\xd8\xff",
        b"\xff\xd8\xff\xe1",
        b"\xff\xd8\xff\xe1\x00\x01",
        b"\xff\xd8\xff\xe1\x00\x20Exif\x00\x00",
        b"\xff\xd8\x00\x00",
        b"\xff\xd8\xff\xd9",
    ],
)
def test_reject_malformed_jpeg(
    tmp_path: Path,
    content: bytes,
):
    file = tmp_path / "broken.jpg"
    file.write_bytes(content)

    with pytest.raises(ValueError):
        inspect_jpeg_segments(file)


def test_lossless_rejects_malformed_header(tmp_path: Path):
    file = tmp_path / "broken.jpg"

    file.write_bytes(
        b"\xff\xd8\xff\xe1\x00\x20Exif\x00\x00"
    )

    with pytest.raises(ValueError):
        strip_exif_bytes(file)

    assert file.exists()
