from conans import ConanFile


class PkgcConan(ConanFile):
    requires = "pkga/[>0.0 <1.0]@user/testing"
