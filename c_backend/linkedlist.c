#include "structures.h"
#include "common.h"
// 1. LINKED LIST
// ---------------------------------------------------------
EXPORT LinkedList* ll_create() {
    LinkedList *ll = malloc(sizeof(LinkedList));
    if (ll) {
        ll->head = NULL;
        ll->tail = NULL;
        ll->size = 0;
    }
    return ll;
}

EXPORT void ll_append(LinkedList *ll, const char *value) {
    if (!ll) return;
    LLNode *node = malloc(sizeof(LLNode));
    node->value = clone_string(value);
    node->next = NULL;
    node->prev = ll->tail;
    
    if (ll->tail) ll->tail->next = node;
    else ll->head = node;
    
    ll->tail = node;
    ll->size++;
}

EXPORT void ll_prepend(LinkedList *ll, const char *value) {
    if (!ll) return;
    LLNode *node = malloc(sizeof(LLNode));
    node->value = clone_string(value);
    node->prev = NULL;
    node->next = ll->head;
    
    if (ll->head) ll->head->prev = node;
    else ll->tail = node;
    
    ll->head = node;
    ll->size++;
}

EXPORT bool ll_remove(LinkedList *ll, const char *value) {
    if (!ll || !value) return false;
    LLNode *curr = ll->head;
    while (curr) {
        if (strcmp(curr->value, value) == 0) {
            if (curr->prev) curr->prev->next = curr->next;
            else ll->head = curr->next;
            
            if (curr->next) curr->next->prev = curr->prev;
            else ll->tail = curr->prev;
            
            free(curr->value);
            free(curr);
            ll->size--;
            return true;
        }
        curr = curr->next;
    }
    return false;
}

EXPORT int ll_size(LinkedList *ll) {
    return ll ? ll->size : 0;
}

EXPORT void ll_destroy(LinkedList *ll) {
    if (!ll) return;
    LLNode *curr = ll->head;
    while (curr) {
        LLNode *next = curr->next;
        free(curr->value);
        free(curr);
        curr = next;
    }
    free(ll);
}

EXPORT char** ll_to_array(LinkedList *ll, int *out_size) {
    if (!ll || !out_size) return NULL;
    *out_size = ll->size;
    if (ll->size == 0) return NULL;
    
    char **arr = malloc(sizeof(char*) * ll->size);
    LLNode *curr = ll->head;
    int i = 0;
    while (curr && i < ll->size) {
        arr[i++] = clone_string(curr->value);
        curr = curr->next;
    }
    return arr;
}

// ---------------------------------------------------------
