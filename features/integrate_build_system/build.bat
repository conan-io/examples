@ECHO ON

conan create waf-generator user/channel
conan create waf-installer user/channel
conan create waf-build-helper user/channel
conan create waf-mylib user/channel

PUSHD mylib-consumer
RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake .. -G "%CMAKE_GENERATOR%"
cmake --build . --config Release
