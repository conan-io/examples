import os

def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Failed command: %s" % cmd)

# run("cd PkgZ && conan create . PkgZ/0.1@user/testing")
# run("cd PkgA && conan create . PkgA/0.1@user/testing")
# run("cd PkgB && conan create . user/testing")
# run("cd PkgC && conan create . user/testing")
# run("cd App && conan create . user/testing")

# Freeze the App dependencies in a lockfile in the release subfolder
run("conan graph lock App/0.1@user/testing --lockfile=release")

# A new version of Z will not affect at all
# run("cd PkgZ && conan create . PkgZ/0.2@user/testing")
# run("cd PkgA && conan create . PkgA/0.2@user/testing --lockfile=../release")

run("conan graph build-order ./release --json=bo.json --build=missing")

run("cd PkgB && conan create . user/testing --lockfile=../release")
run("cd PkgC && conan create . user/testing --lockfile=../release")
