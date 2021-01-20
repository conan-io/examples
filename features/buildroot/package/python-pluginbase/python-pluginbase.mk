################################################################################
#
# python-pluginbase
#
################################################################################

PYTHON_PLUGINBASE_VERSION = 0.7
PYTHON_PLUGINBASE_SOURCE = pluginbase-$(PYTHON_PLUGINBASE_VERSION).tar.gz
PYTHON_PLUGINBASE_SITE = https://files.pythonhosted.org/packages/6e/f4/1db0a26c1c7fad81a1214ad1b02839a7bd98d8ba68f782f6edcc3d343441
PYTHON_PLUGINBASE_SETUP_TYPE = setuptools
PYTHON_PLUGINBASE_LICENSE = BSD-3-Clause
PYTHON_PLUGINBASE_LICENSE_FILES = LICENSE

$(eval $(python-package))
$(eval $(host-python-package))
