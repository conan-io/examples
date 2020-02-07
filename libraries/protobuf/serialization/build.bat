@ECHO ON

RMDIR /Q /S build
MKDIR build
PUSHD build

conan install ..
cmake .. -G "%CMAKE_GENERATOR%"
cmake --build . --config Release

bin\sensor.exe

python -m venv _exproto
_exproto\bin\activate.bat
pip install -U protobuf
python ..\main.py
