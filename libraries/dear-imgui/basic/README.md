## Conan Dear ImGui example

1. Install conan: https://docs.conan.io/en/latest/installation.html
2. Clone this repo: `git clone https://github.com/czoido/dear-imgui-conan-example.git`
3. Install dependencies, compile and run

## Windows with Visual Studio:

```bash
cd dear-imgui-conan-example
mkdir build
cd build
conan install .. -s build_type=Release
conan install .. -s build_type=Debug
cmake .. -G "Visual Studio 15 2017 Win64"
cmake --build . --config Release
cd Release
dear-imgui-conan
```

## Linux:

```bash
cd dear-imgui-conan-example
mkdir build
cd build
conan install .. -s build_type=Release
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
./dear-imgui-conan
```
