from conans import ConanFile


class PkgbConan(ConanFile):
    requires = "pkga/[>0.0 <1.0]@user/testing"
