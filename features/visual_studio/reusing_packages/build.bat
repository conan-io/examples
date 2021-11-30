@echo off

pushd ..\creating_packages
conan create . demo/testing
popd

conan create . demo/testing
