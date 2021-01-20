################################################################################
# Conan package infrastructure
#
# This file implements an infrastructure that eases development of
# package .mk files for Meson packages. It should be used for all
# packages that use Meson as their build system.
#
# See the Buildroot documentation for details on the usage of this
# infrastructure
#
# In terms of implementation, this Meson infrastructure requires
# the .mk file to only specify metadata information about the
# package: name, version, download URL, etc.
#
# We still allow the package .mk file to override what the different
# steps are doing, if needed. For example, if <PKG>_BUILD_CMDS is
# already defined, it is used as the list of commands to perform to
# build the package, instead of the default Meson behaviour. The
# package can also define some post operation hooks.
#
################################################################################

#
# Pass PYTHONNOUSERSITE environment variable when invoking Meson or Ninja, so
# $(HOST_DIR)/bin/python3 will not look for Meson modules in
# $HOME/.local/lib/python3.x/site-packages
#
#CONAN		= PYTHONNOUSERSITE=y $(HOST_DIR)/bin/conan
CONAN		= conan

################################################################################
# inner-conan-package -- defines how the configuration, compilation and
# installation of a Conan package should be done, implements a few hooks to
# tune the build process and calls the generic package infrastructure to
# generate the necessary make targets
#
#  argument 1 is the lowercase package name
#  argument 2 is the uppercase package name, including a HOST_ prefix
#             for host packages
#  argument 3 is the uppercase package name, without the HOST_ prefix
#             for host packages
#  argument 4 is the type (target or host)
################################################################################

define inner-conan-package

$(2)_CONF_ENV			?=
$(2)_CONF_OPTS			?=
$(2)_CONAN_ENV			?= CONAN_USER_HOME=$$(BASE_DIR)

CONAN_SETTING_COMPILER 			?= gcc
CONAN_SETTING_COMPILER_VERSION 	?=
CONAN_SETTING_ARCH 				?= $(BR2_ARCH)
CONAN_REMOTE					?=
CONAN_BUILD_POLICY				?=

# TODO (uilian): Use Conan privded by buildroot
# $(2)_DEPENDENCIES += host-python-conan

CONAN_OPTION_SHARED = $$(if $$(BR2_STATIC_LIBS),False,True)
CONAN_SETTING_BUILD_TYPE = $$(if $$(BR2_ENABLE_DEBUG),Debug,Release)

ifeq ($(BR2_GCC_VERSION_8_X),y)
CONAN_SETTING_COMPILER_VERSION = 8
else ifeq ($(BR2_GCC_VERSION_7_X),y)
CONAN_SETTING_COMPILER_VERSION = 7
else ifeq ($(BR2_GCC_VERSION_6_X),y)
CONAN_SETTING_COMPILER_VERSION = 6
else ifeq ($(BR2_GCC_VERSION_5_X),y)
CONAN_SETTING_COMPILER_VERSION = 5
else ifeq ($(BR2_GCC_VERSION_4_9_X),y)
CONAN_SETTING_COMPILER_VERSION = 4.9
endif

ifeq ($(BR2_x86_64),y)
CONAN_SETTING_ARCH = x86_64
else ifeq ($(BR2_x86_i686),y)
CONAN_SETTING_ARCH = x86
else ifeq ($(BR2_x86_i486),y)
CONAN_SETTING_ARCH = x86
else ifeq ($(BR2_x86_i586),y)
CONAN_SETTING_ARCH = x86
else ifeq ($(BR2_ARCH),arm)
CONAN_SETTING_ARCH = armv7
else ifeq ($(BR2_ARCH),armhf)
CONAN_SETTING_ARCH = armv7hf
else ifeq ($(call qstrip,$(BR2_ARCH)),powerpc64)
CONAN_SETTING_ARCH = ppc64
else ifeq ($(call qstrip,$(BR2_ARCH)),powerpc64le)
CONAN_SETTING_ARCH = ppc64le
endif

ifeq ($(BR2_ARM_CPU_ARMV4),y)
CONAN_SETTING_ARCH = armv4
else ifeq ($(BR2_ARM_CPU_ARMV5),y)
CONAN_SETTING_ARCH = armv5hf
else ifeq ($(BR2_ARM_CPU_ARMV6),y)
CONAN_SETTING_ARCH = armv6
else ifeq ($(BR2_ARM_CPU_ARMV7A),y)
CONAN_SETTING_ARCH = armv7
else ifeq ($(BR2_ARM_CPU_ARMV8A),y)
CONAN_SETTING_ARCH = armv8
endif

ifeq ($(CONAN_BUILD_POLICY_MISSING),y)
CONAN_BUILD_POLICY = missing
else ifeq ($(CONAN_BUILD_POLICY_OUTDATED),y)
CONAN_BUILD_POLICY = outdated
else ifeq ($(CONAN_BUILD_POLICY_CASCADE),y)
CONAN_BUILD_POLICY = cascade
else ifeq ($(CONAN_BUILD_POLICY_ALWAYS),y)
CONAN_BUILD_POLICY = always
else ifeq ($(CONAN_BUILD_POLICY_NEVER),y)
CONAN_BUILD_POLICY = never
endif

