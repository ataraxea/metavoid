from pathlib import Path

import os
import tempfile

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
    """Create and verify a JPEG copy without EXIF."""

    output = file.with_name(
        f"{file.stem}_clean{file.suffix}"
    )

    if output.exists():
        raise FileExistsError(
            f"Output already exists: {output}"
        )

    temporary_path = None

    try:
        with Image.open(file) as image:
            if image.format != "JPEG":
                raise ValueError("Expected a JPEG image")

            cleaned = ImageOps.exif_transpose(image)

            fd, name = tempfile.mkstemp(
                prefix=".metavoid-",
                suffix=".tmp",
                dir=file.parent,
            )

            temporary_path = Path(name)

            with os.fdopen(fd, "wb") as stream:
                cleaned.save(
                    stream,
                    format="JPEG",
                    quality=95,
                    exif=b"",
                )

                stream.flush()
                os.fsync(stream.fileno())

        with Image.open(temporary_path) as result:
            result.load()

            if result.format != "JPEG":
                raise ValueError("Invalid output format")

            if result.getexif():
                raise ValueError(
                    "EXIF verification failed"
                )

        os.link(temporary_path, output)

        return output

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
