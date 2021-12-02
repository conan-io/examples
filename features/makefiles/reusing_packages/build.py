import os
import subprocess
from contextlib import contextmanager


def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Failed command: %s" % cmd)


@contextmanager
def chdir(path):
    current_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current_path)


def main():
    with chdir("../creating_packages"):
        run("conan create . demo/testing")
    run("conan create . demo/testing")


if __name__ == '__main__':
    main()
