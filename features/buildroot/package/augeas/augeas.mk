################################################################################
#
# augeas
#
################################################################################

AUGEAS_VERSION = 1.11.0
AUGEAS_SITE = http://download.augeas.net
AUGEAS_INSTALL_STAGING = YES
AUGEAS_LICENSE = LGPL-2.1+
AUGEAS_LICENSE_FILES = COPYING
AUGEAS_DEPENDENCIES = host-pkgconf readline libxml2

# patching examples/Makefile.am, can be removed when updating from version 1.9.0
AUGEAS_AUTORECONF = YES

AUGEAS_CONF_OPTS = --disable-gnulib-tests

# Remove the test lenses which occupy about 1.4 MB on the target
define AUGEAS_REMOVE_TEST_LENSES
	rm -rf $(TARGET_DIR)/usr/share/augeas/lenses/dist/tests
endef
AUGEAS_POST_INSTALL_TARGET_HOOKS += AUGEAS_REMOVE_TEST_LENSES

$(eval $(autotools-package))
