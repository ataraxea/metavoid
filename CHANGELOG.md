# Changelog

All notable changes to Metavoid will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

## [0.1.0] — Initial Release

### Added

- Cross-platform command-line interface
- JPEG EXIF metadata inspection
- GPS coordinate parsing
- File format detection using magic bytes
- Verbose JPEG segment inspection
- JPEG metadata cleaning using Pillow
- Lossless EXIF removal without recompression
- Custom output paths with `--output`
- Original file replacement with `--in-place`
- Protection against accidental output overwrites
- EXIF Orientation safety checks
- CLI version information with `--version`
- Automated tests using pytest
- GitHub Actions testing on Linux, Windows, and macOS

### Known Limitations

- JPEG is the only supported cleaning format.
- Lossless mode removes recognized EXIF segments only.
- Other metadata may remain after cleaning.
- Lossless cleaning rejects images requiring Orientation correction.
- Complete privacy or anonymity is not guaranteed.