#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from __future__ import print_function
import os
import json
import sys
from distutils.dir_util import copy_tree

def get_dirs():
    data = json.load(open("conanbuildinfo.json"))
    dep_lib_dirs = dict()
    dep_bin_dirs = dict()
    for dep in data["dependencies"]:
        root = dep["rootpath"]
        lib_paths = dep["lib_paths"]
        bin_paths = dep["bin_paths"]
        for lib_path in lib_paths:
            if os.listdir(lib_path):
                 lib_dir = os.path.relpath(lib_path, root)
                 dep_lib_dirs[lib_path] = lib_dir
        for bin_path in bin_paths:
            if os.listdir(bin_path):
                bin_dir = os.path.relpath(bin_path, root)
                dep_bin_dirs[bin_path] = bin_dir
    return dep_lib_dirs, dep_bin_dirs

def chmod_plus_x(name):
    if os.name == 'posix':
        os.chmod(name, os.stat(name).st_mode | 0o111)

def create_entry_point(destdir, dep_lib_dirs, dep_bin_dirs):
    executable = "md5"
    varname = "$PWD"
    def _format_dirs(dirs):
        return ":".join(["%s/%s" % (varname, d) for d in dirs])
    path = _format_dirs(set(dep_bin_dirs.values()))
    ld_library_path = _format_dirs(set(dep_lib_dirs.values()))
    exe = varname + "/" + executable
    content = """#!/usr/bin/env bash
set -ex
export PATH=$PATH:{path}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{ld_library_path}
pushd $(dirname {exe})
$(basename {exe})
popd
""".format(path=path,
           ld_library_path=ld_library_path,
           exe=exe)
    entrypoint = os.path.join(destdir, "conan-entrypoint.sh")
    with open(entrypoint, "w") as f:
        f.write(content)
    chmod_plus_x(entrypoint)

def copy_files(destdir, dep_lib_dirs, dep_bin_dirs):
    for src_lib_dir, dst_lib_dir in dep_lib_dirs.items():
        copy_tree(src_lib_dir, os.path.join(destdir, dst_lib_dir))
    for src_bin_dir, dst_bin_dir in dep_bin_dirs.items():
        copy_tree(src_bin_dir, os.path.join(destdir, dst_bin_dir))

def main(argv):
    dep_lib_dirs, dep_bin_dirs = get_dirs()
    print(dep_lib_dirs, dep_bin_dirs)
    copy_files(argv[1], dep_lib_dirs, dep_bin_dirs)
    create_entry_point(argv[1], dep_lib_dirs, dep_bin_dirs)

if __name__ == '__main__':
    main(sys.argv)
