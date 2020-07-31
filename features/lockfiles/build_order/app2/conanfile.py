
from conans import ConanFile

required_conan_version = ">=1.28"

class App2Conan(ConanFile):
    requires = "libc/[>0.0 <1.0]@user/testing"
