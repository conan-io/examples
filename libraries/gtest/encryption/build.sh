#!/bin/bash

set -e
set -x

rm -rf build source package

conan source . --source-folder source
conan install . --install-folder build
conan build . --source-folder source --build-folder build
conan package . --source-folder source --build-folder build --package-folder package
conan export-pkg . conan/testing --package-folder package

conan test test_package conan-gtest-example/0.1.0@conan/testing
