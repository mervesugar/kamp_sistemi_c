#include "structures.h"
#include "common.h"
// 3. QUEUE
// ---------------------------------------------------------
EXPORT Queue* queue_create() {
    Queue *q = malloc(sizeof(Queue));
    if (q) {
        q->front = NULL;
        q->rear = NULL;
        q->size = 0;
    }
    return q;
}

EXPORT void queue_enqueue(Queue *q, const char *item) {
    if (!q || !item) return;
    QueueNode *node = malloc(sizeof(QueueNode));
    node->item = clone_string(item);
    node->next = NULL;
    if (q->rear) q->rear->next = node;
    else q->front = node;
    q->rear = node;
    q->size++;
}

EXPORT char* queue_dequeue(Queue *q) {
    if (!q || !q->front) return NULL;
    QueueNode *node = q->front;
    char *item = node->item;
    q->front = node->next;
    if (!q->front) q->rear = NULL;
    free(node);
    q->size--;
    return item;
}

EXPORT char* queue_peek(Queue *q) {
    if (!q || !q->front) return NULL;
    return clone_string(q->front->item);
}

EXPORT bool queue_is_empty(Queue *q) {
    return !q || q->size == 0;
}

EXPORT int queue_size(Queue *q) {
    return q ? q->size : 0;
}

EXPORT void queue_destroy(Queue *q) {
    if (!q) return;
    QueueNode *curr = q->front;
    while (curr) {
        QueueNode *next = curr->next;
        free(curr->item);
        free(curr);
        curr = next;
    }
    free(q);
}

EXPORT char** queue_to_array(Queue *q, int *out_size) {
    if (!q || !out_size) return NULL;
    *out_size = q->size;
    if (q->size == 0) return NULL;
    
    char **arr = malloc(sizeof(char*) * q->size);
    QueueNode *curr = q->front;
    int i = 0;
    while (curr && i < q->size) {
        arr[i++] = clone_string(curr->item);
        curr = curr->next;
    }
    return arr;
}

// ---------------------------------------------------------
