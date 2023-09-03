from conans import ConanFile, tools, CMake
from conans.errors import ConanInvalidConfiguration


class Recipe(ConanFile):
    name = "hidden"
    version = "1.0"

    settings = "os", "compiler", "build_type", "arch"
    license = "MIT"
    author = "Conan Team"
    description = "Library requires C++14 to build, but API is C++11 compatible"

    generators = "cmake"
    exports_sources = "CMakeLists.txt", "src/mylib.cpp", "include/mylib.h"

    def configure(self):
        if self.settings.compiler.get_safe('cppstd'):
            tools.check_min_cppstd(self, "11")

    def validate(self):
        if self.settings.compiler.get_safe('cppstd'):
            tools.check_min_cppstd(self, "14")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="include", keep_path=False)
        self.copy("*.lib", dst="lib", src="lib", keep_path=False)
        self.copy("*.a", dst="lib", src="lib", keep_path=False)
        self.copy("LICENSE", dst="licenses", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mylib"]

    def package_id(self):
        for cppstd in ("11", "14", "17", "20"):
            for gnu in ("", "gnu"):
                compatible_pkg = self.info.clone()
                compatible_pkg.settings.compiler.cppstd = "{}{}".format(gnu, cppstd)
                self.compatible_packages.append(compatible_pkg)
