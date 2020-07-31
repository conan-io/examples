
from conans import ConanFile

required_conan_version = ">=1.28"

class App1Conan(ConanFile):
    settings = "build_type"
    requires = "libd/[>0.0 <1.0]@user/testing"
