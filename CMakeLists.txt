cmake_minimum_required(VERSION 3.10)
project(imageprocessing C)

set(CMAKE_C_STANDARD 11)

# Liste de TOUS tes fichiers .c nécessaires
add_executable(imageprocessing 
    main.c 
    bmp8.c 
    bmp24-partie2.c
)

# On s'assure que les headers sont trouvés
include_directories(.)
