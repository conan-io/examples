@ECHO ON

pip install -U protobuf

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake .. -G "%CMAKE_GENERATOR%"
cmake --build . --config Release

bin\sensor.exe
ECHO. 2>__init__.py

POPD
python main.py