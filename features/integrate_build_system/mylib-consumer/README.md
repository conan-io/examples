## How to Use

1. `mkdir build && cd build`
2. `conan install ..`

#### Build for Windows:
```
cmake .. -G "Visual Studio 15 Win64"
cmake --build . --config Release
```

#### Build for Linux:
```
cmake .. -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build .
```