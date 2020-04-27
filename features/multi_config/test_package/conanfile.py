import os
from six import StringIO
from conans import ConanFile, CMake


class HelloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        os.chdir("bin")
        output = StringIO()
        if self.settings.build_type != 'Release':
            return
        self.run(".%sexample" % os.sep, run_environment=True, output=output)
        assert ("Hello World {}!".format(str(self.settings.build_type)) in output.getvalue()), output.getvalue()
