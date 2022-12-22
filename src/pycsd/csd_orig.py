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

from math import *


def to_csd(num, places=0):
    """Convert the argument to CSD Format."""

    # figure out binary range, special case for 0
    if num == 0:
        return "0"
    if fabs(num) < 1.0:
        n = 0
    else:
        n = ceil(log(fabs(num) * 3.0 / 2.0, 2))

    csd_digits = []

    # Hone in on the CSD code for the input number
    remainder = num
    previous_non_zero = False
    n -= 1

    while n >= -places:

        limit = pow(2.0, n + 1) / 3.0

        # decimal point?
        if n == -1:
            csd_digits.extend(["."])

        # convert the number
        if previous_non_zero:
            csd_digits.extend(["0"])
            prev_non_zero = False

        elif remainder > limit:
            csd_digits.extend(["+"])
            remainder -= pow(2.0, n)
            prev_non_zero = True

        elif remainder < -limit:
            csd_digits.extend(["-"])
            remainder += pow(2.0, n)
            prev_non_zero = True

        else:
            csd_digits.extend(["0"])
            prev_non_zero = False

        n -= 1

    # Always have something before the point
    if fabs(num) < 1.0:
        csd_digits.insert(0, "0")

    csd_str = "".join(csd_digits)

    return csd_str


def to_decimal(csd_str):
    """Convert the CSD string to a decimal"""

    #  Find out what the MSB power of two should be, keeping in
    # mind we may have a fractional CSD number
    try:
        (m, n) = csd_str.split(".")
        csd_str = csd_str.replace(".", "")  # get rid of point now...
    except ValueError:
        m = csd_str
        n = ""

    msb_power = len(m) - 1

    num = 0.0
    for ii in range(len(csd_str)):

        power_of_two = 2.0 ** (msb_power - ii)

        if csd_str[ii] == "+":
            num += power_of_two
        elif csd_str[ii] == "-":
            num -= power_of_two

    return num
