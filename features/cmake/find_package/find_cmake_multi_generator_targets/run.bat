PUSHD hello
conan create . user/channel -s build_type=Debug
conan create . user/channel -s build_type=Release
POPD

PUSHD bye
conan create . user/channel -s build_type=Debug
conan create . user/channel -s build_type=Release
POPD

PUSHD project

rd /s /q "build"
mkdir build
PUSHD BUILD
conan install .. -s build_type=Debug
conan install .. -s build_type=Release
cmake .. -G "Visual Studio 15 2017 Win64"
cmake --build . --config Debug
cmake --build . --config Release
Debug\example.exe
Release\example.exe

POPD
POPD
