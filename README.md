<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/csdigit.svg?branch=main)](https://cirrus-ci.com/github/<USER>/csdigit)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/csdigit/main.svg)](https://coveralls.io/r/<USER>/csdigit)
[![PyPI-Server](https://img.shields.io/pypi/v/csdigit.svg)](https://pypi.org/project/csdigit/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/csdigit.svg)](https://anaconda.org/conda-forge/csdigit)
[![Monthly Downloads](https://pepy.tech/badge/csdigit/month)](https://pepy.tech/project/csdigit)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/csdigit)
-->

[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![ReadTheDocs](https://readthedocs.org/projects/csdigit/badge/?version=latest)](https://csdigit.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/luk036/csdigit/branch/main/graph/badge.svg?token=B8UXKlkDsc)](https://codecov.io/gh/luk036/csdigit)

# 🔄 csdigit

> Canonical Signed Digit Conversion in Python

A Canonical Signed Digit (CSD) is a specific form of signed-digit representation of numbers. In the context of CSD, each digit is constrained to a value of -1, 0, or 1, and no two consecutive digits are permitted to be non-zero. This representation has the advantage of being unique and having a minimal number of non-zero digits. CSD is frequently employed in digital signal processing applications, such as filter design, due to its capacity for the efficient implementation of arithmetic operations through the use of straightforward adders and subtractors. The number of adders and subtracters necessary to implement a CSD coefficient is equal to the number of non-zero digits in the library, minus one.

The objective of this library is to facilitate the conversion of numbers between decimal format and a special representation known as Canonical Signed Digit (CSD). CSD is a method of representing numbers using a mere three symbols: The symbols "0," "+," and "-" are used. It is particularly advantageous in specific domains within computer science and digital signal processing.

The primary objective of this library is to provide the necessary functions for the conversion of decimal numbers to CSD format and vice versa. The library accepts decimal numbers in their standard form (e.g., 28.5 or -0.5) and converts them to CSD strings (e.g., "+00-00.+" or "0.-"). It is also capable of performing the inverse operation, transforming CSD strings into decimal numbers.

The library contains a number of functions, each with a specific role.

1. to_csd: This function takes a decimal number and the number of decimal places desired, and outputs a CSD string. To illustrate, the function can be used to convert the decimal number 28.5 to the CSD string "+00-00.+0," with two decimal places.

2. to_csd_i: This function is analogous to to_csd, but it is designed for use with integers. The function converts whole numbers to CSD format, omitting the decimal point.

3. The functions to_decimal_using_pow and to_decimal perform the inverse of the to_csd function. They accept a CSD string as input and return a decimal number.

4. The to_csdnnz function is a variant of the to_csd function that allows the user to specify the maximum number of non-zero digits in the result.

5. The to_csdnnz_i function is a variant of the to_csd_i function that allows the user to specify the maximum number of non-zero digits in the result.

The library fulfills its intended function through a sequence of mathematical operations and logical tests. In order to effect a conversion from decimal to CSD, the system employs the use of powers of 2 in order to ascertain which of the three symbols (+, -, or 0) is to be used at each position within the CSD string. The algorithm then performs repeated divisions of the input number by two and compares the result to specific thresholds to determine the appropriate symbol to use.

In order to perform the conversion from CSD to decimal, the algorithm proceeds by multiplying the running total by 2 and then adding, subtracting, or performing no further action based on the value of the symbol in the CSD string. This is done for each symbol in the string, where the symbol values are +, -, or 0. A distinct logic is employed for the integral and fractional parts, respectively.

Furthermore, the library incorporates error-checking mechanisms to guarantee the exclusive utilisation of valid CSD symbols. It also furnishes comprehensive documentation and illustrative examples for each function, thus facilitating user comprehension of the operational procedures.

In conclusion, this library offers a comprehensive set of tools for working with CSD representations, facilitating the conversion between decimal and CSD formats in a variety of ways.

## Used By

[multiplierless](https://github.com/luk036/multiplierless)

## 👀 See also

- [csd-rs](https://luk036.github.io/csd-rs)
- [csd-cpp](https://luk036.github.io/csd-cpp)

<!-- pyscaffold-notes -->

## 👉 Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
