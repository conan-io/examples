#!/bin/bash

set -e
set -x

rm -rf say/cmake-build-release
rm -rf hello/cmake-build-release


conan editable add say/ say/0.1@user/channel

pushd say
conan install .
mkdir cmake-build-release
pushd cmake-build-release
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../build/generators/conan_toolchain.cmake
cmake --build .
popd
popd

mkdir hello/cmake-build-release
pushd hello/cmake-build-release
conan install ..
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build .
./hello
popd

# Modification to code
pushd say/cmake-build-release
cp ../src/say2.cpp ../src/say.cpp
cmake --build .
popd

# build consumer again
pushd hello/cmake-build-release
cmake --build .
./hello
popd

conan editable remove say/0.1@user/channel
