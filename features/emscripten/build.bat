@echo off

conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -pr emscripten.profile -s arch_build=x86_64 --build missing
conan install conanfile.txt  -pr emscripten.profile -s arch_build=x86_64
