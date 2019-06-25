cmake_minimum_required(VERSION 3.0)
project(PackageTest CXX)

find_package(bye CONFIG)
add_executable(example example.cpp)
target_link_libraries(example bye::bye)
