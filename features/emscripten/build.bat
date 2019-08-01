@echo off

conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -k -p emscripten.profile --build missing
conan install conanfile.txt  -pr emscripten.profile
