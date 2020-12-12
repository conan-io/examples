set -x
set -e

conan export library/conanfile.py library/1.0@
conan export app/conanfile.py app/1.0@

conan install app/1.0@ --build=missing
