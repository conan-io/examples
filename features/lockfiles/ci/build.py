import os, json, shutil

def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Failed command: %s" % cmd)

def load(filename):
    with open(filename, "r") as f:
        return f.read()

def rm(path):
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)

rm("release")
rm("build_server_folder")
rm("bo.json")
run('conan remove "*" -f')

run("conan config set general.default_package_id_mode=full_version_mode")
run("cd PkgZ && conan create . PkgZ/0.1@user/testing")
run("cd PkgA && conan create . PkgA/0.1@user/testing")
run("cd PkgB && conan create . user/testing")
run("cd PkgC && conan create . user/testing")
run("cd App && conan create . user/testing")

# Freeze the App dependencies in a lockfile in the release subfolder
print("\n********** Freeze dependencies in a lockfile ***********")
run("conan graph lock App/0.1@user/testing --lockfile=release")

# A new version of Z will not affect at all
run("cd PkgZ && conan create . PkgZ/0.2@user/testing")
# There is a change in A, a new version that we want to test
print("\n********** Creating PkgA/0.2 ***********")
run("cd PkgA && conan create . PkgA/0.2@user/testing --lockfile=../release")

print("\n********** Computing the build order after PkgA/0.2 ***********")
run("conan graph build-order ./release --json=bo.json --build=missing")

build_order = json.loads(load("bo.json"))

while build_order:
    # Simulates building in a different build server
    os.makedirs("build_server_folder/release")
    shutil.copy2("release/conan.lock", "build_server_folder/release")
    os.chdir("build_server_folder")
    print("\nBuild order is: %s" % build_order)
    _, pkg_ref = build_order[0][0]
    pkg_ref = pkg_ref.split("#", 1)[0]
    print("\n********** Rebuild affected package: %s ***********" % pkg_ref)
    run("conan graph clean-modified release/")
    run("conan install %s --build=%s --lockfile=release" % (pkg_ref, pkg_ref))
    os.chdir("..")
    run("conan graph update-lock release build_server_folder/release")
    rm("build_server_folder")
    # Update the build order after changes
    run("conan graph build-order ./release --json=bo.json --build=missing")
    build_order = json.loads(load("bo.json"))        
