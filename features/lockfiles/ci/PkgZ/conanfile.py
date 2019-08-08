from conans import ConanFile, tools


class PkgzConan(ConanFile):
    exports_sources = "src/*"

    def build(self):
        tools.replace_in_file("src/helloz.h", "%V%", self.version)

    def package(self):
        self.copy("*.h", dst="include", src="src")
