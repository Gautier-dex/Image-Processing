cmake_minimum_required(VERSION 3.10)
project(imageprocessing C)

set(CMAKE_C_STANDARD 11)

# On inclut tous les fichiers sources pour que la compilation soit complète
add_executable(imageprocessing 
    main.c 
    bmp8.c 
    bmp24-partie2.c
)
