"""
Needs 1 Artifactory repo in: http://localhost:8081/artifactory/api/conan/ci-master
"""

import os

from utils.ci import CI
from utils.user import User
from utils.utils import setenv, chdir

User.base_folder = os.path.realpath(os.path.dirname(__file__))
CI.base_folder = os.path.realpath(os.path.dirname(__file__))
ci_server = CI()


def package_pipeline(ci, repository, branch):
    job, job_folder = ci.new_job()
    cache_folder = os.path.join(job_folder, "cache")
    os.makedirs(cache_folder, exist_ok=True)
    with setenv("CONAN_USER_HOME", cache_folder):
        ci.run("conan remote remove conan-center")
        ci.run("conan remote add master http://localhost:8081/artifactory/api/conan/ci-master -f")
        ci.run("conan user admin -p=password -r=master")
        with chdir(job_folder):
            ci.run("git clone %s" % repository)
            repo_folder = os.path.basename(repository)
            with chdir(repo_folder):
                ci.run("git checkout %s" % branch)
                ci.run("conan create . user/testing")
        if branch == "master":
            ci.run("conan upload * -r=master --all --confirm")


# Create 3 repos in the server
git_server = User("git_server")
repos_urls = {}
for pkg in ("hello", "chat", "app"):
    git_server.cd(pkg)
    repos_urls[pkg] = git_server.current_folder
    git_server.git_init(readme=True)
    git_server.run("git config --bool core.bare true")

# User bob puts some code and create packages
bob = User("bob")
for pkg in ("hello", "chat", "app"):
    repo = repos_urls[pkg]
    bob.git_clone(repo)
    bob.cd(pkg)
    bob.copy_code("sources/%s" % pkg)
    # bob.local_build()
    # bob.conan_create()
    bob.git_commit()
    bob.git_push()
    # Every push fires a package pipeline
    package_pipeline(ci_server, repo, "master")
