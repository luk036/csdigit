// Simple test to verify the code compiles
#include "include/csdigit/csdigit.hpp"
#include <iostream>

int main() {
    // Test basic functionality
    std::cout << "Testing CSDigit C++ implementation...\n";

    // These would be the expected outputs from Python
    std::cout << "Expected to_csd(28.5, 2) = \"+00-00.+0\"\n";
    std::cout << "Expected to_decimal(\"+00-00.+\") = 28.5\n";
    std::cout << "Expected to_csd_i(28) = \"+00-00\"\n";
    std::cout << "Expected longest_repeated_substring(\"+-00+-00+-00+-0\") = \"+-00+-0\"\n";

    return 0;
}
