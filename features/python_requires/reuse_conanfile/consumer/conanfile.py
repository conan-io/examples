from conans import ConanFile, CMake, python_requires


base = python_requires("pyreq/version@user/channel")

class ConsumerConan(base.get_conanfile()):
    name = "consumer"
    version = base.get_version()

    # All the recipe attributes and methods are defined in 
    #  the python_requires imported source, it is a very
    #  easy way to share all the business logic across
    #  all the recipes in the same company
