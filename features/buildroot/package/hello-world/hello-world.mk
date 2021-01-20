################################################################################
#
# HELLO_WORLD
#
################################################################################

HELLO_WORLD_VERSION = 0.1.0
HELLO_WORLD_SITE = ./package/hello-world
HELLO_WORLD_SITE_METHOD = local
HELLO_WORLD_SUBDIR = src
HELLO_WORLD_DEPENDENCIES = conan-zlib
HELLO_WORLD_CONF_OPTS = -DCMAKE_VERBOSE_MAKEFILE=ON

$(eval $(cmake-package))
