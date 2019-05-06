import os
import shutil
from conans import ConanFile, CMake, tools
from scm_utils import get_version


class PythonRequires(ConanFile):
    name = "pyreq"
    version = "version"

    exports = "scm_utils.py"
    exports_sources = "CMakeLists.txt"


def get_conanfile():
    class BaseConanFile(ConanFile):
        name = "wont-be-inherited"
        version = "wont-be-inherited"
        
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = "cmake"
        exports_sources = "src/*"

        def source(self):
            # Copy the CMakeLists.txt file exported with the python requires
            pyreq = self.python_requires["pyreq"]
            shutil.copy(src=os.path.join(pyreq.exports_sources_folder, "CMakeLists.txt"), dst=self.source_folder)

            # Rename the project to match the consumer name
            tools.replace_in_file(os.path.join(self.source_folder, "CMakeLists.txt"),
                                            "add_library(mylibrary ${sources})",
                                            "add_library({} ${{sources}})".format(self.name))

        def build(self):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

        def package(self):
            self.copy("*.h", dst="include", src="src")
            self.copy("*.lib", dst="lib", keep_path=False)
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.dylib*", dst="lib", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)

        def package_info(self):
            self.cpp_info.libs = [self.name]

    return BaseConanFile
