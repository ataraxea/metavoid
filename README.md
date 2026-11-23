# Metavoid

**A cross-platform CLI tool for inspecting JPEG metadata and removing EXIF information.**

Metavoid is a lightweight, open-source Python utility for inspecting image metadata and cleaning JPEG files directly from your terminal.

Built with Python, Typer, and Pillow.

## Features

- Inspect JPEG EXIF metadata, including GPS information
- Identify JPEG segments such as EXIF, XMP, ICC profiles, and comments
- Remove EXIF metadata from JPEG images
- Lossless EXIF removal without image recompression
- Choose between creating a new file and replacing the original
- Specify a custom output path
- Preserve the original file by default
- Automated tests on Linux, Windows, and macOS

## Installation

**Requirements:** Python 3.12 or newer and pipx.

Install directly from GitHub:

`pipx install git+https://github.com/ataraxea/metavoid.git`

Verify installation:

`metavoid --version`

The command `metavoid` is available from your terminal after installation, provided the pipx application directory is on your PATH.

## Usage

**Inspect a file**

`metavoid inspect photo.jpg`

**Inspect JPEG segments**

`metavoid inspect photo.jpg --verbose`

**Create a cleaned copy**

`metavoid clean photo.jpg`

The original file is preserved.

**Remove EXIF without recompression**

`metavoid clean photo.jpg --lossless`

**Replace the original file**

`metavoid clean photo.jpg --in-place`

Warning: This operation replaces the original file. Create a backup before using it on important images.

**Choose a custom output file**

`metavoid clean photo.jpg --output public.jpg`

Short form:

`metavoid clean photo.jpg -o public.jpg`

The `--output` and `--in-place` options cannot be used together. Existing output files are not overwritten by default.

## Limitations

Metavoid v0.1.0 focuses on JPEG metadata inspection and EXIF cleaning.

- Lossless mode removes recognized EXIF APP1 segments, not all metadata.
- XMP, ICC profiles, comments, and other information may remain.
- Lossless mode rejects JPEG images that require EXIF Orientation correction.
- Standard cleaning re-encodes JPEG images and may change their size or quality.
- Cleaning other file formats is not supported yet.
- Removing EXIF does not guarantee anonymity or complete removal of sensitive information.

## Development

Clone the repository:

`git clone https://github.com/ataraxea/metavoid.git`

`cd metavoid`

Install dependencies:

`uv sync --locked`

Run the tests:

`uv run pytest -v`

Run the CLI locally:

`uv run metavoid --help`

## Contributing

Contributions, bug reports, and improvement suggestions are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development instructions.

## License

See [LICENSE](LICENSE) for licensing information.

## Status

**v0.1.0 — Initial public release preparation.**

The project is under active development.