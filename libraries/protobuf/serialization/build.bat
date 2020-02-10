@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake ..
cmake --build . --config Release

bin\sensor.exe

pip install protobuf
python ../main.py
pip uninstall -y protobuf
