
from conans import ConanFile


class App1Conan(ConanFile):
    requires = "pkgd/[>0.0 <1.0]@user/testing"
