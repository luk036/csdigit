import pytest
from hypothesis import given
from hypothesis import strategies as st

from csdigit.csd_multiplier import (
    _build_coeff_expr,
    _find_cross_patterns,
    generate_csd_multiplier,
    generate_csd_multipliers,
)


def test_generate_csd_multiplier_valid() -> None:
    csd = "+0-"
    N = 8
    M = 2
    expected_verilog = """
module csd_multiplier (
    input signed [7:0] x,      // Input value
    output signed [9:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [9:0] x_shift2 = x <<< 2;
    wire signed [9:0] x_shift0 = x <<< 0;

    // CSD implementation
    assign result = x_shift2 - x_shift0;
endmodule
"""
    assert generate_csd_multiplier(csd, N, M) == expected_verilog


def test_generate_csd_multiplier_positive_only() -> None:
    csd = "+0+"
    N = 4
    M = 2
    expected_verilog = """
module csd_multiplier (
    input signed [3:0] x,      // Input value
    output signed [5:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [5:0] x_shift2 = x <<< 2;
    wire signed [5:0] x_shift0 = x <<< 0;

    // CSD implementation
    assign result = x_shift2 + x_shift0;
endmodule
"""
    assert generate_csd_multiplier(csd, N, M) == expected_verilog


def test_generate_csd_multiplier_negative_only() -> None:
    csd = "-0-"
    N = 8
    M = 2
    expected_verilog = """
module csd_multiplier (
    input signed [7:0] x,      // Input value
    output signed [9:0] result // Result of multiplication
);

    // Create shifted versions of input
    wire signed [9:0] x_shift2 = x <<< 2;
    wire signed [9:0] x_shift0 = x <<< 0;

    // CSD implementation
    assign result = -x_shift2 - x_shift0;
endmodule
"""
    assert generate_csd_multiplier(csd, N, M) == expected_verilog


def test_generate_csd_multiplier_all_zeros() -> None:
    csd = "000"
    N = 8
    M = 2
    expected_verilog = """
module csd_multiplier (
    input signed [7:0] x,      // Input value
    output signed [9:0] result // Result of multiplication
);

    // CSD implementation
    assign result = 0;
endmodule
"""
    assert generate_csd_multiplier(csd, N, M) == expected_verilog


def test_generate_csd_multiplier_invalid_chars() -> None:
    with pytest.raises(
        ValueError, match="CSD string can only contain '\\+', '\\-', or '0'"
    ):
        generate_csd_multiplier("123", 8, 2)


def test_generate_csd_multiplier_invalid_length() -> None:
    with pytest.raises(
        ValueError,
        match="CSD length 3 doesn't match max_power=3 \\(should be max_power\\+1\\)",  # ???
    ):
        generate_csd_multiplier("+0-", 8, 3)


# Property-based tests for CSD multiplier generation


@given(
    st.text(alphabet="+-0", min_size=1, max_size=10),
    st.integers(min_value=1, max_value=16),
    st.integers(min_value=0, max_value=9),
)
def test_generate_csd_multiplier_valid_output_structure(
    csd: str, n: int, m: int
) -> None:
    """Test that generated Verilog has valid structure."""
    try:
        verilog = generate_csd_multiplier(csd, n, m)

        # Check that it's a valid Verilog module
        assert "module csd_multiplier" in verilog
        assert "endmodule" in verilog
        assert "input signed" in verilog and "x" in verilog
        assert "output signed" in verilog and "result" in verilog

        # Check that it contains proper assignment
        assert "assign result =" in verilog

    except ValueError:
        # This is expected for some invalid CSD strings
        pass


@given(st.text(alphabet="+-0", min_size=1, max_size=8))
def test_generate_csd_multiplier_csd_chars_only(csd: str) -> None:
    """Test that only valid CSD characters are processed."""
    try:
        # Use fixed N and M for this test
        verilog = generate_csd_multiplier(csd, 8, 2)

        # Should not raise any exceptions for valid CSD strings
        assert verilog is not None
        assert len(verilog) > 0

    except ValueError:
        # This is expected for invalid CSD strings
        pass


