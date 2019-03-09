cmake_minimum_required(VERSION 3.0)

# CHANGE PROJECT NAME, SOURCES AND DEPENDANT TARGETS
project(hello CXX)

set(TARGET_NAME ${PROJECT_NAME})
set(${TARGET_NAME}_SRC hello.cpp)
set(${TARGET_NAME}_HEADERS hello.h)
set(TARGETS_TO_FIND "")
set(DEBUG_LIBRARY_SUFFIX "")


# GENERIC PART
add_library(${TARGET_NAME} ${${TARGET_NAME}_SRC} ${${TARGET_NAME}_HEADERS})
set_target_properties(${TARGET_NAME} PROPERTIES
                       PUBLIC_HEADER "${${TARGET_NAME}_HEADERS}"
                       OUTPUT_NAME "${TARGET_NAME}$<$<CONFIG:Debug>:${DEBUG_LIBRARY_SUFFIX}>")

target_include_directories(${TARGET_NAME} PUBLIC
                           "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
                           "$<INSTALL_INTERFACE:$<INSTALL_PREFIX>/${CMAKE_INSTALL_INCLUDEDIR}>")

foreach(dep ${TARGETS_TO_FIND})
    find_package(${dep})
    target_link_libraries(${TARGET_NAME} ${dep}::${dep})
endforeach()


# Write the library and headers
install(TARGETS ${TARGET_NAME} EXPORT ${TARGET_NAME}Targets
        LIBRARY       DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        ARCHIVE       DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        RUNTIME       DESTINATION "${CMAKE_INSTALL_BINDIR}"
        PUBLIC_HEADER DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}")

# Export the target to be used by other projects
export(EXPORT ${TARGET_NAME}Targets
  FILE "${CMAKE_CURRENT_BINARY_DIR}/${TARGET_NAME}/${TARGET_NAME}Targets.cmake"
  NAMESPACE ${TARGET_NAME}::
)

set(ConfigPackageLocation lib/cmake/${TARGET_NAME})

# Install the exported target
install(EXPORT ${TARGET_NAME}Targets
  FILE ${TARGET_NAME}Targets.cmake
  NAMESPACE ${TARGET_NAME}::
  DESTINATION ${ConfigPackageLocation}
)

# Install the XXXConfig.cmake file
install(
  FILES
    ${TARGET_NAME}Config.cmake
  DESTINATION
    ${ConfigPackageLocation}
)
