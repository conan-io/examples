################################################################################
#
# odroid-mali
#
################################################################################

ODROID_MALI_VERSION = 4f8a541693fee5fdcaa162a7fd8922861a4ba0a9
ODROID_MALI_SITE = $(call github,mdrjr,c2_mali,$(ODROID_MALI_VERSION))
ODROID_MALI_LICENSE = Hardkernel EULA
ODROID_MALI_LICENSE_FILES = README.md

ODROID_MALI_INSTALL_STAGING = YES
ODROID_MALI_PROVIDES = libegl libgles

ifeq ($(BR2_PACKAGE_ODROID_MALI_X11),y)
ODROID_MALI_HEADERS_SUBDIR = x11/mali_headers/
ODROID_MALI_LIBS_SUBDIR = x11/mali_libs/
# The X11 blobs are linked against those libraries, and the headers
# include headers from those libraries
ODROID_MALI_DEPENDENCIES += \
	libdrm xlib_libX11 xlib_libXdamage \
	xlib_libXext xlib_libXfixes
else
define ODROID_MALI_FIX_EGL_PC
	$(SED) "s/Cflags: /Cflags: -DMESA_EGL_NO_X11_HEADERS /" \
		$(STAGING_DIR)/usr/lib/pkgconfig/egl.pc
endef
ODROID_MALI_HEADERS_SUBDIR = fbdev/mali_headers/
ifeq ($(BR2_aarch64),y)
ODROID_MALI_LIBS_SUBDIR = fbdev/mali_libs/
else
ODROID_MALI_LIBS_SUBDIR = fbdev/32bit_libs/
endif
endif

define ODROID_MALI_INSTALL_LIBS
	cp -dpfr $(@D)/$(ODROID_MALI_LIBS_SUBDIR)/lib* $(1)/usr/lib/
endef

define ODROID_MALI_INSTALL_STAGING_CMDS
	$(call ODROID_MALI_INSTALL_LIBS,$(STAGING_DIR))
	mkdir -p $(STAGING_DIR)/usr/lib/pkgconfig
	cp -dpfr $(@D)/pkgconfig/*.pc $(STAGING_DIR)/usr/lib/pkgconfig/
	cp -dpfr $(@D)/$(ODROID_MALI_HEADERS_SUBDIR)/* $(STAGING_DIR)/usr/include
	$(ODROID_MALI_FIX_EGL_PC)
endef

define ODROID_MALI_INSTALL_TARGET_CMDS
	$(call ODROID_MALI_INSTALL_LIBS,$(TARGET_DIR))
endef

$(eval $(generic-package))
