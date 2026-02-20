#include "bmp8.h"
#include <stdio.h>
#include <stdlib.h>
#include "Bonus-Affichage-utilisateur.h"
//Début des fonctions du 1.2

t_bmp8 * bmp8_loadImage(const char * filename) {
    //fonction qui ouvre l'image et récupère les informations de l'image tel que la taille en terme de pixel :je crois(hauteur , largeur), la profondeur de couleur et la taille de donnée
    FILE *file = fopen(filename, "rb");
    if (file == NULL) {

        return NULL;
    }

    t_bmp8 * bmp8 = malloc(sizeof(t_bmp8));
    fread(bmp8->header, sizeof(unsigned char), 54, file);

    bmp8->width = *(unsigned int *)&bmp8->header[18];
    bmp8-> height = *(unsigned int *)&bmp8->header[22];
    bmp8-> colorDepth = *(unsigned int *)&bmp8->header[28];
    bmp8 -> dataSize = *(unsigned int *)&bmp8->header[34];

    fread(bmp8->colorTable, sizeof(unsigned char), 1024, file);

    bmp8->data = malloc(bmp8->dataSize);
    fread(bmp8->data, sizeof(unsigned char), bmp8->dataSize, file);

    fclose(file);
    return bmp8;
}



void bmp8_saveImage(const char *filename, t_bmp8 *img) {
    FILE *file = fopen(filename, "wb");
    if (img == NULL || file == NULL) return;

    // Ecriture du header
    if (fwrite(img->header, sizeof(unsigned char), 54, file) != 54) {
        printf("Erreur lors de l’ecriture du header.\n");
        fclose(file);
        return;
    }

    // Ecriture de colorTable
    if (fwrite(img->colorTable, sizeof(unsigned char), 1024, file) != 1024) {
        printf("Erreur lors de l’ecriture de la palette de couleurs.\n");
        fclose(file);
        return;
    }

    // Ecriture de data , t'as compris c'est toujours la même chose
    if (fwrite(img->data, sizeof(unsigned char), img->dataSize, file) != img->dataSize) {
        printf("Erreur lors de l’ecriture des données de pixels.\n");
        fclose(file);
        return;
    }

    fclose(file);
}




void bmp8_free(t_bmp8 * img) {

    if (img != NULL) {
        free(img->data);
        free(img);
    }
}


void bmp8_printInfo(t_bmp8 * img) {

    if (img != NULL) {
        printf("Image Info :\n");
        printf("Width : %d\n", img->width) ;
        printf("Height : %d\n", img->height);
        printf("Color Depth : %d\n", img->colorDepth);
        printf("Data Size : %d\n", img->dataSize);
    }
}

// FIN des fonctions du 1.2
// Début des fonctions du 1.3

void bmp8_negative(t_bmp8 * img) {
    for (int i = 0; i < img->dataSize; i++) {
        img->data[i] = -(img->data[i] - 255);
    }
}


void bmp8_brightness(t_bmp8 * img, int value) {
    for (int i = 0; i < img->dataSize; i++) {
        if (img->data[i] + value > 255) {
            img->data[i] = 255;
        }
        else if ((img->data[i] + value) < 0) {
            img->data[i] = 0;
        }
        else {
            img->data[i] = img->data[i] + value;
        }
    }
}


void bmp8_threshold(t_bmp8 * img, int threshold) {
    for (int i = 0; i < img->dataSize; i++) {
        if (img->data[i] < threshold) {
            img->data[i] = 0;
        }
        else {
            img->data[i] = 255;
        }
    }
}


void bmp8_applyFilter(t_bmp8 * img, int choix, int kernelSize) { // je me permet de changer ici les paramètres de la fonction pour utiliser ma fonction bonus sur les noyaux.

    bmp8_saveImage("temp.bmp", img);                  // Sauvegarde de l'image temporaire , car besoin d'une copie de l'image.
    t_bmp8 *copie = bmp8_loadImage("temp.bmp");       // il va falloir modifier les pixels au fur et à mesure mais si on modifie directement les pixels de l'image cela va impacter la modification des autres pixels aux tours et donc rien n'iras. C'est pourquoi on passe ici par une copie de l'image pour éviter de fausser toutes les valeurs.

    float **kernel = choix_kernel(choix); // J'appelle ici ma fonction bonus d'un autre fichier :)
    float somme;

    for (int y = kernelSize / 2; y <= img->height -  2 ; y++) {  //on met kernelSize / 2 pour pouvoir automatiser pour toutes tailles de kernel mais dans notre cas juste mettre 1 aurait suffit car on est sur un kernel de 3 * 3.

        for (int x = kernelSize / 2; x <= img->width -  2 ; x++) {

            somme = 0.0;

            for (int i = -(kernelSize / 2) ; i <= kernelSize / 2 ; i++) {

                for (int j = -(kernelSize / 2) ; j <= kernelSize / 2; j++) {
                                                                                                                            // pour la partie copie->data : on fait + i et non - i comme dans l'exemple de la formule du doc de la somme car on nous dit que "La convolution inverse les lignes et les colonnes du masque"
                    somme += copie->data[(y + i) * img->width + (x + j)] * kernel[i + kernelSize / 2][j + kernelSize / 2];
                                                                                                                            // pour la partie * kernel : on aurait pu mettre + 1 dans notre cas en 3 * 3 mais pour automatiser pour toutes tailles de filtres autant mettre kernelSize / 2 ce qui ne rajoute pas de difficulté particulière mais permet de marcher pour tous.

                } // quatrième for
            } // troisième for

            if (somme < 0) {
                somme = 0;
            }

            if (somme > 255) {
                somme = 255;
            }

            img->data[y * img->width + x] = (unsigned char)somme;

        } //deuxième for
    } //premier for

    bmp8_free(copie);
}


