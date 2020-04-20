import os
import shutil
import stat
from contextlib import contextmanager


def run(cmd):
    print("RUNNING: %s" % cmd)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Command failed: %s" % cmd)


@contextmanager
def chdir(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(old_dir)


@contextmanager
def setenv(key, value):
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old_value is not None:
            os.environ[key] = old_value


def load(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def save(filename, content):
    with open(filename, "w") as f:
        f.write(content)


def replace(filename, original, replacement):
    content = load(filename)
    content2 = content.replace(original, replacement)
    if content2 == content:
        raise Exception("No replacement of '%s' has been done" % original)
    save(filename, content2)


def changed_files(base_branch, user_branch):
    run("git diff %s %s --name-only > diff.txt" % (base_branch, user_branch))
    diff = load("diff.txt")
    os.remove("diff.txt")
    modified = diff.splitlines()
    return modified


def rmdir(folder):
    def _change_permissions(func, path, exc_info):
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise OSError("Cannot change permissions for {}! Exception info: {}".format(path, exc_info))

    if os.path.exists(folder):
        shutil.rmtree(folder, onerror=_change_permissions)
