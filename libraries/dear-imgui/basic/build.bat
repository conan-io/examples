@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake .. -G "Visual Studio 15 2017 Win64"
cmake --build . --config Release

Release\dear-imgui-conan.exe
