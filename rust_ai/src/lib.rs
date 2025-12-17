//! Canonical Signed Digit (CSD) Conversion Library
//!
//! This library provides functions for converting between decimal numbers and Canonical Signed Digit (CSD) representation.
//! CSD is a special signed-digit representation where each digit is limited to -1, 0, or 1, and consecutive non-zero digits are not allowed.
//! This representation is particularly useful in digital signal processing applications such as filter design,
//! as it enables efficient arithmetic operations using simple adders and subtractors.
//!
//! # Examples
//!
//! ```
//! use csdigit::*;
//!
//! // Convert decimal to CSD
//! let csd = to_csd(28.5, 2);
//! assert_eq!(csd, "+00-00.+0");
//!
//! // Convert CSD to decimal
//! let decimal = to_decimal("+00-00.+");
//! assert_eq!(decimal, 28.5);
//!
//! // Convert integer to CSD
//! let csd_int = to_csd_i(28);
//! assert_eq!(csd_int, "+00-00");
//! ```

use std::f64;

/// Convert a decimal number to CSD representation with specified decimal places.
///
/// # Arguments
///
/// * `decimal_value` - The decimal value to convert
/// * `places` - Number of decimal places in the CSD representation
///
/// # Examples
///
/// ```
/// use csdigit::to_csd;
/// assert_eq!(to_csd(28.5, 2), "+00-00.+0");
/// assert_eq!(to_csd(-0.5, 2), "0.-0");
/// assert_eq!(to_csd(0.0, 2), "0.00");
/// assert_eq!(to_csd(0.0, 0), "0.");
/// ```
pub fn to_csd(decimal_value: f64, places: i32) -> String {
    if decimal_value == 0.0 {
        return if places > 0 {
            format!("0.{}", "0".repeat(places as usize))
        } else {
            "0.".to_string()
        };
    }

    let abs_val = decimal_value.abs();
    let (rem, mut csd_list) = if abs_val < 1.0 {
        (0, vec!["0".to_string()])
    } else {
        let rem_val = (abs_val * 1.5).log2().ceil() as i32;
        (rem_val, Vec::new())
    };

    let mut value = decimal_value;
    let mut p2n = 2.0_f64.powi(rem);

    for _ in 0..rem {
        p2n /= 2.0;
        let det = 1.5 * value;
        if det > p2n {
            csd_list.push("+".to_string());
            value -= p2n;
        } else if det < -p2n {
            csd_list.push("-".to_string());
            value += p2n;
        } else {
            csd_list.push("0".to_string());
        }
    }

    csd_list.push(".".to_string());

    for _ in 0..places {
        p2n /= 2.0;
        let det = 1.5 * value;
        if det > p2n {
            csd_list.push("+".to_string());
            value -= p2n;
        } else if det < -p2n {
            csd_list.push("-".to_string());
            value += p2n;
        } else {
            csd_list.push("0".to_string());
        }
    }

    csd_list.join("")
}

/// Convert an integer to CSD representation.
///
/// # Arguments
///
/// * `decimal_value` - The integer value to convert
///
/// # Examples
///
/// ```
/// use csdigit::to_csd_i;
/// assert_eq!(to_csd_i(28), "+00-00");
/// assert_eq!(to_csd_i(0), "0");
/// ```
pub fn to_csd_i(decimal_value: i32) -> String {
    if decimal_value == 0 {
        return "0".to_string();
    }

    let mut value = decimal_value;
    let rem = ((value.abs() * 3 / 2) as f64).log2().ceil() as u32;
    let mut p2n = 1 << rem;
    let mut csd_list = Vec::new();

    while p2n > 1 {
        let p2n_half = p2n >> 1;
        let det = 3 * value;
        if det > p2n as i32 {
            csd_list.push("+".to_string());
            value -= p2n_half as i32;
        } else if det < -(p2n as i32) {
            csd_list.push("-".to_string());
            value += p2n_half as i32;
        } else {
            csd_list.push("0".to_string());
        }
        p2n = p2n_half;
    }

    csd_list.join("")
}

/// Convert a CSD string to a decimal number.
///
/// # Arguments
///
/// * `csd` - The CSD string to convert
///
/// # Examples
///
/// ```
/// use csdigit::to_decimal;
/// assert_eq!(to_decimal("+00-00.+"), 28.5);
/// assert_eq!(to_decimal("0.-"), -0.5);
/// assert_eq!(to_decimal("0"), 0.0);
/// assert_eq!(to_decimal("0.0"), 0.0);
/// assert_eq!(to_decimal("0.+"), 0.5);
/// ```
pub fn to_decimal(csd: &str) -> f64 {
    if !csd.contains('.') {
        let mut integral = 0;
        for ch in csd.chars() {
            integral *= 2;
            match ch {
                '+' => integral += 1,
                '-' => integral -= 1,
                '0' => {}
                _ => log::info!("Encounter unknown character {}", ch),
            }
        }
        return integral as f64;
    }

    let parts: Vec<&str> = csd.split('.').collect();
    if parts.len() != 2 {
        return 0.0;
    }

    let integral_part = parts[0];
    let fractional_part = parts[1];

    let mut integral_float = 0.0;
    for ch in integral_part.chars() {
        integral_float *= 2.0;
        match ch {
            '+' => integral_float += 1.0,
            '-' => integral_float -= 1.0,
            '0' => {}
            _ => log::info!("Encounter unknown character {}", ch),
        }
    }

    let mut fractional = 0.0;
    let mut scale = 0.5;
    for ch in fractional_part.chars() {
        match ch {
            '+' => fractional += scale,
            '-' => fractional -= scale,
            '0' => {}
            _ => log::info!("Encounter unknown character {}", ch),
        }
        scale /= 2.0;
    }

    integral_float + fractional
}

