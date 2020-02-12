#!/usr/bin/env bash

set -ex

conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -pr emscripten.profile --build missing
conan install conanfile.txt  -pr emscripten.profile
