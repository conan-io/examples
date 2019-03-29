#!/usr/bin/env bash

set -e
pushd hello
conan create . user/channel -s build_type=Debug
conan create . user/channel -s build_type=Release
popd

pushd bye
conan create . user/channel -s build_type=Debug
conan create . user/channel -s build_type=Release
popd

pushd project

rm -rf "build"
mkdir build
pushd build

conan install .. -s build_type=Debug
conan install .. -s build_type=Release

cmake .. -DCMAKE_BUILD_TYPE=Debug
cmake --build .
./example

cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
./example

popd
popd
