# GEMINI.md

## Project Overview

This project, `csdigit`, is a Python library for Canonical Signed Digit (CSD) conversion. CSD is a number representation system that uses only three symbols: `+`, `-`, and `0`. It is used in digital signal processing and other areas of computer science for efficient arithmetic operations.

The library provides functions to convert numbers between decimal format and CSD format. It supports both integers and floating-point numbers.

The main functions are:
* `to_csd`: Converts a decimal number to a CSD string.
* `to_csd_i`: Converts an integer to a CSD string.
* `to_decimal`: Converts a CSD string to a decimal number.
* `to_csdnnz`: Converts a decimal number to a CSD string with a specified maximum number of non-zero digits.
* `to_csdnnz_i`: Converts an integer to a CSD string with a specified maximum number of non-zero digits.

The project is structured as a standard Python package using `setuptools` and `PyScaffold`.

## Building and Running

### Dependencies

The project's dependencies are managed in `requirements/` folder.

* **Runtime dependencies:** `decorator`
* **Testing dependencies:** `codecov`, `coverage`, `hypothesis`, `pytest`, `pytest-benchmark`, `pytest-cov`

### Testing

The project uses `tox` for managing test environments and `pytest` for running tests.

To run the tests, execute the following command:

```bash
tox
```

This will run the tests in an isolated environment.

### Linting and Formatting

The project uses `pre-commit` with `isort`, `black`, and `flake8` to enforce code style and quality.

To run the linters and formatters, execute the following command:

```bash
pre-commit run --all-files
```

### Building the Package

The project uses `tox` to manage the build process.

To build the source distribution and wheel, run:

```bash
tox -e build
```

The distributable files will be located in the `dist/` directory.

To clean the build artifacts, run:

```bash
tox -e clean
```

### Documentation

The project's documentation is built using `Sphinx`.

To build the documentation, run:

```bash
tox -e docs
```

The generated documentation will be in `docs/_build/html/`.

## Development Conventions

* **Code Style:** The project follows the `black` code style and uses `isort` to sort imports. `flake8` is used for linting.
* **Testing:** The project uses `pytest` for testing. Tests are located in the `tests/` directory.
* **Commits:** The project uses `pre-commit` to run checks before each commit.
* **Versioning:** The project uses `setuptools_scm` for automatic versioning based on Git tags.
