# Changelog

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
