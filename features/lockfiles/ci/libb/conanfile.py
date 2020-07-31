from conans import ConanFile

required_conan_version = ">=1.28"

class LibBConan(ConanFile):
    settings = "build_type"
    requires = "liba/[>0.0 <1.0]@user/testing"
# Some changes# Some changes# Some changes# Some changes# Some changes# Some changes# Some changes# Some changes# Some changes# Some changes