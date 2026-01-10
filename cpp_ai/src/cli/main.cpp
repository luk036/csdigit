//! @file main.cpp
//! @brief CSDigit CLI application

#include "csdigit/csdigit.hpp"
#include <iostream>
#include <string>
#include <cstdlib>
#include <cstring>

void print_help() {
    std::cout << "CSDigit CLI - Canonical Signed Digit Conversion Tool\n\n";
    std::cout << "Usage:\n";
    std::cout << "  csdigit to-csd <decimal> [--places <n>]    Convert decimal to CSD\n";
    std::cout << "  csdigit to-csdnnz <decimal> [--nnz <n>]    Convert decimal to CSD with non-zero limit\n";
    std::cout << "  csdigit to-decimal <csd_string>            Convert CSD string to decimal\n";
    std::cout << "  csdigit --help                             Show this help message\n";
    std::cout << "  csdigit --version                          Show version information\n\n";
    std::cout << "Options:\n";
    std::cout << "  --places <n>    Number of decimal places (default: 4)\n";
    std::cout << "  --nnz <n>       Maximum non-zero digits (default: 4)\n";
    std::cout << "  -v, --verbose   Verbose output\n";
}

void print_version() {
    std::cout << "CSDigit CLI version 0.1.0\n";
    std::cout << "Copyright (c) 2025 Wai-Shing Luk\n";
    std::cout << "MIT License\n";
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        print_help();
        return 1;
    }

    std::string command = argv[1];

    if (command == "--help" || command == "-h") {
        print_help();
        return 0;
    }

    if (command == "--version" || command == "-v") {
        print_version();
        return 0;
    }

    if (command == "to-csd") {
        if (argc < 3) {
            std::cerr << "Error: Missing decimal value\n";
            return 1;
        }

        double decimal = std::stod(argv[2]);
        int places = 4;

        // Parse optional --places argument
        for (int i = 3; i < argc; ++i) {
            if (strcmp(argv[i], "--places") == 0 && i + 1 < argc) {
                places = std::stoi(argv[i + 1]);
                break;
            }
        }

        try {
            std::string result = csdigit::to_csd(decimal, places);
            std::cout << result << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            return 1;
        }

    } else if (command == "to-csdnnz") {
        if (argc < 3) {
            std::cerr << "Error: Missing decimal value\n";
            return 1;
        }

        double decimal = std::stod(argv[2]);
        int nnz = 4;

        // Parse optional --nnz argument
        for (int i = 3; i < argc; ++i) {
            if (strcmp(argv[i], "--nnz") == 0 && i + 1 < argc) {
                nnz = std::stoi(argv[i + 1]);
                break;
            }
        }

        try {
            std::string result = csdigit::to_csdnnz(decimal, nnz);
            std::cout << result << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            return 1;
        }

    } else if (command == "to-decimal") {
        if (argc < 3) {
            std::cerr << "Error: Missing CSD string\n";
            return 1;
        }

        std::string csd_str = argv[2];

        try {
            double result = csdigit::to_decimal(csd_str);
            std::cout << result << std::endl;
        } catch (const std::exception& e) {
            std::cerr << "Error: " << e.what() << std::endl;
            return 1;
        }

    } else {
        std::cerr << "Error: Unknown command '" << command << "'\n";
        print_help();
        return 1;
    }

    return 0;
}
