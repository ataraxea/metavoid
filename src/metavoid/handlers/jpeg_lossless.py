import os
import tempfile

from io import BytesIO
from pathlib import Path

from PIL import Image, ExifTags

from metavoid.handlers.jpeg_segments import strip_exif_bytes


def clean_jpeg_lossless(file: Path) -> Path:
    """Remove JPEG EXIF without recompressing image data."""

    output = file.with_name(
        f"{file.stem}_lossless{file.suffix}"
    )

    with Image.open(file) as image:
        image.load()

        if image.format != "JPEG":
            raise ValueError("Expected a JPEG image")

        orientation = image.getexif().get(
            ExifTags.Base.Orientation, 1
        )

        if orientation != 1:
            raise ValueError(
                "Lossless cleaning of rotated JPEGs "
                "is not supported yet"
            )

    cleaned = strip_exif_bytes(file)

    # Verify the resulting JPEG before writing it.
    with Image.open(BytesIO(cleaned)) as image:
        image.load()

        if image.format != "JPEG" or image.getexif():
            raise ValueError("JPEG verification failed")

    temporary_path = None

    try:
        fd, name = tempfile.mkstemp(
            prefix=".metavoid-",
            suffix=".tmp",
            dir=file.parent,
        )
        temporary_path = Path(name)

        with os.fdopen(fd, "wb") as stream:
            stream.write(cleaned)
            stream.flush()
            os.fsync(stream.fileno())

        # Publish without overwriting an existing file.
        os.link(temporary_path, output)

    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    return output
