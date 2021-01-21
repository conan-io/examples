#!/bin/python
import os
import urllib.request
import tarfile
import subprocess
import shutil


if __name__ == "__main__":
    tarfilename = "2019.05.1.tar.gz"
    buildrootdir = "buildroot-2019.05.1"
    print("Cleaning director ...")
    try:
        os.remove(tarfilename)
        shutil.rmtree(buildrootdir)
    except:
        pass
    tarfilename = "2019.05.1.tar.gz"
    print("Downloading Buildroot ...")
    urllib.request.urlretrieve("https://github.com/buildroot/buildroot/archive/{}".format(tarfilename), tarfilename)
    print("Extracting .tar.gz ...")
    tar = tarfile.open(tarfilename, "r:gz")
    tar.extractall()
    tar.close()
    os.remove(tarfilename)
    print("Applying Conan patch ...")
    os.chdir(buildrootdir)

    patchcontent = open("../0001-conan-support.patch")
    process = subprocess.Popen(["patch", "-p1"], stdin=patchcontent)
    process.wait()

    subprocess.check_call(["patch", "-p1", "<", "../0001-conan-support.patch"])
