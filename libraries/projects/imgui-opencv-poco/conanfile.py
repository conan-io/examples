from conans import ConanFile, CMake


class ImguiOpencvDemo(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "imgui/1.79",\
               "glfw/3.3.2",\
               "glew/2.1.0",\
               "opencv/2.4.13.7",\
               "poco/1.10.1"

    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("imgui_impl_glfw.cpp", dst="../src", src="./res/bindings")
        self.copy("imgui_impl_opengl3.cpp", dst="../src", src="./res/bindings")
        self.copy("imgui_impl_glfw.h*", dst="../include", src="./res/bindings")
        self.copy("imgui_impl_opengl3.h*", dst="../include", src="./res/bindings")
