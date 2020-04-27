#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools


class HelloConan(ConanFile):
    name = "hello"
    version = "0.0.1"
    settings = "os", "compiler", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
    exports_sources = "hello.h", "hello.cpp", "CMakeLists.txt"

    # Alternative 1: Remove runtime and use always default (MD/MDd)
    def configure(self):
        if self.settings.compiler == "Visual Studio":
            del self.settings.compiler.runtime

    # Alternative 2: if you want to keep MD-MDd/MT-MTd configuration
    # def package_id(self):
    #     if self.settings.compiler == "Visual Studio":
    #         if "MD" in self.settings.compiler.runtime:
    #             self.info.settings.compiler.runtime = "MD/MDd"
    #         else:
    #             self.info.settings.compiler.runtime = "MT/MTd"

    def build(self):
        # Alternative 1: Use always default runtime (MD/MDd)
        cmake_debug = CMake(self, build_type="Debug")
        # Alternative 2: if you want to keep MD-MDd/MT-MTd configuration (uncomment section in CMakeLists.txt)
        # cmake_debug.defintions["CONAN_LINK_RUNTIME_MULTI"] = cmake_debug.definitions["CONAN_LINK_RUNTIME"]
        # cmake_debug.definitions["CONAN_LINK_RUNTIME"] = False
        cmake_debug.configure(build_folder="Debug")
        cmake_debug.build()

        if self.settings.os != "Windows":
            print_strings(self, "Debug/lib/libhello_d.a", "DEBUG")

        cmake_release = CMake(self, build_type="Release")
        # Alternative 2: if you want to keep MD-MDd/MT-MTd configuration (uncomment section in CMakeLists.txt)
        # cmake_release.defintions["CONAN_LINK_RUNTIME_MULTI"] = cmake_release.definitions["CONAN_LINK_RUNTIME"]
        # cmake_release.definitions["CONAN_LINK_RUNTIME"] = False
        cmake_release.configure()
        cmake_release.build()

        if self.settings.os != "Windows":
            print_strings(self, "lib/libhello.a", "RELEASE")

    def package(self):
        self.copy("*.h", dst="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.dylib*", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.release.libs = ["hello"]
        self.cpp_info.debug.libs = ["hello_d"]

def print_strings(conanfile, library, build_type):
    # This function is printing the strings contained in the binary
    #  trying to add insights about a issue related to the multi_config
    #  generator in Mac CI
    conanfile.output.info("*"*30)
    conanfile.output.info(build_type)
    conanfile.output.info("*"*30)
    conanfile.run("strings {} | grep Hello".format(library))
    conanfile.output.info("*"*30)
