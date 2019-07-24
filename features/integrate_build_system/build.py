import os
import subprocess
import shutil
from conans import tools


def run(command):
    subprocess.check_output(command, shell=True)


if __name__ == "__main__":
    run("conan create waf-generator user/channel")
    run("conan create waf-installer user/channel")
    run("conan create waf-build-helper user/channel")
    run("conan create waf-mylib user/channel")

    with tools.chdir("mylib-consumer"):
        shutil.rmtree("build", ignore_errors=True)
        os.mkdir("build")

        run("conan source . --source-folder=build")
        run("conan install . --install-folder=build")
        run("conan build . --build-folder=build")