#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import stat
import platform
import subprocess
import tempfile
import logging
from contextlib import contextmanager


FAIL_FAST = os.getenv("FAIL_FAST", "0").lower() in ["1", "y", "yes", "true"]
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
    script = "build.bat" if platform.system() == "Windows" else "build.sh"
    for root, dirs, files in os.walk("."):
        for file in files:
            if os.path.basename(file) == script:
                builds.append(os.path.join(root, file))
    return builds


def chmod_x(script):
    logging.debug("chmod +x {}".format(script))
    st = os.stat(script)
    os.chmod(script, st.st_mode | stat.S_IEXEC)


def get_conan_env():
    temp_folder = tempfile.mkdtemp(prefix="conan-", suffix="-home")
    os.environ["CONAN_USER_HOME"] = temp_folder
    logging.debug("CONAN_USER_HOME: {}".format(temp_folder))
    return os.environ


def configure_profile():
    subprocess.check_output("conan profile new default --detect",
                            stderr=subprocess.STDOUT,
                            shell=True)
    if platform.system() == "Linux":
        subprocess.check_output("conan profile update settings.compiler.libcxx=libstdc++11 default",
                                stderr=subprocess.STDOUT,
                                shell=True)


def run_scripts(scripts):
    results = {}
    for script in scripts:
        chmod_x(script)
        abspath = os.path.abspath(script)
        env = get_conan_env()
        configure_profile()
        with chdir(os.path.dirname(script)):
            logging.debug("run {}".format(abspath))
            result = subprocess.call(abspath, env=env)
            results[script] = result
            if result != 0 and FAIL_FAST:
                break
    return results


def print_results(results):
    print("\n\n=== CONAN EXAMPLES: RESULTS ===")
    for build, result in results.items():
        build_name = os.path.dirname(build)[2:].upper()
        message = "{}: {}".format(build_name, "OK" if result == 0 else "ERROR")
        print(message)


def validate_results(results):
    for value in results.values():
        if value != 0:
            sys.exit(value)


if __name__ == "__main__":
    scripts = get_build_list()
    results = run_scripts(scripts)
    print_results(results)
    validate_results(results)
