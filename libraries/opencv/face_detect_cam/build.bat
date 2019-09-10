@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake .. -G "Visual Studio 15 Win64"
cmake --build . --config Release

PUSHD bin
camera.exe

POPD
POPD
