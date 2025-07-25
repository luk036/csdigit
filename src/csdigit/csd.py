"""
Canonical Signed Digit (CSD) Conversion

This code is all about converting numbers between decimal format and a special representation called Canonical Signed Digit (CSD). CSD is a way of writing numbers using only three symbols: 0, +, and -. It's particularly useful in certain areas of computer science and digital signal processing.

The main purpose of this code is to provide functions that can convert decimal numbers to CSD format and vice versa. It takes in regular decimal numbers (like 28.5 or -0.5) and converts them to CSD strings (like "+00-00.+" or "0.-"), and it can also do the reverse, taking CSD strings and converting them back to decimal numbers.

The code contains several functions, each with a specific role:

1. to_csd: This function takes a decimal number and the number of decimal places desired, and outputs a CSD string. For example, it can convert 28.5 to "+00-00.+0" (with 2 decimal places).

2. to_csd_i: Similar to to_csd, but it works specifically with integers. It converts whole numbers to CSD format without a decimal point.

3. to_decimal_using_pow and to_decimal: These functions do the opposite of to_csd. They take a CSD string and convert it back to a decimal number.

4. to_csdnnz: This function is a variation of to_csd that allows you to specify the maximum number of non-zero digits in the result.

4. to_csdnnz_i: This function is a variation of to_csd_i that allows you to specify the maximum number of non-zero digits in the result.

The code achieves its purpose through a series of mathematical operations and logical checks. For the decimal to CSD conversion, it uses powers of 2 to determine which symbols (+, -, or 0) to use at each position in the CSD string. It repeatedly divides the input number by 2 and checks if it's greater than, less than, or close to certain thresholds to decide which symbol to use.

For the CSD to decimal conversion, it goes through each symbol in the CSD string, multiplying the running total by 2 and adding 1, subtracting 1, or doing nothing based on whether the symbol is +, -, or 0.

An important aspect of the code is how it handles the decimal point in CSD representations. It uses a separate logic for the part before the decimal point (the integral part) and the part after (the fractional part).

The code also includes error checking to ensure that only valid CSD symbols are used, and it provides detailed documentation and examples for each function to help users understand how to use them.

Overall, this code provides a comprehensive set of tools for working with CSD representations, allowing users to easily convert between decimal and CSD formats in various ways.
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
    # Calculate absolute value to determine initial conditions
    absnum = fabs(decimal_value)
    if absnum < 1.0:
        # For numbers less than 1, start with '0' and no remainder
        rem = 0
        csd = "0"
    else:
        # For larger numbers, calculate the highest power of 2 needed
        rem = int(ceil(log(absnum * 1.5, 2)))
        csd = ""
    p2n = pow(2.0, rem)  # Initialize power of 2

    def loop_fn(value):
        nonlocal rem, decimal_value, p2n, csd
        while rem > value:
            rem -= 1
            p2n /= 2.0  # Decrease power of 2 each iteration
            det = 1.5 * decimal_value  # Decision threshold
            if det > p2n:
                csd += "+"
                decimal_value -= p2n  # Subtract current power of 2
            elif det < -p2n:
                csd += "-"
                decimal_value += p2n  # Add current power of 2
            else:
                csd += "0"  # No change needed

    # Process integer part (before decimal point)
    loop_fn(0)
    csd += "."  # Add decimal point
    # Process fractional part (after decimal point)
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

    # Calculate highest power of 2 needed
    rem = ceil(log(abs(decimal_value) * 1.5, 2))
    p2n = pow(2, rem)
    csd = ""
    while p2n > 1:
        # convert the number
        p2n_half = p2n >> 1  # Equivalent to dividing by 2
        det = 3 * decimal_value  # Decision threshold (3x for integer version)
        if det > p2n:
            csd += "+"
            decimal_value -= p2n_half  # Subtract half the current power of 2
        elif det < -p2n:
            csd += "-"
            decimal_value += p2n_half  # Add half the current power of 2
        else:
            csd += "0"  # No change needed
        p2n = p2n_half  # Move to next lower power of 2
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
    loc: int = 0  # Tracks position of decimal point
    for pos, digit in enumerate(csd):
        if digit == "0":
            decimal_value *= 2.0  # Shift left (multiply by 2)
        elif digit == "+":
            decimal_value = decimal_value * 2.0 + 1.0  # Shift left and add 1
        elif digit == "-":
            decimal_value = decimal_value * 2.0 - 1.0  # Shift left and subtract 1
        elif digit == ".":
            loc = pos + 1  # Mark decimal point position
        else:
            raise ValueError(ERROR1)
    if loc != 0:
        # Adjust for fractional part by dividing by appropriate power of 2
        decimal_value /= pow(2.0, len(csd) - loc)

    return decimal_value


def to_decimal_integral(csd: str) -> Tuple[int, int]:
    """Handle integral part of CSD string."""
    decimal_value: int = 0
    for pos, digit in enumerate(csd):
        if digit == "0":
            decimal_value <<= 1  # Bit shift left (equivalent to *2)
        elif digit == "+":
            decimal_value = (decimal_value << 1) + 1  # Shift left and add 1
        elif digit == "-":
            decimal_value = (decimal_value << 1) - 1  # Shift left and subtract 1
        elif digit == ".":
            return decimal_value, pos + 1  # Return value and decimal position
        else:
            raise ValueError(ERROR1)
    return decimal_value, 0  # Return value and 0 if no decimal point found


def to_decimal_fractional(csd: str) -> float:
    """Handle fractional part of CSD string."""
    decimal_value = 0.0
    scale = 0.5  # Start with 1/2 for first digit after decimal
    for digit in csd:
        if digit == "0":
            pass  # No change to value
        elif digit == "+":
            decimal_value += scale  # Add current place value
        elif digit == "-":
            decimal_value -= scale  # Subtract current place value
        else:
            raise ValueError(ERROR1)
        scale /= 2.0  # Move to next fractional place (1/4, 1/8, etc.)
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
    # First process integral part (before decimal point)
    integral, loc = to_decimal_integral(csd)
    if loc == 0:
        return integral  # If no decimal point, return integer part

    # Then process fractional part (after decimal point)
    fractional = to_decimal_fractional(csd[loc:])
    return integral + fractional  # Combine both parts


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
    absnum = fabs(decimal_value)
    if absnum < 1.0:
        rem = 0
        csd = "0"
    else:
        rem = ceil(log(absnum * 1.5, 2))
        csd = ""
    p2n = pow(2, rem)
    # Process until we've used all non-zero digits or reached zero
    while rem > 0 or (nnz > 0 and fabs(decimal_value) > 1e-100):
        if rem == 0:
            csd += "."  # Add decimal point when we reach fractional part
        p2n /= 2
        rem -= 1
        det = 1.5 * decimal_value
        if det > p2n:
            csd += "+"
            decimal_value -= p2n
            nnz -= 1  # Decrement non-zero digit count
        elif det < -p2n:
            csd += "-"
            decimal_value += p2n
            nnz -= 1  # Decrement non-zero digit count
        else:
            csd += "0"
        if nnz == 0:
            decimal_value = 0.0  # Stop processing if no more non-zero digits allowed
    return csd


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
    # figure out binary range, special case for 0
    if decimal_value == 0:
        return "0"

    rem = ceil(log(abs(decimal_value) * 1.5, 2))
    p2n = pow(2, rem)
    csd = ""
    while p2n > 1:
        # convert the number
        p2n_half = p2n >> 1
        det = 3 * decimal_value  # Decision threshold (3x for integer version)
        if det > p2n:
            csd += "+"
            decimal_value -= p2n_half
            nnz -= 1  # Decrement non-zero digit count
        elif det < -p2n:
            csd += "-"
            decimal_value += p2n_half
            nnz -= 1  # Decrement non-zero digit count
        else:
            csd += "0"
        p2n = p2n_half
        if nnz == 0:
            decimal_value = 0  # Stop processing if no more non-zero digits allowed
    return csd


if __name__ == "__main__":
    import doctest

    doctest.testmod()
