from hypothesis import given
from hypothesis.strategies import integers

from csdigit.csd import to_csd, to_csd_i, to_decimal, to_decimal_i


def test_csd_s():
    number = -342343593459544395894535439534985
    assert number == to_decimal_i(to_csd_i(number))


@given(integers())
def test_csd_i(number):
    assert number == to_decimal_i(to_csd_i(number))


@given(integers())
def test_csd(number):
    fnum = number / 8
    assert fnum == to_decimal(to_csd(fnum, 4))
