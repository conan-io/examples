cmake_minimum_required(VERSION 2.8.12)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(example example.cpp)
if (CONAN_SETTINGS_BUILD_TYPE STREQUAL "Debug")
    target_link_libraries(example ${CONAN_LIBS_DEBUG})
else()
    target_link_libraries(example ${CONAN_LIBS_RELEASE})
endif()
