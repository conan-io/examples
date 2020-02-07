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

python -m venv _exproto
ls -la 
ls -la _exproto
ls -la _exproto/bin
_exproto/bin/pip install -U protobuf
_exproto/bin/python ../main.py
