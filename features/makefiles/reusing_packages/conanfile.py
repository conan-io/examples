from conans import ConanFile
from conan.tools.gnu import Autotools


class AppConan(ConanFile):
    name = "app"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "Makefile", "src/*"
    requires = "hello/0.1@demo/testing"
    generators = "AutotoolsDeps", "AutotoolsToolchain"

    def layout(self):
        self.folders.source = "src"

    def build(self):
        atools = Autotools(self)
        atools.make()

    def package(self):
        self.copy("*app", dst="bin", keep_path=False)
        self.copy("*app.exe", dst="bin", keep_path=False)
