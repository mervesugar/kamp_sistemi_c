// Ortak fonksiyonlarin ve makrolarin header dosyasi
#ifndef COMMON_H
#define COMMON_H

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif


static char* clone_string(const char *src) {
    if (!src) return NULL;
    char *dest = malloc(strlen(src) + 1);
    if (dest) strcpy(dest, src);
    return dest;
}


EXPORT void free_string_array(char **arr, int size);
EXPORT void free_string(char *str);

#endif // COMMON_H
