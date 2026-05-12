#include "structures.h"
#include "common.h"
// 7. PRIORITY QUEUE (Max-Heap based)
// ---------------------------------------------------------
static void pq_swap(PQNode *a, PQNode *b) {
    PQNode t = *a; *a = *b; *b = t;
}

EXPORT PriorityQueue* pq_create(int initial_capacity) {
    if (initial_capacity <= 0) initial_capacity = 16;
    PriorityQueue *pq = malloc(sizeof(PriorityQueue));
    if (pq) {
        pq->capacity = initial_capacity;
        pq->size = 0;
        pq->counter = 0;
        pq->heap = malloc(sizeof(PQNode) * initial_capacity);
    }
    return pq;
}

EXPORT void pq_enqueue(PriorityQueue *pq, void *item, int priority) {
    if (!pq) return;
    if (pq->size == pq->capacity) {
        pq->capacity *= 2;
        pq->heap = realloc(pq->heap, sizeof(PQNode) * pq->capacity);
    }
    int i = pq->size++;
    pq->heap[i].priority = priority;
    pq->heap[i].item = item;
    pq->heap[i].counter = pq->counter++; // FIFO for same priority

    while (i != 0) {
        int parent = (i - 1) / 2;
        // Öncelik değerine göre elemanları Max-Heap yapısında sıralar.
        bool swap = false;
        if (pq->heap[parent].priority < pq->heap[i].priority) swap = true;
        else if (pq->heap[parent].priority == pq->heap[i].priority && pq->heap[parent].counter > pq->heap[i].counter) swap = true;
        
        if (swap) {
            pq_swap(&pq->heap[i], &pq->heap[parent]);
            i = parent;
        } else break;
    }
}

static void pq_heapify(PriorityQueue *pq, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < pq->size) {
        bool swap = false;
        if (pq->heap[left].priority > pq->heap[largest].priority) swap = true;
        else if (pq->heap[left].priority == pq->heap[largest].priority && pq->heap[left].counter < pq->heap[largest].counter) swap = true;
        if (swap) largest = left;
    }
    if (right < pq->size) {
        bool swap = false;
        if (pq->heap[right].priority > pq->heap[largest].priority) swap = true;
        else if (pq->heap[right].priority == pq->heap[largest].priority && pq->heap[right].counter < pq->heap[largest].counter) swap = true;
        if (swap) largest = right;
    }
    if (largest != i) {
        pq_swap(&pq->heap[i], &pq->heap[largest]);
        pq_heapify(pq, largest);
    }
}

EXPORT void* pq_dequeue(PriorityQueue *pq) {
    if (!pq || pq->size <= 0) return NULL;
    if (pq->size == 1) {
        pq->size--;
        return pq->heap[0].item;
    }
    void *item = pq->heap[0].item;
    pq->heap[0] = pq->heap[pq->size - 1];
    pq->size--;
    pq_heapify(pq, 0);
    return item;
}

EXPORT void* pq_peek(PriorityQueue *pq) {
    return (!pq || pq->size == 0) ? NULL : pq->heap[0].item;
}

EXPORT bool pq_is_empty(PriorityQueue *pq) {
    return !pq || pq->size == 0;
}

EXPORT int pq_size(PriorityQueue *pq) { return pq ? pq->size : 0; }

EXPORT void pq_destroy(PriorityQueue *pq) {
    if (!pq) return;
    free(pq->heap);
    free(pq);
}

EXPORT void** pq_to_array(PriorityQueue *pq, int *out_size) {
    if (!pq || !out_size) return NULL;
    *out_size = pq->size;
    if (pq->size == 0) return NULL;
    
    // Sıralama işlemi için dizinin bir kopyasını oluşturur.
    PriorityQueue *temp = pq_create(pq->size);
    for(int i=0; i<pq->size; i++) temp->heap[i] = pq->heap[i];
    temp->size = pq->size;
    
    void **arr = malloc(sizeof(void*) * pq->size);
    for(int i=0; i<pq->size; i++) {
        arr[i] = pq_dequeue(temp);
    }
    pq_destroy(temp);
    return arr;
}

// ---------------------------------------------------------
