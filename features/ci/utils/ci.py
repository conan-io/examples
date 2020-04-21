import json
import os

from utils.utils import load, chdir, setenv, rmdir


class CI(object):
    base_folder = None

    def __init__(self, product=None):
        self.ci_folder = os.path.join(self.base_folder, "tmp", "ci")
        rmdir(self.ci_folder)
        self.product = product
        self._build_counter = 0

    def new_job(self):
        job = self._build_counter
        self._build_counter += 1
        job_folder = os.path.join(self.ci_folder, "build%s" % job)
        return job, job_folder

    def product_pipeline(self, job):
        if not self.product:
            return
        self._run("conan graph lock %s--build" % self.product)  # Always all build, as soon as we export, it will change
        self._run("conan graph build-order . --build=missing --json=build-order.json")
        build_order = json.loads(load("build-order.json"))
        print("*********** BUILD-ORDER *******************\n%s" % build_order)
        for level_to_build in build_order:
            for to_build in level_to_build:
                ref = to_build[1].split(":")[0]
                print("Building ", ref)
                self.build_pkg(ref, lockfile="../..")

    def build(self, repo, branch):
        job = self._build_counter
        self._build_counter += 1
        self.package_pipeline(repo, branch, job)
        self.product_pipeline(job)

    def run(self, cmd):
        print("RUNNING (CI): %s" % cmd)
        ret = os.system(cmd)
        if ret != 0:
            raise Exception("Command failed: %s" % cmd)

    def build_pkg(self, ref, lockfile=None):
        lockfile = "" if not lockfile else " --lockfile=%s" % lockfile
        self._run("conan install %s --build=%s %s" % (ref, ref.name, lockfile))
