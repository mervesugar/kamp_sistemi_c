#include "structures.h"
#include "common.h"
// 5. HASH MAP
// ---------------------------------------------------------
static unsigned int hash_str(const char *str, int capacity) {
    unsigned int hash = 5381;
    int c;
    while ((c = *str++)) hash = ((hash << 5) + hash) + c;
    return hash % capacity;
}

EXPORT HashMap* hashmap_create(int capacity) {
    if (capacity <= 0) capacity = 64;
    HashMap *hm = malloc(sizeof(HashMap));
    if (hm) {
        hm->capacity = capacity;
        hm->size = 0;
        hm->buckets = calloc(capacity, sizeof(HNode*));
    }
    return hm;
}

EXPORT void hashmap_insert(HashMap *hm, const char *key, void *value) {
    if (!hm || !key) return;
    unsigned int idx = hash_str(key, hm->capacity);
    HNode *node = hm->buckets[idx];
    while (node) {
        if (strcmp(node->key, key) == 0) {
            node->value = value;
            return;
        }
        node = node->next;
    }
    HNode *new_node = malloc(sizeof(HNode));
    new_node->key = clone_string(key);
    new_node->value = value;
    new_node->next = hm->buckets[idx];
    hm->buckets[idx] = new_node;
    hm->size++;
}

EXPORT void* hashmap_get(HashMap *hm, const char *key) {
    if (!hm || !key) return NULL;
    unsigned int idx = hash_str(key, hm->capacity);
    HNode *node = hm->buckets[idx];
    while (node) {
        if (strcmp(node->key, key) == 0) return node->value;
        node = node->next;
    }
    return NULL;
}

EXPORT bool hashmap_delete(HashMap *hm, const char *key) {
    if (!hm || !key) return false;
    unsigned int idx = hash_str(key, hm->capacity);
    HNode *node = hm->buckets[idx];
    HNode *prev = NULL;
    while (node) {
        if (strcmp(node->key, key) == 0) {
            if (prev) prev->next = node->next;
            else hm->buckets[idx] = node->next;
            free(node->key);
            free(node);
            hm->size--;
            return true;
        }
        prev = node;
        node = node->next;
    }
    return false;
}

EXPORT bool hashmap_contains(HashMap *hm, const char *key) {
    return hashmap_get(hm, key) != NULL;
}

EXPORT int hashmap_size(HashMap *hm) {
    return hm ? hm->size : 0;
}

EXPORT void hashmap_destroy(HashMap *hm) {
    if (!hm) return;
    for (int i = 0; i < hm->capacity; i++) {
        HNode *node = hm->buckets[i];
        while (node) {
            HNode *next = node->next;
            free(node->key);
            free(node);
            node = next;
        }
    }
    free(hm->buckets);
    free(hm);
}

EXPORT char** hashmap_all_keys(HashMap *hm, int *out_size) {
    if (!hm || !out_size) return NULL;
    *out_size = hm->size;
    if (hm->size == 0) return NULL;
    char **keys = malloc(sizeof(char*) * hm->size);
    int idx = 0;
    for (int i = 0; i < hm->capacity; i++) {
        HNode *node = hm->buckets[i];
        while (node && idx < hm->size) {
            keys[idx++] = clone_string(node->key);
            node = node->next;
        }
    }
    return keys;
}

EXPORT void** hashmap_all_values(HashMap *hm, int *out_size) {
    if (!hm || !out_size) return NULL;
    *out_size = hm->size;
    if (hm->size == 0) return NULL;
    void **values = malloc(sizeof(void*) * hm->size);
    int idx = 0;
    for (int i = 0; i < hm->capacity; i++) {
        HNode *node = hm->buckets[i];
        while (node && idx < hm->size) {
            values[idx++] = node->value;
            node = node->next;
        }
    }
    return values;
}

// ---------------------------------------------------------
