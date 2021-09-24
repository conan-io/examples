@ECHO ON

RMDIR /Q /S say/build
RMDIR /Q /S hello/build


conan editable add say/ say/0.1@user/channel

PUSHD "say"

conan install .

PUSHD "build"
cmake ..
cmake --build . --config Release

POPD
POPD

MKDIR "hello/build"
PUSHD "hello/build"

conan install ..
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build . --config Release

"bin/hello.exe"

POPD
POPD

conan editable remove say/0.1@user/channel
