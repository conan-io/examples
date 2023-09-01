import os
import urllib.request
import tarfile
import subprocess
import shutil


if __name__ == "__main__":
    tarfilename = "2019.05.1.tar.gz"
    buildrootdir = "buildroot-2019.05.1"

    print("Cleaning directory ...")
    shutil.rmtree(buildrootdir, True)

    if not os.path.isfile(tarfilename):
        print("Downloading Buildroot ...")
        urllib.request.urlretrieve("https://github.com/buildroot/buildroot/archive/{}".format(tarfilename), tarfilename)

    print("Extracting .tar.gz ...")
    tar = tarfile.open(tarfilename, "r:gz")
    tar.extractall()
    tar.close()

    print("Applying Conan patch ...")
    patchcontent = open("0001-conan-support.patch")
    process = subprocess.Popen(["patch", "-p1", "-d", buildrootdir], stdin=patchcontent)
    process.wait()

    print("Building Linux image ...")
    shutil.copy2("conan_config", os.path.join(buildrootdir, ".config"))
    subprocess.call(["make", "clean", "-C", buildrootdir])
    subprocess.check_call(["make", "-C", buildrootdir])
