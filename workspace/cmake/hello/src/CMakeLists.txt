cmake_minimum_required(VERSION 2.8.12)

project(Hello)

if(EXISTS ${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
    include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo_multi.cmake)
else()
    include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
endif()

conan_basic_setup(NO_OUTPUT_DIRS)

add_library(hello hello.cpp)
conan_target_link_libraries(hello)
