# Conan GTest Example

## Getting Started

* Download conan client from [Conan.io](https://conan.io).

* Run the following command.

```bash
conan create . user/channel
```

The above command will export, build and test a conan package for a custom encryption library.

## Synopsis

[Conan.io](https://conan.io) example for [gtest](https://github.com/google/googletest/) project.

The project is using OpenSSL to build an encryption library, and using Google test to ensure that the library is built correctly.
The Google test library is required in the **test_package/conanfile.py**.

A different approach would be running the test at the end of the **build()** method in the root conanfile.py and require gtest library as a **build_require**,
so it would be only downloaded when the encryption library has to be built from sources.

With that approach, the **test_package** project could just run an example using/linking with the encryption library.
