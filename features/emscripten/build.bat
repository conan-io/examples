@echo off
set CONAN_USER_HOME=
set CONAN_USER_HOME_SHORT=1
set CONAN_USE_ALWAYS_SHORT_PATHS=1
conan remove conan-hello-emscripten/* -f
conan create . conan/testing  -k -p emscripten.profile --build missing
conan install conanfile.txt  -pr emscripten.profile
