#! /usr/bin/env python
"""
Run all the tests
"""

import sys

sys.path.append("./csd")

import unittest
from test import *  # noqa: F403

unittest.main()
