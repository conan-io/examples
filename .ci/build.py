#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import stat
import subprocess
import tempfile
import logging
from contextlib import contextmanager


LOGGING_LEVEL = int(os.getenv("CONAN_LOGGING_LEVEL", logging.INFO))
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=LOGGING_LEVEL)


@contextmanager
def chdir(dir_path):
    current = os.getcwd()
    os.chdir(dir_path)
    logging.debug("cd {}".format(dir_path))
    try:
        yield
    finally:
        logging.debug("cd {}".format(current))
        os.chdir(current)


def get_build_list():
    builds = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if os.path.basename(file) == "build.sh":
                builds.append(os.path.join(root, file))
    return builds


def chmod_x(script):
    logging.debug("chmod +x {}".format(script))
    st = os.stat(script)
    os.chmod(script, st.st_mode | stat.S_IEXEC)


def get_conan_env():
    temp_folder = tempfile.mkdtemp(prefix="conan-", suffix="-home")
    os.environ["CONAN_USER_HOME"] = temp_folder
    return os.environ


def run_scripts(scripts):
    results = {}
    for script in scripts:
        chmod_x(script)
        with chdir(os.path.dirname(script)):
            results[script] = subprocess.call(script, env=get_conan_env())
    return results


def print_results(results):
    print("\n\n=== CONAN EXAMPLES: RESULTS ===")
    for build, result in results.items():
        build_name = os.path.basename(build)[2:].upper()
        message = "{}: {}".format(build, "OK" if result == 0 else "ERROR")
        print(message)


if __name__ == "__main__":
    scripts = get_build_list()
    results = run_scripts(scripts)
    print_results(results)
