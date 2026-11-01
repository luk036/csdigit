"""CSD multiplier demo: Celsius to Fahrenheit for an air-conditioner display.

The display shows integer degrees Fahrenheit::

    F = round(9/5 * C + 32)

For an AC panel the input range is ``C in [-9, 30]`` and the last displayed
digit (1 degF) is all that matters.

A CSD constant multiplier computes ``a * x`` from ``x <<< p`` terms, where the
constant ``a`` has only ``nnz`` non-zero digits (``nnz - 1`` adders).  Since
``9/5 = 1.8`` is not a dyadic rational, the demo searches for a fixed-point
approximation ``a / 2**k`` and then emits

    F = (a * C + 32 * 2**k + 2**(k-1)) >> k

using :func:`csdigit.csd_multiplier.generate_csd_multiplier` for ``a * C``.
The final add folds the ``+32`` offset and the rounding term into one constant.

Run with::

    python examples/temperature_c_to_f.py

It prints the nnz sweep, writes ``temperature_c_to_f.v`` and
``temperature_c_to_f_tb.v`` next to this file, and simulates the testbench with
Icarus Verilog when ``iverilog``/``vvp`` are available.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

from csdigit.csd import to_csd_i
from csdigit.csd_multiplier import generate_csd_multiplier

C_MIN = -9
C_MAX = 30
MAX_NNZ = 6
K_MAX = 12
SEARCH_WINDOW = 64
INPUT_WIDTH = 8


class Approximation(NamedTuple):
    """One candidate fixed-point approximation of 9/5."""

    budget: int
    coefficient: int
    scale: int
    csd: str
    max_error: float
    mismatches: int


def count_nnz(csd: str) -> int:
    """Count non-zero digits in a CSD string.

    :param csd: CSD string containing only ``+``, ``-`` and ``0``
    :type csd: str
    :return: number of ``+`` and ``-`` digits
    :rtype: int

    Examples:
        >>> count_nnz("+00-0+0-")
        4
    """
    return csd.count("+") + csd.count("-")


def ideal_display(celsius: int) -> int:
    """Return the correctly rounded Fahrenheit reading.

    ``floor(1.8 * C + 32 + 0.5)`` is evaluated in integers; the numerator is
    positive over ``[-9, 30]`` so Python's floor division is exact.

    :param celsius: temperature in degrees Celsius
    :type celsius: int
    :return: nearest integer temperature in degrees Fahrenheit
    :rtype: int

    Examples:
        >>> ideal_display(-9)
        16
        >>> ideal_display(30)
        86
    """
    return (18 * celsius + 325) // 10


def hardware_display(celsius: int, coefficient: int, scale: int) -> int:
    """Evaluate the fixed-point datapath that the generated Verilog builds.

    :param celsius: temperature in degrees Celsius
    :type celsius: int
    :param coefficient: integer CSD coefficient ``a``
    :type coefficient: int
    :param scale: number of fractional bits ``k``
    :type scale: int
    :return: Fahrenheit reading produced by ``(a*C + offset) >> k``
    :rtype: int

    Examples:
        >>> hardware_display(-9, 115, 6)
        16
        >>> hardware_display(30, 115, 6)
        86
    """
    offset = 32 * (1 << scale) + ((1 << (scale - 1)) if scale else 0)
    return (coefficient * celsius + offset) >> scale


def evaluate(coefficient: int, scale: int) -> tuple[float, int]:
    """Measure an approximation against the ideal display.

    :param coefficient: integer CSD coefficient ``a``
    :type coefficient: int
    :param scale: number of fractional bits ``k``
    :type scale: int
    :return: maximum pre-rounding error and number of wrong readings
    :rtype: tuple[float, int]
    """
    ratio = coefficient / float(1 << scale)
    max_error = max(abs(ratio * c - 1.8 * c) for c in range(C_MIN, C_MAX + 1))
    mismatches = sum(
        hardware_display(c, coefficient, scale) != ideal_display(c)
        for c in range(C_MIN, C_MAX + 1)
    )
    return max_error, mismatches


def search() -> tuple[dict[int, Approximation], dict[int, Approximation]]:
    """Sweep scale and coefficient for every nnz budget.

    :return: best exact and best effort approximation per nnz budget
    :rtype: tuple[dict[int, Approximation], dict[int, Approximation]]
    """
    exact: dict[int, Approximation] = {}
    best_effort: dict[int, Approximation] = {}
    for budget in range(1, MAX_NNZ + 1):
        exact_candidate: Approximation | None = None
        effort_candidate: Approximation | None = None
        for scale in range(0, K_MAX + 1):
            target = 1.8 * (1 << scale)
            low = max(1, round(target) - SEARCH_WINDOW)
            high = round(target) + SEARCH_WINDOW
            for coefficient in range(low, high + 1):
                csd = to_csd_i(coefficient)
                if count_nnz(csd) > budget:
                    continue
                max_error, mismatches = evaluate(coefficient, scale)
                candidate = Approximation(
                    budget, coefficient, scale, csd, max_error, mismatches
                )
                if mismatches == 0 and (
                    exact_candidate is None
                    or (max_error, scale, coefficient)
                    < (
                        exact_candidate.max_error,
                        exact_candidate.scale,
                        exact_candidate.coefficient,
                    )
                ):
                    exact_candidate = candidate
                if effort_candidate is None or (
                    mismatches,
                    max_error,
                    scale,
                    coefficient,
                ) < (
                    effort_candidate.mismatches,
                    effort_candidate.max_error,
                    effort_candidate.scale,
                    effort_candidate.coefficient,
                ):
                    effort_candidate = candidate
        if exact_candidate is not None:
            exact[budget] = exact_candidate
        assert effort_candidate is not None
        best_effort[budget] = effort_candidate
    return exact, best_effort


def build_verilog(approx: Approximation) -> str:
    """Build the multiplier plus the temperature converter top module.

    :param approx: chosen fixed-point approximation
    :type approx: Approximation
    :return: Verilog source of both modules
    :rtype: str
    """
    max_power = len(approx.csd) - 1
    multiplier = generate_csd_multiplier(approx.csd, INPUT_WIDTH, max_power)
    product_width = INPUT_WIDTH + max_power
    offset = 32 * (1 << approx.scale) + (
        (1 << (approx.scale - 1)) if approx.scale else 0
    )
    top = f"""
