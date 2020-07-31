
from conans import ConanFile


class App2Conan(ConanFile):
    requires = "pkgc/[>0.0 <1.0]@user/testing"
