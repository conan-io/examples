#!/bin/bash

set -e
set -x

rm -rf tmp

conan source  . --source-folder=tmp/source
conan install . --install-folder=tmp/build
conan build   . --source-folder=tmp/source --build-folder=tmp/build
conan package . --source-folder=tmp/source --build-folder=tmp/build --package-folder=tmp/package

# NOTE: Use --force to prevent ERROR: Package already exists
conan export-pkg . user/testing --source-folder=tmp/source --build-folder=tmp/build --force

# You can also test the package that was just exported
conan test test_package Hello/1.0@user/testing

# Finally, run a full create, does all of the above + test_package
conan create . user/testing
