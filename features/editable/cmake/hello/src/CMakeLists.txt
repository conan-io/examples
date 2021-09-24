cmake_minimum_required(VERSION 2.8.12)

project(Hello)

find_package(say REQUIRED)

add_executable(hello hello.cpp)
target_link_libraries(hello say::say)
