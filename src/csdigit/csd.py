"""
Canonical Signed Digit (CSD) conversion utilities.

Provides functions to convert between decimal numbers and Canonical Signed Digit
(CSD) representation — a signed-digit representation using only ``+``, ``-``,
and ``0`` symbols with no consecutive non-zero digits.

Functions:
    to_csd: Convert a decimal float to CSD string with specified precision.
    to_csd_i: Convert an integer to CSD string.
    to_decimal: Convert a CSD string to a decimal number.
    to_decimal_using_pow: Convert a CSD string to decimal using pow() (deprecated).
    to_csdnnz: Convert a decimal float to CSD with limited non-zero digits.
    to_csdnnz_i: Convert an integer to CSD with limited non-zero digits.
"""

import logging
from math import fabs, frexp, ldexp


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
    if decimal_value == 0.0:
        return "0." + "0" * places if places > 0 else "0."

    abs_val = fabs(decimal_value)
    if abs_val < 1.0:
        remainder = 0
        csd_list = ["0"]
    else:
        mant, exp = frexp(abs_val * 1.5)
        remainder = exp - 1 if mant == 0.5 else exp
        csd_list = []

    power_of_two = ldexp(1.0, remainder)

    for _ in range(remainder):
        power_of_two /= 2.0
        determinant = 1.5 * decimal_value
        if determinant > power_of_two:
            csd_list.append("+")
            decimal_value -= power_of_two
        elif determinant < -power_of_two:
            csd_list.append("-")
            decimal_value += power_of_two
            logging.debug(f"decimal_value = {decimal_value}")
        else:
            csd_list.append("0")

    csd_list.append(".")

    for _ in range(places):
        power_of_two /= 2.0
        determinant = 1.5 * decimal_value
        if determinant > power_of_two:
            csd_list.append("+")
            decimal_value -= power_of_two
        elif determinant < -power_of_two:
            csd_list.append("-")
            decimal_value += power_of_two
        else:
            csd_list.append("0")

    return "".join(csd_list)


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
    if decimal_value == 0:
        return "0"

    remainder = (abs(decimal_value) * 3 // 2).bit_length()
    power_of_two = 1 << remainder
    csd_list = []
    while power_of_two > 1:
        power_of_two_half = power_of_two >> 1
        determinant = 3 * decimal_value
        if determinant > power_of_two:
            csd_list.append("+")
            decimal_value -= power_of_two_half
        elif determinant < -power_of_two:
            csd_list.append("-")
            decimal_value += power_of_two_half
        else:
            csd_list.append("0")
        power_of_two = power_of_two_half
    return "".join(csd_list)


def to_decimal_using_pow(csd: str) -> float:
    """
    The `to_decimal_using_pow` function converts a Canonical Signed Digit (CSD) string to a decimal
    number using the pow function.

    .. deprecated:: 0.1.0
        Use `to_decimal` instead.

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
    # import warnings
    # warnings.warn(
    #     "`to_decimal_using_pow` is deprecated, use `to_decimal` instead.",
    #     DeprecationWarning,
    #     stacklevel=2,
    # )
    decimal_value: float = 0.0
    location: int = 0  # Tracks position of decimal point
    for pos, digit in enumerate(csd):
        if digit == "0":
            decimal_value *= 2.0  # Shift left (multiply by 2)
        elif digit == "+":
            decimal_value = decimal_value * 2.0 + 1.0  # Shift left and add 1
        elif digit == "-":
            decimal_value = decimal_value * 2.0 - 1.0  # Shift left and subtract 1
        elif digit == ".":
            location = pos + 1  # Mark decimal point position
        else:
            logging.info(f"Encounter unknown character {digit}")
            # raise ValueError(ERROR1)
    if location != 0:
        # Adjust for fractional part by dividing by appropriate power of 2
        decimal_value /= pow(2.0, len(csd) - location)

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
    if "." not in csd:
        integral: int = 0
        for digit in csd:
            integral *= 2
            if digit == "+":
                integral += 1
            elif digit == "-":
                integral -= 1
            elif digit != "0":
                logging.info(f"Encounter unknown character {digit}")
                # raise ValueError(ERROR1)
        return integral

    integral_part, fractional_part = csd.split(".", 1)
    integral: int = 0
    for digit in integral_part:
        integral *= 2
        if digit == "+":
            integral += 1
        elif digit == "-":
            integral -= 1
        elif digit != "0":
            logging.info(f"Encounter unknown character {digit}")
            # raise ValueError(ERROR1)

    fractional: float = 0.0
    scale = 0.5
    for digit in fractional_part:
        if digit == "+":
            fractional += scale
        elif digit == "-":
            fractional -= scale
        elif digit != "0":
            logging.info(f"Encounter unknown character {digit}")
            # raise ValueError(ERROR1)
        scale /= 2.0

    return float(integral) + fractional


def to_csdnnz(decimal_value: float, nnz: int) -> str:
    """
    The `to_csdnnz` function converts a given decimal number into a Canonical Signed Digit (CSD)
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
    :return: The function `to_csdnnz` returns a string representation of the given `decimal_value` in Canonical
        Signed Digit (CSD) format.

    Examples:
        >>> to_csdnnz(28.5, 4)
        '+00-00.+'
        >>> to_csdnnz(-0.5, 4)
        '0.-'
        >>> to_csdnnz(0.0, 4)
        '0'
        >>> to_csdnnz(0.5, 4)
        '0.+'
    """
    if decimal_value == 0.0:
        return "0"

    abs_val = fabs(decimal_value)
    if abs_val < 1.0:
        remainder = 0
        csd_list = ["0"]
    else:
        mant, exp = frexp(abs_val * 1.5)
        remainder = exp - 1 if mant == 0.5 else exp
        csd_list = []

    power_of_two = ldexp(1.0, remainder)

    while remainder > 0 or (nnz > 0 and fabs(decimal_value) > 1e-100):
        if remainder == 0:
            csd_list.append(".")
        power_of_two /= 2
        remainder -= 1
        if nnz > 0:
            determinant = 1.5 * decimal_value
            if determinant > power_of_two:
                csd_list.append("+")
                decimal_value -= power_of_two
                nnz -= 1
            elif determinant < -power_of_two:
                csd_list.append("-")
                decimal_value += power_of_two
                nnz -= 1
            else:
                csd_list.append("0")
        else:
            csd_list.append("0")

        # if nnz > 0 and determinant > power_of_two:
        #     csd_list.append("+")
        #     decimal_value -= power_of_two
        #     nnz -= 1
        # elif nnz > 0 and determinant < -power_of_two:
        #     csd_list.append("-")
        #     decimal_value += power_of_two
        #     nnz -= 1
        # else:
        #     csd_list.append("0")

    return "".join(csd_list)


def to_csdnnz_i(decimal_value: int, nnz: int) -> str:
    """
    The `to_csdnnz_i` function converts a given integer into a Canonical Signed Digit (CSD)
    representation with a specified number of non-zero digits.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    :param decimal_value: The `decimal_value` parameter is an integer that represents the decimal value to be converted to
        CSD format
    :type decimal_value: int
    :param nnz: The parameter `nnz` stands for "number of non-zero bits". It represents the maximum
        number of non-zero bits allowed in the output CSD (Canonical Signed Digit) representation of the
        given `decimal_value`
    :type nnz: int
    :return: The function `to_csdnnz_i` returns a string representation of the given `decimal_value` in Canonical
        Signed Digit (CSD) format.

    Examples:
        >>> to_csdnnz_i(28, 4)
        '+00-00'
        >>> to_csdnnz_i(-0, 4)
        '0'
        >>> to_csdnnz_i(0, 4)
        '0'
        >>> to_csdnnz_i(37, 2)
        '+00+00'
        >>> to_csdnnz_i(158, 2)
        '+0+00000'
    """
    if decimal_value == 0:
        return "0"

    remainder = (abs(decimal_value) * 3 // 2).bit_length()
    power_of_two = 1 << remainder
    csd_list = []
    while power_of_two > 1:
        power_of_two_half = power_of_two >> 1
        determinant = 3 * decimal_value
        if nnz > 0 and determinant > power_of_two:
            csd_list.append("+")
            decimal_value -= power_of_two_half
            nnz -= 1
        elif nnz > 0 and determinant < -power_of_two:
            csd_list.append("-")
            decimal_value += power_of_two_half
            nnz -= 1
        else:
            csd_list.append("0")
        power_of_two = power_of_two_half
    return "".join(csd_list)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
