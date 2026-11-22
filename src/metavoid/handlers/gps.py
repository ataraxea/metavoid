from collections.abc import Mapping

from PIL.ExifTags import GPS


def to_decimal(coordinates, reference: str) -> float:
    """Convert EXIF GPS coordinates to decimal degrees."""

    degrees, minutes, seconds = map(float, coordinates)

    result = degrees + minutes / 60 + seconds / 3600

    if reference in ("S", "W"):
        result = -result
    elif reference not in ("N", "E"):
        raise ValueError(f"Invalid GPS reference: {reference}")

    return result


def read_gps(gps_info: Mapping) -> dict[str, str]:
    """Extract latitude and longitude from a GPS IFD."""

    required = (
        GPS.GPSLatitude,
        GPS.GPSLatitudeRef,
        GPS.GPSLongitude,
        GPS.GPSLongitudeRef,
    )

    if not all(tag in gps_info for tag in required):
        return {}

    try:
        latitude = to_decimal(
            gps_info[GPS.GPSLatitude],
            gps_info[GPS.GPSLatitudeRef],
        )

        longitude = to_decimal(
            gps_info[GPS.GPSLongitude],
            gps_info[GPS.GPSLongitudeRef],
        )
    except (ValueError, TypeError, OverflowError, ZeroDivisionError):
        return {}

    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return {}

    return {
        "GPSLatitude": f"{latitude:.6f}",
        "GPSLongitude": f"{longitude:.6f}",
    }
