"""
Canonical Signed Digit Conversion
"""
from math import ceil, fabs, log


def to_csd(num: float, places: int) -> str:
    """Convert to CSD (Canonical Signed Digit) string representation

    The function `to_csd` converts a given number to its
    Canonical Signed Digit (CSD) representation
    with a specified number of decimal places.

    The `num` parameter is a double precision floating-point
    number that represents the value
    to be converted to CSD (Canonic Signed Digit) representation.

    The `places` parameter in the `to_csd` function represents
    the number of decimal places to include in the CSD
    (Canonical Signed Digit) representation of the given `num`.

    The function `to_csd` returns a string representation
    of the given `num` in Canonical Signed Digit (CSD) format.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    Args:
        num (float): decimal value to be converted to CSD format
        places (int): number of fractional places

    Returns:
        str: containing the CSD value

    Examples:
        >>> to_csd(28.5, 2)
        '+00-00.+0'
        >>> to_csd(-0.5, 2)
        '0.-0'
        >>> to_csd(0.0, 2)
        '0'
        >>> to_csd(0.0, 0)
        '0'
    """
    # figure out binary range, special case for 0
    if num == 0.0:
        return "0"

    absnum = fabs(num)
    if absnum < 1.0:
        rem = 0
        csd = "0"
    else:
        rem = int(ceil(log(absnum * 1.5, 2)))
        csd = ""
    p2n = pow(2.0, rem)
    # eps = pow(2, -places)
    while rem > -places:
        if rem == 0:
            csd += "."
        # convert the number
        rem -= 1
        p2n /= 2.0
        det = 1.5 * num
        if det > p2n:
            csd += "+"
            num -= p2n
        elif det < -p2n:
            csd += "-"
            num += p2n
        else:
            csd += "0"
    return csd


def to_csd_i(num: int) -> str:
    """Convert the argument `num` to a string in CSD Format.

    The function converts a given integer into a Canonical Signed
    Digit (CSD) representation.

    The parameter `num` is an integer that represents the number
    for which we want to generate the CSD (Canonical Signed Digit)
    representation.

    The function `to_csd_i` returns a string.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    Args:
        num (int): decimal value to be converted to CSD format

    Returns:
        str: containing the CSD value

    Examples:
        >>> to_csd_i(28)
        '+00-00'
        >>> to_csd_i(-0)
        '0'
        >>> to_csd_i(0)
        '0'
    """
    # figure out binary range, special case for 0
    if num == 0:
        return "0"

    rem = ceil(log(abs(num) * 1.5, 2))
    p2n = pow(2, rem)
    csd = ""
    while p2n > 1:
        # convert the number
        p2n_half = p2n // 2
        det = 3 * num
        if det > p2n:
            csd += "+"
            num -= p2n_half
        elif det < -p2n:
            csd += "-"
            num += p2n_half
        else:
            csd += "0"
        p2n = p2n_half
    return csd


def to_decimal_using_pow(csd: str) -> float:
    """Convert the argument to a decimal number

    The function `to_decimal_using_pow` takes a CSD (Canonical
    Signed Digit) string as input and converts it to a decimal
    number with a pow function.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    Args:
        csd (str): string containing the CSD value

    Returns:
        float: decimal value of the CSD format

    Examples:
        >>> to_decimal_using_pow("+00-00.+")
        28.5
        >>> to_decimal_using_pow("0.-")
        -0.5
        >>> to_decimal_using_pow("0")
        0.0
    """

    num: float = 0.0
    loc: int = 0
    for pos, digit in enumerate(csd):
        if digit == "0":
            num *= 2.0
        elif digit == "+":
            num = num * 2.0 + 1.0
        elif digit == "-":
            num = num * 2.0 - 1.0
        elif digit == ".":
            loc = pos + 1
        else:
            raise ValueError("Work with 0, +, -, . only")
    if loc != 0:
        num /= pow(2.0, len(csd) - loc)

    return num


