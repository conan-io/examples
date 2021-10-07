cmake_minimum_required(VERSION 3.15)
project(say CXX)

add_library(say src/say.cpp)

set_target_properties(say PROPERTIES PUBLIC_HEADER "src/say.h")
install(TARGETS say DESTINATION "."
        PUBLIC_HEADER DESTINATION include
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
