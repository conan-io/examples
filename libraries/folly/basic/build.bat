@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake ..
cmake --build . --config Release

bin\folly_example.exe
