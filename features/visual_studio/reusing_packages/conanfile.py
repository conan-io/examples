from conans import ConanFile
from conan.tools.microsoft import MSBuild


class ChatConan(ConanFile):
    name = "Chat"
    version = "0.1"
    license = "MIT"
    url = "https://github.com/conan-io/examples"
    requires = "Hello/0.1@demo/testing"
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "src/*", "build/*"
    generators = "MSBuildDeps", "MSBuildToolchain"

    def build(self):
        msbuild = MSBuild(self)
        msbuild.build("build/ChatLib/ChatLib.sln")

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ChatLib"]
