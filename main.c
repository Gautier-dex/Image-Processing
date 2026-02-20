#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "bmp8.h"

int main(void) {

	t_bmp8 *img = bmp8_loadImage("PieceJointeProjet/lena_gray.bmp");

	// pour tester la dernière fonction avec les filtres :

	float **kernel = malloc(3 * sizeof(float *));
	for (int i = 0; i < 3; i++) {
		kernel[i] = malloc(3 * sizeof(float));
	}

	float outline[3][3] = {
		{-1, -1, -1},
		{-1,  8, -1},
		{-1, -1, -1}
	};

	float emboss[3][3] = {
		{-2, -1, 0},
		{-1,  1, 1},
		{ 0,  1, 2}
	};

	for (int i = 0; i < 3; i++) {
		for (int j = 0; j < 3; j++) {
			kernel[i][j] = outline[i][j];
		}
	}

	bmp8_applyFilter(img, kernel, 3);

	bmp8_saveImage("lena_outline.bmp", img);

	for (int i = 0; i < 3; i++) {
		free(kernel[i]);
	}
	free(kernel);
	bmp8_free(img);

	return 0;
}
