if "%CMAKE_GENERATOR%"=="" (
    ECHO CMAKE_GENERATOR environment variable not defined. Please define the CMake generator in the CMAKE_GENERATOR environment variable.
)
else (
    @ECHO ON
    RMDIR /Q /S say/build
    RMDIR /Q /S hello/build
    RMDIR /Q /S chat/build
    RMDIR /Q /S build

    MKDIR build
    PUSHD build

    conan workspace install ../conanws_vs.yml
    conan workspace install ../conanws_vs.yml -s build_type=Debug
    cmake .. -G "%CMAKE_GENERATOR%"
    cmake --build . --config Release
    cmake --build . --config Debug

    POPD

    chat\build\Release\app.exe
    chat\build\Debug\app.exe
)
