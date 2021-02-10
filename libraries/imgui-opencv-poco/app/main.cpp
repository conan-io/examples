// demo application to run a shader that 
// opens an image from the internet
// and applies a threshold
// using Imgui, Opencv and Poco

#include "../include/gui_renderer.hpp"

int main(int, char **)
{
	GUIRenderer renderer;
    renderer.InitGUI();
    renderer.Render();
    return 0;
}
