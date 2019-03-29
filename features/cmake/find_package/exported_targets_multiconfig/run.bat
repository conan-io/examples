PUSHD hello
conan create . user/channel
POPD

PUSHD bye
conan create . user/channel
POPD

PUSHD project
rd /s /q "build"
mkdir build
PUSHD BUILD

conan install ..
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -G "Visual Studio 15 2017 Win64"
cmake --build . --config Debug
cmake --build . --config Release

Debug\example.exe
Release\example.exe

POPD
POPD
