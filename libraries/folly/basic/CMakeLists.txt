cmake_minimum_required(VERSION 3.1.3)
project(folly_example CXX)

set(CMAKE_VERBOSE_MAKEFILE ON)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} CONAN_PKG::folly)
set_target_properties(${PROJECT_NAME} PROPERTIES CXX_STANDARD 14)