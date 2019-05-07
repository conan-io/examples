cmake_minimum_required(VERSION 2.8)

project(conan-hello-emscripten)

include(conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} main.cpp)

target_include_directories(${PROJECT_NAME} PRIVATE ${CONAN_INCLUDE_DIRS})
target_link_libraries(${PROJECT_NAME} PRIVATE ${CONAN_LIBS})

set_target_properties(${PROJECT_NAME} PROPERTIES
  SUFFIX ".html"
  LINK_FLAGS "--emrun")

install(TARGETS ${PROJECT_NAME}
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)
  
install(FILES
  ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${PROJECT_NAME}.js
  ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/${PROJECT_NAME}.wasm
  DESTINATION bin)
