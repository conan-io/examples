[![Build Status](https://travis-ci.com/uilianries/conan-protobuf-example.svg?branch=master)](https://travis-ci.com/uilianries/conan-protobuf-example)

# Conan Protobuf Example

## Protobuf example using Conan for blog post

- Conan.io blog: https://blog.conan.io

#### How to build
To build this project using cmake:

    git clone https://github.com/uilianries/conan-protobuf-example.git
    cd conan-protobuf-example
    mkdir build && cd build
    conan install ..
    cmake ..
    cmake --build .
    bin/sensor

#### Requirements
- CMake >=3.1.3
- C++ compiler with C++11 support (Protobuf requirement)
- Conan >=1.9.1