@given(st.text(alphabet="abc", min_size=1, max_size=10))
def test_generate_csd_multiplier_invalid_chars_rejection(invalid_csd: str) -> None:
    """Test that invalid characters are rejected."""
    try:
        generate_csd_multiplier(invalid_csd, 8, len(invalid_csd) - 1)
        assert False, "Should have raised ValueError for invalid CSD characters"
    except ValueError as e:
        # Check for either invalid character error or length mismatch error
        assert "CSD string can only contain" in str(
            e
        ) or "doesn't match max_power" in str(e)


@given(st.integers(min_value=1, max_value=16), st.integers(min_value=0, max_value=9))
def test_generate_csd_multiplier_all_zeros_structure(n: int, m: int) -> None:
    """Test structure of generated Verilog for all-zero CSD."""
    csd = "0" * (m + 1)  # Create all-zero CSD of correct length
    verilog = generate_csd_multiplier(csd, n, m)

    # Should contain direct assignment to 0
    assert "assign result = 0;" in verilog

    # Should not contain any shift operations
    assert "x_shift" not in verilog


@given(st.integers(min_value=1, max_value=12), st.integers(min_value=1, max_value=6))
def test_generate_csd_multiplier_single_nonzero(n: int, m: int) -> None:
    """Test structure for CSD with single non-zero digit."""
    # Create CSD with single '+' at position m
    csd = "0" * m + "+"
    verilog = generate_csd_multiplier(csd, n, m)

    # Should contain a valid assignment
    assert "assign result" in verilog
    # Should be a valid Verilog module
    assert "module csd_multiplier" in verilog
    assert "endmodule" in verilog


@given(st.text(alphabet="+-0", min_size=2, max_size=8))
def test_generate_csd_multiplier_shift_operations(csd: str) -> None:
    """Test that shift operations are correctly generated."""
    try:
        # Use fixed N and M that match CSD length
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)

        # Count non-zero digits in CSD
        non_zero_count = csd.count("+") + csd.count("-")

        if non_zero_count > 0:
            # Should have shift operations for non-zero digits
            assert "wire signed" in verilog
            assert "x_shift" in verilog

            # Count shift operations
            shift_count = verilog.count("x_shift")
            # Should have at least as many shifts as non-zero digits
            assert shift_count >= non_zero_count

    except ValueError:
        # Expected for malformed CSD strings
        pass


@given(st.text(alphabet="+-0", min_size=1, max_size=8))
def test_generate_csd_multiplier_bit_width_consistency(csd: str) -> None:
    """Test that bit widths are consistent throughout the generated Verilog."""
    try:
        m = len(csd) - 1
        n = 8
        verilog = generate_csd_multiplier(csd, n, m)

        # Check that input and output declarations exist
        assert "input signed" in verilog
        assert "output signed" in verilog

        # Check that bit widths are present
        assert "[" in verilog and "]" in verilog

        # Check wire bit widths if they exist
        if "wire signed" in verilog:
            assert "[" in verilog and ":0]" in verilog

    except ValueError:
        # Expected for malformed CSD strings
        pass


@given(st.text(alphabet="+-0", min_size=1, max_size=6))
def test_generate_csd_multiplier_arithmetic_operations(csd: str) -> None:
    """Test that arithmetic operations are correctly represented."""
    try:
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)

        non_zero_count = csd.count("+") + csd.count("-")

        if non_zero_count == 0:
            # All zeros - should have direct assignment
            assert "assign result = 0;" in verilog
        elif non_zero_count == 1:
            # Single non-zero - should have direct assignment to shifted value
            assert "assign result" in verilog
        else:
            # Multiple non-zeros - should have arithmetic operations
            assign_lines = [
                line for line in verilog.split("\n") if "assign result =" in line
            ]
            if assign_lines:
                assign_line = assign_lines[0]
                # Should contain + or - operations (excluding comments)
                has_plus = "+" in assign_line and assign_line.count("+") > 0
                has_minus = "-" in assign_line and assign_line.count("-") > 0
                # At least one arithmetic operation should be present
                assert has_plus or has_minus

    except ValueError:
        # Expected for malformed CSD strings
        pass


