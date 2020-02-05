@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan & true

conan install ..
cmake .. -G "%CMAKE_GENERATOR%"
cmake --build . --config Release
