#!/bin/bash

set -e
set -x

rm -rf build
mkdir build
pushd build

conan install .. -pr:h=default -pr:b=default --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build .

./sensor

python ../main.py
