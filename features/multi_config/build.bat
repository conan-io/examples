@ECHO ON

REM Create the multiconfig package
conan create . user/testing

REM Test same pacakge with both build type configurations: Debug & Release
conan test test_package hello/0.0.1@user/testing -s build_type=Debug
conan test test_package hello/0.0.1@user/testing -s build_type=Release
