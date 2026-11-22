import pytest

from PIL.ExifTags import GPS

from metavoid.handlers.gps import read_gps, to_decimal


@pytest.mark.parametrize(
    ("coordinates", "reference", "expected"),
    [
        ((56, 57, 0), "N", 56.95),
        ((56, 57, 0), "S", -56.95),
        ((24, 6, 0), "E", 24.1),
        ((24, 6, 0), "W", -24.1),
    ],
)
def test_to_decimal(coordinates, reference, expected):
    result = to_decimal(coordinates, reference)
    assert result == pytest.approx(expected)


def test_invalid_reference():
    with pytest.raises(ValueError):
        to_decimal((56, 57, 0), "X")


def test_read_gps():
    gps_info = {
        GPS.GPSLatitude: (56, 57, 0),
        GPS.GPSLatitudeRef: "N",
        GPS.GPSLongitude: (24, 6, 0),
        GPS.GPSLongitudeRef: "E",
    }

    result = read_gps(gps_info)

    assert result == {
        "GPSLatitude": "56.950000",
        "GPSLongitude": "24.100000",
    }


def test_missing_gps():
    assert read_gps({}) == {}


def test_incomplete_gps():
    gps_info = {
        GPS.GPSLatitude: (56, 57, 0),
        GPS.GPSLatitudeRef: "N",
    }

    assert read_gps(gps_info) == {}


def test_out_of_range_gps():
    gps_info = {
        GPS.GPSLatitude: (120, 0, 0),
        GPS.GPSLatitudeRef: "N",
        GPS.GPSLongitude: (24, 0, 0),
        GPS.GPSLongitudeRef: "E",
    }

    assert read_gps(gps_info) == {}
