from conans import ConanFile
from conans import tools
from conan.tools.gnu import Autotools


class HelloConan(ConanFile):
    name = "hello"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*"
    generators = "AutotoolsToolchain"

    def build(self):
        with tools.chdir("src"):
            atools = Autotools(self)
            atools.make()

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]
