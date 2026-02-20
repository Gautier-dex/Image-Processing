#ifndef BONUS_AFFICHAGE_UTILISATEUR_H
#define BONUS_AFFICHAGE_UTILISATEUR_H
#include "bmp24-partie2.h"
#include "bmp8.h"


float** choix_kernel(int choix);
int nombre_de_bits(const char *filename);

void bmp24_printInfo(t_bmp24 *img);

void filtres_8(t_bmp8 *img, int choix);
void filtres_24(t_bmp24 *img, int choix);

#endif //BONUS_AFFICHAGE_UTILISATEUR_H
