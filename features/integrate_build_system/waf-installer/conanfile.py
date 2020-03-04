from conans import ConanFile, tools
import os


class WAFInstallerConan(ConanFile):
    name = "waf"
    version = "2.0.19"
    description = "Waf is a Python-based build system"
    settings = "os_build"
    homepage = "https://gitlab.com/ita1024/waf"
    license = "BSD"
    exports_sources = ["LICENSE"]

    def build(self):
        source_url = "https://waf.io/waf-%s" % (self.version)
        self.output.warn("Downloading Waf build system: %s" % (source_url))
        tools.download(source_url, "waf")
        if self.settings.os_build == "Windows":
            tools.download(
                "https://gitlab.com/ita1024/waf/raw/waf-{}/utils/waf.bat".format(self.version), "waf.bat")
        elif self.settings.os_build == "Linux" or self.settings.os_build == "Macos":
            self.run("chmod 755 waf")

    def package(self):
        self.copy(pattern="LICENSE", src='.', dst="licenses")
        self.copy('waf', src='.', dst="bin", keep_path=False)
        self.copy('waf.bat', src='.', dst="bin", keep_path=False)

    def package_info(self):
        self.output.info("Using Waf %s version" % self.version)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
