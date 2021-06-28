cmake_minimum_required(VERSION 3.15)
project(hello CXX)

message(STATUS "CMAKE VERSION = ${CMAKE_VERSION}!!!")

add_library(hello hello.cpp)
