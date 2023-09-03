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

def save(filename, content):
    with open(filename, "w") as f:
        return f.write(content)


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
    rm("locks")
    rm("bo_release.json")
    rm("bo_debug.json")


def ci_pipeline():
    clean()
    run("conan config set general.default_package_id_mode=full_version_mode")
    for config in ("Release", "Debug"):
        run("conan create liba liba/0.1@user/testing -s build_type=%s" % config)
        run("conan create libb libb/0.1@user/testing -s build_type=%s" % config)
        run("conan create libc libc/0.1@user/testing -s build_type=%s" % config)
        run("conan create libd libd/0.1@user/testing -s build_type=%s" % config)
        run("conan create app1 app1/0.1@user/testing -s build_type=%s" % config)
        run("conan create app2 app2/0.1@user/testing -s build_type=%s" % config)

    # A developer does some change to the libb
    with chdir("libb"):
        libb = load("conanfile.py")
        libb = libb + "# Some changes"
        save("conanfile.py", libb)

        run("conan lock create conanfile.py --name=libb --version=0.2 "
            "--user=user --channel=testing --lockfile-out=../locks/libb_deps_base.lock --base")

    # Even if liba gets a new 0.2 version, the lockfile will avoid it
    # For example, one could run:
    run("conan create liba liba/0.2@user/testing")
    # ... and we'd still be using liba/0.1 below.
    
    with chdir("libb"):
        # This will be useful to capture the revision
        run("conan export . libb/0.2@user/testing --lockfile=../locks/libb_deps_base.lock "
            "--lockfile-out=../locks/libb_base.lock")
        print(load("../locks/libb_base.lock"))
        # Capture the configuration lockfiles, one per configuration
        run("conan lock create conanfile.py --name=libb --version=0.2 "
            "--user=user --channel=testing --lockfile=../locks/libb_base.lock --lockfile-out=../locks/libb_deps_debug.lock -s build_type=Debug")
        run("conan lock create conanfile.py --name=libb --version=0.2 "
            "--user=user --channel=testing --lockfile=../locks/libb_base.lock --lockfile-out=../locks/libb_deps_release.lock")
        # Now build libb
        run("conan create . libb/0.2@user/testing --lockfile=../locks/libb_deps_release.lock")
        run("conan create . libb/0.2@user/testing --lockfile=../locks/libb_deps_debug.lock")

    # Capture the app1 base lockfile
    run("conan lock create --reference=app1/0.1@user/testing --lockfile=locks/libb_base.lock "
        "--lockfile-out=locks/app1_base.lock --base")
    # And one lockfile per configuration
    run("conan lock create --reference=app1/0.1@user/testing --lockfile=locks/app1_base.lock "
        "--lockfile-out=locks/app1_release.lock")
    run("conan lock create --reference=app1/0.1@user/testing --lockfile=locks/app1_base.lock "
        "--lockfile-out=locks/app1_debug.lock -s build_type=Debug")

    run("conan lock build-order locks/app1_release.lock --json=bo_release.json")
    run("conan lock build-order locks/app1_debug.lock --json=bo_debug.json")
    build_order_release = json.loads(load("bo_release.json"))
    build_order_debug = json.loads(load("bo_debug.json"))

    for level in build_order_release:
        for item in level:
            ref, pid, context, id_ = item
            print(item)
            run("conan install %s --build=%s --lockfile=locks/app1_release.lock "
                "--lockfile-out=locks/app1_release_updated.lock" % (ref, ref))
            run("conan lock update locks/app1_release.lock locks/app1_release_updated.lock")

    print(load("locks/app1_release.lock"))
    clean()

if __name__ == '__main__':
    home = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))
    with setenv("CONAN_USER_HOME", home):
        ci_pipeline()
