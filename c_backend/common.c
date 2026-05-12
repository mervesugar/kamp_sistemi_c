// Proje genelinde kullanilan ortak yardimci fonksiyonlar
#include "structures.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

// Utility
static char* clone_string(const char *src) {
    if (!src) return NULL;
    char *dest = malloc(strlen(src) + 1);
    if (dest) strcpy(dest, src);
    return dest;
}

EXPORT void free_string_array(char **arr, int size) {
    if (!arr) return;
    for (int i = 0; i < size; i++) {
        if (arr[i]) free(arr[i]);
    }
    free(arr);
}

EXPORT void free_string(char *str) {
    if (str) free(str);
}

// ---------------------------------------------------------
