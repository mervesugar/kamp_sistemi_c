#ifndef STRUCTURES_H
#define STRUCTURES_H

#include <stddef.h>
#include <stdbool.h>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

// ---------------------------------------------------------
// 1. LINKED LIST (Doubly Linked)
// ---------------------------------------------------------
typedef struct LLNode {
    char *value;
    struct LLNode *prev;
    struct LLNode *next;
} LLNode;

typedef struct LinkedList {
    LLNode *head;
    LLNode *tail;
    int size;
} LinkedList;

EXPORT LinkedList* ll_create();
EXPORT void ll_append(LinkedList *ll, const char *value);
EXPORT void ll_prepend(LinkedList *ll, const char *value);
EXPORT bool ll_remove(LinkedList *ll, const char *value);
EXPORT int ll_size(LinkedList *ll);
EXPORT void ll_destroy(LinkedList *ll);
// Bağlı listedeki tüm elemanları bir dizi olarak döndürür.
EXPORT char** ll_to_array(LinkedList *ll, int *out_size);

// ---------------------------------------------------------
// 2. STACK
// ---------------------------------------------------------
typedef struct StackNode {
    char *item;
    struct StackNode *next;
} StackNode;

typedef struct Stack {
    StackNode *top;
    int size;
} Stack;

EXPORT Stack* stack_create();
EXPORT void stack_push(Stack *s, const char *item);
EXPORT char* stack_pop(Stack *s);
EXPORT char* stack_peek(Stack *s);
EXPORT bool stack_is_empty(Stack *s);
EXPORT int stack_size(Stack *s);
EXPORT void stack_destroy(Stack *s);

// ---------------------------------------------------------
// 3. QUEUE
// ---------------------------------------------------------
typedef struct QueueNode {
    char *item;
    struct QueueNode *next;
} QueueNode;

typedef struct Queue {
    QueueNode *front;
    QueueNode *rear;
    int size;
} Queue;

EXPORT Queue* queue_create();
EXPORT void queue_enqueue(Queue *q, const char *item);
EXPORT char* queue_dequeue(Queue *q);
EXPORT char* queue_peek(Queue *q);
EXPORT bool queue_is_empty(Queue *q);
EXPORT int queue_size(Queue *q);
EXPORT void queue_destroy(Queue *q);
EXPORT char** queue_to_array(Queue *q, int *out_size);

// ---------------------------------------------------------
// 4. CAMP SET (Set Veri Yapısı)
// ---------------------------------------------------------
typedef struct CampSet {
    char **items;
    int capacity;
    int size;
} CampSet;

EXPORT CampSet* set_create(int initial_capacity);
EXPORT void set_add(CampSet *s, const char *item);
EXPORT void set_remove(CampSet *s, const char *item);
EXPORT bool set_contains(CampSet *s, const char *item);
EXPORT int set_size(CampSet *s);
EXPORT void set_destroy(CampSet *s);
EXPORT char** set_to_array(CampSet *s, int *out_size);

// Utility
EXPORT void free_string_array(char **arr, int size);
EXPORT void free_string(char *str);
// ---------------------------------------------------------
// 5. HASH MAP
// ---------------------------------------------------------
typedef struct HNode {
    char *key;
    void *value;
    struct HNode *next;
} HNode;

typedef struct HashMap {
    HNode **buckets;
    int capacity;
    int size;
} HashMap;

EXPORT HashMap* hashmap_create(int capacity);
EXPORT void hashmap_insert(HashMap *hm, const char *key, void *value);
EXPORT void* hashmap_get(HashMap *hm, const char *key);
EXPORT bool hashmap_delete(HashMap *hm, const char *key);
EXPORT bool hashmap_contains(HashMap *hm, const char *key);
EXPORT int hashmap_size(HashMap *hm);
EXPORT void hashmap_destroy(HashMap *hm);
// Returns an array of keys (strings)
EXPORT char** hashmap_all_keys(HashMap *hm, int *out_size);
// Returns an array of values (void pointers)
EXPORT void** hashmap_all_values(HashMap *hm, int *out_size);

// ---------------------------------------------------------
// 6. BST (Binary Search Tree)
// ---------------------------------------------------------
typedef struct BSTNode {
    char *key;
    void *value;
    struct BSTNode *left;
    struct BSTNode *right;
} BSTNode;

typedef struct BST {
    BSTNode *root;
    int size;
} BST;

EXPORT BST* bst_create();
EXPORT void bst_insert(BST *tree, const char *key, void *value);
EXPORT void* bst_search(BST *tree, const char *key);
EXPORT void bst_delete(BST *tree, const char *key);
// Range query: returns array of (void*) values where low <= key <= high
EXPORT void** bst_range_query(BST *tree, const char *low, const char *high, int *out_size);
EXPORT int bst_size(BST *tree);
EXPORT void bst_destroy(BST *tree);

