from conans import ConanFile, CMake


class HelloConan(ConanFile):
    name = "hello"
    version = "1.0"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "src/*"

    def build(self):
        for bt in ("Debug", "Release"):
            cmake = CMake(self, build_type=bt)
            cmake.configure(source_folder="src")
            cmake.build()
            cmake.install()
