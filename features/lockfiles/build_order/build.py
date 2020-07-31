import os, json, shutil
import subprocess
from contextlib import contextmanager


def run(cmd, assert_error=False):
    print("*********** Running: %s" % cmd)
    ret = os.system(cmd)
    if ret == 0 and assert_error:
        raise Exception("Command unexpectedly succedeed: %s" % cmd)
    if ret != 0 and not assert_error:
        raise Exception("Failed command: %s" % cmd)

def load(filename):
    with open(filename, "r") as f:
        return f.read()

def rm(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

@contextmanager
def chdir(path):
    current_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(current_path)

@contextmanager
def setenv(key, value):
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old_value is not None:
            os.environ[key] = old_value


def clean():
    rm("tmp")
    rm("app1.lock")
    rm("app2.lock")
    rm("build_order.json")
    rm("build_order2.json")


def build_order():
    clean()

    run("conan config set general.default_package_id_mode=full_version_mode")
    run("conan export pkga pkga/0.1@user/testing")
    run("conan export pkgb pkgb/0.1@user/testing")
    run("conan export pkgc pkgc/0.1@user/testing")
    run("conan export pkgd pkgd/0.1@user/testing")
    run("conan export app1 app1/0.1@user/testing")
    run("conan export app2 app2/0.1@user/testing")

    run("conan lock create --reference=app1/0.1@user/testing --lockfile-out=app1.lock")
    print(load("app1.lock"))
    run("conan lock build-order app1.lock --json=build_order.json")
    print(load("build_order.json"))

    run("conan install app1/0.1@user/testing --build=missing")
    run("conan install app2/0.1@user/testing --build=missing")

    run("conan lock create --reference=app1/0.1@user/testing --lockfile-out=app1.lock")
    print(load("app1.lock"))
    run("conan lock build-order app1.lock --json=build_order.json")
    print(load("build_order.json"))  # Empty []

    run("conan lock create --reference=app1/0.1@user/testing --lockfile-out=app1.lock --build")
    print(load("app1.lock"))
    run("conan lock build-order app1.lock --json=build_order.json")
    print(load("build_order.json"))  # All deps

    # Modifying pkgb outside the version range
    run("conan create pkgb pkgb/2.0@user/testing")
    run("conan lock create --reference=app1/0.1@user/testing --lockfile-out=app1.lock")
    print(load("app1.lock"))
    run("conan lock build-order app1.lock --json=build_order.json")
    print(load("build_order.json"))

    # Modifying pkgb, what needs to be built?
    run("conan create pkgb pkgb/0.2@user/testing")
    run("conan lock create --reference=app1/0.1@user/testing --lockfile-out=app1.lock")
    print(load("app1.lock"))
    run("conan lock build-order app1.lock --json=build_order.json")
    print(load("build_order.json"))
    run("conan lock create --reference=app2/0.1@user/testing --lockfile-out=app2.lock")
    print(load("app2.lock"))
    run("conan lock build-order app2.lock --json=build_order2.json")
    print(load("build_order2.json"))



    clean()


if __name__ == '__main__':
    home = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))
    with setenv("CONAN_USER_HOME", home):
        build_order()

