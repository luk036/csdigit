"""CSD multiplier demo: a separable 7-tap Gaussian blur filter.

The blur kernel is a 7-tap Gaussian with ``sigma = 2`` and an integer scale of
``1024``.  The exact kernel is ``[72, 134, 195, 222, 195, 134, 72]``; its
coefficients sum to 1024.  A separable 2D blur applies this 1D kernel
horizontally and vertically, so the 1D adder cost is paid twice.

For an 8-bit image, the worst-case pre-round output error of a CSD
approximation is

    255 * max(P, N) / 1024,

where ``P`` and ``N`` are the sums of the positive and negative coefficient
errors over the full kernel.  Using the L1 sum instead would be conservative
when the coefficient errors have mixed signs.  The demo searches, within a
+/-32 coefficient window around the exact kernel, for the minimum total NNZ
under two error targets:

* ``0.5`` LSB: 18 NNZ, worst-case error 0.498 LSB;
* ``1.0`` LSB: 16 NNZ, worst-case error 0.996 LSB.

The exact kernel needs 21 NNZ.  The 18-NNZ design is emitted as a symmetric
1D FIR: three pair pre-adds, four CSD coefficient multipliers, three product
adds, and one rounding add, for 13 adders per pass (26 for the separable 2D
filter, excluding line buffers).  The direct non-symmetric form would need 18
adders per pass.

Run with::

    python examples/gaussian_blur_csd.py

It writes ``gaussian_blur_1d.v`` and ``gaussian_blur_1d_tb.v`` next to this
file and simulates them with Icarus Verilog when available.
"""

from __future__ import annotations

import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import NamedTuple

from csdigit.csd import to_csd_i
from csdigit.csd_multiplier import generate_csd_multiplier

SIGMA = 2.0
SCALE = 1024
TAPS = 7
INPUT_WIDTH = 11
EXACT_INDEPENDENT = (222, 195, 134, 72)
SEARCH_WINDOW = 32


class Approximation(NamedTuple):
    """One symmetric CSD kernel approximation.

    The independent coefficients are ``(center, +-1, +-2, +-3)``; the full
    kernel is ``(a3, a2, a1, a0, a1, a2, a3)``.
    """

    target_lsb: float
    independent: tuple[int, int, int, int]
    weights: tuple[int, int, int, int]
    positive_error: int
    negative_error: int

    @property
    def full_kernel(self) -> tuple[int, int, int, int, int, int, int]:
        """Return the seven coefficients in image order.

        :return: full kernel from left to right
        :rtype: tuple[int, int, int, int, int, int, int]
        """
        a0, a1, a2, a3 = self.independent
        return (a3, a2, a1, a0, a1, a2, a3)

    @property
    def total_nnz(self) -> int:
        """Return the NNZ of the full seven-tap kernel.

        :return: sum of the seven CSD weights
        :rtype: int
        """
        a0, a1, a2, a3 = self.weights
        return a0 + 2 * (a1 + a2 + a3)

    @property
    def worst_error_lsb(self) -> float:
        """Return the worst-case pre-round error in output LSBs.

        :return: ``255 * max(positive_error, negative_error) / SCALE``
        :rtype: float
        """
        return 255.0 * max(self.positive_error, self.negative_error) / SCALE

    @property
    def coefficient_adders(self) -> int:
        """Return the adders inside the four coefficient multipliers.

        :return: sum of ``weight - 1`` over the independent coefficients
        :rtype: int
        """
        return sum(weight - 1 for weight in self.weights)

    @property
    def one_dimensional_adders(self) -> int:
        """Return the adders in the symmetric 1D pass.

        The count is three pair pre-adds, the coefficient adders, three
        product-accumulation adders, and one rounding adder.

        :return: arithmetic cells in one 1D pass
        :rtype: int
        """
        return 3 + self.coefficient_adders + 3 + 1

    @property
    def two_dimensional_adders(self) -> int:
        """Return the arithmetic cells in the separable 2D filter.

        :return: two times the 1D adder count, excluding line buffers
        :rtype: int
        """
        return 2 * self.one_dimensional_adders


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


