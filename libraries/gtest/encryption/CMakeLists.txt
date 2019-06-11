CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
PROJECT(encrypter CXX)

# Initialize Conan #############################################################
INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

# Create Encrypter library #####################################################
ADD_LIBRARY(${CMAKE_PROJECT_NAME} encrypter.cpp)
TARGET_LINK_LIBRARIES(${CMAKE_PROJECT_NAME} ${CONAN_LIBS})

# Install Encrypter library ####################################################
install(TARGETS ${CMAKE_PROJECT_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)
install(FILES encrypter.h DESTINATION include)