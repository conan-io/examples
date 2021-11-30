@echo off

pushd ..\creating_packages
conan create . demo/testing
conan create . demo/testing -s compiler=msvc -s compiler.version=19.15 -s compiler.runtime=static -s compiler.cppstd=17
popd

conan create . demo/testing
conan create . demo/testing -s compiler=msvc -s compiler.version=19.15 -s compiler.runtime=static -s compiler.cppstd=17
