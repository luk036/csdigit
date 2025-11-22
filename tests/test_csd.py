from hypothesis import given
from hypothesis.strategies import integers
import logging

from csdigit.csd import (  # to_decimal_i,
    to_csd,
    to_csd_i,
    to_csdnnz,
    to_csdnnz_i,
    to_decimal,
    to_decimal_using_pow,
)


def test_csd_special():
    number = -342343593459544395894535439534985
    assert number == to_decimal(to_csd_i(number))


def test_to_decimal_using_pow(caplog):
    assert to_decimal_using_pow("+00-00.+") == 28.5
    # with pytest.raises(ValueError):
    #     to_decimal_using_pow("+00-00.+XXX00+")
    caplog.set_level(logging.INFO)
    to_decimal_using_pow("+00-00.+X00+")
    assert "Encounter unknown character" in caplog.text


def test_to_decimal(caplog):
    assert to_decimal("+00-00.+") == 28.5
    assert to_decimal("0") == 0
    assert to_decimal("0.0") == 0.0
    assert to_decimal("-0.0") == -2.0
    assert to_decimal("+0.-") == 1.5
    # with pytest.raises(ValueError):
    #     to_decimal("+00-00.+XXX00+")
    # with pytest.raises(ValueError):
    #     to_decimal("+00XXX-00.+00+")
    caplog.set_level(logging.INFO)
    to_decimal("+00-00.+X00+")
    assert "Encounter unknown character" in caplog.text


def test_to_csd():
    assert to_csd(28.5, 2) == "+00-00.+0"
    assert to_csd(-0.5, 2) == "0.-0"
    assert to_csd(0.0, 0) == "0."
    assert to_csd(28.5, 0) == "+00-00."
    assert to_csd(-28.5, 2) == "-00+00.-0"


def test_to_csdnn():
    assert to_csdnnz(28.5, 4) == "+00-00.+"
    assert to_csdnnz(-0.5, 4) == "0.-"
    assert to_csdnnz(0.0, 4) == "0"
    assert to_csdnnz(28.5, 2) == "+00-00"


def test_to_csdnn_i():
    assert to_csdnnz_i(28, 4) == "+00-00"
    assert to_csdnnz_i(-0, 4) == "0"
    assert to_csdnnz_i(0, 4) == "0"
    assert to_csdnnz_i(158, 2) == "+0+00000"
    assert to_csdnnz_i(-28, 4) == "-00+00"


def test_to_csd_debug(caplog):
    caplog.set_level(logging.DEBUG)
    assert to_csd(28.5, 2) == "+00-00.+0"

@given(integers())
def test_csd_i(number):
    assert number == to_decimal(to_csd_i(number))


@given(integers())
def test_csd(number):
    fnum = number / 8
    assert fnum == to_decimal(to_csd(fnum, 4))


@given(integers())
def test_csd_using_pow(number):
    fnum = number / 8
    assert fnum == to_decimal_using_pow(to_csd(fnum, 4))
