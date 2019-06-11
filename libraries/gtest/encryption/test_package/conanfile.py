from conans import ConanFile
from conans import CMake


class TestConanGTestExample(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "gtest/1.8.1@bincrafters/stable"
    default_options = {"gtest:shared": True}

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def test(self):
        cmake = self._configure_cmake()
        cmake.test()
