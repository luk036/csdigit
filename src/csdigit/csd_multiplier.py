"""
CSD Multiplier — Verilog Code Generation

Translates a Canonical Signed Digit (CSD) string into a synthesizable Verilog
module that implements constant multiplication using only shift-and-add/subtract
operations. When the CSD string contains repeated patterns, LCSRe (Longest
Common Substring with Repeated Elements) is used to share hardware via a
sub-expression wire.
"""

from typing import Optional

from csdigit.lcsre import longest_repeated_substring


def _build_range_expr(csd: str, start: int, length: int, max_power: int) -> str:
    """Build a flat Verilog expression for csd[start:start+length].

    Returns empty string if the range has no non-zero digits.
    """
    expr_parts: list[str] = []
    for i in range(start, start + length):
        power = max_power - i
        ch = csd[i]
        if ch == "+":
            expr_parts.append(f"x_shift{power}")
        elif ch == "-":
            expr_parts.append(f"-x_shift{power}")
    if not expr_parts:
        return ""

    # Build signed expression: first term without sign prefix, rest with signs
    result = expr_parts[0]
    for part in expr_parts[1:]:
        if part.startswith("-"):
            result += " - " + part[1:]
        else:
            result += " + " + part
    return result


def _find_pattern_occurrences(csd: str, pattern: str) -> list[int]:
    """Find all non-overlapping positions of |pattern| in |csd|."""
    positions: list[int] = []
    pos = 0
    while True:
        pos = csd.find(pattern, pos)
        if pos == -1:
            break
        positions.append(pos)
        pos += len(pattern)
    return positions


def generate_csd_multiplier(csd: str, input_width: int, max_power: int) -> str:
    """
    Generate Verilog code for a CSD multiplier module with LCSRe optimization.

    When the CSD string contains repeated non-overlapping patterns (detected
    via the longest_repeated_substring algorithm), the generated Verilog
    factors out a shared sub-expression wire — reducing the number of adders.

    Args:
        csd: CSD string (e.g., "+00-00+0+")
        input_width: Bit width of the input signal x
        max_power: Highest power of two in the CSD (must be len(csd)-1)

    Returns:
        Verilog module code as a string

    Raises:
        ValueError: If csd length doesn't match max_power+1 or the string
                    contains characters other than '+', '-', '0'
    """
    # --- validation ---
    if len(csd) != max_power + 1:
        raise ValueError(
            f"CSD length {len(csd)} doesn't match max_power={max_power} "
            f"(should be max_power+1)"
        )
    if not all(ch in "+-0" for ch in csd):
        raise ValueError("CSD string can only contain '+', '-', or '0'")

    # Parse CSD and collect non-zero terms
    terms: list[tuple[int, str]] = []
    for index, ch in enumerate(csd):
        power = max_power - index
        if ch == "+":
            terms.append((power, "add"))
        elif ch == "-":
            terms.append((power, "sub"))

    output_width = input_width + max_power

    # --- module header ---
    verilog = f"""
module csd_multiplier (
    input signed [{input_width - 1}:0] x,      // Input value
    output signed [{output_width - 1}:0] result // Result of multiplication
);"""

    # --- wire declarations (deduplicated powers) ---
    if terms:
        verilog += "\n\n    // Create shifted versions of input"
        for p in sorted({p for p, _op in terms}, reverse=True):
            verilog += (
                f"\n    wire signed [{output_width - 1}:0] x_shift{p} = x <<< {p};"
            )

    # --- detect LCSRe optimization opportunity ---
    repeated = longest_repeated_substring(csd)
    use_opt = False
    pat_positions: list[int] = []
    if repeated and len(repeated) > 1:
        pat_nnz = repeated.count("+") + repeated.count("-")
        if pat_nnz >= 2:
            pat_positions = _find_pattern_occurrences(csd, repeated)
            use_opt = len(pat_positions) >= 2

    # --- combinational logic ---
    if not terms:
        verilog += "\n\n    // CSD implementation"
        verilog += "\n    assign result = 0;"
    elif use_opt:
        # --- LCSRe-optimized path: share repeated sub-expression ---
        base_pos = pat_positions[0]
        pat_expr = _build_range_expr(csd, base_pos, len(repeated), max_power)
        verilog += f'\n\n    // LCSRe: repeated pattern "{repeated}"'
        verilog += f"\n    wire signed [{output_width - 1}:0] _pat = {pat_expr};"

        # Build full expression from segments
        expr_parts: list[str] = []
        cur = 0
        for pos in pat_positions:
            # prefix/gap before this occurrence
            if pos > cur:
                gap_expr = _build_range_expr(csd, cur, pos - cur, max_power)
                if gap_expr:
                    expr_parts.append(gap_expr)

            # the pattern occurrence (shifted if not the first)
            shift = pos - base_pos
            if shift == 0:
                expr_parts.append("_pat")
            else:
                expr_parts.append(f"(_pat >>> {shift})")

            cur = pos + len(repeated)

        # suffix after the last occurrence
        if cur < len(csd):
            suffix_expr = _build_range_expr(csd, cur, len(csd) - cur, max_power)
            if suffix_expr:
                expr_parts.append(suffix_expr)

        # Join all parts with " + ", but handle leading minus terms correctly
        # (first part might start with "-" from a negative gap term)
        result_expr = " + ".join(expr_parts)
        verilog += "\n\n    // CSD implementation (LCSRe optimized)"
        verilog += f"\n    assign result = {result_expr};"
    else:
        # --- flat path (no repeated pattern) ---
        first_power, first_op = terms[0]
        if first_op == "sub":
            expr = f"-x_shift{first_power}"
        else:
            expr = f"x_shift{first_power}"

        for power, operation in terms[1:]:
            if operation == "add":
                expr += f" + x_shift{power}"
            else:
                expr += f" - x_shift{power}"

        verilog += "\n\n    // CSD implementation"
        verilog += f"\n    assign result = {expr};"

    verilog += "\nendmodule\n"
    return verilog


