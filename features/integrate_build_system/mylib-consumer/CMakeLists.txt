cmake_minimum_required(VERSION 2.8.12)
project(WafLibConsumer)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(demo main.cpp)
target_link_libraries(demo ${CONAN_LIBS})