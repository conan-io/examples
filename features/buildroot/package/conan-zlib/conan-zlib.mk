################################################################################
#
# Conan zlib package
#
################################################################################

CONAN_ZLIB_VERSION = 1.2.11
CONAN_ZLIB_INSTALL_STAGING = YES
CONAN_ZLIB_LICENSE = Zlib
CONAN_ZLIB_LICENSE_FILES = licenses/LICENSE
CONAN_ZLIB_SITE = $(call github,conan-io,conan-center-index,134dd3b84d629d27ba3474e01b688e9c0f25b9c8)
CONAN_ZLIB_REFERENCE = zlib/$(CONAN_ZLIB_VERSION)@
CONAN_ZLIB_SUBDIR = recipes/zlib/1.2.11

$(eval $(conan-package))
