pushd hello
conan create . user/channel
popd

pushd bye
conan create . user/channel
popd

pushd project
rd /s /q "build"
mkdir build
pushd build

conan install ..
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -G "Visual Studio 15 2017 Win64"
cmake --build . --config Debug
cmake --build . --config Release

Debug\example
Release\example

popd
popd
