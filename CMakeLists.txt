cmake_minimum_required(VERSION 3.10)
project(msoff C)

set(CMAKE_C_STANDARD 99)

add_executable(msoff src/main.c)

target_link_libraries(msoff user32)