/// Convert a decimal number to CSD representation with a maximum number of non-zero digits.
///
/// # Arguments
///
/// * `decimal_value` - The decimal value to convert
/// * `nnz` - Maximum number of non-zero digits allowed in the CSD representation
///
/// # Examples
///
/// ```
/// use csdigit::to_csdnnz;
/// assert_eq!(to_csdnnz(28.5, 4), "+00-00.+");
/// assert_eq!(to_csdnnz(-0.5, 4), "0.-");
/// assert_eq!(to_csdnnz(0.0, 4), "0");
/// assert_eq!(to_csdnnz(0.5, 4), "0.+");
/// ```
pub fn to_csdnnz(decimal_value: f64, nnz: i32) -> String {
    if decimal_value == 0.0 {
        return "0".to_string();
    }

    let abs_val = decimal_value.abs();
    let (mut rem, mut csd_list) = if abs_val < 1.0 {
        (0, vec!["0".to_string()])
    } else {
        let rem_val = (abs_val * 1.5).log2().ceil() as i32;
        (rem_val, Vec::new())
    };

    let mut value = decimal_value;
    let mut p2n = 2.0_f64.powi(rem);
    let mut nnz_remaining = nnz;

    while rem > 0 || (nnz_remaining > 0 && value.abs() > 1e-100) {
        if rem == 0 {
            csd_list.push(".".to_string());
        }
        p2n /= 2.0;
        rem -= 1;
        let det = 1.5 * value;
        if nnz_remaining > 0 && det > p2n {
            csd_list.push("+".to_string());
            value -= p2n;
            nnz_remaining -= 1;
        } else if nnz_remaining > 0 && det < -p2n {
            csd_list.push("-".to_string());
            value += p2n;
            nnz_remaining -= 1;
        } else {
            csd_list.push("0".to_string());
        }
    }

    csd_list.join("")
}

/// Convert an integer to CSD representation with a maximum number of non-zero digits.
///
/// # Arguments
///
/// * `decimal_value` - The integer value to convert
/// * `nnz` - Maximum number of non-zero digits allowed in the CSD representation
///
/// # Examples
///
/// ```
/// use csdigit::to_csdnnz_i;
/// assert_eq!(to_csdnnz_i(28, 4), "+00-00");
/// assert_eq!(to_csdnnz_i(0, 4), "0");
/// assert_eq!(to_csdnnz_i(37, 2), "+00+00");
/// assert_eq!(to_csdnnz_i(158, 2), "+0+00000");
/// ```
pub fn to_csdnnz_i(decimal_value: i32, nnz: i32) -> String {
    if decimal_value == 0 {
        return "0".to_string();
    }

    let mut value = decimal_value;
    let rem = ((value.abs() * 3 / 2) as f64).log2().ceil() as i32;
    let mut p2n = 2_i32.pow(rem as u32);
    let mut csd_list = Vec::new();
    let mut nnz_remaining = nnz;

    while p2n > 1 {
        let p2n_half = p2n >> 1;
        let det = 3 * value;
        if nnz_remaining > 0 && det > p2n {
            csd_list.push("+".to_string());
            value -= p2n_half;
            nnz_remaining -= 1;
        } else if nnz_remaining > 0 && det < -p2n {
            csd_list.push("-".to_string());
            value += p2n_half;
            nnz_remaining -= 1;
        } else {
            csd_list.push("0".to_string());
        }
        p2n = p2n_half;
    }

    csd_list.join("")
}

/// Find the longest repeated non-overlapping substring in a string.
///
/// # Arguments
///
/// * `cs` - The input string
///
/// # Examples
///
/// ```
/// use csdigit::longest_repeated_substring;
/// assert_eq!(longest_repeated_substring("+-00+-00+-00+-0"), "+-00+-0");
/// ```
pub fn longest_repeated_substring(cs: &str) -> String {
    let n = cs.len();
    let mut lcsre = vec![vec![0; n + 1]; n + 1];
    
    let mut res = String::new();
    let mut res_length = 0;
    let mut index = 0;
    
    let chars: Vec<char> = cs.chars().collect();
    
    for i in 1..=n {
        for j in (i + 1)..=n {
            if chars[i - 1] == chars[j - 1] && lcsre[i - 1][j - 1] < (j - i) {
                lcsre[i][j] = lcsre[i - 1][j - 1] + 1;
                
                if lcsre[i][j] > res_length {
                    res_length = lcsre[i][j];
                    index = i.max(index);
                }
            } else {
                lcsre[i][j] = 0;
            }
        }
    }
    
    if res_length > 0 {
        res = cs[index - res_length..index].to_string();
    }
    
    res
}

