@ECHO ON

RMDIR /Q /S say/build
RMDIR /Q /S hello/build

MKDIR "say/build/Release"
MKDIR "hello/build"

conan export say/ say/0.1@user/channel
conan editable add say/ say/0.1@user/channel --layout=layout_vs

PUSHD say/build/Release

conan install ../..
cmake ../../src -DCMAKE_BUILD_TYPE=Release
cmake --build .

POPD
PUSHD hello/build

conan install ..
cmake ../src/ -DCMAKE_BUILD_TYPE=Release
cmake --build .

conan editable remove say/0.1@user/channel

bin/hello