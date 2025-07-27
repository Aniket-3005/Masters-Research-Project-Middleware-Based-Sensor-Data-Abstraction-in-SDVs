cmake_minimum_required(VERSION 3.20)
project("generated_code")

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/..
    ${CMAKE_CURRENT_SOURCE_DIR}/../generated
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build type default
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to 'Release' as none was specified.")
    set(CMAKE_BUILD_TYPE Release CACHE STRING
        "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel."
        FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

message(STATUS "Configuring RawImageMsg...")

# RawImageMsg shared library
add_library(RawImageMsg_lib
    RawImageMsgTypeObjectSupport.cxx
    RawImageMsgPubSubTypes.cxx
)

target_link_libraries(RawImageMsg_lib
    fastcdr
    fastdds
)

# Publisher executable
add_executable(dds_rpi_publisher
    ../main.cpp
    RawImageMsgTypeObjectSupport.cxx
    RawImageMsgPubSubTypes.cxx
)

target_link_libraries(dds_rpi_publisher
    RawImageMsg_lib
    fastcdr
    fastdds
)

