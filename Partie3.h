#ifndef PARTIE3_H
#define PARTIE3_H


#include "bmp8.h"
#include "bmp24-partie2.h"

unsigned int * bmp8_computeHistogram(t_bmp8 * img);
unsigned int * bmp8_computeCDF(unsigned int * hist);
void bmp8_equalize(t_bmp8 * img);

unsigned int *bmp24_computeHistogramY(t_bmp24 *img);
unsigned int *bmp24_computeCDF(unsigned int *hist, int total_pixels);
void bmp24_equalize(t_bmp24 *img);


#endif //PARTIE3_H