cmake_minimum_required(VERSION 2.8)
project(MyHello CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_library(pkgb hello.cpp)

add_executable(greet greet.cpp)
target_link_libraries(greet PRIVATE pkgb)
