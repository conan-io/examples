################################################################################
#
# python-conan
#
################################################################################

PYTHON_CONAN_VERSION = 1.18.0
PYTHON_CONAN_SOURCE = conan-$(PYTHON_CONAN_VERSION).tar.gz
PYTHON_CONAN_SITE = https://files.pythonhosted.org/packages/30/26/27483b3e8cc0f1af517e3cd1e8f0a59289c8636a46449d4401948f2e443e
PYTHON_CONAN_SETUP_TYPE = setuptools
PYTHON_CONAN_LICENSE = MIT
PYTHON_CONAN_LICENSE_FILES = LICENSE.md
HOST_PYTHON_CONAN_DEPENDENCIES = host-python-pluginbase python-semver python-patch python-bottle

$(eval $(host-python-package))
