cmake_minimum_required(VERSION 2.8.12)



set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

project(CameraApp)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

conan_basic_setup()

add_executable(camera  main.cpp)
target_link_libraries(camera ${CONAN_LIBS})

if(WIN32)
    target_link_libraries(camera vfw32.lib)
endif()