import os
import subprocess


def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Failed command: %s" % cmd)


def main():
    run("conan create waf-generator user/channel")
    run("conan create waf-installer user/channel")
    run("conan create waf-build-helper user/channel")
    run("conan create waf-mylib user/channel -s compiler.cppstd=14")
    run("conan create mylib-consumer waf-consumer/1.0@user/channel -s compiler.cppstd=14")


if __name__ == '__main__':
    main()
