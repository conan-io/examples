import os
from conans import ConanFile, tools


class GoInjectConan(ConanFile):
    name = "go-inject"
    version = "1.0"
    license = "MIT"
    homepage = "https://github.com/codegangsta/inject"
    no_copy_source = True

    def source(self):
        tools.get("https://github.com/codegangsta/inject/archive/v1.0-rc1.tar.gz",
                  sha256="22b265ea391a19de6961aaa8811ecfcc5bbe7979594e30663c610821cdad6c7b")

    def package(self):
        self.copy(pattern='*',
                  dst=os.path.join("src", "github.com", "codegangsta", "inject"),
                  src="inject-1.0-rc1", keep_path=True)
