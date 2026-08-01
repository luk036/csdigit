# AGENTS.md - Agent Guidelines for csdigit

## Build, Lint, and Test Commands

### Testing
```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_csd.py

# Run a single test function
pytest tests/test_csd.py::test_csd_special

# Run tests matching a pattern
pytest -k "to_csdnnz"

# Run with coverage
pytest --cov csdigit --cov-report term-missing

# Run with hypothesis and pytest-benchmark (both in testing extras)
pytest --benchmark-only
```

Note: `addopts` in `setup.cfg` is commented out — coverage/verbose are NOT enabled by default, so pass `--cov` explicitly.

### Linting and Formatting
```bash
# Run all pre-commit hooks (recommended before committing)
pre-commit run --all-files

# Individual tools
black src/csdigit tests/    # Format code
isort src/csdigit tests/    # Sort imports (black profile)
flake8 src/ tests/          # Lint (max line length: 256)
mypy src/                   # Type check (Python 3.12 target)
```

### Build
```bash
tox -e build          # Build sdist + wheel
tox -e clean          # Remove build artifacts
```

### Documentation
```bash
tox -e docs           # Build HTML docs
tox -e doctests       # Run doctests
tox -e linkcheck      # Check broken links
```

## Code Style Guidelines

### Imports
- **Order**: stdlib → third-party → local (enforced by isort)
- **Tooling**: isort with Black profile (`.isort.cfg`, `known_first_party = csdigit`)
- Type hints from `typing` module: `List`, `Sequence`, `Tuple`, `Union`

### Formatting
- **Formatter**: Black (23.7.0)
- **Line length**: 256 characters (configured in setup.cfg)
- **Linting**: flake8 ignores E203, W503 (Black-compatible)
- **Pre-commit**: Enforced via `.pre-commit-config.yaml`

### Type Hints
- **Required**: All function parameters and return types
- **Style**: `param: type`, `-> ReturnType` (e.g., `def to_csd(decimal_value: float, places: int) -> str`)

### Naming Conventions
- **Functions**: snake_case (e.g., `to_csd`, `to_csdnnz`, `longest_repeated_substring`)
- **Private helpers**: Prefix with underscore (e.g., `_csd_str_to_int`)
- **Variables**: lowercase_with_underscores
- **Constants**: UPPER_CASE

### Docstrings
- **Style**: Sphinx/reStructuredText with `:param:`, `:type:`, `:return:`
- **Examples**: Include `>>>` doctest examples in every public function
- **Module docs**: Start with a descriptive module docstring
```python
def to_csd(decimal_value: float, places: int) -> str:
    """
    The `to_csd` function converts a given decimal number to its Canonical Signed Digit (CSD)
    representation with a specified number of decimal places.

    :param decimal_value: The decimal value to be converted
    :type decimal_value: float
    :param places: The number of decimal places to include
    :type places: int
    :return: CSD string representation

    Examples:
        >>> to_csd(28.5, 2)
        '+00-00.+0'
    """
```

### Error Handling
- **Pattern**: Log-and-continue for invalid CSD characters, not exceptions
  ```python
  else:
      logging.info(f"Encounter unknown character {digit}")
  ```
- **Deprecation**: Mark old functions with `.. deprecated::` (e.g., `to_decimal_using_pow`)
- **Testing**: Use `caplog` to assert log messages and `pytest.raises` for exceptions

### Testing Patterns
- **Framework**: pytest with hypothesis property-based tests and pytest-benchmark
- **Coverage**: `.coveragerc` with branch coverage, `source = csdigit`
- **Naming**: `test_*` prefix with descriptive names
- **Hypothesis**: Use `given`/`assume` for round-trip properties
```python
def test_csd_special() -> None:
    number = -342343593459544395894535439534985
    assert number == to_decimal(to_csd_i(number))
```

### Pre-commit Hooks
- trailing-whitespace, check-added-large-files, check-ast, check-json,
  check-merge-conflict, check-xml, check-yaml, debug-statements,
  end-of-file-fixer, requirements-txt-fixer, mixed-line-ending,
  isort (5.12.0), black (23.7.0), flake8 (6.1.0)
- Excludes `docs/conf.py` and `src/pycsd/`

### Configuration Files
- `setup.cfg`: Package metadata, flake8 settings (line length 256)
- `pyproject.toml`: Build system (setuptools_scm)
- `tox.ini`: Test environments (default, build, clean, docs, doctests, linkcheck, publish)
- `.isort.cfg`: Import sorting (Black profile, `known_first_party = csdigit`)
- `mypy.ini`: Type checking (Python 3.12)
- `.coveragerc`: Branch coverage config

## Key Project Context

csdigit is a Canonical Signed Digit (CSD) conversion library:
- **Core functions**: `to_csd`, `to_csd_i`, `to_csdnnz`, `to_csdnnz_i` (decimal → CSD), `to_decimal`, `to_decimal_using_pow` (CSD → decimal)
- **CSD multiplier**: `csd_multiplier.py` generates hardware multiplier Verilog from CSD strings, using `lcsre.py` (longest repeated substring) for sub-expression sharing
- **CLI**: Available via `python -m csdigit.cli` (no console_scripts entry point)
- **Key dependencies**: None at runtime (pure stdlib: `logging`, `math`); `hypothesis` + `pytest-benchmark` for testing
- **Used by**: [multiplierless](https://github.com/luk036/multiplierless)
