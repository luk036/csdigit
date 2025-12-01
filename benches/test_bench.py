from csdigit import csd
from pycsd import csd_orig


def run_csd():
    a = 1.3
    b = csd.to_decimal(csd.to_csd(a, 100))
    assert a == b


def run_csd_orig():
    a = 1.3
    b = csd_orig.to_decimal(csd_orig.to_csd(a, 100))
    assert a == b


def test_csd(benchmark) -> None:
    benchmark(run_csd)


def test_csd_orig(benchmark) -> None:
    benchmark(run_csd_orig)
