import os, json, shutil, sys
import platform
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
    rm("pkgb/build")
    rm("pkgb/locks")
    rm("consume")
    run("conan remove '*' -f")

def single_config():
    clean()

    run("conan config set general.default_package_id_mode=full_version_mode")
    run("conan create pkga pkga/0.1@user/testing")

    with chdir("pkgb"):
        run("conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_deps.lock")
        print(load("locks/pkgb_deps.lock"))

    run("conan create pkga pkga/0.2@user/testing")

    os.makedirs("pkgb/build")
    with chdir("pkgb/build"):
        run("conan install ..")
        if platform.system() == "Windows":
            run('cmake ../src -G "{}"'.format(os.getenv("CMAKE_GENERATOR")))
        else:
            run("cmake ../src -DCMAKE_BUILD_TYPE=Release")
        run("cmake --build . --config Release")
        run(os.sep.join(["bin", "greet"]))

        run("conan install .. --lockfile=../locks/pkgb_deps.lock")
        run("cmake --build . --config Release")
        run(os.sep.join(["bin", "greet"]))

        run("conan install .. --lockfile=../locks/pkgb_deps.lock --build=pkga", assert_error=True)

    with chdir("pkgb"):
        run("conan create . user/stable --lockfile=locks/pkgb_deps.lock", assert_error=True)
        run("conan create . user/testing --lockfile=locks/pkgb_deps.lock --lockfile-out=locks/pkgb.lock")
        print(load("locks/pkgb.lock"))
        run("conan create . user/testing --lockfile=locks/pkgb.lock", assert_error=True)
        run("conan create . user/testing --lockfile=locks/pkgb_deps.lock")

    os.makedirs("consume")
    with chdir("consume"):
        run("conan install pkgb/0.1@user/testing --lockfile=../pkgb/locks/pkgb.lock")
        run(os.sep.join(["bin", "greet"]))

    clean()

def multi_config():
    # Multi-configuration
    clean()

    run("conan create pkga pkga/0.1@user/testing")
    run("conan create pkga pkga/0.1@user/testing -s build_type=Debug")

    with chdir("pkgb"):
        run("conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_release.lock")
        run("conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_debug.lock -s build_type=Debug")
        rm("locks")
        run("conan lock create conanfile.py --user=user --channel=testing --lockfile-out=locks/pkgb_base.lock --base")
        run("conan lock create conanfile.py --user=user --channel=testing --lockfile=locks/pkgb_base.lock --lockfile-out=locks/pkgb_deps_debug.lock -s build_type=Debug")
        run("conan lock create conanfile.py --user=user --channel=testing --lockfile=locks/pkgb_base.lock --lockfile-out=locks/pkgb_deps_release.lock")
        print(load("locks/pkgb_base.lock"))
        print(load("locks/pkgb_deps_release.lock"))
        print(load("locks/pkgb_deps_debug.lock"))

    run("conan create pkga pkga/0.2@user/testing")
    run("conan create pkga pkga/0.2@user/testing -s build_type=Debug")

    os.makedirs("pkgb/build")
    with chdir("pkgb/build"):
        for config in ("Release", "Debug"):
            run("conan install .. --lockfile=../locks/pkgb_deps_%s.lock -s build_type=%s" % (config.lower(), config), assert_error=True)
            run("conan install .. --lockfile=../locks/pkgb_deps_%s.lock" % config.lower())
            if platform.system() == "Windows":
                run('cmake ../src -G "{}"'.format(os.getenv("CMAKE_GENERATOR")))
            else:
                run("cmake ../src -DCMAKE_BUILD_TYPE=%s" % config)
            run("cmake --build . --config %s" % config)
            run(os.sep.join(["bin", "greet"]))
            run("conan install .. -s build_type=%s" % config)
            run("cmake --build . --config %s" % config)
            run(os.sep.join(["bin", "greet"]))

            run("conan install .. --lockfile=../locks/pkgb_deps_%s.lock --build=pkga" % config.lower(), assert_error=True)


    with chdir("pkgb"):
        for config in ("Release", "Debug"):
            run("conan create . user/stable --lockfile=locks/pkgb_deps_%s.lock" % config.lower(), assert_error=True)
            run("conan create . user/testing --lockfile=locks/pkgb_deps_%s.lock --lockfile-out=locks/pkgb_%s.lock" % (config.lower(), config.lower()))
            print(load("locks/pkgb_%s.lock" % config.lower()))
            run("conan create . user/testing --lockfile=locks/pkgb_%s.lock" % config.lower(), assert_error=True)

    os.makedirs("consume")
    with chdir("consume"):
        for config in ("Release", "Debug"):
            run("conan install pkgb/0.1@user/testing --lockfile=../pkgb/locks/pkgb_%s.lock" % config.lower())
            run(os.sep.join(["bin", "greet"]))

    clean()


if __name__ == '__main__':
    home = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))
    with setenv("CONAN_USER_HOME", home):
        if platform.system() == "Windows":
            if not os.getenv("CMAKE_GENERATOR"):
                print("CMAKE_GENERATOR environment variable not defined. "
                      "Please define the CMake generator in the CMAKE_GENERATOR environment variable.")
                sys.exit()
        single_config()
        multi_config()
