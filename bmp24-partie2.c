#include "bmp24-partie2.h"
#include <stdio.h>

// Début 2.3

t_pixel ** bmp24_allocateDataPixels (int width, int height){

}

void bmp24_freeDataPixels (t_pixel ** pixels, int height){

}


t_bmp24 * bmp24_allocate (int width, int height, int colorDepth) {

}


void bmp24_free (t_bmp24 * img) {

}

// Fin 2.3

// Début 2.4

/*
 * @brief Positionne le curseur de fichier à la position `position` dans le fichier `file`,
 * puis lit `n` éléments de taille `size` dans `buffer`.
 * @param position La position à partir de laquelle il faut lire dans file.
 * @param buffer Le buffer pour stocker les données lues.
 * @param size La taille de chaque élément à lire.
 * @param n Le nombre d'éléments à lire.
 * @param file Le descripteur de fichier dans lequel il faut lire.
 * @return void
 */
void file_rawRead(uint32_t position, void *buffer, uint32_t size, size_t n, FILE *file) {
    fseek(file, position, SEEK_SET);
    fread(buffer, size, n, file);
}

/*
 * @brief Positionne le curseur de fichier à la position `position` dans le fichier `file`,
 * puis écrit `n` éléments de taille `size` depuis le `buffer`.
 * @param position La position à partir de laquelle il faut écrire dans file.
 * @param buffer Le buffer contenant les éléments à écrire.
 * @param size La taille de chaque élément à écrire.
 * @param n Le nombre d'éléments à écrire.
 * @param file Le descripteur de fichier dans lequel il faut écrire.
 * @return void
 */
void file_rawWrite(uint32_t position, void *buffer, uint32_t size, size_t n, FILE *file) {
    fseek(file, position, SEEK_SET);
    fwrite(buffer, size, n, file);
}

void bmp24_readPixelValue(t_bmp24 *image, int x, int y, FILE *file) {

}

void bmp24_readPixelData(t_bmp24 *image, FILE *file) {

}

void bmp24_writePixelValue(t_bmp24 *image, int x, int y, FILE *file) {

}

void bmp24_writePixelData(t_bmp24 *image, FILE *file) {

}

//Fin 2.4

//Début 2.5

void bmp24_negative(t_bmp24 *img) {

}

void bmp24_grayscale(t_bmp24 *img) {

}

void bmp24_brightness(t_bmp24*img, int value) {

}

//Fin 2.5

//Début 2.6

t_pixel bmp24_convolution(t_bmp24 *img, int x, int y, float **kernel, int kernelSize) {

}


// Fin 2.6