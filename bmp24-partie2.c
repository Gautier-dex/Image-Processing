
#include "Bonus-Affichage-utilisateur.h"
#include "bmp24-partie2.h"
#include <stdio.h>
#include <stdlib.h>

// Début 2.3

t_pixel ** bmp24_allocateDataPixels (int width, int height){
    t_pixel **matrice = (t_pixel **) malloc(height * sizeof(t_pixel *));
    if (matrice == NULL) {
        return NULL;
    }
    for (int i = 0; i < height; i++) {
        matrice[i] = (t_pixel *) malloc(width * sizeof(t_pixel));
    }
    return matrice;
}

void bmp24_freeDataPixels (t_pixel ** pixels, int height) {
    if (pixels == NULL)
        return;
    for (int i = 0; i < height; i++) {
        free(pixels[i]);
    }
    free(pixels);
}


t_bmp24 *bmp24_allocate(int width, int height, int colorDepth) {
    t_bmp24 *img = (t_bmp24 *) malloc(sizeof(t_bmp24));
    if (img == NULL)
        return NULL;

    img->data = bmp24_allocateDataPixels(width, height);
    if (img->data == NULL) {
        free(img);
        return NULL;
    }
    img->width = width;
    img->height = height;
    img->colorDepth = colorDepth;

    return img;
}


void bmp24_free(t_bmp24 *img) {
    if (img == NULL)
        return;

    bmp24_freeDataPixels(img->data, img->height);
    free(img);
}


// Fin 2.3

// Début 2.4


void file_rawRead (uint32_t position, void * buffer, uint32_t size, size_t n, FILE * file) {
    fseek(file, position, SEEK_SET);
    fread(buffer, size, n, file);
}

void file_rawWrite (uint32_t position, void * buffer, uint32_t size, size_t n, FILE * file) {
    fseek(file, position, SEEK_SET);
    fwrite(buffer, size, n, file);
}

// 2.4.2 les 4 fcts :
// fct 1 : Lire un pixel
void bmp24_readPixelValue(t_bmp24 *image, int x, int y, FILE *file) {
    if (image == NULL || file == NULL) return;

    unsigned char couleurs[3]; // [blue, green, red]
    int largeur = image->width;
    int hauteur = image->height;

    int taille_ligne = ((largeur * 3 + 3) / 4) * 4;  //ici il nous est dit qu'il n'est pas nécessaire de gérer le padding : donc pas besoin de vérifier qu'il s'agit bien d'un multiple de 4
                                                     //Mais nous on veut que notre programme marche pour le maximum de cas donc au lieu de juste faire "largeur * 3" , on fait "((largeur * 3 + 3) / 4) * 4"
                                                     //Donc en une phrase cette ligne permet de calculer combien d’octets prend une ligne d’image 24 bits dans le fichier BMP.
                                                     // largeur * 3 : chaque pixel = 3 octets , + 3 : permet d'arrondir car on travaille sur des entiers , / 4 : on s'assure que le résultat soit bien un multiple de 4 , * 4 : pour revenir sur le bon résultat voulue :)

    int ligne_fichier = hauteur - 1 - y; //je rappelle axe des y est inversée

    uint32_t position = image->header.offset + ligne_fichier * taille_ligne + x * 3; // position exacte dans le fichier

    file_rawRead(position, couleurs, sizeof(unsigned char), 3, file);

    image->data[y][x].red = couleurs[2];   // ordre BMP : BGR
    image->data[y][x].green = couleurs[1];
    image->data[y][x].blue = couleurs[0];
}


// fct 2 : Lire toute l'image
void bmp24_readPixelData(t_bmp24 *image, FILE *file) {
    if (image == NULL || file == NULL) return;
    int x, y;

    for (y = 0; y < image->height; y++) {
        for (x = 0; x < image->width; x++) {
            bmp24_readPixelValue(image, x, y, file);
        }
    }
}

// fct 3 : Écrire un pixel
void bmp24_writePixelValue(t_bmp24 *image, int x, int y, FILE *file) {
    if (image == NULL || file == NULL) return;

    int ligne_inverse = image->height - 1 - y;
    uint32_t position = image->header.offset + (ligne_inverse * image->width + x) * 3;

    unsigned char bgr[3] = {
            image->data[y][x].blue,
            image->data[y][x].green,
            image->data[y][x].red
    };

    file_rawWrite(position, bgr, sizeof(unsigned char), 3, file);
}


// fct 4 : Écrire toute l'image
void bmp24_writePixelData(t_bmp24 *image, FILE *file) {
    int x, y;

    for (y = 0; y < image->height; y++) {
        for (x = 0; x < image->width; x++) {
            bmp24_writePixelValue(image, x, y, file);
        }
    }
}


// fct 2.4.3 : Charger une image
t_bmp24 *bmp24_loadImage(const char *filename) {
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {
        printf("Erreur : impossible d’ouvrir le fichier %s.\n", filename);
        return NULL;
    }

    // On va lire la hauteur , longueur et profondeur
    int width, height, colorDepth;
    fseek(file, BITMAP_WIDTH, SEEK_SET);
    fread(&width, sizeof(int), 1, file);

    fseek(file, BITMAP_HEIGHT, SEEK_SET);
    fread(&height, sizeof(int), 1, file);

    fseek(file, BITMAP_DEPTH, SEEK_SET);
    fread(&colorDepth, sizeof(short), 1, file);

    t_bmp24 *img = bmp24_allocate(width, height, colorDepth);
    if (img == NULL) {
        fclose(file);
        return NULL;
    }

    // pareil pour header et info
    file_rawRead(0, &img->header, sizeof(t_bmp_header), 1, file);
    file_rawRead(HEADER_SIZE, &img->header_info, sizeof(t_bmp_info), 1, file);

    bmp24_readPixelData(img, file);

    fclose(file);
    return img;
}



