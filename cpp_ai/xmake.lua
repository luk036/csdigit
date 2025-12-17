-- xmake.lua for csdigit C++ project
set_project("csdigit")
set_version("0.1.0")

-- Set C++ standard
set_languages("c++17")

-- Add doctest for testing
add_requires("doctest")

-- Library target
target("csdigit")
set_kind("static")
add_headerfiles("include/csdigit/*.hpp")
add_files("src/csdigit/*.cpp")
add_includedirs("include", { public = true })
-- set_targetdir("$(buildir)/lib")

-- CLI executable
target("csdigit_cli")
set_kind("binary")
add_files("src/cli/main.cpp")
add_deps("csdigit")
-- set_targetdir("$(buildir)/bin")

-- Tests
target("csdigit_tests")
set_kind("binary")
add_files("tests/test_csdigit.cpp")
add_deps("csdigit")
add_packages("doctest")
-- set_targetdir("$(buildir)/tests")
add_tests("default", { runargs = { "--success" } })

-- Examples
target("example_basic")
set_kind("binary")
add_files("examples/basic_usage.cpp")
add_deps("csdigit")
-- set_targetdir("$(buildir)/examples")

target("example_cli")
set_kind("binary")
add_files("examples/cli_usage.cpp")
add_deps("csdigit")
-- set_targetdir("$(buildir)/examples")

-- Build all by default
add_rules("mode.debug", "mode.release")
if is_mode("debug") then
	set_symbols("debug")
	set_optimize("none")
else
	set_symbols("hidden")
	set_optimize("fastest")
	set_strip("all")
end
