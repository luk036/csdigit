def generate_csd_multiplier(csd, N, M):
    """
    Generate Verilog code for a CSD multiplier module with proper signed handling.

    Args:
        csd (str): CSD string (e.g., "+00-00+0+")
        N (int): Input bit width
        M (int): Highest power in CSD (must be len(csd)-1)

    Returns:
        str: Verilog module code
    """
    # Validate inputs
    if len(csd) != M + 1:
        raise ValueError(f"CSD length {len(csd)} doesn't match M={M} (should be M+1)")

    if not all(c in "+-0" for c in csd):
        raise ValueError("CSD string can only contain '+', '-', or '0'")

    # Parse CSD and collect non-zero terms
    terms = []
    for i, c in enumerate(csd):
        power = M - i  # Most significant digit is highest power
        if c == "+":
            terms.append((power, "+"))
        elif c == "-":
            terms.append((power, "-"))

    # Generate module header
    verilog_code = f"""
// CSD Multiplier for pattern: {csd} (value: {sum((1 if c == '+' else -1 if c == '-' else 0) * 2**(M-i) for i, c in enumerate(csd))})
module csd_multiplier (
    input signed [{N-1}:0] x,      // Input value (signed)
    output signed [{N+M-1}:0] result // Result (signed)
);"""

    # Generate shifted versions
    if terms:
        verilog_code += (
            "\n\n    // Signed shifted versions (Verilog handles sign extension)"
        )
        powers_needed = {p for p, op in terms}
        for p in sorted(powers_needed, reverse=True):
            verilog_code += f"\n    wire signed [{N+M-1}:0] x_shift{p} = $signed({{ {{{M-p}{{x[{N-1}]}}}}, x }}) << {p};"

    # Generate the computation
    verilog_code += "\n\n    // CSD implementation with signed arithmetic"
    if not terms:
        verilog_code += "\n    assign result = 0;"
    else:
        first_power, first_op = terms[0]
        expr = f"{first_op}x_shift{first_power}".replace("+", "")  # Remove unary +

        for power, op in terms[1:]:
            expr += f" {op} x_shift{power}"

        verilog_code += f"\n    assign result = {expr};"

    verilog_code += "\nendmodule\n"
    return verilog_code


# Example usage
if __name__ == "__main__":
    csd = "+00-00+"  # Represents 57
    N = 8  # Input bit width
    M = 6  # Highest power (2^6 for this CSD)

    verilog_code = generate_csd_multiplier(csd, N, M)
    print(verilog_code)
