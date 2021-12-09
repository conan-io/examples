from conans import ConanFile
from conan.tools.cmake import CMake
from conan.tools.layout import cmake_layout

import os


class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain", "CMakeDeps"

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        cmd = os.path.join(self.cpp.build.bindirs[0], "example")
        self.run(cmd)