# ---------------------------------------------------------------------------
# Cross-CSE: multiple CSD multipliers sharing sub-expressions
# ---------------------------------------------------------------------------


def _find_cross_patterns(
    csd_list: list[str], min_nnz: int = 2
) -> dict[str, list[tuple[int, int]]]:
    """Find substrings (NNZ >= min_nnz) appearing in >= 2 CSD strings.

    Returns dict mapping pattern -> [(csd_idx, position), ...].
    """
    patterns: dict[str, list[tuple[int, int]]] = {}
    for ci, csd in enumerate(csd_list):
        n = len(csd)
        for i in range(n):
            for j in range(i + 2, n + 1):
                sub = csd[i:j]
                nnz = sub.count("+") + sub.count("-")
                if nnz >= min_nnz:
                    patterns.setdefault(sub, []).append((ci, i))
    # Keep only patterns crossing >= 2 different CSD strings
    return {
        sub: occ for sub, occ in patterns.items() if len({ci for ci, _ in occ}) >= 2
    }


def _build_coeff_expr(
    csd: str,
    max_power: int,
    pattern: Optional[str],
    base_pos: int,
    cse_name: str,
) -> str:
    """Build a single coefficient's expression, using shared CSE wire if applicable.

    The expression is: gap_terms + shifted_cse + gap_terms + ...
    """
    if pattern is None:
        # Flat expression (no CSE)
        return _build_range_expr(csd, 0, len(csd), max_power)

    parts: list[str] = []
    cur = 0
    positions = _find_pattern_occurrences(csd, pattern)
    for pos in positions:
        # gap before this occurrence
        if pos > cur:
            gap = _build_range_expr(csd, cur, pos - cur, max_power)
            if gap:
                parts.append(gap)
        # CSE reference
        shift = pos - base_pos
        if shift == 0:
            parts.append(cse_name)
        else:
            parts.append(f"({cse_name} >>> {shift})")
        cur = pos + len(pattern)
    # suffix
    if cur < len(csd):
        gap = _build_range_expr(csd, cur, len(csd) - cur, max_power)
        if gap:
            parts.append(gap)

    if not parts:
        return ""
    return " + ".join(parts)


