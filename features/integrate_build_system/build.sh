#!/bin/bash

conan create waf-generator user/channel
conan create waf-installer user/channel
conan create waf-build-helper user/channel
conan create waf-mylib user/channel

set -e
set -x

pushd mylib-consumer
rm -rf build
mkdir build
pushd build

conan install ..
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
