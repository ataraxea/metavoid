from pathlib import Path

from PIL import Image, ExifTags
from PIL import ImageOps

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



def clean_jpeg(file: Path) -> Path:
    """Create a JPEG copy without EXIF metadata."""

    output = file.with_name(
        f"{file.stem}_clean{file.suffix}"
    )

    with Image.open(file) as image:
        if image.format != "JPEG":
            raise ValueError("Expected a JPEG image")

        cleaned = ImageOps.exif_transpose(image)

        created = False

        try:
            with output.open("xb") as stream:
                created = True
                cleaned.save(
                    stream,
                    format="JPEG",
                    quality=95,
                    exif=b"",
                )

            with Image.open(output) as result:
                result.load()

                if result.getexif():
                    raise ValueError(
                        "EXIF verification failed"
                    )

        except Exception:
            if created:
                output.unlink(missing_ok=True)
            raise

    return output
