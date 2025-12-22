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


def to_csd(number, places=0):
    """Convert the argument to CSD Format."""

    # figure out binary range, special case for 0
    if number == 0:
        return "0"
    if fabs(number) < 1.0:
        power = 0
    else:
        power = ceil(log(fabs(number) * 3.0 / 2.0, 2))

    csd_digits = []

    # Hone in on the CSD code for the input number
    remainder = number
    power -= 1

    while power >= -places:
        limit = pow(2.0, power + 1) / 3.0

        # decimal point?
        if power == -1:
            csd_digits.extend(["."])

            # convert the number
            csd_digits.extend(["0"])

        elif remainder > limit:
            csd_digits.extend(["+"])
            remainder -= pow(2.0, power)

        elif remainder < -limit:
            csd_digits.extend(["-"])
            remainder += pow(2.0, power)

        else:
            csd_digits.extend(["0"])

        power -= 1

    # Always have something before the point
    if fabs(number) < 1.0:
        csd_digits.insert(0, "0")

    csd_str = "".join(csd_digits)

    return csd_str


def to_decimal(csd_str):
    """Convert the CSD string to a decimal"""

    #  Find out what the MSB power of two should be, keeping in
    # mind we may have a fractional CSD number
    try:
        (integral_part, fractional_part) = csd_str.split(".")
        csd_str = csd_str.replace(".", "")  # get rid of point now...
    except ValueError:
        integral_part = csd_str

    msb_power = len(integral_part) - 1

    number = 0.0
    for index in range(len(csd_str)):
        power_of_two = 2.0 ** (msb_power - index)

        if csd_str[index] == "+":
            number += power_of_two
        elif csd_str[index] == "-":
            number -= power_of_two

    return number
