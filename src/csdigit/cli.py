"""
This is a to_csd file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         to_csd = csdigit.to_csd:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``to_csd`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

from csdigit import __version__
from csdigit.csd import to_csd, to_csdnnz, to_decimal

__author__ = "Wai-Shing Luk"
__copyright__ = "Wai-Shing Luk"
__license__ = "MIT"

# Initialize logger for the module
_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    # Create argument parser with program description
    parser = argparse.ArgumentParser(description="Converts a decimal to a CSD format")

    # Add version information argument
    parser.add_argument(
        "--version",
        action="version",
        version="csdigit {ver}".format(ver=__version__),
    )

    # Add conversion options with type checking and default values
    parser.add_argument(
        "-c",
        "--to_csd",
        dest="decimal",
        help="a decimal number",
        type=float,
        metavar="FLOAT",
        default=float("Inf"),  # Use infinity as sentinel value
    )
    parser.add_argument(
        "-f",
        "--to_csdnnz",
        dest="decimal2",
        help="a decimal number",
        type=float,
        metavar="FLOAT",
        default=float("Inf"),
    )
    parser.add_argument(
        "-d",
        "--to_decimal",
        dest="csdstr",
        help="a CSD string",
        type=str,
        metavar="STR",
        default="",  # Empty string as sentinel value
    )

    # Add precision control parameters
    parser.add_argument(
        "-p",
        "--places",
        dest="places",
        help="How many places",
        type=int,
        metavar="INT",
        default=4,
    )
    parser.add_argument(
        "-z",
        "--nnz",
        dest="nnz",
        help="How many non-zeros",
        type=int,
        metavar="INT",
        default=4,
    )

    # Add logging level control arguments
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel) -> None:
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    # Configure logging format and output stream
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main(args) -> None:
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    _logger.debug("Starting crazy calculations...")

    # Check which conversion option was specified and execute corresponding function
    if args.decimal != float("Inf"):
        ans = to_csd(args.decimal, args.places)
        print(f"{ans}")
    if args.decimal2 != float("Inf"):
        ans = to_csdnnz(args.decimal2, args.nnz)
        print(f"{ans}")
    if args.csdstr != "":
        ans = to_decimal(args.csdstr)
        print(f"{ans}")

    _logger.info("Script ends here")


def run() -> None:
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    # Pass all arguments except the script name
    main(sys.argv[1:])


if __name__ == "__main__":
    # Guard clause to prevent script execution when imported as module
    # https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m csdigit.to_csd 42
    #
    run()
