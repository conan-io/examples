# set minimum cmake version
cmake_minimum_required(VERSION 3.5 FATAL_ERROR)

# project name and language
project(imgui-opencv LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(imgui-opencv 
    app/main.cpp 
    src/imgui_impl_glfw.cpp
    src/imgui_impl_opengl3.cpp
    src/gui_renderer.cpp
    src/downloader.cpp
    include/imgui_impl_glfw.h
    include/imgui_impl_opengl3.h
    include/gui_renderer.hpp
    include/downloader.h
)

target_link_libraries(imgui-opencv ${CONAN_LIBS})