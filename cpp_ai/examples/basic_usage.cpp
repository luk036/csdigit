//! @file basic_usage.cpp
//! @brief Basic usage examples for CSDigit library

#include "csdigit/csdigit.hpp"
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "=== CSDigit Basic Usage Examples ===\n\n";

    // Example 1: Convert decimal to CSD
    std::cout << "1. Decimal to CSD conversion:\n";
    std::string csd1 = csdigit::to_csd(28.5, 2);
    std::cout << "   to_csd(28.5, 2) = " << csd1 << "\n";

    std::string csd2 = csdigit::to_csd(-0.5, 2);
    std::cout << "   to_csd(-0.5, 2) = " << csd2 << "\n";

    std::string csd3 = csdigit::to_csd(0.0, 2);
    std::cout << "   to_csd(0.0, 2) = " << csd3 << "\n";

    // Example 2: Convert CSD to decimal
    std::cout << "\n2. CSD to decimal conversion:\n";
    double dec1 = csdigit::to_decimal("+00-00.+");
    std::cout << "   to_decimal(\"+00-00.+\") = " << std::setprecision(10) << dec1 << "\n";

    double dec2 = csdigit::to_decimal("0.-");
    std::cout << "   to_decimal(\"0.-\") = " << dec2 << "\n";

    double dec3 = csdigit::to_decimal("0.+");
    std::cout << "   to_decimal(\"0.+\") = " << dec3 << "\n";

    // Example 3: Integer to CSD
    std::cout << "\n3. Integer to CSD conversion:\n";
    std::string csd_int1 = csdigit::to_csd_i(28);
    std::cout << "   to_csd_i(28) = " << csd_int1 << "\n";

    std::string csd_int2 = csdigit::to_csd_i(-15);
    std::cout << "   to_csd_i(-15) = " << csd_int2 << "\n";

    // Example 4: CSD with non-zero limit
    std::cout << "\n4. CSD with non-zero digit limit:\n";
    std::string csd_nnz1 = csdigit::to_csdnnz(28.5, 4);
    std::cout << "   to_csdnnz(28.5, 4) = " << csd_nnz1 << "\n";

    std::string csd_nnz2 = csdigit::to_csdnnz_i(37, 2);
    std::cout << "   to_csdnnz_i(37, 2) = " << csd_nnz2 << "\n";

    // Example 5: Longest repeated substring
    std::cout << "\n5. Longest repeated substring:\n";
    std::string lrs = csdigit::longest_repeated_substring("+-00+-00+-00+-0");
    std::cout << "   longest_repeated_substring(\"+-00+-00+-00+-0\") = " << lrs << "\n";

    // Example 6: Verilog multiplier generation
    std::cout << "\n6. Verilog multiplier generation:\n";
    std::string verilog = csdigit::generate_csd_multiplier("+00-00+0", 8, 7);
    std::cout << "   generate_csd_multiplier(\"+00-00+0\", 8, 7):\n";
    std::cout << verilog << "\n";

    std::cout << "\n=== Examples Complete ===\n";
    return 0;
}
