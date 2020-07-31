
from conans import ConanFile

required_conan_version = ">=1.28"

class App2Conan(ConanFile):
    requires = "pkgc/[>0.0 <1.0]@user/testing"
