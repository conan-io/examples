cmake_minimum_required(VERSION 3.15)
project(app)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(app src/main.cpp)
target_link_libraries(app ${CONAN_LIBS})
