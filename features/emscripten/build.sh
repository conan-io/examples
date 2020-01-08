#!/usr/bin/env bash

set -ex

conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -k -p emscripten.profile
conan install conanfile.txt  -pr emscripten.profile
