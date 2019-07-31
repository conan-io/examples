@echo off

set CONAN_USER_HOME=C:/projects/CONAN_HOME/emscripten

conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -k -p emscripten.profile --build missing
conan install conanfile.txt  -pr emscripten.profile
