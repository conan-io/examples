from conans import ConanFile
from conans import CMake


class ConanGTestExample(ConanFile):
    """Build Conan GTest Example"""
    name = "conan-gtest-example"
    version = "0.1.0"
    url = "https://github.com/conan-io/examples"
    author = "lasote"
    license = "MIT"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    exports = "*"
    description = "Google Test example of use for conan.io"
    requires = "openssl/1.1.1e"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["encrypter"]
