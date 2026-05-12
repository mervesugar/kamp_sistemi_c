#include "structures.h"
#include "common.h"
// 4. CAMP SET (Set / Küme Veri Yapısı)
// ---------------------------------------------------------
EXPORT CampSet* set_create(int initial_capacity) {
    if (initial_capacity <= 0) initial_capacity = 16;
    CampSet *s = malloc(sizeof(CampSet));
    if (s) {
        s->capacity = initial_capacity;
        s->size = 0;
        s->items = malloc(sizeof(char*) * initial_capacity);
    }
    return s;
}

EXPORT void set_add(CampSet *s, const char *item) {
    if (!s || !item) return;
    if (set_contains(s, item)) return;
    
    if (s->size >= s->capacity) {
        s->capacity *= 2;
        s->items = realloc(s->items, sizeof(char*) * s->capacity);
    }
    s->items[s->size++] = clone_string(item);
}

EXPORT void set_remove(CampSet *s, const char *item) {
    if (!s || !item) return;
    for (int i = 0; i < s->size; i++) {
        if (strcmp(s->items[i], item) == 0) {
            free(s->items[i]);
            // Elemanı listeden çıkarır
            s->items[i] = s->items[s->size - 1];
            s->size--;
            return;
        }
    }
}

EXPORT bool set_contains(CampSet *s, const char *item) {
    if (!s || !item) return false;
    for (int i = 0; i < s->size; i++) {
        if (strcmp(s->items[i], item) == 0) return true;
    }
    return false;
}

EXPORT int set_size(CampSet *s) {
    return s ? s->size : 0;
}

EXPORT void set_destroy(CampSet *s) {
    if (!s) return;
    for (int i = 0; i < s->size; i++) {
        free(s->items[i]);
    }
    free(s->items);
    free(s);
}

EXPORT char** set_to_array(CampSet *s, int *out_size) {
    if (!s || !out_size) return NULL;
    *out_size = s->size;
    if (s->size == 0) return NULL;
    
    char **arr = malloc(sizeof(char*) * s->size);
    for (int i = 0; i < s->size; i++) {
        arr[i] = clone_string(s->items[i]);
    }
    return arr;
}

// ---------------------------------------------------------
