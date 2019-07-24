import os

from conans import ConanFile, python_requires

waf_import = python_requires("waf-build-helper/0.1@user/channel")


class TestWafConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    name = "waf-consumer"
    generators = "Waf"
    requires = "mylib-waf/1.0@user/channel"
    build_requires = "WafGen/0.1@user/channel", "waf/2.0.18@user/channel"
    exports_sources = "wscript", "main.cpp"

    def build(self):
        waf = waf_import.WafBuildEnvironment(self)
        waf.configure()
        waf.build()
