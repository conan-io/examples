@echo off

conan remove conan-hello-emscripten/* -f
conan create . conan/testing  --profile:host=emscripten.profile --profile:build=default --build missing
conan install conanfile.txt  --profile:host=emscripten.profile --profile:build=default --build missing