def full_kernel(
    independent: tuple[int, int, int, int]
) -> tuple[int, int, int, int, int, int, int]:
    """Expand a symmetric independent kernel to seven taps.

    :param independent: ``(center, +-1, +-2, +-3)`` coefficients
    :type independent: tuple[int, int, int, int]
    :return: seven coefficients in image order
    :rtype: tuple[int, int, int, int, int, int, int]
    """
    a0, a1, a2, a3 = independent
    return (a3, a2, a1, a0, a1, a2, a3)


def worst_error_lsb(independent: tuple[int, int, int, int]) -> tuple[int, int, float]:
    """Compute the exact worst-case convolution error.

    For independent 8-bit pixels, the maximum of ``sum(delta_i * x_i)`` is
    ``255 * max(P, N)``, where ``P`` and ``N`` are the positive and negative
    error sums.  This is tighter than the L1 bound when errors have mixed
    signs.

    :param independent: ``(center, +-1, +-2, +-3)`` coefficients
    :type independent: tuple[int, int, int, int]
    :return: positive error sum, negative error sum, and worst error in LSBs
    :rtype: tuple[int, int, float]

    Examples:
        >>> worst_error_lsb((224, 194, 134, 72))
        (2, 2, 0.498046875)
    """
    delta = tuple(a - c for a, c in zip(independent, EXACT_INDEPENDENT))
    d0, d1, d2, d3 = delta
    positive = sum(d for d in (d3, d2, d1, d0, d1, d2, d3) if d > 0)
    negative = sum(-d for d in (d3, d2, d1, d0, d1, d2, d3) if d < 0)
    return positive, negative, 255.0 * max(positive, negative) / SCALE


def exact_approximation() -> Approximation:
    """Return the exact, sum-normalized integer Gaussian kernel.

    :return: exact kernel with zero approximation error
    :rtype: Approximation
    """
    weights = tuple(count_nnz(to_csd_i(a)) for a in EXACT_INDEPENDENT)
    return Approximation(0.0, EXACT_INDEPENDENT, weights, 0, 0)


def search(target_lsb: float) -> Approximation | None:
    """Find the minimum-NNZ kernel under a worst-case error target.

    The search is exhaustive within ``+/-SEARCH_WINDOW`` of the exact kernel.

    :param target_lsb: maximum pre-round error in output LSBs
    :type target_lsb: float
    :return: best approximation, or ``None`` if the search fails
    :rtype: Approximation | None
    """
    best: Approximation | None = None
    for a0 in range(
        EXACT_INDEPENDENT[0] - SEARCH_WINDOW, EXACT_INDEPENDENT[0] + SEARCH_WINDOW + 1
    ):
        for a1 in range(
            EXACT_INDEPENDENT[1] - SEARCH_WINDOW,
            EXACT_INDEPENDENT[1] + SEARCH_WINDOW + 1,
        ):
            for a2 in range(
                EXACT_INDEPENDENT[2] - SEARCH_WINDOW,
                EXACT_INDEPENDENT[2] + SEARCH_WINDOW + 1,
            ):
                remainder = SCALE - a0 - 2 * a1 - 2 * a2
                if remainder % 2:
                    continue
                a3 = remainder // 2
                if a3 <= 0 or abs(a3 - EXACT_INDEPENDENT[3]) > SEARCH_WINDOW:
                    continue
                independent = (a0, a1, a2, a3)
                positive, negative, error = worst_error_lsb(independent)
                if error >= target_lsb:
                    continue
                weights = tuple(count_nnz(to_csd_i(a)) for a in independent)
                candidate = Approximation(
                    target_lsb, independent, weights, positive, negative
                )
                if best is None or (
                    candidate.total_nnz,
                    candidate.worst_error_lsb,
                    independent,
                ) < (
                    best.total_nnz,
                    best.worst_error_lsb,
                    best.independent,
                ):
                    best = candidate
    return best


def multiplier_module(coefficient: int) -> str:
    """Generate and rename one CSD multiplier module.

    :param coefficient: positive integer coefficient
    :type coefficient: int
    :return: Verilog module named ``csd_mult_<coefficient>``
    :rtype: str
    """
    csd = to_csd_i(coefficient)
    module = generate_csd_multiplier(csd, INPUT_WIDTH, len(csd) - 1)
    return module.replace("module csd_multiplier", f"module csd_mult_{coefficient}", 1)


