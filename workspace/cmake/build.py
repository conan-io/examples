import os
import shutil

def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception("Command failed: %s" % cmd)

def init_folders():
    shutil.rmtree("say/build", ignore_errors=True)
    shutil.rmtree("hello/build", ignore_errors=True)
    shutil.rmtree("chat/build", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    os.mkdir("build")

# Visual Studio
init_folders()
os.chdir("build")
run("conan workspace install ../conanws_vs.yml")
run("conan workspace install ../conanws_vs.yml -s build_type=Debug")
run('cmake .. -G "Visual Studio 15 Win64"')
run('cmake --build . --config Release')
run('cmake --build . --config Debug')
os.chdir("..")
run('cd chat/build/Release && app')
run('cd chat/build/Debug && app')


# MinGW/Gcc
init_folders()
shutil.rmtree("build_release", ignore_errors=True)
os.mkdir("build_release")
shutil.rmtree("build_debug", ignore_errors=True)
os.mkdir("build_debug")

run("cd build_release && conan workspace install -pr=mingw ../conanws_gcc.yml")
run("cd build_debug   && conan workspace install -pr=mingw ../conanws_gcc.yml -s build_type=Debug")

generator = "MinGW Makefiles"
# First two are useless, they fail in my system due to sh.exe in the path for MinGW
os.system('cd build_release && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Release' % generator )
os.system('cd build_debug && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Debug' % generator )
run('cd build_release && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Release' % generator )
run('cd build_debug && cmake .. -G "%s" -DCMAKE_BUILD_TYPE=Debug' % generator )

run('cd build_release && cmake --build .')
run('cd build_debug && cmake --build .')

# create
print "GCC!!!"
run('cd chat/build/Release && app')
run('cd chat/build/Debug && app')

run("conan create say user/testing")
run("conan create hello user/testing")
run("conan create chat user/testing")