## imgui - opencv

Just a simple demo to add opencv, imgui and poco libraries to a project using Conan.io
The program will download a picture from the Internet and apply a threshold to the image with the desired level through an slider.

![use](https://raw.githubusercontent.com/conan-io/examples/master/libraries/imgui-opencv-poco/data/screen-capture.gif)

## How to use:

This project provides 2 build systems. CMake one should work for all platforms. It also integrates a Visual Studio project, only
for those interested in the pure Visual Studio integration without using CMake, but not mandatory, you can use the CMake one for
Windows and having CMake compile with Visual Studio compiler.

1. Install conan: https://docs.conan.io/en/latest/installation.html
2. Clone this repo: `git clone https://github.com/conan-io/examples.git`
3. `cd libraries/imgui-opencv-poco`

For CMake

4. `mkdir build && cd build`
5. `conan install ..`
6. `conan build ..`
7. `./bin/imgui-opencv`

For Visual Studio 16 2019

4. `cd msvc`
5. `conan install .. -g=MSBuildDeps -if=conan`
6. Open msvc.sln
7. Change to Release and x64 configuration in IDE
8. Build solution & run


#### App running
* You can use a custom url to load your image
* Click 'Open' to open the image
* Apply a threshold with the slider
