#!/bin/bash

set -e
set -x

rm -rf build
rm -rf say/build
rm -rf hello/build
rm -rf chat/build
mkdir build

pushd build

conan workspace install ../conanws_gcc.yml
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

popd
chat/build/Release/app
