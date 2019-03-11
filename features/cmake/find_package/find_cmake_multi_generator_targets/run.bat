cd hello && conan create . user/channel -s build_type=Debug && conan create . user/channel -s build_type=Release && cd ..
cd bye &&   conan create . user/channel -s build_type=Debug && conan create . user/channel -s build_type=Release && cd ..

cd project_targets && mkdir build && cd build
conan install .. -s build_type=Debug
conan install .. -s build_type=Release
cmake .. -G "Visual Studio 15 2017 Win64"
cmake --build . --config Debug
cmake --build . --config Release
Debug\example.exe
Release\example.exe

cd project_global && mkdir build && cd build
conan install .. -s build_type=Debug
conan install .. -s build_type=Release
cmake .. -G "Visual Studio 15 2017 Win64"
cmake --build . --config Debug
cmake --build . --config Release
Debug\example.exe
Release\example.exe
