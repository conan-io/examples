from conans import ConanFile, AutoToolsBuildEnvironment
from conans import tools


class AppConan(ConanFile):
    name = "app"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*"
    requires = "hello/0.1@user/testing"

    def build(self):
        with tools.chdir("src"):
            atools = AutoToolsBuildEnvironment(self)
            atools.make()

    def package(self):
        self.copy("*app", dst="bin", keep_path=False)
        self.copy("*app.exe", dst="bin", keep_path=False)

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
