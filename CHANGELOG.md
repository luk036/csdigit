# Changelog

## Version 0.6 (2026-11-20)

### Documentation
- **CSD tutorial paper, talk and demos**: Added the canonical-signed-digit tutorial paper, its accompanying presentation, and the demonstration scripts. (#2562cd1)

## Version 0.5 (2026-10-09)

### Bug Fixes
- **Package metadata**: Replaced the PyScaffold placeholder description and URLs in `setup.cfg` with the real csdigit project info. (#78f1f81)
- **Ruff warnings**: Resolved F403/E402/F821 warnings in the test files. (#9444e6f)
- **mypy config**: Removed the duplicate `ignore_missing_imports` entry from `mypy.ini`. (#ec86626)

### Testing & Code Quality
- **Multiplier tests**: Added `tests/test_csd_multiplier.py` (+78 lines) covering the CSD multiplier generators. (#64e3603)

### Code Cleanup
- **`MultiplierSpec` + shared `validate_csd`**: Introduced a `MultiplierSpec` parameter object and a single `validate_csd` helper so `generate_csd_multipliers` no longer takes bare positional tuples and both generators share one CSD format rule (legacy tuples still accepted). (#64e3603)
- **Simplified `to_decimal()`**: Extracted the duplicated parsing logic into a `_csd_str_to_int` helper. (#1f6e397)
- **Removed AI slop**: Stripped boilerplate from docstrings and comments and removed unused imports from the benchmark files. (#70b8612, #17d9897)
- **Formatting**: Formatted the benchmark files with black. (#e5f5873)

### Documentation
- **AGENTS.md**: Added agent guidelines for the repository. (#f6d7977)
- **Python/C++/Rust comparison**: Added `compare-py-cpp-rs.md`. (#ec86626)

### Build & CI
- **Updated GitHub Actions**: `checkout`→v4, `setup-python`→v5, `codecov-action`→v4. (#e7bd7f3)

## Version 0.4 (2026-07-16)

### Documentation
- **Sphinx docs with plot_directive and svgbob**: Enabled matplotlib `plot_directive` for auto-generated figures and `sphinxcontrib.svgbob` for ASCII-to-SVG diagrams. Added CSD distribution and conversion example plots under `docs/examples/`. Added svgbob diagram to `csd.py` module docstring. (#a6e57f8)

### Code Cleanup
- **Removed PyScaffold boilerplate**: Deleted `skeleton.py` and `test_skeleton.py` (unused Fibonacci CLI scaffold). (#27813b4)
- **Dropped Python < 3.9 compat**: Removed `importlib-metadata` conditional dependency and compat guard from `__init__.py` (project now targets 3.10+). (#27813b4)
- **Config cleanup**: Removed dead `fibonacci = skeleton:run` entry point from `setup.cfg` and unused `ignore_missing_imports` from `mypy.ini`. (#27813b4)
- **Removed stale files**: Deleted `IFLOW.md` and duplicate `LICENSE`. (#27813b4)
- **Updated `.gitignore`**: Added `.ruff_cache/` and `.benchmarks/`. (#27813b4)

### Build & CI
- **CI repair**: Fixed broken `entry_points` configuration and lingering `skeleton` imports breaking the CI pipeline. (#0b2459b)

### Testing & Code Quality
- **Benchmark & verification scripts**: Added `benches/bench_csd.py` and `benches/verify_output.py` for performance tracking and output verification. (#09da08a)
