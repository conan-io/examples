if "%CMAKE_GENERATOR%"=="" (
    ECHO CMAKE_GENERATOR environment variable not defined. Please define the CMake generator in the CMAKE_GENERATOR environment variable.
)
else (
    @ECHO ON

    RMDIR /Q /S build
    MKDIR build
    PUSHD build

    conan install ..
    cmake .. -G "%CMAKE_GENERATOR%"
    cmake --build . --config Release

    bin\md5.exe
)
