# Algorithmic Comparison: csdigit (Python) vs csd-cpp (C++) vs csd-rs (Rust)

> **Date**: 2026-07-05
> **Scope**: Core CSD conversion algorithms, LCSRe, CSD multiplier generation
> **Origin**: All three projects trace to the same Harnesser/ita_c source (GPL2)

---

## Table of Contents

1. [Scope and Structure](#1-scope-and-structure)
2. [Core CSD Conversion — `to_csd` (float → CSD)](#2-core-csd-conversion--to_csd-float--csd)
3. [Integer CSD — `to_csd_i` (int → CSD)](#3-integer-csd--to_csd_i-int--csd)
4. [Limited Non-Zero Digits — `to_csdnnz` / `to_csdnnz_i`](#4-limited-non-zero-digits--to_csdnnz--to_csdnnz_i)
5. [Decimal Conversion — `to_decimal`](#5-decimal-conversion--to_decimal)
6. [LCSRe — Longest Repeated Substring](#6-lcsre--longest-repeated-substring)
7. [CSD Multiplier Verilog Generation](#7-csd-multiplier-verilog-generation)
8. [Error Handling](#8-error-handling)
9. [Integer Width Support](#9-integer-width-support)
10. [API Design Patterns](#10-api-design-patterns)
11. [Performance & Memory](#11-performance--memory)
12. [Testing](#12-testing)
13. [Complete Difference Matrix](#13-complete-difference-matrix)
14. [Summary](#14-summary)

---

## 1. Scope and Structure

All three libraries implement the same domain-specific algorithms for **Canonical Signed Digit (CSD)** representation, where each digit is constrained to `-1`, `0`, or `+1` (`-`, `0`, `+`) and no two consecutive digits are non-zero.

### Module Layout

| Component | Python (`csdigit`) | C++ (`csd-cpp`) | Rust (`csd-rs`) |
|---|---|---|---|
| CSD conversion | `src/csdigit/csd.py` | `source/csd.cpp` + `include/csd/csd.hpp` | `src/csd.rs` |
| LCSRe | `src/csdigit/lcsre.py` | `source/lcsre.cpp` + `include/csd/lcsre.hpp` | `src/lcsre.rs` |
| CSD multiplier | `src/csdigit/csd_multiplier.py` | `source/csd_multiplier.cpp` + `include/csd/csd_multiplier.hpp` | `src/csd_multiplier.rs` |
| Library root | `__init__.py` | CMake target | `lib.rs` |
| CLI | `cli.py` | `standalone/` | `main.rs` |

All three share the same function suite: `to_csd`, `to_csd_i`, `to_decimal`, `to_csdnnz`, `to_csdnnz_i`, `generate_csd_multiplier`, `generate_csd_multipliers`, `longest_repeated_substring`.

**Rust feature flags**: The `multiplier` and `lcsre` modules are gated behind Cargo feature flags (both enabled by default). Python and C++ have no equivalent conditional compilation.

---

## 2. Core CSD Conversion — `to_csd` (float → CSD)

### Algorithm (common to all three)

```
1. If value == 0, return "0." + "0"*places
2. Compute starting bit position from abs(value) * 1.5
3. For each bit position (high to low):
     det = 1.5 * value
     if det >  p2n → emit '+', value -= p2n
     if det < -p2n → emit '-', value += p2n
     else          → emit '0'
     p2n /= 2
4. Insert '.' between integer and fractional parts
```

### Starting Power Computation — **The only algorithmic divergence**

| Language | Method | Code |
|---|---|---|
| **Python** | `frexp()` + mantissa check | `mant, exp = frexp(abs_val * 1.5)` then `exp-1` if `mant == 0.5` |
| **C++** | `frexp()` + mantissa check | Same as Python |
| **Rust** | `log2().ceil()` | `(absnum * 1.5).log2().ceil() as i32` |

Rust uses a direct floating-point logarithm instead of `frexp`. Mathematically equivalent but a genuinely different computation path. The `frexp` approach decomposes the number into mantissa and exponent directly from the IEEE 754 representation; `log2().ceil()` goes through the FPU logarithm unit.

**Why no `frexp()` in Rust?** The Rust standard library simply does not provide an `frexp()` function — it's not in `std` or `core`. (Unlike C++ with `<cmath>` and Python with `math.frexp()`.) The closest Rust alternative would be extracting the exponent manually via `f64::to_bits()` → mask/shift, but that's more involved than the clean `log2().ceil()` path. Notably, the `log2()` approach **eliminates the mantissa-is-0.5 special case** that both Python and C++ require:

```python
# Python/C++ need this odd branch:
mant, exp = frexp(abs_val * 1.5)
if mant == 0.5:
    remainder = exp - 1
else:
    remainder = exp
```

```rust
// Rust just does this — no branch needed:
let rem = (absnum * 1.5).log2().ceil() as i32;
```

So the absence of `frexp()` in Rust isn't a deficiency — it produced cleaner code through a mathematically different (but equivalent) path.

### Loop Structure

| Language | Integer part | Fractional part | Control flow |
|---|---|---|---|
| Python | `for _ in range(remainder)` | `for _ in range(places)` | Two explicit loops |
| C++ | `loop_fn(0)` | `loop_fn(-places)` | Lambda called twice |
| Rust | `while rem > 0` | `while frac_places > 0` | Two while loops |

Algorithmically identical — just different syntactic sugar. C++'s lambda is a DRY refactor of Python's two loops; Rust is explicit like Python but uses `while`.

### Zero Handling

| Detail | Python | C++ | Rust |
|---|---|---|---|
| Zero output (places>0) | `"0." + "0"*places` | `"0." + "0"*places` | `"0." + "0"*places` |
| Zero output (places=0) | `"0."` | `"0."` | `"0."` |

Identical.

---

## 3. Integer CSD — `to_csd_i` (int → CSD)

### Starting Power — **Divergent**

| Language | Method | Example for v=28 |
|---|---|---|
| **Python** | `(abs(v) * 3 // 2).bit_length()` | `(28*3//2=42).bit_length()=6` → start at 2⁶ |
| **C++** | `highest_power_of_two_in(abs(v)*3/2) * 2` | `hp2(42)=32, *2=64` → start at 64 = 2⁶ |
| **Rust** | Same as C++: `highest_power_of_two_in(...) * 2` | Same as C++ |

The Python `bit_length()` method computes `⌊log₂(n)⌋ + 1` directly as a CPU instruction. The C++/Rust `highest_power_of_two_in` is a classic bit-twiddle:

```c
x |= x >> 1;  x |= x >> 2;  x |= x >> 4;
x |= x >> 8;  x |= x >> 16;
return x ^ (x >> 1);
```

Both converge to the same value. The Rust version is additionally declared `pub const fn`, enabling compile-time evaluation.

### Loop Body

All three use the same integer-optimized determinant:
```
det = 3 * decimal_value
compare det with ±p2n  (where p2n is 2× the highest power of 2)
```

Python: `determinant = 3 * decimal_value; if determinant > power_of_two`
C++: `auto const det = 3 * decimal_value; if (det > p2n)`
Rust: `let det = 3 * decimal_value; if det > p2n`

Identical.

---

## 4. Limited Non-Zero Digits — `to_csdnnz` / `to_csdnnz_i`

### Termination Strategy — **Three different mechanisms**

| Language | Mechanism | Effect |
|---|---|---|
| **Python** | Checks `nnz > 0` in each `if` branch, decrements `nnz` on non-zero, continues emitting `'0'` for remaining bits | Iterates all positions |
| **C++** | Sets `decimal_value = 0` / `0.0` when `nnz == 0`, causing the outer loop condition to fail | May exit early |
| **Rust** | Checks `nnz > 0` per branch, then `if nnz == 0 && rem < 0 { break; }` | Hybrid: breaks after integer bits done |

**Same output**, different internal control flow:

- **Python**: most explicit — keeps looping to fill `'0'` at every remaining position
- **C++**: most aggressive — zeroes the value so the outer `while` condition collapses
- **Rust**: middle ground — breaks only after integer bits are processed, using `rem < 0` as the guard

### Integer NNZ — Rust has dedicated variants

Python and C++ each have one `to_csdnnz_i` that works on `int` (Python) or `int` (C++ i32). **Rust has three**:

| Rust function | Underlying implementation |
|---|---|
| `to_csdnnz_i(i32, u32)` | Delegates to `to_csdnnz(decimal_value as f64, nnz)` |
| `to_csdnnz_i64(i64, u32)` | **Dedicated** integer loop with tail-zero padding |
| `to_csdnnz_i128(i128, u32)` | **Dedicated** integer loop with tail-zero padding |

The `i64`/`i128` versions have a unique feature not present in any other variant: when `nnz` is exhausted, they fill remaining positions with `'0'` via a secondary `while p2n > 1 { csd.push('0'); p2n >>= 1; }` loop, guaranteeing a fixed-length output.

---

## 5. Decimal Conversion — `to_decimal`

### Algorithm (common to all)

```
Integral part:  result = 0; for each digit d: result = result * 2 + (d)
Fractional part: scale = 0.5; for each digit d: result += scale * (d); scale /= 2
```

### Variant Count — **Rust dominates**

| Variant | Python | C++ | Rust |
|---|---|---|---|
| `to_decimal(str) → f64` | ✓ | ✓ | ✓ |
| `to_decimal_i(str) → i32/i64/i128` | ✗ | ✓ (i32) | ✓ (i32 + i64 + i128) |
| `to_decimal_using_pow` | ✓ (deprecated) | ✗ | ✗ |
| `to_decimal_using_switch` | ✗ | ✓ | ✗ |
| `to_decimal_safe` → `Result` | ✗ | ✗ | ✓ (validates consec. non-zero) |
| `to_decimal_result` → `Result` | ✗ | ✗ | ✓ (pre-validates characters) |
| `to_decimal_i_safe` → `Result` | ✗ | ✗ | ✓ |
| `to_decimal_i_result` → `Result` | ✗ | ✗ | ✓ |
| `to_decimal_i64` / `i64_result` | ✗ | ✗ | ✓ |
| `to_decimal_i128` / `i128_result` | ✗ | ✗ | ✓ |
| `to_decimal_integral_safe` | ✗ | ✗ | ✓ |
| `to_decimal_fractional` | ✗ | ✗ | ✓ |
| `to_decimal_fractional_safe` | ✗ | ✗ | ✓ |
| **Total** | **2** | **3** | **12** |

### Integral Part — Arithmetic Style

| Language | Operations | Notes |
|---|---|---|
| Python | `integral *= 2; if '+': integral += 1` | `int` is unbounded |
| C++ | `integral <<= 1; if '+': integral += 1` | Uses bit-shift |
| Rust | `result << 1; if '+': result + 1` | Uses bit-shift, `const fn` |

Equivalent — any optimizing compiler produces the same instructions for `*= 2` and `<<= 1`.

### Fractional Part — Identical

All three use the same `scale = 0.5; scale /= 2.0` accumulation pattern.

### Input Validation

| Language | Invalid characters | Consecutive non-zero | Empty string |
|---|---|---|---|
| Python | `logging.info(...)`, continues silently | Not checked | Not checked |
| C++ | `throw invalid_argument` | Not checked | Not checked |
| Rust (safe) | `Err(CsdError::InvalidCharacter(...))` | `Err(CsdError::ConsecutiveNonZero(...))` | `Err(CsdError::EmptyString)` |

---

## 6. LCSRe — Longest Repeated Substring

### Algorithm — **Identical across all three**

All implement the same space-optimized dynamic programming algorithm:

```python
# 2-row DP table, O(n) space, O(n²) time
lcsre[i][j] = lcsre[i-1][j-1] + 1   if s[i-1] == s[j-1] AND (j-i) > lcsre[i-1][j-1]
            = 0                      otherwise
```

### Implementation comparison

| Detail | Python | C++ | Rust |
|---|---|---|---|
| Data structure | `[0] * (2 * ndim)` | `vector<unsigned int>(2*ndim, 0)` | `vec![0usize; 2 * ndim]` |
| Row switching | `(i % 2) * ndim` | same | same |
| Character access | `csd_string[row_index-1]` | `sv[i-1]` | `bytes[i-1]` |
| Result extraction | slice `[idx-res_len:idx]` | `assign(ptr, len)` | slice `[idx-res_len..idx]` |

**Line-for-line identical.** The Rust version operates on `&[u8]` for slightly faster character comparison. The Python version is the most readable; the C++ and Rust versions are near-verbatim translations.

---

## 7. CSD Multiplier Verilog Generation

### Architecture — **Same algorithms, different packaging**

All three implement:

1. **Single multiplier** (`generate_csd_multiplier`):
   - Parse CSD into (power, add/sub) terms
   - Detect LCSRe pattern (≥2 non-zero digits, ≥2 occurrences)
   - If optimized: emit `_pat` sub-expression wire + shifted references
   - If flat: emit direct `x_shift + x_shift - ...` expression

2. **Multi-coefficient cross-CSE** (`generate_csd_multipliers`):
   - Enumerate all substrings of each CSD string
   - Score by `(nnz - 1) * (occurrences - 1)`
   - Pick best, emit shared `_cse_0` wire

### Structural differences

| Aspect | Python | C++ | Rust |
|---|---|---|---|
| Coefficient type | `(name, csd, iw, mp)` tuple | `MultiplierSpec` struct | `MultiplierSpec` struct + `CsdMultiplier` struct |
| Free-function API | ✓ | ✓ | ✓ |
| Struct-based API | ✗ | ✗ | `CsdMultiplier::new()` + `.generate_verilog()` |
| Cross-CSE string view | N/A | `std::string_view` (no copies) | `String` clones (copies) |
| Pattern occurrence find | `csd.find(pattern, pos)` | `csd_str.find(pattern, pos)` | `csd_str[pos..].find(pattern)` |
| Verilog string building | `verilog += f"..."` | `verilog.reserve()` + `+=` | `write!(verilog, ...)` macro |

### Key Rust-specific features

- **`CsdMultiplier` struct** with methods: `decimal_value()` computes the numeric value of the CSD pattern, and `generate_verilog()` produces the complete module. Python and C++ only have free functions.
- **`get_unique_powers()`** helper returns deduplicated shift amounts, simplifying the wire declaration logic.
- The struct API enables potential future extension (configuration, multiple output formats) that free functions don't naturally support.

### Cross-CSE enumeration

Python and Rust enumerate substrings by iterating `i..n` with inner `j..n` and extracting substrings. C++ uses `std::string_view` to avoid substring copies — a memory optimization not applicable to Python and unnecessary in Rust's slice-based model.

The scoring formula is the same across all three:
```
score = (non_zero_digits_in_pattern - 1) * (occurrences - 1)
```

---

## 8. Error Handling

| Dimension | Python | C++ | Rust |
|---|---|---|---|
| Style | Log and continue | Exceptions | `Result<T, E>` (enum) |
| Invalid character | `logging.info()` | `throw invalid_argument` | `Err(CsdError::InvalidCharacter)` |
| Consecutive non-zero | Not checked | Not checked | `Err(CsdError::ConsecutiveNonZero)` |
| Empty string | Not checked | Not checked | `Err(CsdError::EmptyString)` |
| Overflow | Not checked | Not checked | `Err(CsdError::Overflow {...})` |
| Precision loss | Not checked | Not checked | `Err(CsdError::PrecisionLoss {...})` |
| Error variants | 0 (passive) | 1 (generic exception) | **7** (typed enum) |
| Error display | Log message only | `what()` string | `Display` + `Error` impl |

**Python is the most permissive** — it logs invalid characters and continues, and never validates CSD format constraints (consecutive non-zero digits, empty strings, etc.).

**C++ is in the middle** — it throws exceptions on invalid characters but doesn't validate format constraints either.

**Rust is the strictest** — it enriches every failure mode with a typed error, validates consecutive non-zero digits, rejects empty strings, and returns `CsdResult<T>` from all fallible operations.

---

## 9. Integer Width Support

| Width | Python | C++ | Rust |
|---|---|---|---|
| `i32` | `int` (unbounded) | `int` (32-bit) | ✓ |
| `i64` | ✗ | ✗ | ✓ |
| `i128` | ✗ | ✗ | ✓ |
| `to_csdnnz_i(width)` | 1 variant | 1 variant | **3** (i32→f64 cast, i64 dedicated, i128 dedicated) |
| `to_csd_i(width)` | 1 variant | 1 variant | **3** (i32, i64, i128) |
| `to_decimal_i(width)` | ✗ | 1 variant | **3** (i32, i64, i128) |

This is the single most impactful functional difference. Python's `int` is unbounded and handles any width transparently. C++ is fixed at 32-bit `int`. Rust explicitly supports three widths with separate implementations.

### Integer type usage in `to_csd_i64` vs `to_csd_i128`

Rust's `to_csd_i128` cannot reuse the `highest_power_of_two_in` helper (which operates on `u32`) because `u128` values may exceed the `u32` range. Instead, it falls back to a manual bit-counting loop:

```rust
let mut highest_bit = 0u32;
let mut temp_mut = temp;
while temp_mut > 0 {
    temp_mut >>= 1;
    highest_bit += 1;
}
let mut p2n = if highest_bit > 0 { 1i128 << highest_bit } else { 0i128 };
```

This is a genuine algorithmic fallback — the bit-twiddle trick doesn't scale beyond 32-bit.

---

## 10. API Design Patterns

### Builder Pattern — **Rust only**

```rust
let csd = CsdBuilder::new(28.5)
    .places(4)
    .max_non_zeros(3)
    .rounding_strategy(RoundingStrategy::Nearest)
    .build()?;
```

The `CsdBuilder` (Rust only) unifies `to_csd`, `to_csdnnz`, and their integer variants into a single fluent interface. It also introduces:

- **`RoundingStrategy` enum** — `Nearest`, `Down`, `Up` (currently a no-op; always produces nearest CSD)
- **`CsdError` / `CsdResult`** — typed error and result aliases

### Free-function API

Python: All functions are module-level with no classes.
C++: All functions are in `namespace csd`, plus a `MultiplierSpec` struct.
Rust: Both free functions AND the `CsdMultiplier` struct.

### Validation Utilities — **Rust only**

```rust
validate_csd_format(csd)   → bool      // checks chars + consecutive non-zero
count_non_zero_digits(csd) → usize     // counts '+' and '-'
is_power_of_two(x)         → bool      // classic x && !(x & (x-1))
```

These are exported and publicly documented in Rust. Python and C++ don't expose equivalent utilities.

### Thread Safety — **Rust only**

Rust uses a `thread_local!` buffer to avoid repeated allocations in `to_csd`:

```rust
thread_local! {
    static STRING_BUFFER: RefCell<Vec<u8>> = const { RefCell::new(Vec::new()) };
}
```

Each thread gets its own reusable buffer, cleared before each conversion. This is invisible to the caller but provides a measurable performance benefit in tight loops.

---

## 11. Performance & Memory

| Aspect | Python | C++ | Rust |
|---|---|---|---|
| String pre-allocation | ✗ (list append, join) | `csd.reserve(estimated)` | `Vec::with_capacity(n)`, `String::with_capacity(n)` |
| Thread-local buffer | ✗ | ✗ | `thread_local!` + `RefCell<Vec<u8>>` |
| Zero-copy substring in cross-CSE | N/A (copies) | `std::string_view` (zero-copy) | `&str` slicing (zero-copy) |
| Constexpr evaluation | ✗ | limited (`CONSTEXPR14` macros) | `const fn` throughout |
| Data structure overhead | Python list (dynamic) | `std::string` (SSO) | `Vec<u8>` → `String` (SSO) |
| Integer ops in to_decimal | `integral *= 2` | `integral <<= 1` | `result << 1` |

### Key observations

- **String pre-allocation**: Python doesn't need it (list/join pattern). C++ and Rust both estimate capacity before building.
- **Thread-local buffer**: Rust's `with_string_buffer` avoids reallocation across calls in the same thread — unique among the three.
- **Zero-copy substrings**: C++ uses `std::string_view` and Rust uses `&str` slicing in cross-CSE. Python copies substrings.
- **Constexpr**: Rust's `const fn` on `highest_power_of_two_in`, `to_decimal_i`, and `is_power_of_two` enables compile-time evaluation. C++ has `CONSTEXPR14` macros that provide limited `constexpr` support. Python has no equivalent.

---

## 12. Testing

| Aspect | Python | C++ | Rust |
|---|---|---|---|
| Unit tests | `tests/*.py` (pytest) | `test/source/*.cpp` (Doctest) | Inline `#[cfg(test)]` modules |
| Doctests | ✓ (doctest in docstrings) | Doxygen examples only | Doc-test `/// ```rust` examples |
| Property-based tests | ✗ | ✗ | `quickcheck` (8 roundtrip properties) |
| Stress tests | ✗ | ✓ (`test_stress.cpp`) | ✗ |
| Random/fuzz | `hypothesis/` directory | `rapidcheck.md` + `test_rapidcheck.cpp` | ✗ |

### Test coverage focus

- **Python**: Heavy on edge cases (zeros, negatives, boundary values), roundtrip verification via `doctest`
- **C++**: Comprehensive stress testing (`test_stress.cpp`), property-based with RapidCheck (`test_rapidcheck.cpp`), dedicated test for each function
- **Rust**: Property-based testing with quickcheck (8 properties: roundtrip for `to_csd`, `to_csd_i`, power-of-two invariant, safe-decimal valid/invalid classification), per-function unit tests inline

Rust's quickcheck properties are particularly notable — they express algorithmic invariants directly:

```rust
#[quickcheck]
fn test_csd_roundtrip(d: i32) -> bool {
    let f = d as f64 / 8.0;
    let csd = to_csd(f, places);
    let recovered = to_decimal(&csd);
    (f - recovered).abs() < 1e-10
}
```

---

## 13. Complete Difference Matrix

| # | Area | Python | C++ | Rust |
|---|---|---|---|---|
| **Core algorithms** | | | | |
| 1 | `to_csd` start power | `frexp` + mantissa check | `frexp` + mantissa check | `log2().ceil()` |
| 2 | `to_csd_i` start power | `bit_length()` | bit-twiddle `hp2()` | `const fn` bit-twiddle |
| 3 | `to_csdnnz` termination | conditional per branch | zero-out value to exit loop | conditional + `break` |
| 4 | `to_csdnnz_i` padding | tail emits `0` naturally | sets `value=0`, loop collapses | dedicated i64/i128: explicit zero-pad loop |
| 5 | `to_decimal` variants | 2 | 3 | **12** |
| **Integer widths** | | | | |
| 6 | i32 support | ✓ (unbounded int) | ✓ | ✓ |
| 7 | i64 support | ✗ | ✗ | ✓ |
| 8 | i128 support | ✗ | ✗ | ✓ |
| 9 | Dedicated NNZ impls by width | 1 for all widths | 1 for i32 | **3** (i32→f64 cast, i64, i128) |
| **Error handling** | | | | |
| 10 | Invalid character | log + continue | throw | `Err` variant |
| 11 | Consecutive non-zero check | ✗ | ✗ | ✓ |
| 12 | Empty string check | ✗ | ✗ | ✓ |
| 13 | Overflow detection | ✗ | ✗ | ✓ |
| 14 | Error type variants | 0 (passive) | 1 | **7** |
| **API design** | | | | |
| 15 | Builder pattern | ✗ | ✗ | `CsdBuilder` |
| 16 | `RoundingStrategy` | ✗ | ✗ | enum (no-op) |
| 17 | Struct-based multiplier API | ✗ | ✗ | `CsdMultiplier` struct |
| 18 | Validation utilities | ✗ | ✗ | `validate_csd_format`, `count_nnz`, `is_power_of_two` |
| **Performance** | | | | |
| 19 | String pre-allocation | ✗ (list/join) | `reserve()` | `reserve()`, `with_capacity()` |
| 20 | Thread-local buffer | ✗ | ✗ | ✓ |
| 21 | Zero-copy substrings in CSE | ✗ (copies) | `string_view` | `&str` slices |
| 22 | Constexpr | ✗ | limited (`CONSTEXPR14`) | `const fn` |
| **Testing** | | | | |
| 23 | Property-based tests | ✗ (hypothesis dir only) | RapidCheck | quickcheck (8 properties) |
| 24 | Doctests | ✓ | ✗ | ✓ |
| 25 | Stress tests | ✗ | ✓ | ✗ |
| **Meta** | | | | |
| 26 | Feature flags | ✗ | ✗ | `multiplier`, `lcsre`, `std` |
| 27 | LCSRe algorithm | identical | identical | identical (byte slice) |
| 28 | Cross-CSE algorithm | identical | identical | identical |
| 29 | CSD multiplier scoring | `(nnz-1)*(occ-1)` | same | same (`saturating_sub`) |

---

## 14. Summary

### No fundamental algorithmic differences

The core CSD conversion, LCSRe, and cross-CSE algorithms are **line-for-line identical** across all three languages. Every implementation is a direct translation of the same Harnesser/ita_c origin. The output for any given input is the same in all three.

### Where they diverge

1. **`to_csd` start power**: Rust uses `log2().ceil()` instead of `frexp`. Results are identical.
2. **`to_csd_i` start power**: Python uses `bit_length()`; C++/Rust use a bit-twiddle `highest_power_of_two_in`. Same values.
3. **`to_csdnnz` termination**: Three different mechanisms (per-branch check, value-zeroing, break) — all produce the same output.
4. **API surface**: Rust has 12 `to_decimal` variants vs 3 (C++) and 2 (Python). Rust also has a `CsdBuilder` and `CsdMultiplier` struct.
5. **Integer width**: Rust supports i32/i64/i128; Python uses unbounded int; C++ is i32 only.
6. **Error model**: Rust returns typed `CsdResult<T>` with 7 error variants; C++ throws; Python logs and continues.
7. **Validation**: Rust validates consecutive non-zero digits and empty strings; Python and C++ do not.
8. **Testing**: Rust has property-based quickcheck roundtrip tests; C++ has stress + RapidCheck; Python has hypothesis support.
9. **Performance**: Rust has thread-local string buffers, const fn, and zero-copy slices; C++ has `reserve()` and `string_view`; Python relies on the runtime.

### Verdict

If you know the algorithm in one language, you know it in all three. The algorithmic core is the same; the divergences are in **API design philosophy, error handling strictness, and integer type support** rather than in any mathematical or algorithmic choice.
