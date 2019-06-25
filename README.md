[![Build Status](https://travis-ci.org/conan-io/examples.svg?branch=master)](https://travis-ci.org/conan-io/examples)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/conan-io/examples?svg=true)](https://ci.appveyor.com/project/ConanCIintegration/examples)

# Conan Examples

Several Conan examples to complement the documentation and blog.

## Examples

### [Getting started with Conan](libraries/poco/md5)

Example how to use Conan to consume binaries.

Documentation: https://docs.conan.io/en/latest/getting_started.html

### [Package development flow](features/package_development_flow)

Example how to use Conan commands to develop a package recipe.

Documentation: https://docs.conan.io/en/latest/developing_packages/package_dev_flow.html

### [Workspace](features/workspace)

Example how to use Conan Workspaces.

Documentation: https://docs.conan.io/en/latest/developing_packages/workspaces.html

### [Serializing your data with Protobuf](libraries/protobuf/serialization)

Demonstrate how to use Protobuf to serialize data between C++ and Python.

Blog Post: https://blog.conan.io/2019/03/06/Serializing-your-data-with-Protobuf.html

### [Using Facebook Folly with Conan](libraries/folly/basic)

Demonstrate how to use Folly to validate an URI using Futures, FBString, Executors, and Format.

Blog Post: https://blog.conan.io/2018/12/03/Using-Facebook-Folly-with-Conan.html

### [An introduction to Dear ImGui and how to use with Conan](libraries/dear-imgui/basic)

Demonstrate how to use Dear ImGui with Conan to add a GUI to an OpenGL3 application. 

### [Exporting targets with CMake and reuse with find_package()](features/cmake/find_package/exported_targets_multiconfig)

Use CMake to declare, export and install the targets of some libraries and using Conan to reuse them with
``find_package`` and the multi-configuration project.

### [Using the cmake_find_package_multi generator](features/cmake/find_package/find_cmake_multi_generator_targets)

Demonstrate how to use the ``cmake_find_package_multi`` generator to integrate seamlessly CMake with Conan
using ``find_package`` in a multi-configuration project.


### [Multi-configuration package (N configs -> 1 package)](features/multi_config)

Example on how to create multi-configuration debug/release packages covering the N configs -> 1 package use case:

- Remove the ``build_type`` from settings.
- Have a CMake script that differentiate debug and release artifacts (``set_target_properties(hello PROPERTIES DEBUG_POSTFIX _d)``).
- Have a ``build()`` that builds both configs.
- Have a ``package_info()`` method that accounts for both configs ``self.cpp_info.debug.libs``, etc.

Documentation: https://docs.conan.io/en/latest/creating_packages/package_approaches.html#n-configs-1-package

## How can I reproduce the build steps?

All our examples can be built on Windows, Linux and Mac. If you are interested to reproduce
the examples in your environment, please follow the CI scripts:

* Linux / MacOS: [travis.yml](.travis.yml)
* Windows: [appveyor](appveyor.yml)

In addition, you should be able to inspect our logs by clicking on the badges at the top of this file.

## LICENSE
[MIT](LICENSE)
