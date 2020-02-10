@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan remote add bincrafters https://api.bintray.com/conan/bincrafters/public-conan

conan install ..
cmake ..
cmake --build . --config Release

conan remote remove bincrafters