
from conans import ConanFile


class PkgDConan(ConanFile):
    requires = "pkgb/[>0.0 <1.0]@user/testing", "pkgc/[>0.0  <1.0]@user/testing"
