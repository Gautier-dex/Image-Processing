#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "bmp8.h"
#include "bmp24-partie2.h"

int main(int argc, char *argv[]) {
    // Usage: ./imageprocessing <input.bmp> <output.bmp> <filter>
    if (argc < 4) {
        printf("Usage: %s <input.bmp> <output.bmp> <filter>\n", argv[0]);
        return 1;
    }

    char *inputFile = argv[1];
    char *outputFile = argv[2];
    char *filter = argv[3];

    // On essaie de charger en 8-bit d'abord
    t_bmp8 *img8 = bmp8_loadImage(inputFile);
    
    if (img8 != NULL) {
        if (strcmp(filter, "negative") == 0) {
            bmp8_negative(img8);
        } else if (strcmp(filter, "threshold") == 0) {
            bmp8_threshold(img8, 128);
        } else if (strcmp(filter, "brightness") == 0) {
            bmp8_brightness(img8, 50);
        } else if (strcmp(filter, "outline") == 0) {
            float **kernel = malloc(3 * sizeof(float *));
            for (int i = 0; i < 3; i++) kernel[i] = malloc(3 * sizeof(float));
            float outline[3][3] = {{-1, -1, -1}, {-1, 8, -1}, {-1, -1, -1}};
            for (int i = 0; i < 3; i++)
                for (int j = 0; j < 3; j++) kernel[i][j] = outline[i][j];
            bmp8_applyFilter(img8, kernel, 3);
            for (int i = 0; i < 3; i++) free(kernel[i]);
            free(kernel);
        }
        bmp8_saveImage(outputFile, img8);
        bmp8_free(img8);
    } else {
        printf("Erreur de chargement de l'image.\n");
        return 1;
    }

    return 0;
}
