# CSDigit - Canonical Signed Digit Conversion in Rust

A Rust implementation of the CSDigit library for converting between decimal numbers and Canonical Signed Digit (CSD) representation.

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

## Installation

Add this to your `Cargo.toml`:

```toml
[dependencies]
csdigit = "0.1"
```

Or install the CLI tool:

```bash
cargo install csdigit
```

## Usage

### As a Library

```rust
use csdigit::*;

// Convert decimal to CSD
let csd = to_csd(28.5, 2);
assert_eq!(csd, "+00-00.+0");

// Convert CSD to decimal
let decimal = to_decimal("+00-00.+");
assert_eq!(decimal, 28.5);

// Convert integer to CSD
let csd_int = to_csd_i(28);
assert_eq!(csd_int, "+00-00");

// Convert with non-zero limit
let csd_nnz = to_csdnnz(28.5, 4);
assert_eq!(csd_nnz, "+00-00.+");

// Find longest repeated substring
let lrs = longest_repeated_substring("+-00+-00+-00+-0");
assert_eq!(lrs, "+-00+-0");

// Generate Verilog multiplier
let verilog = generate_csd_multiplier("+00-00+0", 8, 7);
println!("{}", verilog);
```

### Command Line Interface

```bash
# Convert decimal to CSD
csdigit to-csd 28.5 --places 2

# Convert decimal to CSD with non-zero limit
csdigit to-csdnnz 28.5 --nnz 4

# Convert CSD to decimal
csdigit to-decimal "+00-00.+"

# Verbose output
csdigit to-csd 28.5 -vv
```

## API Reference

### Core Functions

- `to_csd(decimal_value: f64, places: i32) -> String`
- `to_csd_i(decimal_value: i32) -> String`
- `to_decimal(csd: &str) -> f64`
- `to_csdnnz(decimal_value: f64, nnz: i32) -> String`
- `to_csdnnz_i(decimal_value: i32, nnz: i32) -> String`
- `longest_repeated_substring(cs: &str) -> String`
- `generate_csd_multiplier(csd: &str, n: usize, m: usize) -> String`

## Examples

See the `examples/` directory for more usage examples.

## Testing

Run the test suite:

```bash
cargo test
```

Run tests with verbose output:

```bash
cargo test -- --nocapture
```

## Building

Build the library:

```bash
cargo build
```

Build with optimizations:

```bash
cargo build --release
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Original Python implementation by Harnesser (https://sourceforge.net/projects/pycsd/)
Rust port by Wai-Shing Luk (luk036@gmail.com)