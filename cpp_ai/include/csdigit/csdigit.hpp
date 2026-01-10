//! @file csdigit.hpp
//! @brief Canonical Signed Digit (CSD) Conversion Library for C++17
//!
//! This library provides functions for converting between decimal numbers and Canonical Signed Digit (CSD) representation.
//! CSD is a special signed-digit representation where each digit is limited to -1, 0, or 1, and consecutive non-zero digits are not allowed.
//! This representation is particularly useful in digital signal processing applications such as filter design,
//! as it enables efficient arithmetic operations using simple adders and subtractors.
//!
//! @author Wai-Shing Luk (luk036@gmail.com)
//! @date 2025
//! @license MIT

#ifndef CSDIGIT_HPP
#define CSDIGIT_HPP

#include <string>
#include <cmath>
#include <cstdint>
#include <vector>
#include <stdexcept>

namespace csdigit {

//! Convert a decimal number to CSD representation with specified decimal places.
//!
//! @param decimal_value The decimal value to convert
//! @param places Number of decimal places in the CSD representation
//! @return CSD string representation
//!
//! @example
//! @code
//! auto csd = to_csd(28.5, 2);  // Returns "+00-00.+0"
//! @endcode
std::string to_csd(double decimal_value, int places);

//! Convert an integer to CSD representation.
//!
//! @param decimal_value The integer value to convert
//! @return CSD string representation
//!
//! @example
//! @code
//! auto csd = to_csd_i(28);  // Returns "+00-00"
//! @endcode
std::string to_csd_i(int32_t decimal_value);

//! Convert a CSD string to a decimal number.
//!
//! @param csd The CSD string to convert
//! @return Decimal value
//!
//! @example
//! @code
//! auto decimal = to_decimal("+00-00.+");  // Returns 28.5
//! @endcode
double to_decimal(const std::string& csd);

//! Convert a decimal number to CSD representation with a maximum number of non-zero digits.
//!
//! @param decimal_value The decimal value to convert
//! @param nnz Maximum number of non-zero digits allowed in the CSD representation
//! @return CSD string representation
//!
//! @example
//! @code
//! auto csd = to_csdnnz(28.5, 4);  // Returns "+00-00.+"
//! @endcode
std::string to_csdnnz(double decimal_value, int nnz);

//! Convert an integer to CSD representation with a maximum number of non-zero digits.
//!
//! @param decimal_value The integer value to convert
//! @param nnz Maximum number of non-zero digits allowed in the CSD representation
//! @return CSD string representation
//!
//! @example
//! @code
//! auto csd = to_csdnnz_i(28, 4);  // Returns "+00-00"
//! @endcode
std::string to_csdnnz_i(int32_t decimal_value, int nnz);

//! Find the longest repeated non-overlapping substring in a string.
//!
//! @param cs The input string
//! @return Longest repeated substring
//!
//! @example
//! @code
//! auto lrs = longest_repeated_substring("+-00+-00+-00+-0");  // Returns "+-00+-0"
//! @endcode
std::string longest_repeated_substring(const std::string& cs);

//! Generate Verilog code for a CSD multiplier module with proper signed handling.
//!
//! @param csd CSD string (e.g., "+00-00+0+")
//! @param n Input bit width
//! @param m Highest power in CSD (must be len(csd)-1)
//! @return Verilog module code
//!
//! @example
//! @code
//! auto verilog = generate_csd_multiplier("+00-00+0", 8, 7);
//! @endcode
std::string generate_csd_multiplier(const std::string& csd, size_t n, size_t m);

} // namespace csdigit

#endif // CSDIGIT_HPP
