#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil
import platform
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def init_folders():
    shutil.rmtree("say/build", ignore_errors=True)
    shutil.rmtree("hello/build", ignore_errors=True)
    shutil.rmtree("chat/build", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("build_release", ignore_errors=True)
    shutil.rmtree("build_debug", ignore_errors=True)
    os.mkdir("build")

if __name__ == "__main__":
    init_folders()
    if platform.system() == "Windows":
        cmake_generator = os.getenv("CMAKE_GENERATOR", "Visual Studio 15 2017 Win64")
        if "Visual Studio" in cmake_generator:
            print("Windows Visual Studio build")
            os.chdir("build")
            run("conan workspace install ../conanws_vs.yml")
            run("conan workspace install ../conanws_vs.yml -s build_type=Debug")
            run('cmake .. -G "%s"' % cmake_generator)
            run('cmake --build . --config Release')
            run('cmake --build . --config Debug')
            os.chdir("..")
            run(os.path.join('chat', 'build', 'Release', 'app.exe'))
            run(os.path.join('chat', 'build', 'Debug', 'app.exe'))
        else:
            print("Windows MinGW build")
            os.mkdir("build_release")
            os.mkdir("build_debug")
            run("cd build_release && conan workspace install -pr=mingw ../conanws_gcc.yml")
            run("cd build_debug   && conan workspace install -pr=mingw ../conanws_gcc.yml -s build_type=Debug")

            run('cd build_release && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Release' % cmake_generator)
            run('cd build_debug && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Debug' % cmake_generator)
            run('cd build_release && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Release' % cmake_generator)
            run('cd build_debug && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Debug' % cmake_generator)

            run('cd build_release && cmake --build .')
            run('cd build_debug && cmake --build .')

            run('cd chat/build/Release && app')
            run('cd chat/build/Debug && app')

            run("conan create say user/testing")
            run("conan create hello user/testing")
            run("conan create chat user/testing")
    else:
        print("Unix build")
        os.chdir("build")
        run("conan workspace install ../conanws_gcc.yml")
        run('cmake .. -DCMAKE_BUILD_TYPE=Release')
        run('cmake --build .')
        os.chdir("..")
        run(os.path.join('chat', 'build', 'Release', 'app'))
