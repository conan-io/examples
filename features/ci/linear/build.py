import os

from utils.ci import CI
from utils.user import User

User.base_folder = os.path.realpath(os.path.dirname(__file__))
CI.base_folder = os.path.realpath(os.path.dirname(__file__))
ci = CI()

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
    ci.package_pipeline(repo, "master")
