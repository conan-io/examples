import os
from conans import ConanFile, python_requires


base = python_requires("waf-build-helper/0.1@user/channel")


class MyLibConan(base.get_conanfile()):
    settings = "os", "compiler", "build_type", "arch", "arch_build"
    name = "mylib-waf"
    version = "1.0"
    license = "MIT"
    author = "Conan Team"
    description = "Just a simple example of using Conan to package a Waf lib"
    topics = ("conan", "libs", "Waf")
    exports = "wscript", "src/mylib.cpp", "include/mylib.hpp", "LICENSE"
    build_requires = "waf/2.0.18@user/channel"

    def build(self):
        waf = base.WafBuildEnvironment(self)
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
