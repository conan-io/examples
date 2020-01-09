pushd hello
conan create . user/channel -s build_type=Debug
conan create . user/channel -s build_type=Release
popd

pushd bye
conan create . user/channel -s build_type=Debug
conan create . user/channel -s build_type=Release
popd

pushd project

rd /s /q "build"
mkdir build
pushd BUILD
conan install .. -s build_type=Debug
conan install .. -s build_type=Release
cmake ..
cmake --build . --config Debug
cmake --build . --config Release
Debug\example.exe
Release\example.exe

popd
popd
