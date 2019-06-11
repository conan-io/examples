CMAKE_MINIMUM_REQUIRED(VERSION 2.8)
PROJECT(encryption-test CXX)

# Initialize Conan #############################################################
INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

# Create application test ######################################################
ADD_EXECUTABLE(${PROJECT_NAME} encryption_test.cpp)
TARGET_LINK_LIBRARIES(${PROJECT_NAME} ${CONAN_LIBS})

# Include Encryptor test #######################################################
ENABLE_TESTING()
ADD_TEST(NAME encryption
         WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
         COMMAND ${PROJECT_NAME})
