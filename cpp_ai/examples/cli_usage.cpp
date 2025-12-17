//! @file cli_usage.cpp
//! @brief CLI usage examples for CSDigit library

#include <iostream>

int main() {
    std::cout << "=== CSDigit CLI Usage Examples ===\n\n";
    
    std::cout << "The CSDigit CLI provides the following commands:\n\n";
    
    std::cout << "1. Convert decimal to CSD:\n";
    std::cout << "   csdigit_cli to-csd 28.5 --places 2\n";
    std::cout << "   Output: +00-00.+0\n\n";
    
    std::cout << "2. Convert decimal to CSD with non-zero limit:\n";
    std::cout << "   csdigit_cli to-csdnnz 28.5 --nnz 4\n";
    std::cout << "   Output: +00-00.+\n\n";
    
    std::cout << "3. Convert CSD string to decimal:\n";
    std::cout << "   csdigit_cli to-decimal \"+00-00.+\"\n";
    std::cout << "   Output: 28.5\n\n";
    
    std::cout << "4. Help information:\n";
    std::cout << "   csdigit_cli --help\n";
    std::cout << "   csdigit_cli to-csd --help\n\n";
    
    std::cout << "Common options:\n";
    std::cout << "   --places <INT>    Number of decimal places (default: 4)\n";
    std::cout << "   --nnz <INT>       Maximum non-zero digits (default: 4)\n";
    std::cout << "   --help            Show help information\n";
    std::cout << "   --version         Show version information\n\n";
    
    std::cout << "=== CLI Examples Complete ===\n";
    return 0;
}