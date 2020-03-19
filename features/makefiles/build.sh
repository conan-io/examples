#!/usr/bin/env bash

set -ex

pushd hellolib
conan create . user/testing
popd

pushd helloapp
conan create . user/testing

conan install app/0.1@user/testing

./bin/app
