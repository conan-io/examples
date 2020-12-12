from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration


class Recipe(ConanFile):
    name = "app"
    version = "1.0"

    settings = "os", "compiler", "build_type", "arch"
    license = "MIT"
    author = "Conan Team"
    description = "App, requires nothing special"

    generators = "cmake", "cmake_find_package"
    exports_sources = "CMakeLists.txt", "src/main.cpp"

    options = {'use_hidden': [True, False]}
    default_options = {'use_hidden': False}

    def requirements(self):
        if self.options.use_hidden:
            self.requires("hidden/1.0")
        else:
            self.requires("library/1.0")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("app*", dst="bin", src="bin", keep_path=False)
        self.copy("LICENSE", dst="licenses", src=".", keep_path=False)
