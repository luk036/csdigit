//! Basic usage examples for the CSDigit library

use csdigit::*;

fn main() {
    println!("=== CSDigit Basic Usage Examples ===\n");

    // Example 1: Convert decimal to CSD
    println!("1. Decimal to CSD conversion:");
    let csd1 = to_csd(28.5, 2);
    println!("   to_csd(28.5, 2) = {}", csd1);

    let csd2 = to_csd(-0.5, 2);
    println!("   to_csd(-0.5, 2) = {}", csd2);

    let csd3 = to_csd(0.0, 2);
    println!("   to_csd(0.0, 2) = {}", csd3);

    // Example 2: Convert CSD to decimal
    println!("\n2. CSD to decimal conversion:");
    let dec1 = to_decimal("+00-00.+");
    println!("   to_decimal(\"+00-00.+\") = {}", dec1);

    let dec2 = to_decimal("0.-");
    println!("   to_decimal(\"0.-\") = {}", dec2);

    let dec3 = to_decimal("0.+");
    println!("   to_decimal(\"0.+\") = {}", dec3);

    // Example 3: Integer to CSD
    println!("\n3. Integer to CSD conversion:");
    let csd_int1 = to_csd_i(28);
    println!("   to_csd_i(28) = {}", csd_int1);

    let csd_int2 = to_csd_i(-15);
    println!("   to_csd_i(-15) = {}", csd_int2);

    // Example 4: CSD with non-zero limit
    println!("\n4. CSD with non-zero digit limit:");
    let csd_nnz1 = to_csdnnz(28.5, 4);
    println!("   to_csdnnz(28.5, 4) = {}", csd_nnz1);

    let csd_nnz2 = to_csdnnz_i(37, 2);
    println!("   to_csdnnz_i(37, 2) = {}", csd_nnz2);

    // Example 5: Longest repeated substring
    println!("\n5. Longest repeated substring:");
    let lrs = longest_repeated_substring("+-00+-00+-00+-0");
    println!("   longest_repeated_substring(\"+-00+-00+-00+-0\") = {}", lrs);

    // Example 6: Verilog multiplier generation
    println!("\n6. Verilog multiplier generation:");
    let verilog = generate_csd_multiplier("+00-00+0", 8, 7);
    println!("   generate_csd_multiplier(\"+00-00+0\", 8, 7):");
    println!("{}", verilog);

    println!("\n=== Examples Complete ===");
}
