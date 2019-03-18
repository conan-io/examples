[![Build Status](https://travis-ci.org/conan-io/examples.svg?branch=master)](https://travis-ci.org/conan-io/examples)
[![Build Status AppVeyor](https://ci.appveyor.com/api/projects/status/github/conan-io/examples?svg=true)](https://ci.appveyor.com/project/ConanCIintegration/examples)

# Conan Examples

## Several conan examples, to extend the docs.

# Examples

#### [Getting started with Conan](libraries/poco/md5)

Example how to use Conan to consume binaries.

Documentation: https://docs.conan.io/en/latest/getting_started.html

#### [Workspace](features/workspace)

Example how to use Conan Workspaces.

Documentation: https://docs.conan.io/en/latest/developing_packages/workspaces.html

#### [Serializing your data with Protobuf](libraries/protobuf/serialization)

Demonstrate how to use Protobuf to serialize data between C++ and Python.

Blog Post: https://blog.conan.io/2019/03/06/Serializing-your-data-with-Protobuf.html

#### [Using Facebook Folly with Conan](libraries/folly/basic)

Demonstrate how to use Folly to validate an URI using Futures, FBString, Executors, and Format.

Blog Post: https://blog.conan.io/2018/12/03/Using-Facebook-Folly-with-Conan.html

#### How can I reproduce the build steps?

All our examples can be built on Windows, Linux and Mac. If you are insterested to reproduce
the examples in your enviroment, please follow the CI scripts:

* Linux / MacOS: [travis.yml](.travis.yml)
* Windows: [appveyor](appveyor.yml)

In addition, you should be able to inspect our logs by clicking on the badges at the top of this file.

#### LICENSE
[MIT](LICENSE)
