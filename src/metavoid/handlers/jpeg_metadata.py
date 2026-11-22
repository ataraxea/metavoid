from pathlib import Path

from metavoid.handlers.jpeg_segments import inspect_jpeg_segments


def classify_segment(marker: str, payload: bytes) -> str:
    """Identify known JPEG metadata segments."""

    if marker == "APP0" and payload.startswith(b"JFIF\x00"):
        return "JFIF"

    if marker == "APP1":
        if payload.startswith(b"Exif\x00\x00"):
            return "EXIF"

        if payload.startswith(b"http://ns.adobe.com/xap/1.0/\x00"):
            return "XMP"

    if marker == "APP2" and payload.startswith(b"ICC_PROFILE\x00"):
        return "ICC"

    if marker == "APP13" and payload.startswith(b"Photoshop 3.0\x00"):
        return "Photoshop"

    if marker == "FFFE":
        return "Comment"

    if marker == "FFDA":
        return "Start of Scan"

    return "Other"


def get_jpeg_segment_report(file: Path) -> list[dict]:
    """Return information about JPEG segments."""

    data = file.read_bytes()
    segments = inspect_jpeg_segments(file)

    report = []

    for segment in segments:
        # JPEG length includes its two length bytes.
        payload_start = segment["end"] - segment["length"] + 2
        payload = data[payload_start:segment["end"]]

        report.append({
            "marker": segment["marker"],
            "type": classify_segment(
                segment["marker"],
                payload,
            ),
            "size": segment["end"] - segment["offset"],
        })

    return report
