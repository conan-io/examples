#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import platform
import stat
import subprocess
import sys
import tempfile
import uuid
from collections import OrderedDict
from contextlib import contextmanager
from packaging import version

import colorama
from conans.client.tools.scm import Git
from tabulate import tabulate
from conans import __version__ as conan_version


FAIL_FAST = os.getenv("FAIL_FAST", "0").lower() in ["1", "y", "yes", "true"]
LOGGING_LEVEL = int(os.getenv("CONAN_LOGGING_LEVEL", logging.INFO))
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=LOGGING_LEVEL)


def is_appveyor():
    return os.getenv("APPVEYOR", False)

def appveyor_image():
    return os.getenv("APPVEYOR_BUILD_WORKER_IMAGE","")

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


def writeln_console(message):
    sys.stderr.flush()
    sys.stdout.write(message)
    sys.stdout.write('\n')
    sys.stdout.flush()


def get_examples_to_skip(current_version):
    skip = []
    # Given the Conan version, some examples are skipped
    required_conan = {
        version.parse("1.22.0"): [
            './libraries/dear-imgui/basic',  # Requires fix related to CMake link order/targets
            ],
        version.parse("1.21.0"): [
            './features/deployment',  # Requires 'cpp_info.names'
            './libraries/poco/md5',  # Requires 'cpp_info.names'
            ],
        }
    for v, examples in required_conan.items():
        if current_version < v:
            skip.extend(examples)

    # Some invalid configurations
    if "2017" in appveyor_image():
        skip.append('./libraries/folly')  # Requires VS2019 (>=15)

    return [os.path.normpath(it) for it in skip]


def get_build_list():
    skip_examples = get_examples_to_skip(current_version=version.parse(conan_version))

    builds = []
    script = "build.bat" if platform.system() == "Windows" else "build.sh"
    skip_folders = [os.path.normpath(it) for it in ['./.ci', './.git', './.tox']]
    for root, dirs, files in os.walk('.'):
        root = os.path.normpath(root)
        if root in skip_folders:
            dirs[:] = []
            continue
        if root in skip_examples:
            dirs[:] = []
            sys.stdout.write("Skip {!r} example\n".format(root))
            continue

        # Look for 'build' script, prefer 'build.py' over all of them
        build = [it for it in files if "build.py" in it]
        if not build:
            build = [it for it in files if os.path.basename(it) == script]
        
        if build:
            builds.append(os.path.join(root, build[0]))
            dirs[:] = []
            continue
    return builds


def chmod_x(script):
    logging.debug("chmod +x {}".format(script))
    st = os.stat(script)
    os.chmod(script, st.st_mode | stat.S_IEXEC)


def get_conan_env(script):
    temp_folder = os.path.join(tempfile.gettempdir(), str(uuid.uuid4())[:4])
    os.environ["CONAN_USER_HOME"] = temp_folder
    logging.debug("CONAN_USER_HOME: {}".format(temp_folder))
    return os.environ


def configure_profile(env):
    subprocess.check_output("conan profile new default --detect",
                            stderr=subprocess.STDOUT,
                            shell=True,
                            env=env)
    if platform.system() == "Linux":
        subprocess.check_output("conan profile update settings.compiler.libcxx=libstdc++11 default",
                                stderr=subprocess.STDOUT,
                                shell=True,
                                env=env)


def print_build(script):
    dir_name = os.path.dirname(script)
    dir_name = dir_name[2:] if dir_name.startswith('.') else dir_name
    writeln_console("================================================================")
    writeln_console("* " + colorama.Style.BRIGHT + "{}".format(dir_name.upper()))
    writeln_console("================================================================")


@contextmanager
def ensure_cache_preserved():
    cache_directory = os.environ["CONAN_USER_HOME"]

    git = Git(folder=cache_directory)
    with open(os.path.join(cache_directory, '.gitignore'), 'w') as gitignore:
        gitignore.write(".conan/data/")
    git.run("init .")
    git.run("add .")

    try:
        yield
    finally:
        r = git.run("diff")
        if r:
            writeln_console(">>> " + colorama.Fore.RED + "This is example modifies the cache!")
            writeln_console(r)
            raise Exception("Example modifies cache!")


@contextmanager
def ensure_python_environment_preserved():
    freeze = subprocess.check_output("{} -m pip freeze".format(sys.executable), stderr=subprocess.STDOUT, shell=True).decode()
    try:
        yield
    finally:
        freeze_after = subprocess.check_output("{} -m pip freeze".format(sys.executable), stderr=subprocess.STDOUT, shell=True).decode()
        if freeze != freeze_after:
            writeln_console(">>> " + colorama.Fore.RED + "This example modifies the Python dependencies!")
            removed = set(freeze.splitlines()) - set(freeze_after.splitlines())
            added = set(freeze_after.splitlines()) - set(freeze.splitlines())
            for it in removed:
                writeln_console("- " + it)
            for it in added:
                writeln_console("+ " + it)
            raise Exception("Example modifies Python environment!")


def run_scripts(scripts):
    results = OrderedDict.fromkeys(scripts, '')
    for script in scripts:
        chmod_x(script)
        abspath = os.path.abspath(script)
        env = get_conan_env(script)
        configure_profile(env)
        with chdir(os.path.dirname(script)):
            print_build(script)
            build_script = [sys.executable, abspath] if abspath.endswith(".py") else abspath
            
            # Need to initialize the cache with default files if they are not already there
            try:
                subprocess.call(['conan', 'install', 'foobar/foobar@conan/stable'], env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass
 
            with ensure_python_environment_preserved():
                with ensure_cache_preserved():
                    result = subprocess.call(build_script, env=env)
                
            results[script] = result
            if result != 0 and FAIL_FAST:
                break
    return results


def print_results(results):
    columns = []
    for build, result in results.items():
        build_name = os.path.dirname(build).upper()
        build_name = build_name[2:] if build_name.startswith(".") else build_name
        columns.append([build_name, get_result_message(result)])
    writeln_console("\n")
    writeln_console(tabulate(columns, headers=["CONAN EXAMPLE", "RESULT"], tablefmt="grid"))


def get_result_message(result):
    if result == 0:
        return colorama.Fore.GREEN + "SUCCESS" + colorama.Style.RESET_ALL
    return colorama.Fore.RED + "FAILURE" + colorama.Style.RESET_ALL


def validate_results(results):
    for value in results.values():
        if value != 0:
            sys.exit(value)


if __name__ == "__main__":
    colorama.init(autoreset=True)
    scripts = get_build_list()
    results = run_scripts(scripts)
    print_results(results)
    validate_results(results)
