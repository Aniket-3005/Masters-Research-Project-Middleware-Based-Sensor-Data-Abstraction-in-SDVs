cmake_minimum_required(VERSION 3.5)
project(dds_rpi_publisher)

find_package(fastrtps REQUIRED)
find_package(fastcdr REQUIRED)

include_directories(
    generated
)

file(GLOB SOURCES
    main.cpp
    generated/*.cxx
)

add_executable(dds_rpi_publisher ${SOURCES})

target_link_libraries(dds_rpi_publisher
    fastrtps
    fastcdr
)