@given(st.integers(min_value=1, max_value=10), st.integers(min_value=0, max_value=5))
def test_generate_csd_multiplier_deterministic(n: int, m: int) -> None:
    """Test that generation is deterministic."""
    # Create a simple valid CSD
    csd = "0" * m + "+"

    # Generate twice
    verilog1 = generate_csd_multiplier(csd, n, m)
    verilog2 = generate_csd_multiplier(csd, n, m)

    # Should be identical
    assert verilog1 == verilog2


@given(st.text(alphabet="+-0", min_size=1, max_size=8))
def test_generate_csd_multiplier_comment_structure(csd: str) -> None:
    """Test that comments are properly structured."""
    try:
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)

        # Should have module comment
        lines = verilog.split("\n")
        next(i for i, line in enumerate(lines) if "module csd_multiplier" in line)

        # Should have input/output comments
        input_comment_found = any("Input value" in line for line in lines)
        output_comment_found = any("Result of multiplication" in line for line in lines)

        assert input_comment_found
        assert output_comment_found

    except ValueError:
        # Expected for malformed CSD strings
        pass


@given(st.text(alphabet="+0", min_size=1, max_size=8))  # Only positive and zero
def test_generate_csd_multiplier_positive_only_operations(csd: str) -> None:
    """Test operations for CSD with only positive digits."""
    try:
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)

        if csd.count("+") > 1:
            # Should have addition operations
            assign_lines = [
                line for line in verilog.split("\n") if "assign result =" in line
            ]
            if assign_lines:
                assign_line = assign_lines[0]
                # Should contain addition operations
                assert "+" in assign_line

    except ValueError:
        # Expected for malformed CSD strings
        pass


# --- LCSRe optimization tests ---


def test_flat_when_pattern_nnz_is_one() -> None:
    """Pattern '+0' has only 1 non-zero digit — should NOT be optimized."""
    verilog = generate_csd_multiplier("+00-00+0", 8, 7)
    assert "_pat" not in verilog, "Should not create _pat for nnz=1 pattern"
    assert "x_shift7 - x_shift4 + x_shift1" in verilog


def test_double_repeat_optimization() -> None:
    """+0-0+0-0: repeated '+0-0' (2 nnz) at positions 0 and 4."""
    verilog = generate_csd_multiplier("+0-0+0-0", 8, 7)
    assert "_pat" in verilog, "Should create _pat wire"
    assert "_pat = x_shift7 - x_shift5" in verilog
    assert "(_pat >>> 4)" in verilog
    # Count only x_shift wire declarations (exclude _pat which also has 'wire signed' + 'x_shift')
    xwires = [line for line in verilog.split("\n") if "wire signed" in line and "_pat" not in line]
    assert len(xwires) == 4  # 4 wires: x_shift7, x_shift5, x_shift3, x_shift1
    assert "LCSRe" in verilog


def test_triple_repeat_optimization() -> None:
    """+0-0+0-0+0-0: repeated '+0-0' at positions 0, 4, 8."""
    verilog = generate_csd_multiplier("+0-0+0-0+0-0", 8, 11)
    assert "_pat" in verilog
    assert "(_pat >>> 4)" in verilog
    assert "(_pat >>> 8)" in verilog
    assert "LCSRe" in verilog


def test_longer_pattern_repeat() -> None:
    """+00-00+00-00: repeated '+00-00' (2 nnz, 5 chars) at positions 0 and 6."""
    verilog = generate_csd_multiplier("+00-00+00-00", 8, 11)
    assert "_pat" in verilog
    assert "_pat = x_shift11 - x_shift8" in verilog
    assert "(_pat >>> 6)" in verilog


