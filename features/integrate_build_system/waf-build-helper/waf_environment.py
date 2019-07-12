import os
import shutil
from conans import ConanFile, tools
from conans.client.tools.oss import args_to_string
from conans.util.files import normalize, save
from conans.client.build.compiler_flags import libcxx_flag, libcxx_define, format_defines
from conans.client.build.cppstd_flags import cppstd_flag
from conans.errors import ConanException


class WafBuildEnvironment(object):
    def __init__(self, conanfile):
        self._conanfile = conanfile
        self._arch_build = self._ss("arch_build")
        self._os = self._ss("os")
        self._compiler = self._ss("compiler")
        self._compiler_version = self._ss("compiler.version")
        self._compiler_libcxx = self._ss("compiler.libcxx")
        self._compiler_cppstd = self._ss("compiler.cppstd")
        self._build_type = self._ss("build_type")
        self._compiler_runtime = self._ss("compiler.runtime")
        self._arch_conan2waf = {'x86': 'x86', 'x86_64': 'x64'}

    def _gcc_ver_conan2waf(self, conan_version):
        version = [v for v in conan_version.split('.', 3)]
        while len(version) < 3:
            version.append('0')
        return "('{}', '{}', '{}')".format(version[0], version[1], version[2])

    def _libcxx_flags(self, compiler, libcxx):
        lib_flags = []
        if libcxx:
            stdlib_define = libcxx_define(compiler=compiler, libcxx=libcxx)
            lib_flags.extend(format_defines([stdlib_define]))
            cxxf = libcxx_flag(compiler=compiler, libcxx=libcxx)
            if cxxf:
                lib_flags.append(cxxf)

        return lib_flags

    def _toolchain_content(self):
        sections = []
        sections.append("def configure(conf):")
        sections.append("    if not conf.env.CXXFLAGS:")
        sections.append("       conf.env.CXXFLAGS = []")
        sections.append("    if not conf.env.LINKFLAGS:")
        sections.append("       conf.env.LINKFLAGS = []")
        if "Visual Studio" in self._compiler:
            # first we set the options for the compiler, then load
            if self._compiler_version:
                sections.append("    conf.env.MSVC_VERSION = '{}.0'".format(
                    self._compiler_version))
            try:
                sections.append("    conf.env.MSVC_TARGETS = '{}'".format(
                    self._arch_conan2waf[self._arch_build]))
            except KeyError:
                raise ConanException(
                    "Architecture  '%s' not supported" % self._arch_build)

            sections.append("    conf.env.CXXFLAGS.append('/{}')".format(
                self._compiler_runtime))

            if self._build_type == "Debug":
                sections.append("    conf.env.CXXFLAGS.extend(['/Zi', '/FS'])")
                sections.append("    conf.env.LINKFLAGS.extend(['/DEBUG'])")
            elif self._build_type == "Release":
                sections.append("    conf.env.CXXFLAGS.extend(['/O2'])")
        else:
            sections.append("    conf.env.CC_VERSION = {}".format(
                self._gcc_ver_conan2waf(self._compiler_version)))

            cxxf = self._libcxx_flags(
                compiler=self._compiler, libcxx=self._compiler_libcxx)
            for flag in cxxf:
                sections.append(
                    "    conf.env.CXXFLAGS.append('{}')".format(flag))

            if self._compiler_cppstd:
                cppstdf = cppstd_flag(self._compiler, self._compiler_version,
                                      self._compiler_cppstd)
                sections.append(
                    "    conf.env.CXXFLAGS.append('{}')".format(cppstdf))

            if self._build_type == "Debug":
                sections.append("    conf.env.CXXFLAGS.extend(['-g'])")
            elif self._build_type == "Release":
                sections.append("    conf.env.CXXFLAGS.extend(['-O3'])")

        return "\n".join(sections)

    def _save_toolchain_file(self):
        filename = "waf_conan_toolchain.py"
        content = self._toolchain_content()
        output_path = self._conanfile.build_folder
        content = normalize(content)
        self._conanfile.output.info("Waf Toolchain File created: %s" %
                                    (filename))
        save(
            os.path.join(output_path, filename),
            content,
            only_if_modified=True)

    def configure(self, args=None):
        self._save_toolchain_file()
        args = args or []
        command = "waf configure " + " ".join(arg for arg in args)
        if self._compiler_version:
            command = command + \
                '--msvc_version="msvc {}.0"'.format(self._compiler_version)
        self._run(command)

    def build(self, args=None):
        args = args or []
        command = "waf build " + " ".join(arg for arg in args)
        self._run(command)

    def _run(self, command):
        self._conanfile.run(command)

    def _ss(self, setname):
        """safe setting"""
        return self._conanfile.settings.get_safe(setname)

    def _so(self, setname):
        """safe option"""
        return self._conanfile.options.get_safe(setname)
