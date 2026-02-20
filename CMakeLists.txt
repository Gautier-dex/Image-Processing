cmake_minimum_required(VERSION 3.10)
project(imageprocessing C)

set(CMAKE_C_STANDARD 11)

add_executable(imageprocessing 
    main.c
    bmp8.c
    bmp24-partie2.c
    Bonus-Affichage-utilisateur.c
    Partie3.c
)

# Inclusion des répertoires pour trouver les .h
include_directories(.)
