#!/bin/bash

set -e
set -x

rm -rf say/build
mkdir -p say/build/Release
rm -rf hello/build
mkdir hello/build

conan export say/ say/0.1@user/channel
conan editable add say/ say/0.1@user/channel --layout=layout_gcc

pushd say/build/Release

conan install ../..
cmake ../../src -DCMAKE_BUILD_TYPE=Release
cmake --build .

popd
pushd hello/build

conan install ..
cmake ../src/ -DCMAKE_BUILD_TYPE=Release
cmake --build .

conan editable remove say/0.1@user/channel

bin/hello