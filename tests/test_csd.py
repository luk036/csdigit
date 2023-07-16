from hypothesis import given
from hypothesis.strategies import integers

from csdigit.csd import to_csd, to_csd_i, to_decimal, to_decimal_i
from csdigit.csd import to_decimal_using_pow
from csdigit.csd import to_csdfixed


def test_for():
    for i in range(6):
        print(i)
    else:
        print("nothing")


def test_csd_s():
    number = -342343593459544395894535439534985
    assert number == to_decimal_i(to_csd_i(number))


def test_to_csdfixed():
    assert to_csdfixed(28.5, 4) == "+00-00.+"
    assert to_csdfixed(-0.5, 4) == "0.-"


def test_to_csd_invalid():
    csd_string = "++00-00ZZZZ.+"
    # TODO: check how to test


@given(integers())
def test_csd_i(number):
    assert number == to_decimal_i(to_csd_i(number))


@given(integers())
def test_csd(number):
    fnum = number / 8
    assert fnum == to_decimal(to_csd(fnum, 4))


@given(integers())
def test_csd_using_pow(number):
    fnum = number / 8
    assert fnum == to_decimal_using_pow(to_csd(fnum, 4))
