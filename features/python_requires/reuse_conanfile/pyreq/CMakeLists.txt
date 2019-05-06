cmake_minimum_required(VERSION 2.8)
project(MyCommonCMakeLists CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

file(GLOB sources src/*)

add_library(mylibrary ${sources})
