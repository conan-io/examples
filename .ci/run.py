#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import stat
import platform
import subprocess
import tempfile
import logging
import uuid
from contextlib import contextmanager
from collections import OrderedDict
from tabulate import tabulate
import colorama
import hashlib


FAIL_FAST = os.getenv("FAIL_FAST", "0").lower() in ["1", "y", "yes", "true"]
LOGGING_LEVEL = int(os.getenv("CONAN_LOGGING_LEVEL", logging.INFO))
logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=LOGGING_LEVEL)


def is_appveyor():
    return os.getenv("APPVEYOR", False)


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


def get_build_list():
    builds = []
    folders = ["features", "libraries"]
    script = "build.bat" if platform.system() == "Windows" else "build.sh"
    for folder in folders:
        for root, _, files in os.walk(folder):
            # prefer python when present
            build = [it for it in files if "build.py" in it]
            if build:
                builds.append(os.path.join(root, build[0]))
                break

            for file in files:
                if os.path.basename(file) == script:
                    builds.append(os.path.join(root, file))

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
    # The examples cannot modify the cache
    def compute_hashes():
        hashes = {}
        for root, dirs, filenames in os.walk(cache_directory):
            dirs[:] = [d for d in dirs if d not in ['data', ]]  # Check all files but the storage folder
            for filename in filenames:
                filepath = os.path.join(root, filename)
                hashes[filepath] = hashlib.md5(open(filepath, 'rb').read()).digest()
        return hashes
    
    before_hashes = compute_hashes()
    try:
        yield
    finally:
        after_hashes = compute_hashes()

        added_keys = set(after_hashes.keys()) - set(before_hashes.keys())
        diff_values = [k for k,v in after_hashes.items() if k in before_hashes and before_hashes.get(k) != v]

        if added_keys or diff_values:
            diffs = set(list(added_keys) + diff_values)
            msg = "Current example modifies the cache.\n"
            if added_keys:
                msg += " - New files added to the cache:\n"    
                for item in added_keys:
                    msg += "   + {}\n".format(item)
            if diff_values:
                msg += " - Modified files:\n"    
                for item in diff_values:
                    msg += "   + {}\n".format(item)
            
            raise Exception(msg)


def run_scripts(scripts):
    results = OrderedDict.fromkeys(scripts, '')
    for script in scripts:
        chmod_x(script)
        abspath = os.path.abspath(script)
        env = get_conan_env(script)
        configfile_path = os.path.join(os.environ["CONAN_USER_HOME"], "conan.conf")
        configure_profile(env)
        with chdir(os.path.dirname(script)):
            print_build(script)
            build_script = [sys.executable, abspath] if abspath.endswith(".py") else abspath
            
            subprocess.call(['conan', 'install', 'zlib/1.2.11@conan/stable'], env=env)  # Need to initialize the cache with something
            subprocess.call(['conan', 'config', 'set', 'log.print_run_commands=True'], env=env)
 
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
