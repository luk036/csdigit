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

Canonical Signed Digit (CSD) is a type of signed-digit representation of numbers. In CSD, each digit can only be -1, 0, or 1, and no two consecutive digits can be non-zero. This representation has the advantage of being unique and having a minimal number of non-zero digits. CSD is often used in digital signal processing applications, such as filter design, because it allows for efficient implementation of arithmetic operations using simple adders and subtractors. The number of adders/subtracters required to realize a CSD coefficient is one less than the number of nonzero digits in the code.

This code is all about converting numbers between decimal format and a special representation called Canonical Signed Digit (CSD). CSD is a way of writing numbers using only three symbols: 0, +, and -. It's particularly useful in certain areas of computer science and digital signal processing.

The main purpose of this code is to provide functions that can convert decimal numbers to CSD format and vice versa. It takes in regular decimal numbers (like 28.5 or -0.5) and converts them to CSD strings (like "+00-00.+" or "0.-"), and it can also do the reverse, taking CSD strings and converting them back to decimal numbers.

The code contains several functions, each with a specific role:

1. to_csd: This function takes a decimal number and the number of decimal places desired, and outputs a CSD string. For example, it can convert 28.5 to "+00-00.+0" (with 2 decimal places).

2. to_csd_i: Similar to to_csd, but it works specifically with integers. It converts whole numbers to CSD format without a decimal point.

3. to_decimal_using_pow and to_decimal: These functions do the opposite of to_csd. They take a CSD string and convert it back to a decimal number.

4. to_csdnnz: This function is a variation of to_csd that allows you to specify the maximum number of non-zero digits in the result.

The code achieves its purpose through a series of mathematical operations and logical checks. For the decimal to CSD conversion, it uses powers of 2 to determine which symbols (+, -, or 0) to use at each position in the CSD string. It repeatedly divides the input number by 2 and checks if it's greater than, less than, or close to certain thresholds to decide which symbol to use.

For the CSD to decimal conversion, it goes through each symbol in the CSD string, multiplying the running total by 2 and adding 1, subtracting 1, or doing nothing based on whether the symbol is +, -, or 0.

An important aspect of the code is how it handles the decimal point in CSD representations. It uses a separate logic for the part before the decimal point (the integral part) and the part after (the fractional part).

The code also includes error checking to ensure that only valid CSD symbols are used, and it provides detailed documentation and examples for each function to help users understand how to use them.

Overall, this code provides a comprehensive set of tools for working with CSD representations, allowing users to easily convert between decimal and CSD formats in various ways.

## Used By

[multiplierless](https://github.com/luk036/multiplierless)

## 👀 See also

- [csd-rs](https://luk036.github.io/csd-rs)
- [csd-cpp](https://luk036.github.io/csd-cpp)

<!-- pyscaffold-notes -->

## 👉 Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