// ---------------------------------------------------------
// 7. PRIORITY QUEUE
// ---------------------------------------------------------
typedef struct PQNode {
    int priority;
    int counter;
    void *item;
} PQNode;

typedef struct PriorityQueue {
    PQNode *heap;
    int capacity;
    int size;
    int counter;
} PriorityQueue;

EXPORT PriorityQueue* pq_create(int initial_capacity);
EXPORT void pq_enqueue(PriorityQueue *pq, void *item, int priority);
EXPORT void* pq_dequeue(PriorityQueue *pq);
EXPORT void* pq_peek(PriorityQueue *pq);
EXPORT bool pq_is_empty(PriorityQueue *pq);
EXPORT int pq_size(PriorityQueue *pq);
EXPORT void pq_destroy(PriorityQueue *pq);
// Kuyruktaki elemanları dizi formatında döndürür.
EXPORT void** pq_to_array(PriorityQueue *pq, int *out_size);

// ---------------------------------------------------------
// 8. MAX HEAP
// ---------------------------------------------------------
typedef struct MHNode {
    int value;
    void *item;
} MHNode;

typedef struct MaxHeap {
    MHNode *heap;
    int capacity;
    int size;
} MaxHeap;

EXPORT MaxHeap* maxheap_create(int initial_capacity);
EXPORT void maxheap_push(MaxHeap *mh, int value, void *item);
EXPORT void* maxheap_pop(MaxHeap *mh);
EXPORT bool maxheap_is_empty(MaxHeap *mh);
EXPORT int maxheap_size(MaxHeap *mh);
EXPORT void maxheap_destroy(MaxHeap *mh);
// Returns top k items
EXPORT void** maxheap_top_k(MaxHeap *mh, int k, int *out_size);
// ---------------------------------------------------------
// 9. GRAPH (Adjacency List)
// ---------------------------------------------------------
typedef struct Edge {
    char *target;
    int weight;
    struct Edge *next;
} Edge;

typedef struct GNode {
    char *id;
    Edge *edges;
    struct GNode *next;
} GNode;

typedef struct Graph {
    GNode *head;
    int size;
} Graph;

EXPORT Graph* graph_create();
EXPORT void graph_add_node(Graph *g, const char *node_id);
EXPORT void graph_add_edge(Graph *g, const char *u, const char *v, int weight);
EXPORT void graph_remove_node(Graph *g, const char *node_id);
EXPORT char** graph_neighbors(Graph *g, const char *node_id, int *out_size);
EXPORT char** graph_all_nodes(Graph *g, int *out_size);
// Belirtilen iki nokta arasındaki en kısa rotayı ve mesafesini döndürür.
EXPORT char** graph_dijkstra(Graph *g, const char *start, const char *end, int *out_distance, int *out_size);
EXPORT void graph_destroy(Graph *g);

// ---------------------------------------------------------
// 10. MATRIX 2D
// ---------------------------------------------------------
typedef struct Matrix2D {
    int rows;
    int cols;
    int *data;
} Matrix2D;

EXPORT Matrix2D* matrix_create(int rows, int cols, int default_val);
EXPORT void matrix_set(Matrix2D *m, int row, int col, int value);
EXPORT int matrix_get(Matrix2D *m, int row, int col);
EXPORT void matrix_increment(Matrix2D *m, int row, int col, int amount);
EXPORT int matrix_row_sum(Matrix2D *m, int row);
EXPORT int matrix_col_sum(Matrix2D *m, int col);
EXPORT void matrix_destroy(Matrix2D *m);

// ---------------------------------------------------------
// 11. CAMP TREE (N-ary Tree)
// ---------------------------------------------------------
typedef struct CTNode {
    char *name;
    char *alan_id; // NULL if not leaf
    struct CTNode **children;
    int child_count;
    int child_capacity;
    struct CTNode *parent;
} CTNode;

typedef struct CampTree {
    CTNode *root;
    CTNode *cadir_node;
    CTNode *karavan_node;
    CTNode *bungalov_node;
} CampTree;

EXPORT CampTree* camptree_create();
EXPORT bool camptree_alan_ekle(CampTree *ct, const char *alan_id, const char *alan_tipi);
EXPORT bool camptree_alan_sil(CampTree *ct, const char *alan_id);
EXPORT char** camptree_bolge_alanlari(CampTree *ct, const char *alan_tipi, int *out_size);
EXPORT char* camptree_alan_bolgesi(CampTree *ct, const char *alan_id); // returns string or NULL
EXPORT bool camptree_icerir(CampTree *ct, const char *alan_id);
EXPORT void camptree_destroy(CampTree *ct);

#endif // STRUCTURES_H
