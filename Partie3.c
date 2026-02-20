#include "Partie3.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "bmp24-partie2.h"

//Début 3.3

//Première fonction : partie 3.3.1
unsigned int * bmp8_computeHistogram(t_bmp8 * img) {
    if (img == NULL || img->data == NULL) {
        return NULL;
    }

    unsigned int *histogram = malloc(256 * sizeof(unsigned int));
    if (histogram == NULL) {
        return NULL;
    }

    //On commence par initialiser toutes les cases à 0
    for (int i = 0; i < 256; i++) {
        histogram[i] = 0;
    }

    // Simplement parcourir chaque pixel et rajouté un à la case à laquelle correspond son niveau de gris
    for (unsigned int i = 0; i < img->dataSize; i++) {
        unsigned char pixel_value = img->data[i];  // entre 0 et 255
        histogram[pixel_value]++;
    }

    return histogram;
}

//dexième fonction : partie 3.3.2
unsigned int * bmp8_computeCDF(unsigned int * hist) {

    if (hist == NULL) {
        return NULL;
    }

    unsigned int *cdf = malloc(256 * sizeof(unsigned int));
    if (cdf == NULL) {
        return NULL;
    }

    cdf[0] = hist[0];

    for (int i = 1; i < 256; i++) {
        cdf[i] = cdf[i - 1] + hist[i];
    }

    unsigned int *hist_eq = malloc(256 * sizeof(unsigned int));
    if (hist_eq == NULL) {
        free(cdf);
        return NULL;
    }


    unsigned int cdf_min = cdf[0];

    unsigned int N = cdf[255]; //car cdf[255] = hist[0] + hist[1] + ... + hist[255] donc cela correspond bien au nombre de pixels

    //formule donnée
    for (int i = 0; i < 256; i++) {
        hist_eq[i] = round(((double)(cdf[i] - cdf_min) / (N - cdf_min)) * 255);
    }

    free (cdf);

    return hist_eq;
}


//troisième fonction : partie 3.3.3
void bmp8_equalize(t_bmp8 *img) {
    if (img == NULL) {
        return;
    }

    unsigned int *hist = bmp8_computeHistogram(img);
    if (hist == NULL) {
        return;
    }

    unsigned int *hist_eq = bmp8_computeCDF(hist); // je fais comme indiquer sur le document, donc j'ai enlevé de hist_eq des paramètres car il n'était pas utilisé ¯\_(ツ)_/¯
    if (hist_eq == NULL) {
        free(hist);
        return;
    }

    for (int i = 0; i < img->dataSize; i++) {
        img->data[i] = hist_eq[img->data[i]];
    }

    free(hist);
    free(hist_eq);
}


//Début 3.4

//Pour cette partie je vais reprendre la forme de comment on a réussi à faire bmp8_equalize. C'est à dire que je vais refaire les 2 autres fonctions bmp8_computeCDF et bmp8_computeHistogram mais au format bmp24 :)

unsigned int *bmp24_computeHistogramY(t_bmp24 *img) {
    if (img == NULL || img->data == NULL) {
        return NULL;
    }

    unsigned int *histogram = malloc(256 * sizeof(unsigned int));
    if (histogram == NULL) {
        return NULL;
    }

    for (int i = 0; i < 256; i++) {
        histogram[i] = 0;
    }

    // On parcoure tous les pixels dans le but de calculer Y
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            t_pixel p = img->data[y][x];

            // Formule donnée :
            unsigned char Y = (unsigned char)(0.299 * p.red + 0.587 * p.green + 0.114 * p.blue);

            histogram[Y]++;
        }
    }

    return histogram;
}

unsigned int *bmp24_computeCDF(unsigned int *hist, int total_pixels) {
    if (hist == NULL || total_pixels <= 0) {
        return NULL;
    }

    unsigned int *cdf = malloc(256 * sizeof(unsigned int));
    if (cdf == NULL) {
        return NULL;
    }

    cdf[0] = hist[0];
    for (int i = 1; i < 256; i++) {
        cdf[i] = cdf[i - 1] + hist[i];
    }

    int cdf_min = cdf[0];

    unsigned int *hist_eq = malloc(256 * sizeof(unsigned int));
    if (hist_eq == NULL) {
        free(cdf);
        return NULL;
    }

    //formule de normalisation :
    for (int i = 0; i < 256; i++) {
        hist_eq[i] = round(((double)(cdf[i] - cdf_min) / (total_pixels - cdf_min)) * 255);
    }

    free(cdf);
    return hist_eq;
}

void bmp24_equalize(t_bmp24 *img) {
    if (img == NULL || img->data == NULL) return;

    int total_pixels = img->width * img->height;

    unsigned int *hist = bmp24_computeHistogramY(img);
    if (hist == NULL) return;

    unsigned int *hist_eq = bmp24_computeCDF(hist, total_pixels);
    free(hist);
    if (hist_eq == NULL) return;

    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            t_pixel *p = &img->data[y][x];

            int old_Y = 0.299 * p->red + 0.587 * p->green + 0.114 * p->blue; //utilisation de la formule donnée
            int new_Y = hist_eq[old_Y];

            if (old_Y == 0) continue;

            float ratio = (float)new_Y / old_Y;

            int r = p->red * ratio;
            int g = p->green * ratio;
            int b = p->blue * ratio;

            if (r > 255)
                r = 255;

            if (r < 0)
                r = 0;

            if (g > 255)
                g = 255;

            if (g < 0)
                g = 0;

            if (b > 255)
                b = 255;

            if (b < 0)
                b = 0;

            p->red = r;
            p->green = g;
            p->blue = b;
        }
    }

    free(hist_eq);
}