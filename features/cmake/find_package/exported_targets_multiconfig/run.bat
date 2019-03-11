cd hello && conan create . user/channel && cd ..
cd bye && conan create . user/channel && cd ..
cd project && mkdir build && cd build && conan install .. && cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_paths.cmake -G "Visual Studio 15 2017 Win64"
cmake --build . --config Debug
Debug/example.exe
cmake --build . --config Release
Release/example.exe
