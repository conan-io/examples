@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake .. -G "%CMAKE_GENERATOR%"
cmake --build . --config Release

bin\dear-imgui-conan.exe
