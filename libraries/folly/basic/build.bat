@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install .. --build missing
cmake .. -G "%CMAKE_GENERATOR%"
cmake --build . --config Release

bin\folly_example.exe