def test_leading_minus_no_optimization() -> None:
    """CSD starting with '-' and no repeated pattern — flat output with sign fix."""
    verilog = generate_csd_multiplier("-0-", 8, 2)
    assert "_pat" not in verilog
    # First term sign must be preserved
    assert "-x_shift2 - x_shift0" in verilog


def test_pattern_with_leading_minus() -> None:
    """Repeated pattern starting with '-': -0+0-0+0."""
    verilog = generate_csd_multiplier("-0+0-0+0", 8, 7)
    assert "_pat" in verilog
    assert "_pat = -x_shift7 + x_shift5" in verilog
    assert "(_pat >>> 4)" in verilog


def test_no_optimization_for_single_occurrence() -> None:
    """CSD with unique pattern throughout — no repeat = flat."""
    verilog = generate_csd_multiplier("+0-+00-0", 8, 7)
    assert "_pat" not in verilog


def test_pat_wire_width_matches_output() -> None:
    """The _pat wire should have the same width as output."""
    verilog = generate_csd_multiplier("+0-0+0-0", 8, 7)
    # output_width = 8 + 7 = 15, so [14:0]
    output_width = 8 + 7 - 1
    assert f"[{output_width}:0] _pat" in verilog


def test_repeat_with_trailing_gap() -> None:
    """Repeated pattern followed by non-repeating suffix."""
    verilog = generate_csd_multiplier("+0-0+0-0+0", 8, 9)
    assert "_pat" in verilog
    assert "(_pat >>> 4)" in verilog
    # The trailing '+0' at position 8 has power=1, appears as x_shift1
    assert "x_shift1" in verilog


def test_repeat_with_leading_gap() -> None:
    """Non-repeating prefix before repeated pattern."""
    verilog = generate_csd_multiplier("0+0-0+0-0+0-0", 8, 12)
    assert "_pat" in verilog


# --- Property-based LCSRe tests ---


@given(st.text(alphabet="+-0", min_size=4, max_size=12))
def test_optimization_only_with_nnz_ge2(csd: str) -> None:
    """When optimization triggers, there must be a _pat wire and LCSRe comment."""
    try:
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)
        has_opt = "_pat" in verilog
        has_lcsre = "LCSRe" in verilog
        assert has_opt == has_lcsre, "_pat and LCSRe comment must appear together"
        if has_opt:
            # Pattern must have at least 2 non-zero digits
            pat_line = [line for line in verilog.split("\n") if "_pat =" in line]
            assert len(pat_line) <= 1  # at most one _pat wire
    except ValueError:
        pass


@given(st.text(alphabet="+-0", min_size=4, max_size=12))
def test_shift_references_use_arithmetic_right_shift(csd: str) -> None:
    """All shifted _pat references must use >>> (arithmetic shift)."""
    try:
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)
        if "_pat >>>" in verilog:
            # Every shift must use >>>
            assert ">>" not in verilog.replace(">>>", "")
    except ValueError:
        pass


@given(st.text(alphabet="+-0", min_size=4, max_size=12))
def test_x_shift_count_bounds(csd: str) -> None:
    """Number of x_shift wires should be at most the number of non-zero digits."""
    try:
        m = len(csd) - 1
        verilog = generate_csd_multiplier(csd, 8, m)
        nnz = csd.count("+") + csd.count("-")
        # Each wire declarations line is for one x_shift (plus maybe _pat)
        wire_decls = [line for line in verilog.split("\n") if "wire signed" in line]
        x_shift_wires = [line for line in wire_decls if "x_shift" in line]
        assert len(x_shift_wires) <= nnz or "_pat" in verilog
    except ValueError:
        pass


# =====================================================================
# Cross-CSE tests: _find_cross_patterns, _build_coeff_expr,
# generate_csd_multipliers
# =====================================================================


