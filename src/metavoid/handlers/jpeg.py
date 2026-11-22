from pathlib import Path

from PIL import Image, ExifTags


def read_exif(file: Path) -> dict[str, str]:
    """Read top-level EXIF tags from a JPEG image."""

    metadata = {}

    with Image.open(file) as image:
        if image.format != "JPEG":
            raise ValueError("Expected a JPEG image")

        exif = image.getexif()

        for tag_id, value in exif.items():
            tag_name = ExifTags.TAGS.get(
                tag_id,
                f"Unknown-{tag_id}",
            )

            metadata[str(tag_name)] = str(value)

    return metadata
