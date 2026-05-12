#include "structures.h"
#include "common.h"
// 8. MAX HEAP
// ---------------------------------------------------------
static void mh_swap(MHNode *a, MHNode *b) {
    MHNode t = *a; *a = *b; *b = t;
}

EXPORT MaxHeap* maxheap_create(int initial_capacity) {
    if (initial_capacity <= 0) initial_capacity = 16;
    MaxHeap *mh = malloc(sizeof(MaxHeap));
    if (mh) {
        mh->capacity = initial_capacity;
        mh->size = 0;
        mh->heap = malloc(sizeof(MHNode) * initial_capacity);
    }
    return mh;
}

EXPORT void maxheap_push(MaxHeap *mh, int value, void *item) {
    if (!mh) return;
    if (mh->size == mh->capacity) {
        mh->capacity *= 2;
        mh->heap = realloc(mh->heap, sizeof(MHNode) * mh->capacity);
    }
    int i = mh->size++;
    mh->heap[i].value = value;
    mh->heap[i].item = item;

    while (i != 0 && mh->heap[(i - 1) / 2].value < mh->heap[i].value) {
        mh_swap(&mh->heap[i], &mh->heap[(i - 1) / 2]);
        i = (i - 1) / 2;
    }
}

static void mh_heapify(MaxHeap *mh, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < mh->size && mh->heap[left].value > mh->heap[largest].value) largest = left;
    if (right < mh->size && mh->heap[right].value > mh->heap[largest].value) largest = right;
    
    if (largest != i) {
        mh_swap(&mh->heap[i], &mh->heap[largest]);
        mh_heapify(mh, largest);
    }
}

EXPORT void* maxheap_pop(MaxHeap *mh) {
    if (!mh || mh->size <= 0) return NULL;
    if (mh->size == 1) {
        mh->size--;
        return mh->heap[0].item;
    }
    void *item = mh->heap[0].item;
    mh->heap[0] = mh->heap[mh->size - 1];
    mh->size--;
    mh_heapify(mh, 0);
    return item;
}

EXPORT bool maxheap_is_empty(MaxHeap *mh) { return !mh || mh->size == 0; }
EXPORT int maxheap_size(MaxHeap *mh) { return mh ? mh->size : 0; }
EXPORT void maxheap_destroy(MaxHeap *mh) {
    if (mh) { free(mh->heap); free(mh); }
}

EXPORT void** maxheap_top_k(MaxHeap *mh, int k, int *out_size) {
    if (!mh || !out_size || k <= 0) return NULL;
    int count = (k > mh->size) ? mh->size : k;
    *out_size = count;
    if (count == 0) return NULL;
    
    // Destructively pop from a copy
    MaxHeap *temp = maxheap_create(mh->size);
    for(int i=0; i<mh->size; i++) temp->heap[i] = mh->heap[i];
    temp->size = mh->size;
    
    void **arr = malloc(sizeof(void*) * count);
    for(int i=0; i<count; i++) {
        arr[i] = maxheap_pop(temp);
    }
    maxheap_destroy(temp);
    return arr;
}

// ---------------------------------------------------------