def build_verilog(approx: Approximation) -> str:
    """Build the symmetric 1D Gaussian filter and its multiplier modules.

    :param approx: chosen kernel approximation
    :type approx: Approximation
    :return: Verilog source for four multipliers and the filter top
    :rtype: str
    """
    a0, a1, a2, a3 = approx.independent
    widths = {}
    for coefficient in (a0, a1, a2, a3):
        csd = to_csd_i(coefficient)
        widths[coefficient] = INPUT_WIDTH + len(csd) - 1

    multipliers = "\n".join(multiplier_module(a) for a in (a3, a2, a1, a0))
    top = f"""
module gaussian_blur_1d (
    input  [7:0] x0, x1, x2, x3, x4, x5, x6,
    output [7:0] y
);
    wire signed [10:0] s3 = x0 + x6;
    wire signed [10:0] s2 = x1 + x5;
    wire signed [10:0] s1 = x2 + x4;
    wire signed [10:0] s0 = x3;

    wire signed [{widths[a3] - 1}:0] p3_raw;
    wire signed [{widths[a2] - 1}:0] p2_raw;
    wire signed [{widths[a1] - 1}:0] p1_raw;
    wire signed [{widths[a0] - 1}:0] p0_raw;

    csd_mult_{a3} m3 (.x(s3), .result(p3_raw));
    csd_mult_{a2} m2 (.x(s2), .result(p2_raw));
    csd_mult_{a1} m1 (.x(s1), .result(p1_raw));
    csd_mult_{a0} m0 (.x(s0), .result(p0_raw));

    wire signed [18:0] p3 = p3_raw;
    wire signed [18:0] p2 = p2_raw;
    wire signed [18:0] p1 = p1_raw;
    wire signed [18:0] p0 = p0_raw;
    wire signed [18:0] total = p3 + p2 + p1 + p0;
    wire signed [18:0] rounded = (total + 19'sd512) >>> 10;

    assign y = rounded[7:0];
endmodule
"""
    return multipliers + top


