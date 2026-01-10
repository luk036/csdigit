//! @file csd_multiplier.cpp
//! @brief Implementation of Verilog CSD multiplier generator

#include "csdigit/csdigit.hpp"
#include <sstream>
#include <set>
#include <algorithm>

namespace csdigit {

std::string generate_csd_multiplier(const std::string& csd, size_t n, size_t m) {
    if (csd.size() != m + 1) {
        throw std::invalid_argument("CSD length doesn't match m (should be m+1)");
    }

    for (char c : csd) {
        if (c != '+' && c != '-' && c != '0') {
            throw std::invalid_argument("CSD string can only contain '+', '-', or '0'");
        }
    }

    std::vector<std::pair<size_t, std::string>> terms;
    for (size_t i = 0; i < csd.size(); ++i) {
        size_t power = m - i;
        if (csd[i] == '+') {
            terms.emplace_back(power, "add");
        } else if (csd[i] == '-') {
            terms.emplace_back(power, "sub");
        }
    }

    std::ostringstream verilog_code;
    verilog_code << "\nmodule csd_multiplier (\n"
                 << "    input signed [" << (n - 1) << ":0] x,      // Input value\n"
                 << "    output signed [" << (n + m - 1) << ":0] result // Result of multiplication\n"
                 << ");";

    if (!terms.empty()) {
        verilog_code << "\n\n    // Create shifted versions of input";
        std::set<size_t> powers_needed;
        for (const auto& term : terms) {
            powers_needed.insert(term.first);
        }

        // Sort in descending order
        std::vector<size_t> sorted_powers(powers_needed.begin(), powers_needed.end());
        std::sort(sorted_powers.rbegin(), sorted_powers.rend());

        for (size_t p : sorted_powers) {
            verilog_code << "\n    wire signed [" << (n + m - 1) << ":0] x_shift" << p
                        << " = x <<< " << p << ";";
        }
    }

    verilog_code << "\n\n    // CSD implementation";
    if (terms.empty()) {
        verilog_code << "\n    assign result = 0;";
    } else {
        const auto& [first_power, first_op] = terms[0];
        std::string expr = "x_shift" + std::to_string(first_power);

        for (size_t i = 1; i < terms.size(); ++i) {
            const auto& [power, op] = terms[i];
            if (op == "add") {
                expr += " + x_shift" + std::to_string(power);
            } else {
                expr += " - x_shift" + std::to_string(power);
            }
        }

        verilog_code << "\n    assign result = " << expr << ";";
    }

    verilog_code << "\nendmodule\n";
    return verilog_code.str();
}

} // namespace csdigit
