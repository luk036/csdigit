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

## Used By

[multiplierless](https://github.com/luk036/multiplierless)

## 👀 See also

- [csd-rs](https://luk036.github.io/csd-rs)
- [csd-cpp](https://luk036.github.io/csd-cpp)

<!-- pyscaffold-notes -->

## 👉 Note

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
