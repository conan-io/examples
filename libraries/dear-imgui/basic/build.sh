#!/bin/bash

set -e
set -x

rm -rf build
mkdir build
pushd build

conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

conan install ..
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

conan remote remove bincrafters
