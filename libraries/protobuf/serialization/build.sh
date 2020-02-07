#!/bin/bash

set -e
set -x

rm -rf build
mkdir build
pushd build

conan install ..
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .

bin/sensor


python --copies -m venv _exproto
source _exproto/bin/activate && pip install -U protobuf
_exproto/bin/python ../main.py