def expected_value(
    kernel: tuple[int, int, int, int, int, int, int], pixels: tuple[int, ...]
) -> int:
    """Evaluate the integer convolution and round to the nearest output.

    :param kernel: seven integer coefficients
    :type kernel: tuple[int, int, int, int, int, int, int]
    :param pixels: seven 8-bit input pixels
    :type pixels: tuple[int, ...]
    :return: 8-bit blurred output
    :rtype: int
    """
    return (sum(k * p for k, p in zip(kernel, pixels)) + SCALE // 2) >> 10


def test_vectors() -> list[tuple[int, ...]]:
    """Return edge cases and deterministic random 8-bit vectors.

    :return: seven-pixel input vectors
    :rtype: list[tuple[int, ...]]
    """
    vectors = [
        (0, 0, 0, 0, 0, 0, 0),
        (255, 255, 255, 255, 255, 255, 255),
        (128, 128, 128, 128, 128, 128, 128),
        (0, 255, 0, 255, 0, 255, 0),
        (255, 0, 255, 0, 255, 0, 255),
        (0, 0, 0, 255, 0, 0, 0),
        (0, 0, 255, 0, 255, 0, 0),
        (255, 0, 0, 0, 0, 0, 255),
    ]
    rng = random.Random(42)
    vectors.extend(tuple(rng.randrange(256) for _ in range(7)) for _ in range(24))
    return vectors


def build_testbench(approx: Approximation) -> str:
    """Build a self-checking testbench for the 1D filter.

    The expected values use the approximate CSD kernel, so the testbench
    verifies the RTL implementation rather than the kernel approximation.

    :param approx: chosen kernel approximation
    :type approx: Approximation
    :return: Verilog testbench source
    :rtype: str
    """
    kernel = approx.full_kernel
    checks = []
    for pixels in test_vectors():
        checks.append(
            "        check(8'd{p0}, 8'd{p1}, 8'd{p2}, 8'd{p3}, "
            "8'd{p4}, 8'd{p5}, 8'd{p6}, 8'd{expected});".format(
                p0=pixels[0],
                p1=pixels[1],
                p2=pixels[2],
                p3=pixels[3],
                p4=pixels[4],
                p5=pixels[5],
                p6=pixels[6],
                expected=expected_value(kernel, pixels),
            )
        )
    return f"""
module tb;
    reg  [7:0] x0, x1, x2, x3, x4, x5, x6;
    wire [7:0] y;

    gaussian_blur_1d dut (
        .x0(x0), .x1(x1), .x2(x2), .x3(x3),
        .x4(x4), .x5(x5), .x6(x6), .y(y)
    );

    task check;
        input [7:0] v0, v1, v2, v3, v4, v5, v6;
        input [7:0] expected;
        begin
            x0 = v0; x1 = v1; x2 = v2; x3 = v3;
            x4 = v4; x5 = v5; x6 = v6;
            #1;
            if (y !== expected) begin
                $display("MISMATCH x=%0d,%0d,%0d,%0d,%0d,%0d,%0d y=%0d expected=%0d",
                         v0, v1, v2, v3, v4, v5, v6, y, expected);
                $fatal(1, "Gaussian blur RTL mismatch");
            end
        end
    endtask

    initial begin
{chr(10).join(checks)}
        $display("PASS: all {len(checks)} vectors match the CSD kernel");
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
    :return: ``True`` if the simulation passed or could not be run
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
            [
                iverilog,
                "-g2012",
                "-s",
                "tb",
                "-o",
                str(binary),
                str(dut),
                str(testbench),
            ],
            check=True,
        )
        return subprocess.run([vvp, str(binary)], check=False).returncode == 0


def print_analysis() -> None:
    """Print the kernel, NNZ, and adder analysis for the demo."""
    exact = exact_approximation()
    one_lsb = search(1.0)
    half_lsb = search(0.5)
    assert one_lsb is not None and half_lsb is not None

    print("7-tap Gaussian blur: sigma=2.0, scale=1024, 8-bit pixels")
    print(f"search window: +/-{SEARCH_WINDOW} coefficients around the exact kernel")
    print(
        f"exact kernel: {full_kernel(EXACT_INDEPENDENT)}  (sum={sum(full_kernel(EXACT_INDEPENDENT))})"
    )
    print(
        f"exact full CSD weights: {tuple(count_nnz(to_csd_i(a)) for a in full_kernel(EXACT_INDEPENDENT))}"
    )
    print()
    print(
        "target    coefficients (center first)  weights        NNZ  pre-round err  adders 1D/2D  direct 1D/2D"
    )
    print(
        "---------+------------------------------+--------------+----+------------+-----------+-------------"
    )
    for label, approx in (
        ("exact", exact),
        ("<=1 LSB", one_lsb),
        ("<0.5 LSB", half_lsb),
    ):
        coeffs = approx.independent
        weights = approx.weights
        print(
            f"{label:<8} | {str(coeffs):<28} | {str(weights):<12} | "
            f"{approx.total_nnz:>2} | {approx.worst_error_lsb:>10.6f} | "
            f"{approx.one_dimensional_adders:>3}/{approx.two_dimensional_adders:<3} "
            f"| {approx.total_nnz:>3}/{2 * approx.total_nnz:<3}"
        )
    print()
    print(
        "The direct column is the non-symmetric form: coefficient adders + 6 product adds + 1 round."
    )
    print("The 2D counts exclude line-buffer registers.")
    exact_kernel = full_kernel(EXACT_INDEPENDENT)
    observed = max(
        abs(expected_value(half_lsb.full_kernel, p) - expected_value(exact_kernel, p))
        for p in test_vectors()
    )
    print(
        f"observed rounded difference vs exact Gaussian on test vectors: {observed} LSB"
    )
    print(
        "The 0.498 LSB bound is pre-round; near a boundary the rounded result can differ by 1."
    )
    print()
    print(
        f"chosen RTL: target <0.5 LSB, coefficients {half_lsb.independent}, "
        f"NNZ={half_lsb.total_nnz}, error={half_lsb.worst_error_lsb:.6f} LSB"
    )


def main() -> int:
    """Run the Gaussian-blur demo.

    :return: process exit code
    :rtype: int
    """
    print_analysis()
    half_lsb = search(0.5)
    assert half_lsb is not None
    dut = Path(__file__).resolve().with_name("gaussian_blur_1d.v")
    testbench = Path(__file__).resolve().with_name("gaussian_blur_1d_tb.v")
    dut.write_text(build_verilog(half_lsb), encoding="utf-8")
    testbench.write_text(build_testbench(half_lsb), encoding="utf-8")
    print(f"wrote {dut.name} and {testbench.name}")
    print(flush=True)
    return 0 if simulate(dut, testbench) else 1


if __name__ == "__main__":
    sys.exit(main())