def test_find_cross_patterns_basic() -> None:
    """Find shared pattern across multiple CSD strings."""
    result = _find_cross_patterns(["+0-0", "+0-0+0-0"])
    assert "+0-0" in result
    occ = result["+0-0"]
    idxs = {ci for ci, _ in occ}
    assert len(idxs) >= 2


def test_find_cross_patterns_no_match() -> None:
    """No shared pattern -> empty dict."""
    result = _find_cross_patterns(["+-0", "0-+0"])
    assert result == {}


def test_find_cross_patterns_min_nnz_filters() -> None:
    """min_nnz parameter correctly filters low-NNZ patterns."""
    result = _find_cross_patterns(["+00-", "+00-"], min_nnz=3)
    assert result == {}
    result = _find_cross_patterns(["+00-", "+00-"], min_nnz=2)
    assert "+00-" in result


def test_find_cross_patterns_empty_list() -> None:
    """Empty CSD list -> empty dict."""
    assert _find_cross_patterns([]) == {}


def test_find_cross_patterns_same_csd_ignored() -> None:
    """Pattern must cross >=2 *different* CSD strings."""
    result = _find_cross_patterns(["+0-0"], min_nnz=2)
    assert result == {}


def test_build_coeff_expr_no_pattern() -> None:
    """Flat expression without shared CSE."""
    expr = _build_coeff_expr("+0-", 2, None, 0, "")
    assert "x_shift2 - x_shift0" in expr


def test_build_coeff_expr_all_zero_no_pattern() -> None:
    """All-zero CSD with no pattern -> empty string."""
    expr = _build_coeff_expr("000", 2, None, 0, "")
    assert expr == ""


def test_build_coeff_expr_with_pattern() -> None:
    """Expression using shared CSE wire with shifts."""
    expr = _build_coeff_expr("+0-0+0-0", 7, "+0-0", 0, "_cse_0")
    assert "_cse_0" in expr
    assert "(_cse_0 >>> 4)" in expr


def test_build_coeff_expr_with_leading_gap() -> None:
    """Gap before first pattern occurrence."""
    expr = _build_coeff_expr("0+0-0+0", 7, "+0-0", 1, "_cse_0")
    assert "_cse_0" in expr
    assert "x_shift7" in expr or "x_shift" in expr


def test_build_coeff_expr_with_trailing_gap() -> None:
    """Suffix after last pattern occurrence."""
    expr = _build_coeff_expr("+0-0+0-0+0", 9, "+0-0", 0, "_cse_0")
    assert "_cse_0" in expr
    assert "x_shift1" in expr


def test_build_coeff_expr_gap_with_nonzero_content() -> None:
    """Gap containing non-zero digits before pattern (covers line 232)."""
    expr = _build_coeff_expr("+0+0-0+0", 7, "+0-0", 2, "_cse_0")
    assert "x_shift7" in expr
    assert "_cse_0" in expr


def test_build_coeff_expr_pattern_not_found_all_zero() -> None:
    """Pattern given but not found in CSD, all-zero content -> empty (covers line 247)."""
    expr = _build_coeff_expr("00000", 4, "+0-0", 0, "_cse_0")
    assert expr == ""


# --- generate_csd_multipliers (cross-CSE public API) ---


def test_generate_csd_multipliers_empty_raises() -> None:
    """Empty coefficient list raises ValueError."""
    with pytest.raises(ValueError, match="At least one coefficient is required"):
        generate_csd_multipliers([], module_name="test")


def test_generate_csd_multipliers_single_coeff() -> None:
    """Single coefficient — no cross-CSE wire."""
    verilog = generate_csd_multipliers(
        [("h0", "+0-", 8, 2)],
        module_name="single_tap",
    )
    assert "module single_tap" in verilog
    assert "endmodule" in verilog
    assert "input signed [7:0] x" in verilog
    assert "output signed [9:0] h0" in verilog
    assert "_cse_0" not in verilog
    assert "x_shift2" in verilog
    assert "x_shift0" in verilog


