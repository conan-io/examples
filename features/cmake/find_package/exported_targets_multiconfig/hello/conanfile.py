from conans import ConanFile, CMake


class HelloConan(ConanFile):
    name = "hello"
    version = "1.0"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports_sources = "src/*"

    def configure(self):
        # it is also necessary to remove the VS runtime
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    def build(self):
        for bt in ("Debug", "Release"):
            cmake = CMake(self, build_type=bt)
            cmake.configure(source_folder="src")
            cmake.build()
            cmake.install()
