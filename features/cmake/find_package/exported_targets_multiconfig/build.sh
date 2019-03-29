#!/usr/bin/env bash

set -e
pushd hello
conan create . user/channel
popd

pushd bye
conan create . user/channel
popd

pushd project
rm -rf "build"
mkdir build
pushd build

conan install ..
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -DCMAKE_BUILD_TYPE=Debug
cmake --build .
./example

cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -DCMAKE_BUILD_TYPE=Release
cmake --build .
./example

popd
popd
