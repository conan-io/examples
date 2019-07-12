from conans import ConanFile, CMake
import os

class PkgbConan(ConanFile):
    name = "App"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = "src/*"
    requires = "PkgB/[>0.0]@user/testing", "PkgC/[>0.0]@user/testing"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()
        self.run(os.path.join(".", "bin", "app"))

    def package(self):
        self.copy("*app*", dst="bin", keep_path=False)
