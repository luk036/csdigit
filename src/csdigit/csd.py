"""
Canonical Signed Digit Conversion
"""
from math import ceil, fabs, log


def to_csd(num: float, places: int) -> str:
    """Convert the argument `num` to a string in CSD Format.

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
    """

    # figure out binary range, special case for 0
    if num == 0.0:
        return "0"

    absnum = fabs(num)
    if absnum < 1.0:
        rem = 0.0
        csd = "0"
    else:
        rem = ceil(log(absnum * 1.5, 2))
        csd = ""
    p2n = pow(2, rem)
    eps = pow(2, -places)
    while p2n > eps:
        if p2n == 1.0:
            csd += "."
        # convert the number
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
    """

    # figure out binary range, special case for 0
    if num == 0:
        return "0"

    p2n = 2 ** ceil(log(abs(num) * 1.5, 2))
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


def to_decimal(csd: str) -> float:
    """Convert the argument to a decimal number

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
    """

    num: float = 0.0
    loc: int = -1
    pos: int = -1
    for pos, digit in enumerate(csd):
        if digit == "0":
            num *= 2.0
        elif digit == "+":
            num = num * 2.0 + 1.0
        elif digit == "-":
            num = num * 2.0 - 1.0
        elif digit == ".":
            loc = pos
        else:
            raise ValueError("Work with 0, +, -, . only")
    if loc != -1:
        num /= pow(2.0, pos - loc)

    return num


def to_decimal_i(csd: str) -> int:
    """Convert the argument to a decimal number

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
    """

    if num == 0.0:
        return "0"

    absnum = fabs(num)
    if absnum < 1.0:
        rem = 0.0
        csd = "0"
    else:
        rem = ceil(log(absnum * 1.5, 2))
        csd = ""
    p2n = pow(2.0, rem)
    while p2n > 1.0 or (nnz > 0 and fabs(num) > 1e-100):
        if p2n == 1.0:
            csd += "."
        p2n /= 2.0
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
    import doctest

    doctest.testmod()
