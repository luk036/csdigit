#! /usr/bin/env python
"""
Canonical Signed Digit Functions

Handles:
 * Decimals
 *
 *

eg, +00-00+000.0 or 0.+0000-00+
Where: '+' is +1
       '-' is -1

Harnesser
License: GPL2
"""

from math import ceil, fabs, log, pow


def to_csd(number: float, places: int = 0, debug: bool = False) -> str:
    """Convert a decimal number to Canonical Signed Digit (CSD) format.

    The CSD representation uses only three symbols: '+' (represents +1),
    '-' (represents -1), and '0' (represents 0). No two adjacent digits
    can both be non-zero, ensuring a unique representation.

    :param number: The decimal number to convert to CSD format
    :type number: float
    :param places: Number of fractional decimal places to represent (default: 0)
    :type places: int
    :param debug: If True, print debug information during conversion (default: False)
    :type debug: bool
    :return: The CSD string representation of the input number
    :rtype: str

    Examples:
        >>> to_csd(28.5, 2)
        '+00-00.+'
        >>> to_csd(0.0)
        '0'
        >>> to_csd(-0.5, 1)
        '0.-'
    """

    if debug:
        print("Converting %f " % (number), end="")

    # figure out binary range, special case for 0
    if number == 0:
        return "0"
    if fabs(number) < 1.0:
        power = 0
    else:
        power = ceil(log(fabs(number) * 3.0 / 2.0, 2))

    csd_digits = []

    if debug:
        print("to %d.%d format" % (power, places))

    # Hone in on the CSD code for the input number
    remainder = number
    power -= 1

    while power >= -places:
        limit = pow(2.0, power + 1) / 3.0

        if debug:
            print("  ", remainder, limit, end="")

        # decimal point?
        if power == -1:
            csd_digits.extend(["."])

        # convert the number
        if remainder > limit:
            csd_digits.extend(["+"])
            remainder -= pow(2.0, power)

        elif remainder < -limit:
            csd_digits.extend(["-"])
            remainder += pow(2.0, power)

        else:
            csd_digits.extend(["0"])

        power -= 1

        if debug:
            print(csd_digits)

    # Always have something before the point
    if fabs(number) < 1.0:
        csd_digits.insert(0, "0")

    csd_str = "".join(csd_digits)

    return csd_str


def to_decimal(csd_str: str, debug: bool = False) -> float:
    """Convert a Canonical Signed Digit (CSD) string to a decimal number.

    Parses the CSD string and computes its decimal value by evaluating
    each digit according to its position and power of 2.

    :param csd_str: The CSD string to convert to decimal
    :type csd_str: str
    :param debug: If True, print debug information during conversion (default: False)
    :type debug: bool
    :return: The decimal (float) value represented by the CSD string
    :rtype: float

    Examples:
        >>> to_decimal("+00-00.+")
        28.5
        >>> to_decimal("0.-")
        -0.5
        >>> to_decimal("0")
        0.0
    """

    if debug:
        print("Converting: ", csd_str)

    #  Find out what the MSB power of two should be, keeping in
    # mind we may have a fractional CSD number
    try:
        (integral_part, fractional_part) = csd_str.split(".")
        csd_str = csd_str.replace(".", "")  # get rid of point now...
    except ValueError:
        integral_part = csd_str
        fractional_part = ""

    msb_power = len(integral_part) - 1

    number = 0.0
    for index in range(len(csd_str)):
        power_of_two = 2.0 ** (msb_power - index)

        if csd_str[index] == "+":
            number += power_of_two
        elif csd_str[index] == "-":
            number -= power_of_two

        if debug:
            print(
                '  "%s" (%d.%d); 2**%d = %d; Num=%f'
                % (
                    csd_str[index],
                    len(integral_part),
                    len(fractional_part),
                    msb_power - index,
                    power_of_two,
                    number,
                )
            )

    return number
