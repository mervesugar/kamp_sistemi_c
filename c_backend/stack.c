#include "structures.h"
#include "common.h"
// 2. STACK
// ---------------------------------------------------------
EXPORT Stack* stack_create() {
    Stack *s = malloc(sizeof(Stack));
    if (s) {
        s->top = NULL;
        s->size = 0;
    }
    return s;
}

EXPORT void stack_push(Stack *s, const char *item) {
    if (!s || !item) return;
    StackNode *node = malloc(sizeof(StackNode));
    node->item = clone_string(item);
    node->next = s->top;
    s->top = node;
    s->size++;
}

EXPORT char* stack_pop(Stack *s) {
    if (!s || !s->top) return NULL;
    StackNode *node = s->top;
    char *item = node->item;
    s->top = node->next;
    free(node);
    s->size--;
    return item;
}

EXPORT char* stack_peek(Stack *s) {
    if (!s || !s->top) return NULL;
    return clone_string(s->top->item);
}

EXPORT bool stack_is_empty(Stack *s) {
    return !s || s->size == 0;
}

EXPORT int stack_size(Stack *s) {
    return s ? s->size : 0;
}

EXPORT void stack_destroy(Stack *s) {
    if (!s) return;
    StackNode *curr = s->top;
    while (curr) {
        StackNode *next = curr->next;
        free(curr->item);
        free(curr);
        curr = next;
    }
    free(s);
}

// ---------------------------------------------------------
