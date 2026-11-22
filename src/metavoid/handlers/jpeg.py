from pathlib import Path

from PIL import Image, ExifTags

from metavoid.handlers.gps import read_gps


def read_exif(file: Path) -> dict[str, str]:
    """Read JPEG EXIF metadata, including GPS coordinates."""

    metadata = {}

    with Image.open(file) as image:
        if image.format != "JPEG":
            raise ValueError("Expected a JPEG image")

        exif = image.getexif()

        for tag_id, value in exif.items():
            if tag_id == ExifTags.Base.GPSInfo:
                continue

            tag_name = ExifTags.TAGS.get(
                tag_id,
                f"Unknown-{tag_id}",
            )

            metadata[str(tag_name)] = str(value)

        gps_info = exif.get_ifd(ExifTags.IFD.GPSInfo)
        metadata.update(read_gps(gps_info))

    return metadata
