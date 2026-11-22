
from pathlib import Path

import pytest

from metavoid.core import get_file_info


def test_get_file_info(tmp_path: Path):
    test_file = tmp_path / "example.txt"
    test_file.write_text("Hello, Metavoid!", encoding="utf-8")

    result = get_file_info(test_file)

    assert result["name"] == "example.txt"
    assert result["size"] == 16
    assert result["path"] == str(test_file.resolve())


def test_get_file_info_missing(tmp_path: Path):
    missing_file = tmp_path / "missing.txt"

    with pytest.raises(ValueError):
        get_file_info(missing_file)


def test_get_file_info_directory(tmp_path: Path):
    with pytest.raises(ValueError):
        get_file_info(tmp_path)
