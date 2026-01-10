//! CLI usage examples for the CSDigit library

fn main() {
    println!("=== CSDigit CLI Usage Examples ===\n");

    println!("The CSDigit CLI provides the following commands:\n");

    println!("1. Convert decimal to CSD:");
    println!("   csdigit to-csd 28.5 --places 2");
    println!("   Output: +00-00.+0\n");

    println!("2. Convert decimal to CSD with non-zero limit:");
    println!("   csdigit to-csdnnz 28.5 --nnz 4");
    println!("   Output: +00-00.+\n");

    println!("3. Convert CSD string to decimal:");
    println!("   csdigit to-decimal \"+00-00.+\"");
    println!("   Output: 28.5\n");

    println!("4. Verbose output:");
    println!("   csdigit to-csd 28.5 -vv");
    println!("   (Shows debug information)\n");

    println!("5. Help information:");
    println!("   csdigit --help");
    println!("   csdigit to-csd --help\n");

    println!("Common options:");
    println!("   -p, --places <INT>    Number of decimal places (default: 4)");
    println!("   -z, --nnz <INT>       Maximum non-zero digits (default: 4)");
    println!("   -v                    Verbose output (can use -v, -vv, -vvv)");
    println!("   --help                Show help information");
    println!("   --version             Show version information\n");

    println!("=== CLI Examples Complete ===");
}
