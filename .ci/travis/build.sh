#!/bin/bash

set -e
set -x

if [ "${TRAVIS_OS_NAME}" == "osx" ] && [ "${CONAN_CURRENT_PAGE}" == "1" ]; then
    tox -v features/
elif [ "${TRAVIS_OS_NAME}" == "osx" ] && [ "${CONAN_CURRENT_PAGE}" == "2" ]; then
    tox -v libraries/
else
    tox -v
fi
