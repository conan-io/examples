################################################################################
#
# python-patch
#
################################################################################

PYTHON_PATCH_VERSION = 1.16
PYTHON_PATCH_SOURCE = patch-$(PYTHON_PATCH_VERSION).zip
PYTHON_PATCH_SITE = https://files.pythonhosted.org/packages/da/74/0815f03c82f4dc738e2bfc5f8966f682bebcc809f30c8e306e6cc7156a99
PYTHON_PATCH_SETUP_TYPE = distutils
PYTHON_PATCH_LICENSE = MIT

define PYTHON_PATCH_EXTRACT_CMDS
	$(UNZIP) $(PYTHON_PATCH_DL_DIR)/$(PYTHON_PATCH_SOURCE) -d $(@D)
endef

$(eval $(python-package))
