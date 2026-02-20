#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "bmp8.h"
#include "bmp24-partie2.h"
#include "Bonus-Affichage-utilisateur.h"
#include "Partie3.h"

int main(int argc, char *argv[]) {
    // Le programme attend : ./imageprocessing <entree.bmp> <sortie.bmp> <option_filtre> <valeur_optionnelle>
    if (argc < 4) {
        printf("Usage: %s <entree.bmp> <sortie.bmp> <option_filtre> [valeur]\n", argv[0]);
        return 1;
    }

    char *fichier_entree = argv[1];
    char *fichier_sortie = argv[2];
    int choix = atoi(argv[3]);
    int valeur = (argc > 4) ? atoi(argv[4]) : 0;

    // Détection du format (8 ou 24 bits) via ta fonction dans Bonus-Affichage-utilisateur.c
    int format = nombre_de_bits(fichier_entree);
    
    if (format == 8) {
        t_bmp8 *img8 = bmp8_loadImage(fichier_entree);
        if (!img8) {
            printf("Erreur : Impossible de charger l'image 8-bit\n");
            return 1;
        }

        // Application des filtres selon ton mapping
        if (choix == 1) {
            bmp8_negative(img8);
        } else if (choix == 2) {
            bmp8_brightness(img8, valeur);
        } else if (choix == 3) {
            bmp8_threshold(img8, valeur);
        } else if (choix >= 5 && choix <= 9) {
            // Correction : on passe l'entier 'choix', pas le kernel float**
            bmp8_applyFilter(img8, choix, 3);
        } else if (choix == 55) {
            bmp8_equalize(img8);
        }

        bmp8_saveImage(fichier_sortie, img8);
        bmp8_free(img8);
    } 
    else if (format == 24) {
        t_bmp24 *img24 = bmp24_loadImage(fichier_entree);
        if (!img24) {
            printf("Erreur : Impossible de charger l'image 24-bit\n");
            return 1;
        }

        if (choix == 1) {
            bmp24_negative(img24);
        } else if (choix == 2) {
            bmp24_brightness(img24, valeur);
        } else if (choix == 4) {
            bmp24_grayscale(img24);
        } else if (choix >= 5 && choix <= 9) {
            bmp24_applySelectedFilter(img24, choix);
        } else if (choix == 55) {
            bmp24_equalize(img24);
        }

        bmp24_saveImage(img24, fichier_sortie);
        bmp24_free(img24);
    } else {
        printf("Format non supporté ou erreur de lecture.\n");
        return 1;
    }

    return 0;
}