// fct 2.4.4 : Sauvegarder une image
void bmp24_saveImage(t_bmp24 *img, const char *filename) {
    FILE *file = fopen(filename, "wb");
    if (file == NULL) {
        printf("Erreur : au niveau du save_image.\n");
        return;
    }

    // On fait l'écriture des en-tête
    file_rawWrite(0, &img->header, sizeof(t_bmp_header), 1, file);
    file_rawWrite(HEADER_SIZE, &img->header_info, sizeof(t_bmp_info), 1, file);


    bmp24_writePixelData(img, file);

    fclose(file);
}



// Fin 2.4

// Début 2.5

void bmp24_negative(t_bmp24 *img) {
//je n'appelle pas la fonction loadimage ici, il va falloir alors appeler cette fonction avant de l'utiliser sinon elle ne marchera pas.

    if (img == NULL || img->data == NULL) {
        return;
    }
    for (int i = 0; i < img->height; i++) {
        for (int j = 0; j < img->width; j++) {
            img->data[i][j].red   = 255 - img->data[i][j].red;
            img->data[i][j].green = 255 - img->data[i][j].green;
            img->data[i][j].blue  = 255 - img->data[i][j].blue;
        }
    }
}


void bmp24_grayscale(t_bmp24 *img) {
    if (img == NULL || img->data == NULL)
        return;

    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {

            unsigned char r = img->data[y][x].red; //unsigned car va de 0 à 255
            unsigned char g = img->data[y][x].green;
            unsigned char b = img->data[y][x].blue;
            unsigned char moyenne = (r + g + b) / 3;

            img->data[y][x].red = moyenne;
            img->data[y][x].green = moyenne;
            img->data[y][x].blue = moyenne;
        }
    }
}

void bmp24_brightness(t_bmp24 *img, int value) {
    if (img == NULL || img->data == NULL)
        return;

    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            int r = img->data[y][x].red + value;
            int g = img->data[y][x].green + value;
            int b = img->data[y][x].blue + value;

            if (r > 255)
                r = 255;
            else if (r < 0)
                r = 0;

            if (g > 255)
                g = 255;
            else if (g < 0)
                g = 0;

            if (b > 255)
                b = 255;
            else if (b < 0)
                b = 0;

            img->data[y][x].red = (unsigned char)r; // pour éviter les bugs on utilise (unsigned char).
            img->data[y][x].green = (unsigned char)g;
            img->data[y][x].blue = (unsigned char)b;
        }
    }
}

// Fin 2.5

// Début 2.6

//"Pour cette partie, il se trouve que j’ai déjà créé la fonction bonus sur l’application des noyaux juste avant (j’avais mal lu ce qu’il fallait faire ici).
//Donc je vais faire cette sous-partie un peu différemment de ce qui était attendu, mais en réutilisant la fonction que j’ai créée : au moins, ça ajoute un peu d’ originalité : )

t_pixel bmp24_convolution(t_bmp24 *img, int x, int y, float **kernel, int kernelSize) {
    t_pixel result;
    int offset = kernelSize / 2;

    float red = 0.0f, green = 0.0f, blue = 0.0f; // 0.0f comme vu avant .0f pour que se soit bien un float

    for (int i = -offset; i <= offset; i++) {
        for (int j = -offset; j <= offset; j++) {
            int pixel_x = x + j;
            int pixel_y = y + i;

            t_pixel p = img->data[pixel_y][pixel_x];
            float k = kernel[i + offset][j + offset];

            red   += p.red   * k;
            green += p.green * k;
            blue  += p.blue  * k;
        }
    }

    if (red < 0) {
        result.red = 0;
    } else if (red > 255) {
        result.red = 255;
    } else {
        result.red = red;
    }

    if (green < 0) {
        result.green = 0;
    } else if (green > 255) {
        result.green = 255;
    } else {
        result.green = green;
    }

    if (blue < 0) {
        result.blue = 0;
    } else if (blue > 255) {
        result.blue = 255;
    } else {
        result.blue = blue;
    }

    return result;
}

void bmp24_applySelectedFilter(t_bmp24 *img, int choix) {
    float **kernel = choix_kernel(choix); // J'appelle ici ma fonction bonus d'un autre fichier :), c'est pourquoi je rajoute un paramètre dans ma fonction.
    if (kernel == NULL) {
        printf("Erreur : Filtre pas bon.\n");
        return;
    }

    int kernelSize = 3;

    // Obliger de créer une copie de l'image ici
    t_bmp24 *copy = bmp24_allocate(img->width, img->height, img->colorDepth);
    if (copy == NULL) {
        printf("Erreur : échec de l’allocation mémoire.\n");
        for (int i = 0; i < kernelSize; i++) free(kernel[i]);
        free(kernel);
        return;
    }

    //On utilise la fonction précédente
    for (int y = 1; y < img->height - 1; y++) {
        for (int x = 1; x < img->width - 1; x++) {
            copy->data[y][x] = bmp24_convolution(img, x, y, kernel, kernelSize);
        }
    }

    // Copie des pixels dans l'image de base
    for (int y = 1; y < img->height - 1; y++) {
        for (int x = 1; x < img->width - 1; x++) {
            img->data[y][x] = copy->data[y][x];
        }
    }

    for (int i = 0; i < kernelSize; i++) free(kernel[i]);
    free(kernel);
    bmp24_free(copy);
}

// Fin 2.6