def to_decimal(csd: str) -> float:
    """Convert the argument to a decimal number

    The function `to_decimal` takes a CSD (Canonical Signed Digit) string as
    input and converts it to a decimal number. It iterates through the chars
    of the string and performs the corresponding operations based on the
    character.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    Args:
        csd (str): string containing the CSD value

    Returns:
        float: decimal value of the CSD format

    Examples:
        >>> to_decimal("+00-00.+")
        28.5
        >>> to_decimal("0.-")
        -0.5
        >>> to_decimal("0")
        0.0
        >>> to_decimal("0.0")
        0.0
        >>> to_decimal("0.+")
        0.5
        >>> to_decimal("0.-")
        -0.5
    """

    num: float = 0.0
    # Handle integral part
    loc: int = 0
    for pos, digit in enumerate(csd):
        if digit == "0":
            num *= 2.0
        elif digit == "+":
            num = num * 2.0 + 1.0
        elif digit == "-":
            num = num * 2.0 - 1.0
        elif digit == ".":
            loc = pos + 1
            break
        else:
            raise ValueError("Work with 0, +, -, . only")
    if loc == 0:
        return num

    # Handle fraction part
    scale = 0.5
    for digit in csd[loc:]:
        if digit == "0":
            pass
        elif digit == "+":
            num += scale
        elif digit == "-":
            num -= scale
        else:
            raise ValueError("Work with 0, +, -, . only")
        scale /= 2.0
    return num


def to_decimal_i(csd: str) -> int:
    """Convert the argument to a decimal number

    The function `to_decimal_i` takes a CSD (Canonical Signed Digit) string as
    input and converts it to an integer. It iterates through the characters of
    the string and performs the corresponding operations based on the
    character.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    Args:
        csd (str): string containing the CSD value

    Returns:
        int: decimal value of the CSD format

    Examples:
        >>> to_decimal_i("+00-00")
        28
    """
    num: int = 0
    for digit in csd:
        if digit == "0":
            num *= 2
        elif digit == "+":
            num = num * 2 + 1
        elif digit == "-":
            num = num * 2 - 1
        else:
            raise ValueError("Work with 0, +, - only")
    return num


def to_csdfixed(num: float, nnz: int) -> str:
    """Convert the argument `num` to a string in CSD Format.

    The function `to_csdfixed` converts a given number into a CSD (Canonic
    Signed Digit) representation with a specified number of non-zero digits.

    The parameter `num` is a double precision floating-point number that
    represents the input value for conversion to CSD (Canonic Signed Digit)
    fixed-point representation.
    The parameter `nnz` stands for "number of non-zero bits". It represents the
    maximum number of non-zero bits allowed in the output CSD (Canonical Signed
    Digit) representation of the given `num`.

    The function `to_csdfixed` returns a string representation of the given
    `num` in Canonical Signed Digit (CSD) format.

    Original author: Harnesser
    <https://sourceforge.net/projects/pycsd/>
    License: GPL2

    Args:
        num (float): decimal value to be converted to CSD format
        nnz (int): number of non-zeros

    Returns:
        str: containing the CSD value

    Examples:
        >>> to_csdfixed(28.5, 4)
        '+00-00.+'
        >>> to_csdfixed(-0.5, 4)
        '0.-'
        >>> to_csdfixed(0.0, 4)
        '0'
        >>> to_csdfixed(0.5, 4)
        '0.+'
        >>> to_csdfixed(-0.5, 4)
        '0.-'
        >>> to_csdfixed(0.0, 4)
        '0'
        >>> to_csdfixed(0.5, 4)
        '0.+'
        >>> to_csdfixed(-0.5, 4)
        '0.-'
        >>> to_csdfixed(0.0, 4)
        '0'
        >>> to_csdfixed(0.5, 4)
        '0.+'
        >>> to_csdfixed(-0.5, 4)
        '0.-'
        >>> to_csdfixed(0.0, 4)
        '0'
        >>> to_csdfixed(0.5, 4)
        '0.+'
    """

    if num == 0.0:
        return "0"

    absnum = fabs(num)
    if absnum < 1.0:
        rem = 0
        csd = "0"
    else:
        rem = ceil(log(absnum * 1.5, 2))
        csd = ""
    p2n = pow(2, rem)
    while rem > 0 or (nnz > 0 and fabs(num) > 1e-100):
        if rem == 0:
            csd += "."
        p2n /= 2
        rem -= 1
        det = 1.5 * num
        if det > p2n:
            csd += "+"
            num -= p2n
            nnz -= 1
        elif det < -p2n:
            csd += "-"
            num += p2n
            nnz -= 1
        else:
            csd += "0"
        if nnz == 0:
            num = 0.0
    return csd


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    print(to_csd(28.5, 2))
