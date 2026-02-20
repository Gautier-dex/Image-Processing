#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "bmp8.h"

int main(int argc, char *argv[]) {
    if (argc < 4) {
        printf("Usage: %s <input.bmp> <output.bmp> <filter>\n", argv[0]);
        return 1;
    }

    char *inputFile = argv[1];
    char *outputFile = argv[2];
    char *filter = argv[3];

    t_bmp8 *img = bmp8_loadImage(inputFile);
    if (!img) return 1;

    if (strcmp(filter, "negative") == 0) {
        bmp8_negative(img);
    } 
    else if (strcmp(filter, "threshold") == 0) {
        bmp8_threshold(img, 128);
    } 
    else if (strcmp(filter, "brightness") == 0) {
        bmp8_brightness(img, 50);
    }
    else if (strcmp(filter, "outline") == 0) {
        float **kernel = malloc(3 * sizeof(float *));
        for (int i = 0; i < 3; i++) kernel[i] = malloc(3 * sizeof(float));
        float outline[3][3] = {{-1, -1, -1}, {-1, 8, -1}, {-1, -1, -1}};
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++) kernel[i][j] = outline[i][j];
        
        bmp8_applyFilter(img, kernel, 3);
        
        for (int i = 0; i < 3; i++) free(kernel[i]);
        free(kernel);
    }

    bmp8_saveImage(outputFile, img);
    bmp8_free(img);

    return 0;
}
