//! @file test_csdigit.cpp
//! @brief doctest tests for CSDigit library

#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "csdigit/csdigit.hpp"
#include <string>
#include <cmath>

TEST_CASE("to_csd function") {
    SUBCASE("Basic conversions") {
        CHECK(csdigit::to_csd(28.5, 2) == "+00-00.+0");
        CHECK(csdigit::to_csd(-0.5, 2) == "0.-0");
        CHECK(csdigit::to_csd(0.0, 2) == "0.00");
        CHECK(csdigit::to_csd(0.0, 0) == "0.");
    }
    
    SUBCASE("Round trip") {
        double value = 28.5;
        std::string csd = csdigit::to_csd(value, 4);
        double round_trip = csdigit::to_decimal(csd);
        CHECK(std::abs(round_trip - value) < 1e-10);
    }
}

TEST_CASE("to_csd_i function") {
    CHECK(csdigit::to_csd_i(28) == "+00-00");
    CHECK(csdigit::to_csd_i(0) == "0");
    CHECK(csdigit::to_csd_i(-15) == "-0+00+");
}

TEST_CASE("to_decimal function") {
    CHECK(csdigit::to_decimal("+00-00.+") == doctest::Approx(28.5));
    CHECK(csdigit::to_decimal("0.-") == doctest::Approx(-0.5));
    CHECK(csdigit::to_decimal("0") == doctest::Approx(0.0));
    CHECK(csdigit::to_decimal("0.0") == doctest::Approx(0.0));
    CHECK(csdigit::to_decimal("0.+") == doctest::Approx(0.5));
}

TEST_CASE("to_csdnnz function") {
    CHECK(csdigit::to_csdnnz(28.5, 4) == "+00-00.+");
    CHECK(csdigit::to_csdnnz(-0.5, 4) == "0.-");
    CHECK(csdigit::to_csdnnz(0.0, 4) == "0");
    CHECK(csdigit::to_csdnnz(0.5, 4) == "0.+");
}

TEST_CASE("to_csdnnz_i function") {
    CHECK(csdigit::to_csdnnz_i(28, 4) == "+00-00");
    CHECK(csdigit::to_csdnnz_i(0, 4) == "0");
    CHECK(csdigit::to_csdnnz_i(37, 2) == "+00+00");
    CHECK(csdigit::to_csdnnz_i(158, 2) == "+0+00000");
}

TEST_CASE("longest_repeated_substring function") {
    CHECK(csdigit::longest_repeated_substring("+-00+-00+-00+-0") == "+-00+-0");
    CHECK(csdigit::longest_repeated_substring("abcabc") == "abc");
    CHECK(csdigit::longest_repeated_substring("aaaa") == "aa");
    CHECK(csdigit::longest_repeated_substring("") == "");
    CHECK(csdigit::longest_repeated_substring("a") == "");
}

TEST_CASE("generate_csd_multiplier function") {
    SUBCASE("Valid input") {
        std::string verilog = csdigit::generate_csd_multiplier("+00-00+0", 8, 7);
        CHECK(verilog.find("module csd_multiplier") != std::string::npos);
        CHECK(verilog.find("input signed [7:0] x") != std::string::npos);
        CHECK(verilog.find("output signed [14:0] result") != std::string::npos);
    }
    
    SUBCASE("Invalid CSD length") {
        CHECK_THROWS_AS(csdigit::generate_csd_multiplier("+00-00", 8, 7), std::invalid_argument);
    }
    
    SUBCASE("Invalid characters") {
        CHECK_THROWS_AS(csdigit::generate_csd_multiplier("+00-00a", 8, 6), std::invalid_argument);
    }
}

TEST_CASE("Edge cases") {
    SUBCASE("Very small values") {
        CHECK(csdigit::to_csd(1e-10, 4) == "0.0000");
        CHECK(csdigit::to_csdnnz(1e-10, 2) == "0");
    }
    
    SUBCASE("Large values") {
        CHECK(csdigit::to_csd_i(1000).length() > 0);
        CHECK(csdigit::to_csdnnz_i(1000, 5).length() > 0);
    }
    
    SUBCASE("Negative values") {
        CHECK(csdigit::to_csd(-28.5, 2) == "-00+00.-0");
        CHECK(csdigit::to_csd_i(-28) == "-00+00");
    }
}