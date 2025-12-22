def generate_csd_multiplier(csd: str, input_width: int, max_power: int) -> str:
    """
    Generate Verilog code for a CSD multiplier module with proper signed handling.

    Args:
        csd (str): CSD string (e.g., "+00-00+0+")
        input_width (int): Input bit width
        max_power (int): Highest power in CSD (must be len(csd)-1)

    Returns:
        str: Verilog module code
    """
    # Validate inputs
    if len(csd) != max_power + 1:
        raise ValueError(
            f"CSD length {len(csd)} doesn't match max_power={max_power} (should be max_power+1)"
        )

    if not all(csd_char in "+-0" for csd_char in csd):
        raise ValueError("CSD string can only contain '+', '-', or '0'")

    # Parse CSD and collect non-zero terms
    terms = []
    for index, csd_char in enumerate(csd):
        power = max_power - index  # Most significant digit is highest power
        if csd_char == "+":
            terms.append((power, "add"))
        elif csd_char == "-":
            terms.append((power, "sub"))

    # Generate module header
    verilog_code = f"""
module csd_multiplier (
    input signed [{input_width - 1}:0] x,      // Input value
    output signed [{input_width + max_power - 1}:0] result // Result of multiplication
);"""

    # Generate shifted versions
    if len(terms) > 0:
        verilog_code += "\n\n    // Create shifted versions of input"
        powers_needed = {p for p, operation in terms}
        for p in sorted(powers_needed, reverse=True):
            verilog_code += f"\n    wire signed [{input_width + max_power - 1}:0] x_shift{p} = x <<< {p};"

    # Generate the computation
    verilog_code += "\n\n    // CSD implementation"
    if not terms:
        verilog_code += "\n    assign result = 0;"
    else:
        first_power, first_op = terms[0]
        expr = f"x_shift{first_power}"

        for power, operation in terms[1:]:
            if operation == "add":
                expr += f" + x_shift{power}"
            else:
                expr += f" - x_shift{power}"

        verilog_code += f"\n    assign result = {expr};"

    verilog_code += "\nendmodule\n"
    return verilog_code


# Example usage
if __name__ == "__main__":
    csd = "+00-00+0"  # Represents 114
    input_width = 8  # Input bit width
    max_power = 7  # Highest power (2^7 for this CSD)

    verilog_code = generate_csd_multiplier(csd, input_width, max_power)
    print(verilog_code)
