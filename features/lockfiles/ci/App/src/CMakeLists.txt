cmake_minimum_required(VERSION 2.8)
project(MyApp CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(app app.cpp)
target_link_libraries(app ${CONAN_LIBS})
