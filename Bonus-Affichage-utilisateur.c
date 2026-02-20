#include "Bonus-Affichage-utilisateur.h"
#include <stdio.h>
#include <stdlib.h>

#include "bmp24-partie2.h"
#include "bmp8.h"

float** choix_kernel(int choix) {


    float box_blur[3][3] = {
            {1.0f/9, 1.0f/9, 1.0f/9}, // obliger de mettre .0f car sinon cela fait une division entre 2 entiers et donne 0 et non un chiffre à virgule (float)
            {1.0f/9, 1.0f/9, 1.0f/9},
            {1.0f/9, 1.0f/9, 1.0f/9}
    };

    float gaussian_blur[3][3] = {
            {1.0f/16, 2.0f/16, 1.0f/16},
            {2.0f/16, 4.0f/16, 2.0f/16},
            {1.0f/16, 2.0f/16, 1.0f/16}
    };

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

    float sharpen[3][3] = {
            { 0, -1,  0},
            {-1,  5, -1},
            { 0, -1,  0}
    };


    // On alloue ici le kernel dynamiquement :
    float **kernel = malloc(3 * sizeof(float *));
    for (int i = 0; i < 3; i++) {
        kernel[i] = malloc(3 * sizeof(float));
    }

    float (*result)[3] = NULL;


    switch (choix) {

        case 5:
            result = box_blur;
            break;

        case 6:
            result = gaussian_blur;
            break;

        case 7:
            result = sharpen;
            break;

        case 8:
            result = outline;
            break;

        case 9:
            result = emboss;
            break;
    }

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            kernel[i][j] = result[i][j];
        }
    }
    return kernel;


}


//fonction pour savoir si l'image donner est de 8 ou 24 bits. Utile pour savoir comment appliquer les filtres ou même charger l'image.
int nombre_de_bits(const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (f == NULL) {
        return 1;
    }

    uint16_t bits;

    // De ce que j'ai trouvé il faut se placer à l’offset 0x1C (28) pour lire le champ "bits" ce qui va permettre de récupérer le champs indiquant le nombre de bit.
    fseek(f, 28, SEEK_SET);
    fread(&bits, sizeof(uint16_t), 1, f);
    fclose(f);

    return bits;
}

//pour pouvoir afficher les informations d'une image en bmp24
void bmp24_printInfo(t_bmp24 *img) {
    if (img == NULL) {
        return;
    }
    printf("Image Info:\n");
    printf("Width: %d\n", img->width);
    printf("Height: %d\n", img->height);
    printf("Color Depth: %d\n", img->colorDepth);
}


void filtres_8(t_bmp8 *img, int choix) {
    if (img == NULL) {
        return;
    }

    int value;

    switch (choix) {
        case 1:
            bmp8_negative(img);

            break;

        case 2:
            printf("Choississez une valeur pour appliquer le filtre luminosite : ");
            scanf("%d", &value);


            bmp8_brightness(img, value);

            break;

        case 3:
            printf("Choississez une valeur pour appliquer le filtre binarisation : ");
            scanf("%d", &value);

            bmp8_threshold(img, value);


            break;

        case 4 :

            printf(" Desole cette fonction n'existe pas pour les images en bmp8 mais vous pouvez toujours essayer avec une autre image :) \n");


            break;
    }
}


//à la base je voulais tout faire dans une même fonction avec if else format mais cela posait des problèmes avec l'image pris en paramètre car elle ne peut pas être bmp24 ou bmp8 :,(
void filtres_24(t_bmp24 *img, int choix) {
    if (img == NULL) {
        return;
    }

    int value;

    switch (choix) {
        case 1:

            bmp24_negative(img);

            break;

        case 2:
            printf("Choississez une valeur pour appliquer le filtre luminosite : ");
            scanf("%d", &value);


            bmp24_brightness(img, value);

            break;

        case 3:

            printf(" Desole cette fonction n'existe pas pour les images en bmp24 mais vous pouvez toujours essayer avec une autre image :) \n");


            break;

        case 4 :

            bmp24_grayscale(img);

            break;
    }
}