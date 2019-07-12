#!/bin/bash

set -e
set -x

# Print commands
conan config set log.print_run_commands=True

# Create the multiconfig package
conan create . user/testing

# Test same pacakge with both built type configurations
conan test test_package hello/0.0.1@user/testing -s build_type=Debug
conan test test_package hello/0.0.1@user/testing -s build_type=Release
