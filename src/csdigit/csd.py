"""
Canonical Signed Digit Conversion
"""

from math import ceil, fabs, log
from typing import Tuple

ERROR1 = "Work with 0, +, -, and . only"
ERROR2 = "Work with 0, +, and - only"


def to_csd(decimal_value: float, places: int) -> str:
    """
    The `to_csd` function converts a given decimal number to its Canonical Signed Digit (CSD)
    representation with a specified number of decimal places.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    :param decimal_value: The `decimal_value` parameter is a double precision floating-point number that represents the
        value to be converted to CSD (Canonical Signed Digit) representation
    :type decimal_value: float
    :param places: The `places` parameter in the `to_csd` function represents the number of decimal
        places to include in the CSD (Canonical Signed Digit) representation of the given `decimal_value`
    :type places: int
    :return: The function `to_csd` returns a string representation of the given `decimal_value` in Canonical
        Signed Digit (CSD) format.

    Examples:
        >>> to_csd(28.5, 2)
        '+00-00.+0'
        >>> to_csd(-0.5, 2)
        '0.-0'
        >>> to_csd(0.0, 2)
        '0.00'
        >>> to_csd(0.0, 0)
        '0.'
    """
    absnum = fabs(decimal_value)
    if absnum < 1.0:
        rem = 0
        csd = "0"
    else:
        rem = int(ceil(log(absnum * 1.5, 2)))
        csd = ""
    p2n = pow(2.0, rem)

    def loop_fn(value):
        nonlocal rem, decimal_value, p2n, csd
        while rem > value:
            rem -= 1
            p2n /= 2.0
            det = 1.5 * decimal_value
            if det > p2n:
                csd += "+"
                decimal_value -= p2n
            elif det < -p2n:
                csd += "-"
                decimal_value += p2n
            else:
                csd += "0"

    loop_fn(0)
    csd += "."
    loop_fn(-places)
    return csd


def to_csd_i(decimal_value: int) -> str:
    """
    The `to_csd_i` function converts a given integer into a Canonical Signed Digit (CSD) representation.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    :param decimal_value: The `decimal_value` parameter is an integer that represents the decimal value to be converted to
        CSD format
    :type decimal_value: int
    :return: The function `to_csd_i` returns a string containing the CSD (Canonical Signed Digit) value.

    Examples:
        >>> to_csd_i(28)
        '+00-00'
        >>> to_csd_i(-0)
        '0'
        >>> to_csd_i(0)
        '0'
    """
    # figure out binary range, special case for 0
    if decimal_value == 0:
        return "0"

    rem = ceil(log(abs(decimal_value) * 1.5, 2))
    p2n = pow(2, rem)
    csd = ""
    while p2n > 1:
        # convert the number
        p2n_half = p2n >> 1
        det = 3 * decimal_value
        if det > p2n:
            csd += "+"
            decimal_value -= p2n_half
        elif det < -p2n:
            csd += "-"
            decimal_value += p2n_half
        else:
            csd += "0"
        p2n = p2n_half
    return csd


def to_decimal_using_pow(csd: str) -> float:
    """
    The `to_decimal_using_pow` function converts a Canonical Signed Digit (CSD) string to a decimal
    number using the pow function.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    :param csd: The `csd` parameter is a string containing the CSD (Canonical Signed Digit) value
    :type csd: str

    Examples:
        >>> to_decimal_using_pow("+00-00.+")
        28.5
        >>> to_decimal_using_pow("0.-")
        -0.5
        >>> to_decimal_using_pow("0")
        0.0
        >>> to_decimal_using_pow("0.0")
        0.0
        >>> to_decimal_using_pow("0.+")
        0.5
    """

    decimal_value: float = 0.0
    loc: int = 0
    for pos, digit in enumerate(csd):
        if digit == "0":
            decimal_value *= 2.0
        elif digit == "+":
            decimal_value = decimal_value * 2.0 + 1.0
        elif digit == "-":
            decimal_value = decimal_value * 2.0 - 1.0
        elif digit == ".":
            loc = pos + 1
        else:
            raise ValueError(ERROR1)
    if loc != 0:
        decimal_value /= pow(2.0, len(csd) - loc)

    return decimal_value


def to_decimal_integral(csd: str) -> Tuple[int, int]:
    """Handle integral part of CSD string."""
    decimal_value: int = 0
    for pos, digit in enumerate(csd):
        if digit == "0":
            decimal_value <<= 1
        elif digit == "+":
            decimal_value = (decimal_value << 1) + 1
        elif digit == "-":
            decimal_value = (decimal_value << 1) - 1
        elif digit == ".":
            return decimal_value, pos + 1
        else:
            raise ValueError(ERROR1)
    return decimal_value, 0


def to_decimal_fractional(csd: str) -> float:
    """Handle fractional part of CSD string."""
    decimal_value = 0.0
    scale = 0.5
    for digit in csd:
        if digit == "0":
            pass
        elif digit == "+":
            decimal_value += scale
        elif digit == "-":
            decimal_value -= scale
        else:
            raise ValueError(ERROR1)
        scale /= 2.0
    return decimal_value


def to_decimal(csd: str) -> float:
    """Convert CSD string to decimal number.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    :param csd: The `csd` parameter is a string containing the CSD (Canonical Signed Digit) value that
        we want to convert to a decimal number

    :type csd: str

    Examples:
        >>> to_decimal("+00-00.+")
        28.5
        >>> to_decimal("0.-")
        -0.5
        >>> to_decimal("0")
        0
        >>> to_decimal("0.0")
        0.0
        >>> to_decimal("0.+")
        0.5
    """
    integral, loc = to_decimal_integral(csd)
    if loc == 0:
        return integral

    fractional = to_decimal_fractional(csd[loc:])
    return integral + fractional


def to_csdfixed(decimal_value: float, nnz: int) -> str:
    """
    The `to_csdfixed` function converts a given decimal number into a Canonical Signed Digit (CSD)
    representation with a specified number of non-zero digits.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    :param decimal_value: The `decimal_value` parameter is a double precision floating-point number that represents the
        input value for conversion to CSD (Canonic Signed Digit) fixed-point representation
    :type decimal_value: float
    :param nnz: The parameter `nnz` stands for "number of non-zero bits". It represents the maximum
        number of non-zero bits allowed in the output CSD (Canonical Signed Digit) representation of the
        given `decimal_value`
    :type nnz: int
    :return: The function `to_csdfixed` returns a string representation of the given `decimal_value` in Canonical
        Signed Digit (CSD) format.

    Examples:
        >>> to_csdfixed(28.5, 4)
        '+00-00.+'
        >>> to_csdfixed(-0.5, 4)
        '0.-'
        >>> to_csdfixed(0.0, 4)
        '0'
        >>> to_csdfixed(0.5, 4)
        '0.+'
    """
    absnum = fabs(decimal_value)
    if absnum < 1.0:
        rem = 0
        csd = "0"
    else:
        rem = ceil(log(absnum * 1.5, 2))
        csd = ""
    p2n = pow(2, rem)
    while rem > 0 or (nnz > 0 and fabs(decimal_value) > 1e-100):
        if rem == 0:
            csd += "."
        p2n /= 2
        rem -= 1
        det = 1.5 * decimal_value
        if det > p2n:
            csd += "+"
            decimal_value -= p2n
            nnz -= 1
        elif det < -p2n:
            csd += "-"
            decimal_value += p2n
            nnz -= 1
        else:
            csd += "0"
        if nnz == 0:
            decimal_value = 0.0
    return csd


if __name__ == "__main__":
    import doctest

    doctest.testmod()