/// Generate Verilog code for a CSD multiplier module with proper signed handling.
///
/// # Arguments
///
/// * `csd` - CSD string (e.g., "+00-00+0+")
/// * `n` - Input bit width
/// * `m` - Highest power in CSD (must be len(csd)-1)
///
/// # Examples
///
/// ```
/// use csdigit::generate_csd_multiplier;
/// let verilog = generate_csd_multiplier("+00-00+0", 8, 7);
/// assert!(verilog.contains("module csd_multiplier"));
/// ```
pub fn generate_csd_multiplier(csd: &str, n: usize, m: usize) -> String {
    if csd.len() != m + 1 {
        panic!("CSD length {} doesn't match m={} (should be m+1)", csd.len(), m);
    }
    
    if !csd.chars().all(|c| c == '+' || c == '-' || c == '0') {
        panic!("CSD string can only contain '+', '-', or '0'");
    }
    
    let mut terms = Vec::new();
    for (i, c) in csd.chars().enumerate() {
        let power = m - i;
        match c {
            '+' => terms.push((power, "add")),
            '-' => terms.push((power, "sub")),
            _ => {}
        }
    }
    
    let mut verilog_code = format!(
        "\nmodule csd_multiplier (\n    input signed [{}:0] x,      // Input value\n    output signed [{}:0] result // Result of multiplication\n);",
        n - 1,
        n + m - 1
    );
    
    if !terms.is_empty() {
        verilog_code += "\n\n    // Create shifted versions of input";
        let mut powers_needed: Vec<usize> = terms.iter().map(|&(p, _)| p).collect();
        powers_needed.sort_unstable_by(|a, b| b.cmp(a));
        powers_needed.dedup();
        
        for &p in &powers_needed {
            verilog_code += &format!("\n    wire signed [{}:0] x_shift{} = x <<< {};", n + m - 1, p, p);
        }
    }
    
    verilog_code += "\n\n    // CSD implementation";
    if terms.is_empty() {
        verilog_code += "\n    assign result = 0;";
    } else {
        let (first_power, _) = terms[0];
        let mut expr = format!("x_shift{}", first_power);
        
        for &(power, op) in &terms[1..] {
            if op == "add" {
                expr += &format!(" + x_shift{}", power);
            } else {
                expr += &format!(" - x_shift{}", power);
            }
        }
        
        verilog_code += &format!("\n    assign result = {};", expr);
    }
    
    verilog_code += "\nendmodule\n";
    verilog_code
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_to_csd() {
        assert_eq!(to_csd(28.5, 2), "+00-00.+0");
        assert_eq!(to_csd(-0.5, 2), "0.-0");
        assert_eq!(to_csd(0.0, 2), "0.00");
        assert_eq!(to_csd(0.0, 0), "0.");
    }
    
    #[test]
    fn test_to_csd_i() {
        assert_eq!(to_csd_i(28), "+00-00");
        assert_eq!(to_csd_i(0), "0");
    }
    
    #[test]
    fn test_to_decimal() {
        assert_eq!(to_decimal("+00-00.+"), 28.5);
        assert_eq!(to_decimal("0.-"), -0.5);
        assert_eq!(to_decimal("0"), 0.0);
        assert_eq!(to_decimal("0.0"), 0.0);
        assert_eq!(to_decimal("0.+"), 0.5);
    }
    
    #[test]
    fn test_to_csdnnz() {
        assert_eq!(to_csdnnz(28.5, 4), "+00-00.+");
        assert_eq!(to_csdnnz(-0.5, 4), "0.-");
        assert_eq!(to_csdnnz(0.0, 4), "0");
        assert_eq!(to_csdnnz(0.5, 4), "0.+");
    }
    
    #[test]
    fn test_to_csdnnz_i() {
        assert_eq!(to_csdnnz_i(28, 4), "+00-00");
        assert_eq!(to_csdnnz_i(0, 4), "0");
        assert_eq!(to_csdnnz_i(37, 2), "+00+00");
        assert_eq!(to_csdnnz_i(158, 2), "+0+00000");
    }
    
    #[test]
    fn test_longest_repeated_substring() {
        assert_eq!(longest_repeated_substring("+-00+-00+-00+-0"), "+-00+-0");
    }
    
    #[test]
    fn test_generate_csd_multiplier() {
        let verilog = generate_csd_multiplier("+00-00+0", 8, 7);
        assert!(verilog.contains("module csd_multiplier"));
        assert!(verilog.contains("input signed [7:0] x"));
        assert!(verilog.contains("output signed [14:0] result"));
    }
}