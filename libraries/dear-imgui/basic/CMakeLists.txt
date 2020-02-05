cmake_minimum_required(VERSION 3.0)
project(dear-imgui-conan CXX)

set(CMAKE_PREFIX_PATH ${CMAKE_BINARY_DIR})
set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})

find_package(imgui REQUIRED)

add_executable(dear-imgui-conan main.cpp)
target_link_libraries(dear-imgui-conan imgui::imgui)
