cmake_minimum_required(VERSION 2.8)
project(hello-world CXX)

add_executable(${CMAKE_PROJECT_NAME} main.cpp)
target_link_libraries(${CMAKE_PROJECT_NAME} PUBLIC z)

install(TARGETS ${CMAKE_PROJECT_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)
