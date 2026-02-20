cmake_minimum_required(VERSION 3.10)
project(imageprocessing C)

set(CMAKE_C_STANDARD 11)

# Liste complète de tes fichiers sources
add_executable(imageprocessing 
    main.c 
    bmp8.c 
    bmp24-partie2.c 
    Bonus-Affichage-utilisateur.c 
    Partie3.c
)

# CETTE LIGNE EST CRUCIALE : elle lie la bibliothèque mathématique
target_link_libraries(imageprocessing m)

include_directories(.)
