# CSDigit - Canonical Signed Digit Conversion in C++17

A C++17 implementation of the CSDigit library for converting between decimal numbers and Canonical Signed Digit (CSD) representation.

## Overview

CSD is a special signed-digit representation where each digit is limited to -1, 0, or 1, and consecutive non-zero digits are not allowed. This representation is particularly useful in digital signal processing applications such as filter design, as it enables efficient arithmetic operations using simple adders and subtractors.

## Features

- Convert decimal numbers to CSD representation
- Convert CSD strings back to decimal numbers
- Support for both floating-point and integer conversions
- Non-zero digit limit for CSD conversions
- Longest repeated substring finding algorithm
- Verilog code generation for CSD multipliers
- Command-line interface
- Comprehensive doctest test suite
- CMake and xmake build system support

## Build Systems

### CMake
```bash
mkdir build && cd build
cmake ..
cmake --build .
```

### xmake
```bash
xmake
xmake build
```

## Usage

### As a Library

```cpp
#include "csdigit/csdigit.hpp"
#include <iostream>

int main() {
    // Convert decimal to CSD
    std::string csd = csdigit::to_csd(28.5, 2);
    std::cout << csd << std::endl;  // Output: "+00-00.+0"
    
    // Convert CSD to decimal
    double decimal = csdigit::to_decimal("+00-00.+");
    std::cout << decimal << std::endl;  // Output: 28.5
    
    // Convert integer to CSD
    std::string csd_int = csdigit::to_csd_i(28);
    std::cout << csd_int << std::endl;  // Output: "+00-00"
    
    return 0;
}
```

### Command Line Interface

```bash
# Convert decimal to CSD
./csdigit_cli to-csd 28.5 --places 2

# Convert decimal to CSD with non-zero limit
./csdigit_cli to-csdnnz 28.5 --nnz 4

# Convert CSD to decimal
./csdigit_cli to-decimal "+00-00.+"

# Show help
./csdigit_cli --help
```

## API Reference

### Core Functions

- `std::string to_csd(double decimal_value, int places)`
- `std::string to_csd_i(int32_t decimal_value)`
- `double to_decimal(const std::string& csd)`
- `std::string to_csdnnz(double decimal_value, int nnz)`
- `std::string to_csdnnz_i(int32_t decimal_value, int nnz)`
- `std::string longest_repeated_substring(const std::string& cs)`
- `std::string generate_csd_multiplier(const std::string& csd, size_t n, size_t m)`

## Testing

Run the test suite:

```bash
# With CMake
cd build && ctest

# With xmake
xmake run csdigit_tests
```

## Examples

See the `examples/` directory for more usage examples.

## Building

### CMake
```bash
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build . --config Release
```

### xmake
```bash
xmake config --mode=release
xmake build
```

## Dependencies

- C++17 compiler
- doctest (for testing, automatically fetched by CMake)

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Original Python implementation by Harnesser (https://sourceforge.net/projects/pycsd/)
C++ port by Wai-Shing Luk (luk036@gmail.com)