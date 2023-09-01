import os
from conans import ConanFile, tools


class GoMartiniConan(ConanFile):
    name = "go-martini"
    version = "1.0"
    requires = "go-inject/1.0@"
    license = "MIT"
    homepage = "https://github.com/go-martini/martini"
    no_copy_source = True

    def source(self):
        tools.get("https://github.com/go-martini/martini/archive/v1.0.tar.gz",
                  sha256="3db135845d076d611f4420e0500e91625543a6b00dc9431cbe45d3571741281b")

    def package(self):
        self.copy(pattern="*", dst=os.path.join("src", "github.com", "go-martini", "martini"),
                  src="martini-1.0", keep_path=True)
