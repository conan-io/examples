@echo off
conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan
conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -k -p emscripten.profile --build missing
conan install conanfile.txt  -pr emscripten.profile
