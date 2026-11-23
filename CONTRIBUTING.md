# Contributing to Metavoid

Thank you for your interest in contributing to Metavoid!

Metavoid is an open-source Python CLI project focused on inspecting metadata and safely cleaning JPEG images.

Contributions of all sizes are welcome.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork.
3. Create a new branch for your changes.
4. Install development dependencies.
5. Make your changes and add tests.
6. Open a pull request.

## Development Setup

Metavoid uses Python 3.12+ and uv for development.

Clone the project:

`git clone https://github.com/ataraxea/metavoid.git`

`cd metavoid`

Install dependencies:

`uv sync --locked`

Run the application:

`uv run metavoid --help`

Run all tests:

`uv run pytest -v`

## Development Guidelines

- Keep changes focused and easy to review.
- Add or update tests when changing behavior.
- Preserve backward compatibility where practical.
- Do not silently overwrite user files.
- Avoid introducing unnecessary dependencies.
- Keep metadata-cleaning behavior explicit and documented.
- Do not claim complete metadata removal unless it has been verified.

## Commit Messages

We use Conventional Commits.

Examples:

- `feat: add support for a new metadata type`
- `fix: handle malformed JPEG segments`
- `test: cover EXIF orientation edge cases`
- `docs: improve installation instructions`
- `refactor: simplify JPEG segment parsing`

## Pull Requests

Before opening a pull request:

- Make sure your code works locally.
- Run `uv run pytest -v`.
- Add tests for bug fixes or new functionality.
- Update documentation when user-facing behavior changes.
- Explain what changed and why.

GitHub Actions runs automated checks on Linux, Windows, and macOS.

A pull request may require review and additional changes before merging.

## Reporting Bugs

When reporting a bug, please include:

- Your operating system
- Python version
- Metavoid version (`metavoid --version`)
- The command you executed
- Expected behavior
- Actual behavior
- Relevant error messages

**Privacy note:** Images can contain sensitive information, including GPS coordinates and personal details. Do not upload private photographs or metadata dumps to public issues without reviewing and sanitizing them first.

## Feature Requests

Before implementing a major feature, consider opening an issue to discuss the proposed behavior and scope.

## Security Issues

If you discover a potential security vulnerability, avoid publishing exploit details or sensitive test files in a public issue. Contact the maintainer privately through an available GitHub security-reporting channel.

## Code of Conduct

Please communicate respectfully and keep technical discussions constructive.

Thank you for helping improve Metavoid!