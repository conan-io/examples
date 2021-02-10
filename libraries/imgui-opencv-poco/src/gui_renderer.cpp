#include "gui_renderer.hpp"

static void glfw_error_callback(int error, const char *description)
{
    fprintf(stderr, "Glfw Error %d: %s\n", error, description);
}

GUIRenderer::GUIRenderer(void) : texture_id_(-1), threshold_(127)
{
}

GUIRenderer::~GUIRenderer(void)
{
}

int GUIRenderer::InitGUI()
{
    glfwSetErrorCallback(glfw_error_callback);
    if (!glfwInit())
        return 1;

        // Decide GL+GLSL versions
#if __APPLE__
    // GL 3.2 + GLSL 150
    const char *glsl_version = "#version 150";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // 3.2+ only
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);           // Required on Mac
#else
    // GL 3.0 + GLSL 130
    const char *glsl_version = "#version 130";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
    //glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
    //glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // 3.0+ only
#endif

    // Create window with graphics context
    window_ = glfwCreateWindow(1280, 720, "imgui-opencv demo", NULL, NULL);
    if (window_ == NULL)
        return 1;
    glfwMakeContextCurrent(window_);
    glfwSwapInterval(1); // Enable vsync

    // Initialize OpenGL loader
    bool err = glewInit() != GLEW_OK;
    if (err)
    {
        fprintf(stderr, "Failed to initialize OpenGL loader!\n");
        return 1;
    }
    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO &io = ImGui::GetIO();
    (void)io;
    ImGui::StyleColorsDark();
    // Setup Platform/Renderer bindings
    ImGui_ImplGlfw_InitForOpenGL(window_, true);
    ImGui_ImplOpenGL3_Init(glsl_version);
    return 0;
}

void GUIRenderer::UpdateTexture()
{
    unsigned char *data = thresholded_image_.ptr();
    image_width_ = thresholded_image_.cols;
    image_height_ = thresholded_image_.rows;
    if (texture_id_ == -1)
        glGenTextures(1, &texture_id_);
    glBindTexture(GL_TEXTURE_2D, texture_id_);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image_width_, image_height_, 0, GL_BGR, GL_UNSIGNED_BYTE, data);
    glGenerateMipmap(GL_TEXTURE_2D);
}

void GUIRenderer::ShowImage()
{
    ImGui::Begin("Image");
    // Image downloaded from: https://www.pexels.com/photo/green-bird-1661179/
    static char image_url[256] = "https://raw.githubusercontent.com/conan-io/examples/master/libraries/imgui-opencv-poco/data/bird.jpeg";
    ImGui::InputText("URL:", image_url, IM_ARRAYSIZE(image_url));
    ImGui::SameLine();
    if (ImGui::Button("Open"))
    {
        std::string filename = "";
        try
        {
            filename = downloader_.DownloadFile(std::string(image_url));
        }
        catch (Exception &exc)
        {
            std::cerr << exc.displayText() << std::endl;
        }
        if (filename != "")
        {
            cv::Mat image = cv::imread(filename.c_str());
            if (!image.empty())
            {
                int resized_width = 640;
                double scale = static_cast<float>(resized_width)/image.size().width;
                cv::resize(image, resized_image_, cv::Size(0, 0), scale, scale);
                resized_image_.copyTo(thresholded_image_);
                UpdateTexture();
            }
        }
    }
    if (texture_id_ != -1)
    {
        ImVec2 canvas_size = ImVec2(image_width_, image_height_);
        ImGui::ImageButton((void *)(intptr_t)texture_id_, canvas_size, ImVec2(0, 0), ImVec2(1, 1), 0);
        ImGui::PushItemWidth(300);
        if (ImGui::SliderInt("threshold level", &threshold_, 0, 255))
        {
            cv::threshold(resized_image_, thresholded_image_, threshold_, 255, cv::THRESH_BINARY);
            UpdateTexture();
        }
    }
    ImGui::End();
}

void GUIRenderer::Render()
{
    while (!glfwWindowShouldClose(window_))
    {
        glfwPollEvents();
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        ShowImage();

        ImGui::Render();
        int display_w, display_h;
        glfwMakeContextCurrent(window_);
        glfwGetFramebufferSize(window_, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(0.45, 0.56, 0.67, 1);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        glfwMakeContextCurrent(window_);
        glfwSwapBuffers(window_);
    }
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();
    glfwDestroyWindow(window_);
    glfwTerminate();
}