module temperature_c_to_f (
    input  signed [{INPUT_WIDTH - 1}:0] celsius,
    output signed [7:0] fahrenheit
);

    wire signed [{product_width - 1}:0] product;
    csd_multiplier mul (.x(celsius), .result(product));

    // 32 * 2**k (the +32 offset) plus 2**(k-1) (round to nearest)
    localparam signed [15:0] OFFSET = 16'sd{offset};
    wire signed [15:0] rounded = product + OFFSET;

    assign fahrenheit = rounded >>> {approx.scale};
endmodule
"""
    return multiplier + top


def build_testbench() -> str:
    """Build a self-checking testbench for the whole Celsius range.

    :return: Verilog testbench source
    :rtype: str
    """
    return f"""
module tb;
    reg signed [{INPUT_WIDTH - 1}:0] celsius;
    wire signed [7:0] fahrenheit;
    integer i;
    integer expected;
    integer errors;

    temperature_c_to_f dut (.celsius(celsius), .fahrenheit(fahrenheit));

    initial begin
        errors = 0;
        for (i = {C_MIN}; i <= {C_MAX}; i = i + 1) begin
            celsius = i;
            #1;
            expected = (18 * i + 325) / 10;
            if (fahrenheit !== expected) begin
                errors = errors + 1;
                $display("MISMATCH c=%0d f=%0d expected=%0d", celsius, fahrenheit, expected);
            end
        end
        if (errors == 0)
            $display("PASS: all {C_MAX - C_MIN + 1} readings match round(9/5*C+32)");
        else
            $fatal(1, "FAIL: %0d mismatches", errors);
        $finish;
    end
endmodule
"""


def simulate(dut: Path, testbench: Path) -> bool:
    """Compile and run the testbench when Icarus Verilog is installed.

    :param dut: path to the generated design
    :type dut: Path
    :param testbench: path to the generated testbench
    :type testbench: Path
    :return: ``True`` if the simulation passed (or could not be run)
    :rtype: bool
    """
    iverilog = shutil.which("iverilog")
    vvp = shutil.which("vvp")
    if iverilog is None or vvp is None:
        print("iverilog/vvp not found - generated Verilog was not simulated.")
        return True
    with tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp) / "sim.out"
        subprocess.run(
            [iverilog, "-g2012", "-o", str(binary), str(dut), str(testbench)],
            check=True,
        )
        return subprocess.run([vvp, str(binary)], check=False).returncode == 0


def main() -> int:
    """Run the demo.

    :return: process exit code
    :rtype: int
    """
    exact, best_effort = search()
    chosen = exact[min(exact)]

    print("Celsius -> Fahrenheit with a CSD constant multiplier")
    print(f"input range: {C_MIN} .. {C_MAX} degC,  output: integer degF")
    print()
    print(
        "nnz budget | coefficient | scale | CSD          | max |error| | wrong readings"
    )
    print(
        "-----------+-------------+-------+--------------+-------------+---------------"
    )
    for budget in range(1, MAX_NNZ + 1):
        candidate = exact.get(budget) or best_effort[budget]
        label = "exact" if budget in exact else "best effort"
        print(
            f"{budget:>10} | {candidate.coefficient:>11} | {candidate.scale:>5} "
            f"| {candidate.csd:<12} | {candidate.max_error:>11.6f} "
            f"| {candidate.mismatches:>2}/40  {label}"
        )
    print()
    print(
        f"minimum nnz for exact 1 degF display: {chosen.budget} "
        f"(a={chosen.coefficient}, k={chosen.scale})"
    )
    print(
        f"  a/2**k = {chosen.coefficient}/{1 << chosen.scale} = "
        f"{chosen.coefficient / (1 << chosen.scale):.8f} (9/5 = 1.8)"
    )
    print(
        f"  CSD {chosen.csd}: {chosen.budget} non-zero digits -> {chosen.budget - 1} adders"
    )
    offset = 32 * (1 << chosen.scale) + (1 << (chosen.scale - 1))
    print(f"  datapath: F = ({chosen.coefficient}*C + {offset}) >>> {chosen.scale}")
    print(
        f"  total adders: {chosen.budget - 1} (multiply) + 1 (offset/rounding) = {chosen.budget}"
    )
    print()

    if chosen.budget > 3:
        three = best_effort[3]
        print(
            f"for comparison, 3 nnz ({three.csd}, {three.coefficient}/{1 << three.scale}) "
            f"misses {three.mismatches}/40 readings by 1 degF"
        )
        print()

    dut = Path(__file__).resolve().with_name("temperature_c_to_f.v")
    testbench = Path(__file__).resolve().with_name("temperature_c_to_f_tb.v")
    dut.write_text(build_verilog(chosen), encoding="utf-8")
    testbench.write_text(build_testbench(), encoding="utf-8")
    print(f"wrote {dut.name} and {testbench.name}")
    print(flush=True)

    return 0 if simulate(dut, testbench) else 1


if __name__ == "__main__":
    sys.exit(main())
