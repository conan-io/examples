import os
import shutil

from utils.utils import setenv, chdir, replace, save, rmdir


def activate_user(f):
    def wrapper(user, *args, **kwargs):
        with chdir(user.current_folder):
            with setenv("CONAN_USER_HOME", user.user_cache):
                return f(user, *args, **kwargs)
    return wrapper


class User(object):
    base_folder = None

    def __init__(self, user):
        self._user = user
        self.user_folder = os.path.join(self.base_folder, "tmp", "users", user)
        self.current_folder = self.user_folder
        self.user_cache = os.path.join(self.user_folder, "cache")
        rmdir(self.user_folder)
        os.makedirs(self.user_folder, exist_ok=True)

    def _run(self, cmd):
        print("RUNNING (%s): %s" % (self._user, cmd))
        ret = os.system(cmd)
        if ret != 0:
            raise Exception("Command failed: %s" % cmd)

    @activate_user
    def run(self, cmd):
        self._run(cmd)

    @activate_user
    def clone(self, repo):
        self._run("git clone %s" % repo)

    @activate_user
    def cd(self, folder):
        self.current_folder = os.path.realpath(os.path.join(self.current_folder, folder))
        try:
            os.makedirs(self.current_folder)
        except OSError:
            pass

    @activate_user
    def edit(self, filepath, find_text, replace_text):
        replace(filepath, find_text, replace_text)

    @activate_user
    def commit(self, branch):
        self._run("git checkout -b %s" % branch)
        self._run("git add .")
        self._run("git commit -m %s-changes" % self._user)

    @activate_user
    def local_build(self, lockfile=None):
        lockfile = "" if not lockfile else " --lockfile=%s" % lockfile
        shutil.rmtree("build", ignore_errors=True)
        os.mkdir("build")
        with chdir("build"):
            self._run("conan install .. %s" % lockfile)
            self._run('cmake ../src -G "Visual Studio 15 Win64"')
            self._run('cmake --build . --config Release')

    @activate_user
    def conan_create(self):
        self._run("conan create . user/testing")

    @activate_user
    def copy_code(self, folder):
        src_folder = os.path.join(self.base_folder, folder).replace("\\", "/")
        print("SORUCE FOLDER ", src_folder)
        for elem in os.listdir(src_folder):
            p = os.path.join(src_folder, elem)
            if os.path.isfile(p):
                shutil.copy(p, ".")
            else:
                shutil.copytree(p, os.path.basename(p))

    @activate_user
    def git_init(self, readme=False):
        if readme:
            save("readme.txt", "README")
        self._run("git init .")
        self._run("git config core.autocrlf false")
        self._run("git add .")
        self._run("git commit -m initial")

    @activate_user
    def git_commit(self, msg="commit"):
        self._run("git add .")
        self._run('git commit -m "%s"' % msg)

    @activate_user
    def git_remote_add(self, name, url):
        self._run("git remote add %s %s" % (name, url))

    @activate_user
    def git_push(self, args=""):
        self._run("git push %s" % args)

    @activate_user
    def git_clone(self, url):
        self._run("git clone %s" % url)
