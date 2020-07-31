
from conans import ConanFile

required_conan_version = ">=1.28"

class App1Conan(ConanFile):
    requires = "libd/[>0.0 <1.0]@user/testing"
