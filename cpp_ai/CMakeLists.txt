cmake_minimum_required(VERSION 3.12)
project(csdigit VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(BUILD_SHARED_LIBS "Build shared library" OFF)
option(BUILD_TESTS "Build tests" ON)
option(BUILD_EXAMPLES "Build examples" ON)

# Add doctest if tests are enabled
if(BUILD_TESTS)
    include(FetchContent)
    FetchContent_Declare(
        doctest
        GIT_REPOSITORY https://github.com/doctest/doctest.git
        GIT_TAG v2.4.11
    )
    FetchContent_MakeAvailable(doctest)
endif()

# Library target
add_library(csdigit)
target_sources(csdigit
    PRIVATE
        src/csdigit/csd.cpp
        src/csdigit/csd_multiplier.cpp
        src/csdigit/lcsre.cpp
)

target_include_directories(csdigit
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

# CLI executable
add_executable(csdigit_cli src/cli/main.cpp)
target_link_libraries(csdigit_cli csdigit)

# Tests
if(BUILD_TESTS)
    add_executable(csdigit_tests tests/test_csdigit.cpp)
    target_link_libraries(csdigit_tests csdigit doctest)
    
    # Add test cases
    add_test(NAME csdigit_tests COMMAND csdigit_tests)
endif()

# Examples
if(BUILD_EXAMPLES)
    add_executable(example_basic examples/basic_usage.cpp)
    target_link_libraries(example_basic csdigit)
    
    add_executable(example_cli examples/cli_usage.cpp)
    target_link_libraries(example_cli csdigit)
endif()

# Installation
install(TARGETS csdigit
    EXPORT csdigitTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

install(DIRECTORY include/csdigit DESTINATION include)

# Export targets
install(EXPORT csdigitTargets
    FILE csdigitTargets.cmake
    NAMESPACE csdigit::
    DESTINATION lib/cmake/csdigit
)

# Package configuration
include(CMakePackageConfigHelpers)
configure_package_config_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/csdigitConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/csdigitConfig.cmake
    INSTALL_DESTINATION lib/cmake/csdigit
)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/csdigitConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/csdigitConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/csdigitConfigVersion.cmake
    DESTINATION lib/cmake/csdigit
)