# Check if package reference contains shared option
ifneq (,$(findstring shared,$(shell $(CONAN) inspect -a options $($(3)_REFERENCE))))
$(2)_CONAN_OPTS += -o $(shell echo $($(3)_REFERENCE) | cut -f1 -d/):shared=$$(CONAN_OPTION_SHARED)
endif

ifneq ($(CONAN_REMOTE_NAME),"")
CONAN_REMOTE = -r $$(CONAN_REMOTE_NAME)
endif

#
# Build step. Only define it if not already defined by the package .mk
# file.
#
ifndef $(2)_BUILD_CMDS
ifeq ($(4),target)
define $(2)_BUILD_CMDS
	$$(TARGET_MAKE_ENV) $$(CONAN_ENV) $$($$(PKG)_CONAN_ENV) \
	    CC=$$(TARGET_CC) CXX=$$(TARGET_CXX) \
		$$(CONAN) install $$(CONAN_OPTS) $$($$(PKG)_CONAN_OPTS) \
		$$($$(PKG)_REFERENCE) \
		-s build_type=$$(CONAN_SETTING_BUILD_TYPE) \
		-s arch=$$(CONAN_SETTING_ARCH) \
		-s compiler=$$(CONAN_SETTING_COMPILER) \
		-s compiler.version=$$(CONAN_SETTING_COMPILER_VERSION) \
		-g deploy \
		--build $$(CONAN_BUILD_POLICY) \
		$$(CONAN_REMOTE)
endef
else
define $(2)_BUILD_CMDS
	$$(HOST_MAKE_ENV) $$(CONAN_ENV) $$($$(PKG)_CONAN_ENV) \
		$$(CONAN) install $$(CONAN_OPTS) $$($$(PKG)_CONAN_OPTS) \
		$$($$(PKG)_REFERENCE) \
		-s build_type=$$(CONAN_SETTING_BUILD_TYPE) \
		-s arch=$$(CONAN_SETTING_ARCH) \
		-s compiler=$$(CONAN_SETTING_COMPILER) \
		-s compiler.version=$$(CONAN_SETTING_COMPILER_VERSION) \
		-g deploy \
		--build $$(CONAN_BUILD_POLICY) \
		$$(CONAN_REMOTE)
endef
endif
endif

#
# Host installation step. Only define it if not already defined by the
# package .mk file.
#
ifndef $(2)_INSTALL_CMDS
define $(2)_INSTALL_CMDS
	cp -f -a $$($$(PKG)_BUILDDIR)/bin/. /usr/bin 2>/dev/null || :
	cp -f -a $$($$(PKG)_BUILDDIR)/lib/. /usr/lib 2>/dev/null || :
	cp -f -a $$($$(PKG)_BUILDDIR)/include/. /usr/include 2>/dev/null || :
endef
endif

#
# Staging installation step. Only define it if not already defined by
# the package .mk file.
#
ifndef $(2)_INSTALL_STAGING_CMDS
define $(2)_INSTALL_STAGING_CMDS
	cp -f -a $$($$(PKG)_BUILDDIR)/bin/. $$(STAGING_DIR)/usr/bin 2>/dev/null || :
	cp -f -a $$($$(PKG)_BUILDDIR)/lib/. $$(STAGING_DIR)/usr/lib 2>/dev/null || :
	cp -f -a $$($$(PKG)_BUILDDIR)/include/. $$(STAGING_DIR)/usr/include 2>/dev/null || :
endef
endif

#
# Target installation step. Only define it if not already defined by
# the package .mk file.
#
ifndef $(2)_INSTALL_TARGET_CMDS
define $(2)_INSTALL_TARGET_CMDS
	cp -a $$($$(PKG)_BUILDDIR)/bin/. $$(TARGET_DIR)/usr/bin 2>/dev/null || :
	cp -a $$($$(PKG)_BUILDDIR)/lib/. $$(TARGET_DIR)/usr/lib 2>/dev/null || :
	cp -a $$($$(PKG)_BUILDDIR)/include/. $$(TARGET_DIR)/usr/include 2>/dev/null || :
endef
endif

# Call the generic package infrastructure to generate the necessary
# make targets
$(call inner-generic-package,$(1),$(2),$(3),$(4))

endef

################################################################################
# conan-package -- the target generator macro for Conan packages
################################################################################

conan-package = $(call inner-conan-package,$(pkgname),$(call UPPERCASE,$(pkgname)),$(call UPPERCASE,$(pkgname)),target)
host-conan-package = $(call inner-conan-package,host-$(pkgname),$(call UPPERCASE,host-$(pkgname)),$(call UPPERCASE,$(pkgname)),host)
