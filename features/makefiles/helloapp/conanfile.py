from conans import ConanFile
from conans import tools
from conan.tools.gnu import Autotools


class AppConan(ConanFile):
    name = "app"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*"
    requires = "hello/0.1@user/testing"
    generators = "AutotoolsDeps", "AutotoolsToolchain"

    def build(self):
        with tools.chdir("src"):
            atools = Autotools(self)
            atools.make()

    def package(self):
        self.copy("*app", dst="bin", keep_path=False)
        self.copy("*app.exe", dst="bin", keep_path=False)

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
