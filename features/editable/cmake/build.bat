@ECHO ON

RMDIR /Q /S say\build
RMDIR /Q /S hello\build

REM Put say package in editable mode, and build it
conan editable add say/ say/0.1@user/channel
MKDIR "say/build"
PUSHD "say/build"
conan install ..
cmake ..
cmake --build . --config Release
cmake --build . --config Debug
POPD

REM Build hello consumer
MKDIR "hello/build"
PUSHD "hello/build"
conan install ..
conan install .. -s build_type=Debug
cmake .. -DCMAKE_TOOLCHAIN_FILE=conan_toolchain.cmake
cmake --build . --config Release
cmake --build . --config Debug
"Release/hello.exe"
"Debug/hello.exe"
POPD

REM Do a modification in the source code of the editable say
PUSHD "say/build"
COPY ..\src\say2.cpp ..\src\say.cpp /Y
cmake --build . --config Release
cmake --build . --config Debug
POPD

REM Build and execute the consumer depending on the editable
PUSHD "hello/build"
cmake --build . --config Release
cmake --build . --config Debug
"Release/hello.exe"
"Debug/hello.exe"
POPD


conan editable remove say/0.1@user/channel
