
from conans import ConanFile

required_conan_version = ">=1.28"

class PkgDConan(ConanFile):
    requires = "pkgb/[>0.0 <1.0]@user/testing", "pkgc/[>0.0  <1.0]@user/testing"
