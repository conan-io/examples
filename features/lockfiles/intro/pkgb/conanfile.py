from conans import ConanFile, CMake

required_conan_version = ">=1.28"

class PkgbConan(ConanFile):
    name = "pkgb"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = "src/*"
    requires = "pkga/[>0.0]@user/testing"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="src")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("greet*", dst="bin", src="bin", keep_path=False)

    def deploy(self):
        self.copy("*", dst="bin", src="bin", keep_path=False)
        self.copy_deps("*", dst="bin", src="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["pkgb"]
