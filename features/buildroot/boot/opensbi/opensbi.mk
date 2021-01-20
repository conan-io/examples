################################################################################
#
# opensbi
#
################################################################################

OPENSBI_VERSION = 0.4
OPENSBI_SITE = $(call github,riscv,opensbi,v$(OPENSBI_VERSION))
OPENSBI_LICENSE = BSD-2-Clause
OPENSBI_LICENSE_FILES = COPYING.BSD
OPENSBI_INSTALL_TARGET = NO
OPENSBI_INSTALL_STAGING = YES

OPENSBI_MAKE_ENV = \
	CROSS_COMPILE=$(TARGET_CROSS)

OPENSBI_PLAT = $(call qstrip,$(BR2_TARGET_OPENSBI_PLAT))
ifneq ($(OPENSBI_PLAT),)
OPENSBI_MAKE_ENV += PLATFORM=$(OPENSBI_PLAT)
endif

define OPENSBI_BUILD_CMDS
	$(TARGET_MAKE_ENV) $(OPENSBI_MAKE_ENV) $(MAKE) -C $(@D)
endef

ifneq ($(OPENSBI_PLAT),)
OPENSBI_INSTALL_IMAGES = YES
define OPENSBI_INSTALL_IMAGES_CMDS
	$(INSTALL) -m 0644 -D $(@D)/build/platform/$(OPENSBI_PLAT)/firmware/fw_jump.bin $(BINARIES_DIR)/fw_jump.bin
	$(INSTALL) -m 0644 -D $(@D)/build/platform/$(OPENSBI_PLAT)/firmware/fw_jump.elf $(BINARIES_DIR)/fw_jump.elf
	$(INSTALL) -m 0644 -D $(@D)/build/platform/$(OPENSBI_PLAT)/firmware/fw_dynamic.bin $(BINARIES_DIR)/fw_dynamic.bin
	$(INSTALL) -m 0644 -D $(@D)/build/platform/$(OPENSBI_PLAT)/firmware/fw_dynamic.elf $(BINARIES_DIR)/fw_dynamic.elf
endef
endif

# libsbi.a is not a library meant to be linked in user-space code, but
# with bare metal code, which is why we don't install it in
# $(STAGING_DIR)/usr/lib
define OPENSBI_INSTALL_STAGING_CMDS
	$(INSTALL) -m 0644 -D $(@D)/build/lib/libsbi.a $(STAGING_DIR)/usr/share/opensbi/libsbi.a
endef

$(eval $(generic-package))
