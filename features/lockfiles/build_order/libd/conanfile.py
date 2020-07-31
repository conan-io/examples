
from conans import ConanFile

required_conan_version = ">=1.28"

class LibDConan(ConanFile):
    requires = "libb/[>0.0 <1.0]@user/testing", "libc/[>0.0  <1.0]@user/testing"
