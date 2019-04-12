from conans import ConanFile, CMake


class ByeConan(ConanFile):
    name = "bye"
    version = "1.0"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake_paths"
    exports_sources = "src/*"
    requires = "hello/1.0@user/channel"

    def build(self):
        for bt in ("Debug", "Release"):
            cmake = CMake(self, build_type=bt)
            cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = "conan_paths.cmake"
            cmake.definitions["CMAKE_FIND_DEBUG_MODE"] = "ON"

            cmake.configure(source_folder="src")
            cmake.build()
            cmake.install()
