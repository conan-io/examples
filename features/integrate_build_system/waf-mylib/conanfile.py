import os
from conans import ConanFile, python_requires


class MyLibConan(ConanFile):
    python_requires("waf-build-helper/0.1@user/channel")
    settings = "os", "compiler", "build_type", "arch"
    name = "mylib-waf"
    version = "1.0"
    license = "MIT"
    author = "Conan Team"
    description = "Just a simple example of using Conan to package a Waf lib"
    topics = ("conan", "libs", "Waf")
    exports = "LICENSE"
    exports_sources = "wscript", "src/mylib.cpp", "include/mylib.hpp"
    build_requires = "waf/2.0.19@user/channel"

    def build(self):
        waf = self.python_requires["waf-build-helper"].module.WafBuildEnvironment(self)
        waf.configure()
        waf.build()

    def package(self):
        self.copy("*.hpp", dst="include", src="include", keep_path=False)
        self.copy("*.lib", dst="lib", src="build", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", src="build", keep_path=False)
        self.copy("*.so", dst="lib", src="build", keep_path=False)
        self.copy("*.a", dst="lib", src="build", keep_path=False)
        self.copy("LICENSE", dst="licenses", src=".", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["mylib"]
