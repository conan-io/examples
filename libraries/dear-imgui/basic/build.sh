#!/bin/bash

set -e
set -x

rm -rf build
mkdir build
pushd build

conan config set general.default_package_id_mode=full_version_mode
conan install ..
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
