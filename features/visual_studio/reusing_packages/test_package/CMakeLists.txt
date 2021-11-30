project(PackageTest CXX)
cmake_minimum_required(VERSION 3.0)

find_package(Chat REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example Chat::Chat)
