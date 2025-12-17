//! @file csd.cpp
//! @brief Implementation of CSD conversion functions

#include "csdigit/csdigit.hpp"
#include <algorithm>
#include <sstream>
#include <iomanip>
#include <limits>

namespace csdigit {

std::string to_csd(double decimal_value, int places) {
    if (decimal_value == 0.0) {
        if (places > 0) {
            return "0." + std::string(places, '0');
        } else {
            return "0.";
        }
    }

    double abs_val = std::fabs(decimal_value);
    int rem;
    std::vector<std::string> csd_list;
    
    if (abs_val < 1.0) {
        rem = 0;
        csd_list.push_back("0");
    } else {
        rem = static_cast<int>(std::ceil(std::log2(abs_val * 1.5)));
        // csd_list starts empty
    }

    double value = decimal_value;
    double p2n = std::pow(2.0, rem);

    for (int i = 0; i < rem; ++i) {
        p2n /= 2.0;
        double det = 1.5 * value;
        if (det > p2n) {
            csd_list.push_back("+");
            value -= p2n;
        } else if (det < -p2n) {
            csd_list.push_back("-");
            value += p2n;
        } else {
            csd_list.push_back("0");
        }
    }

    csd_list.push_back(".");

    for (int i = 0; i < places; ++i) {
        p2n /= 2.0;
        double det = 1.5 * value;
        if (det > p2n) {
            csd_list.push_back("+");
            value -= p2n;
        } else if (det < -p2n) {
            csd_list.push_back("-");
            value += p2n;
        } else {
            csd_list.push_back("0");
        }
    }

    std::string result;
    for (const auto& s : csd_list) {
        result += s;
    }
    return result;
}

std::string to_csd_i(int32_t decimal_value) {
    if (decimal_value == 0) {
        return "0";
    }

    int32_t value = decimal_value;
    int rem = static_cast<int>(std::ceil(std::log2(std::abs(value) * 1.5)));
    int32_t p2n = 1 << rem;
    std::vector<std::string> csd_list;

    while (p2n > 1) {
        int32_t p2n_half = p2n >> 1;
        int32_t det = 3 * value;
        if (det > p2n) {
            csd_list.push_back("+");
            value -= p2n_half;
        } else if (det < -p2n) {
            csd_list.push_back("-");
            value += p2n_half;
        } else {
            csd_list.push_back("0");
        }
        p2n = p2n_half;
    }

    std::string result;
    for (const auto& s : csd_list) {
        result += s;
    }
    return result;
}

double to_decimal(const std::string& csd) {
    if (csd.find('.') == std::string::npos) {
        int integral = 0;
        for (char ch : csd) {
            integral *= 2;
            switch (ch) {
                case '+': integral += 1; break;
                case '-': integral -= 1; break;
                case '0': break;
                default: break; // Ignore unknown characters
            }
        }
        return static_cast<double>(integral);
    }

    size_t dot_pos = csd.find('.');
    std::string integral_part = csd.substr(0, dot_pos);
    std::string fractional_part = csd.substr(dot_pos + 1);

    double integral_float = 0.0;
    for (char ch : integral_part) {
        integral_float *= 2.0;
        switch (ch) {
            case '+': integral_float += 1.0; break;
            case '-': integral_float -= 1.0; break;
            case '0': break;
            default: break; // Ignore unknown characters
        }
    }

    double fractional = 0.0;
    double scale = 0.5;
    for (char ch : fractional_part) {
        switch (ch) {
            case '+': fractional += scale; break;
            case '-': fractional -= scale; break;
            case '0': break;
            default: break; // Ignore unknown characters
        }
        scale /= 2.0;
    }

    return integral_float + fractional;
}

std::string to_csdnnz(double decimal_value, int nnz) {
    if (decimal_value == 0.0) {
        return "0";
    }

    double abs_val = std::fabs(decimal_value);
    int rem;
    std::vector<std::string> csd_list;
    
    if (abs_val < 1.0) {
        rem = 0;
        csd_list.push_back("0");
    } else {
        rem = static_cast<int>(std::ceil(std::log2(abs_val * 1.5)));
        // csd_list starts empty
    }

    double value = decimal_value;
    double p2n = std::pow(2.0, rem);
    int nnz_remaining = nnz;

    while (rem > 0 || (nnz_remaining > 0 && std::fabs(value) > 1e-100)) {
        if (rem == 0) {
            csd_list.push_back(".");
        }
        p2n /= 2.0;
        rem -= 1;
        double det = 1.5 * value;
        if (nnz_remaining > 0 && det > p2n) {
            csd_list.push_back("+");
            value -= p2n;
            nnz_remaining -= 1;
        } else if (nnz_remaining > 0 && det < -p2n) {
            csd_list.push_back("-");
            value += p2n;
            nnz_remaining -= 1;
        } else {
            csd_list.push_back("0");
        }
    }

    std::string result;
    for (const auto& s : csd_list) {
        result += s;
    }
    return result;
}

std::string to_csdnnz_i(int32_t decimal_value, int nnz) {
    if (decimal_value == 0) {
        return "0";
    }

    int32_t value = decimal_value;
    int rem = static_cast<int>(std::ceil(std::log2(std::abs(value) * 1.5)));
    int32_t p2n = 1 << rem;
    std::vector<std::string> csd_list;
    int nnz_remaining = nnz;

    while (p2n > 1) {
        int32_t p2n_half = p2n >> 1;
        int32_t det = 3 * value;
        if (nnz_remaining > 0 && det > p2n) {
            csd_list.push_back("+");
            value -= p2n_half;
            nnz_remaining -= 1;
        } else if (nnz_remaining > 0 && det < -p2n) {
            csd_list.push_back("-");
            value += p2n_half;
            nnz_remaining -= 1;
        } else {
            csd_list.push_back("0");
        }
        p2n = p2n_half;
    }

    std::string result;
    for (const auto& s : csd_list) {
        result += s;
    }
    return result;
}

} // namespace csdigit