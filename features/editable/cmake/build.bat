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
cmake ../src/
cmake --build . --config Release

"bin/hello.exe"

conan editable remove say/0.1@user/channel
