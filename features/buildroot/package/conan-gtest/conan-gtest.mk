################################################################################
#
# Conan GTest package
#
################################################################################

CONAN_GTEST_VERSION = 1.8.1
CONAN_GTEST_INSTALL_STAGING = YES
CONAN_GTEST_LICENSE = BSD-3-Clause
CONAN_GTEST_LICENSE_FILES = licenses/LICENSE
CONAN_GTEST_SITE = $(call github,conan-io,conan-center-index,134dd3b84d629d27ba3474e01b688e9c0f25b9c8)
CONAN_GTEST_REFERENCE = zlib/$(CONAN_GTEST_VERSION)@
CONAN_ZLIB_SUBDIR = recipes/gtest/all

$(eval $(conan-package))
