#!/usr/bin/python

import os
import subprocess
import tempfile
from contextlib import contextmanager


@contextmanager
def chdir(dir_path):
    current = os.getcwd()
    os.chdir(dir_path)
    try:
        yield
    finally:
        os.chdir(current)


def get_build_list():
    builds = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if os.path.basename(file) == "build.sh":
                builds.append(os.path.join(root, file))
    return builds


def run_scripts(scripts):
    results = {}
    for script in scripts:
        temp_folder = tempfile.mkdtemp(suffix="conan")
        env = {"CONAN_USER_HOME": temp_folder}
        with chdir(os.path.dirname(script)):
            results[script] = subprocess.call(os.path.basename(script), env=env)
    return results


def print_results(results):
    print("=== CONAN EXAMPLES ===")
    for build, result in results.items():
        message = "{}: {}".format(build, "OK" if result == 0 else "ERROR")
        print(message)


if __name__ == "__main__":
    scripts = get_build_list()
    results = run_scripts(scripts)
    print_results(results)
