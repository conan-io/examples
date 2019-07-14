import os

from conans import ConanFile, python_requires

base = python_requires("waf-build-helper/0.1@user/channel")


class TestWafConan(base.get_conanfile()):
    settings = "os", "compiler", "build_type", "arch", "arch_build"
    name = "waf-consumer"
    generators = "Waf"
    requires = "mylib-waf/1.0@user/channel"
    build_requires = "WafGen/0.1@user/channel", "waf/2.0.18@user/channel"
    exports_sources = "wscript", "main.cpp"

    def build(self):
        waf = base.WafBuildEnvironment(self)
        waf.configure()
        waf.build()