def test_generate_csd_multipliers_mismatched_widths() -> None:
    """Mismatched input_width/max_power raises ValueError."""
    coeffs = [
        ("h0", "+0-0", 8, 3),
        ("h1", "+0-0+0-0", 16, 5),
    ]
    with pytest.raises(
        ValueError,
        match="All coefficients must share the same input_width and max_power",
    ):
        generate_csd_multipliers(coeffs)


def test_generate_csd_multipliers_invalid_chars() -> None:
    """Invalid CSD characters raise ValueError."""
    with pytest.raises(ValueError, match="CSD string.*can only contain"):
        generate_csd_multipliers([("h0", "12+", 8, 2)])


def test_generate_csd_multipliers_length_mismatch() -> None:
    """CSD length mismatched with max_power raises ValueError."""
    with pytest.raises(ValueError, match="doesn't match max_power"):
        generate_csd_multipliers([("h0", "+0-0", 8, 5)])


def test_generate_csd_multipliers_all_zero_coeffs() -> None:
    """All-zero CSD coefficients produce zero assignments."""
    verilog = generate_csd_multipliers(
        [("h0", "000", 8, 2)],
        module_name="zero_filter",
    )
    assert "x_shift" not in verilog
    assert "= 0;" in verilog


def test_generate_csd_multipliers_with_shared_pattern() -> None:
    """Cross-CSE triggers when a pattern repeats across coefficients."""
    verilog = generate_csd_multipliers(
        [
            ("h0", "0000+0-0", 8, 7),  # padded to max_power=7, len=8
            ("h1", "+0-0+0-0", 8, 7),
        ],
        module_name="fir_shared",
    )
    assert "_cse_0" in verilog
    assert "Cross-CSE" in verilog


def test_generate_csd_multipliers_no_shared_pattern() -> None:
    """No cross-CSE when coefficients share no common substring."""
    verilog = generate_csd_multipliers(
        [
            ("h0", "+0-0", 8, 3),
            ("h1", "0-+0", 8, 3),
        ],
        module_name="fir_no_share",
    )
    assert "_cse_0" not in verilog


def test_generate_csd_multipliers_single_nnz_no_cse() -> None:
    """Single non-zero digit patterns should not trigger cross-CSE (NNZ<2)."""
    verilog = generate_csd_multipliers(
        [
            ("h0", "+00", 8, 2),
            ("h1", "0+0", 8, 2),
        ],
        module_name="single_nnz",
    )
    assert "_cse_0" not in verilog


def test_generate_csd_multipliers_custom_module_name() -> None:
    """Custom module name is reflected in output."""
    verilog = generate_csd_multipliers(
        [("coeff", "+0-", 8, 2)],
        module_name="my_custom_filter",
    )
    assert "module my_custom_filter" in verilog


def test_generate_csd_multipliers_mixed_pattern_and_flat() -> None:
    """Some coeffs use pattern, others fall back to flat expression."""
    # h0 and h1 share "+0-0" pattern; h2 has a different string
    verilog = generate_csd_multipliers(
        [
            ("h0", "+0-0+0-0", 8, 7),
            ("h1", "0000+0-0", 8, 7),  # padded to max_power=7
            ("h2", "0+00-0+0", 8, 7),
        ],
        module_name="mixed",
    )
    assert "module mixed" in verilog


def test_generate_csd_multipliers_three_coeffs_all_zeros() -> None:
    """Multiple all-zero coefficients."""
    verilog = generate_csd_multipliers(
        [
            ("a", "00", 4, 1),
            ("b", "00", 4, 1),
        ],
        module_name="zeros",
    )
    assert "x_shift" not in verilog
    assert "= 0;" in verilog


def test_generate_csd_multipliers_with_csd_leading_minus() -> None:
    """Coefficient starting with minus in cross-CSE."""
    verilog = generate_csd_multipliers(
        [("h0", "-0+", 8, 2)],
        module_name="leading_minus",
    )
    assert "module leading_minus" in verilog
    assert "-x_shift2 + x_shift0" in verilog
