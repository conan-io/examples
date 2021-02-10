#pragma once

#include <opencv2/opencv.hpp>
#include "imgui.h"
#include "../include/imgui_impl_glfw.h"
#include "../include/imgui_impl_opengl3.h"
#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "../include/downloader.h"

#include <stdio.h>
#include <vector>
#include <array>

#if defined(_MSC_VER) && (_MSC_VER >= 1900) && !defined(IMGUI_DISABLE_WIN32_FUNCTIONS)
#pragma comment(lib, "legacy_stdio_definitions")
#endif

class GUIRenderer
{
public:
	GUIRenderer();
	~GUIRenderer(void);
	int InitGUI();
	void Render();
	void ShowImage();
	void UpdateTexture();

private:
	GLFWwindow *window_;
	GLuint texture_id_;
	int image_width_, image_height_;
	Downloader downloader_;
	cv::Mat resized_image_;
	cv::Mat thresholded_image_;
	int threshold_;
};
