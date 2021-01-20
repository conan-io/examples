################################################################################
#
# gadgetfs-test
#
################################################################################

GADGETFS_TEST_SOURCE = gadgetfs-test.tar.bz2
GADGETFS_TEST_SITE = http://mirror.egtvedt.no/avr32linux.org/twiki/pub/Main/GadgetFsTest

GADGETFS_TEST_MAKEOPTS = CC="$(TARGET_CC)" CFLAGS="$(TARGET_CFLAGS)" LDFLAGS="$(TARGET_LDFLAGS)"

ifeq ($(BR2_PACKAGE_GADGETFS_TEST_USE_AIO),y)
GADGETFS_TEST_DEPENDENCIES = libaio
GADGETFS_TEST_MAKEOPTS += USE_AIO=y
endif

define GADGETFS_TEST_BUILD_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D) $(GADGETFS_TEST_MAKEOPTS)
endef

define GADGETFS_TEST_INSTALL_TARGET_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D) DESTDIR=$(TARGET_DIR) prefix=/usr install
endef

$(eval $(generic-package))
