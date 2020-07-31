from conans import ConanFile, tools

required_conan_version = ">=1.28"

class PkgaConan(ConanFile):
    settings = "build_type"
    exports_sources = "src/*"

    def build(self):
        tools.replace_in_file("src/helloa.h", "%V%", self.version)
        tools.replace_in_file("src/helloa.h", "%BT%", str(self.settings.build_type))

    def package(self):
        self.copy("*.h", dst="include", src="src")
