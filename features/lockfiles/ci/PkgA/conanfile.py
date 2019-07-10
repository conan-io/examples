from conans import ConanFile, tools


class PkgaConan(ConanFile):
    exports_sources = "src/*"
    requires = "PkgZ/[>0.0]@user/testing"

    def build(self):
        tools.replace_in_file("src/helloa.h", "%V%", self.version)

    def package(self):
        self.copy("*.h", dst="include", src="src")