def generate_csd_multipliers(
    coeffs: list[tuple[str, str, int, int]],
    module_name: str = "csd_filter",
) -> str:
    """Generate a Verilog module with multiple CSD multipliers and cross-CSE.

    When the same CSD substring appears in multiple coefficients, a shared
    sub-expression wire is created — reducing total adder count across the
    entire filter.

    All coefficients must share the same ``input_width`` and ``max_power``
    so that the same bit position encodes the same power of two across all
    multipliers.  If a coefficient is narrower, pad its CSD with leading
    ``'0'`` characters.

    Args:
        coeffs: List of (output_name, csd_str, input_width, max_power) tuples.
                All entries **must** share the same input_width and max_power.
        module_name: Name for the generated Verilog module.

    Returns:
        Verilog module code as a string
    """
    if not coeffs:
        raise ValueError("At least one coefficient is required")

    # --- validation & uniform width enforcement ---
    input_width = coeffs[0][2]
    max_power = coeffs[0][3]

    for name, csd, iw, mp in coeffs:
        if iw != input_width or mp != max_power:
            raise ValueError(
                "All coefficients must share the same input_width and max_power "
                f"for cross-CSE.  Got ({iw},{mp}) for '{name}', "
                f"expected ({input_width},{max_power}). "
                "Pad narrower CSDs with leading '0' characters."
            )
        if len(csd) != max_power + 1:
            raise ValueError(
                f"CSD '{csd}' length {len(csd)} doesn't match "
                f"max_power={max_power} for coefficient '{name}'"
            )
        if not all(ch in "+-0" for ch in csd):
            raise ValueError(
                f"CSD string '{csd}' for '{name}' can only contain '+', '-', or '0'"
            )

    output_width = input_width + max_power

    # --- collect all x_shift powers needed ---
    all_powers: set[int] = set()
    for _, csd, _, _ in coeffs:
        for idx, ch in enumerate(csd):
            if ch != "0":
                all_powers.add(max_power - idx)
    all_powers_sorted = sorted(all_powers, reverse=True)

    # --- find best cross-CSD pattern ---
    csd_strings = [csd for _, csd, _, _ in coeffs]
    cross = _find_cross_patterns(csd_strings)

    best_pattern: Optional[str] = None
    best_occurrences: list[tuple[int, int]] = []
    if cross:

        def _scores(item: tuple[str, list[tuple[int, int]]]) -> int:
            sub, occ = item
            nnz = sub.count("+") + sub.count("-")
            return (nnz - 1) * (len(occ) - 1)

        best_pattern, best_occurrences = max(cross.items(), key=_scores)

    # --- determine base position for the CSE wire ---
    cse_base_pos = 0
    if best_pattern and best_occurrences:
        cse_base_pos = min(pos for _, pos in best_occurrences)

    # --- build Verilog ---
    verilog = f"\nmodule {module_name} ("
    verilog += f"\n    input signed [{input_width - 1}:0] x,      // Input value"

    for name, _csd, _iw, _mp in coeffs:
        ow = _iw + _mp
        verilog += f"\n    output signed [{ow - 1}:0] {name}"

    verilog += "\n);"

    # x_shift wires (use output_width for all)
    if all_powers:
        verilog += "\n\n    // Create shifted versions of input"
        for p in all_powers_sorted:
            verilog += (
                f"\n    wire signed [{output_width - 1}:0] x_shift{p} = x <<< {p};"
            )

    cse_name = "_cse_0"
    if best_pattern:
        cse_expr = _build_range_expr(
            best_pattern, 0, len(best_pattern), max_power - cse_base_pos
        )
        verilog += f'\n\n    // Cross-CSE: shared pattern "{best_pattern}"'
        verilog += f"\n    wire signed [{output_width - 1}:0] {cse_name} = {cse_expr};"

    # Per-coefficient assignments
    for idx, (name, csd_str, _iw, _mp) in enumerate(coeffs):
        verilog += f"\n\n    // {name}: {csd_str}"
        ow = _iw + _mp

        if best_pattern and any(ci == idx for ci, _ in best_occurrences):
            expr = _build_coeff_expr(
                csd_str, max_power, best_pattern, cse_base_pos, cse_name
            )
        else:
            expr = _build_coeff_expr(csd_str, max_power, None, 0, "")

        if not expr:
            verilog += f"\n    wire signed [{ow - 1}:0] {name} = 0;"
        else:
            verilog += f"\n    wire signed [{ow - 1}:0] {name} = {expr};"

    verilog += "\nendmodule\n"
    return verilog


# Example usage
if __name__ == "__main__":
    # No repeated pattern
    print("=== +00-00+0 (no repeat) ===")
    print(generate_csd_multiplier("+00-00+0", 8, 7))

    # Repeated pattern "+0-0" — optimized with _pat wire
    print("=== +0-0+0-0 (repeat: +0-0) ===")
    print(generate_csd_multiplier("+0-0+0-0", 8, 7))

    # Triple repeat
    print("=== +0-0+0-0+0-0 (triple repeat) ===")
    print(generate_csd_multiplier("+0-0+0-0+0-0", 8, 11))

    # Longer pattern
    print("=== +00-00+00-00 (repeat: +00-00) ===")
    print(generate_csd_multiplier("+00-00+00-00", 8, 11))

    # All zeros
    print("=== 000 (all zeros) ===")
    print(generate_csd_multiplier("000", 8, 2))

    # Leading minus — also has sign fix
    print("=== -0- (no repeat benefit) ===")
    print(generate_csd_multiplier("-0-", 8, 2))

    # --- Cross-CSE demo ---
    print("\n===== Cross-CSE Demo =====")
    verilog = generate_csd_multipliers(
        [
            ("h0", "+0-0+0-0", 8, 7),
            ("h1", "+0-0+0-0+0-0", 8, 11),
            ("h2", "+00-00+00-00", 8, 11),
            ("h3", "-0+0-0+", 8, 5),
        ],
        module_name="fir_taps",
    )
    print(verilog)
