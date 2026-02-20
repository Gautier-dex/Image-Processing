cmake_minimum_required(VERSION 3.30)
project(imageprocessing C)

set(CMAKE_C_STANDARD 11)

add_executable(imageprocessing main.c
        bmp8.c
        bmp8.h
        bmp24-partie2.c
        bmp24-partie2.h)
