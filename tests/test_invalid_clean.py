from pathlib import Path

import pytest

from metavoid.core import clean_file


def test_corrupted_jpeg_creates_no_output(
    tmp_path: Path,
):
    original = tmp_path / "corrupted.jpg"
    output = tmp_path / "corrupted_lossless.jpg"

    original.write_bytes(
        b"\xff\xd8\xff\xe1\x00\x20Exif\x00\x00"
    )

    original_bytes = original.read_bytes()

    with pytest.raises((ValueError, OSError)):
        clean_file(original, lossless=True)

    assert not output.exists()
    assert original.read_bytes() == original_bytes
    assert list(tmp_path.glob(".metavoid-*.tmp")) == []
