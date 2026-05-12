#include "structures.h"
#include "common.h"
// 6. BST (Binary Search Tree)
// ---------------------------------------------------------
EXPORT BST* bst_create() {
    BST *tree = malloc(sizeof(BST));
    if (tree) {
        tree->root = NULL;
        tree->size = 0;
    }
    return tree;
}

static BSTNode* bst_insert_node(BSTNode *node, const char *key, void *value, int *size_inc) {
    if (!node) {
        BSTNode *new_node = malloc(sizeof(BSTNode));
        new_node->key = clone_string(key);
        new_node->value = value;
        new_node->left = new_node->right = NULL;
        *size_inc = 1;
        return new_node;
    }
    int cmp = strcmp(key, node->key);
    if (cmp < 0) node->left = bst_insert_node(node->left, key, value, size_inc);
    else if (cmp > 0) node->right = bst_insert_node(node->right, key, value, size_inc);
    else node->value = value; // Update
    return node;
}

EXPORT void bst_insert(BST *tree, const char *key, void *value) {
    if (!tree || !key) return;
    int size_inc = 0;
    tree->root = bst_insert_node(tree->root, key, value, &size_inc);
    tree->size += size_inc;
}

EXPORT void* bst_search(BST *tree, const char *key) {
    if (!tree || !key) return NULL;
    BSTNode *node = tree->root;
    while (node) {
        int cmp = strcmp(key, node->key);
        if (cmp == 0) return node->value;
        node = cmp < 0 ? node->left : node->right;
    }
    return NULL;
}

static BSTNode* bst_delete_node(BSTNode *node, const char *key, int *size_dec) {
    if (!node) return NULL;
    int cmp = strcmp(key, node->key);
    if (cmp < 0) {
        node->left = bst_delete_node(node->left, key, size_dec);
    } else if (cmp > 0) {
        node->right = bst_delete_node(node->right, key, size_dec);
    } else {
        *size_dec = 1;
        if (!node->left) {
            BSTNode *temp = node->right;
            free(node->key); free(node); return temp;
        } else if (!node->right) {
            BSTNode *temp = node->left;
            free(node->key); free(node); return temp;
        }
        BSTNode *temp = node->right;
        while (temp && temp->left) temp = temp->left;
        free(node->key);
        node->key = clone_string(temp->key);
        node->value = temp->value;
        int dummy = 0;
        node->right = bst_delete_node(node->right, temp->key, &dummy);
    }
    return node;
}

EXPORT void bst_delete(BST *tree, const char *key) {
    if (!tree || !key) return;
    int size_dec = 0;
    tree->root = bst_delete_node(tree->root, key, &size_dec);
    tree->size -= size_dec;
}

static void bst_range_rec(BSTNode *node, const char *low, const char *high, void **arr, int *idx) {
    if (!node) return;
    int cmpLow = strcmp(low, node->key);
    int cmpHigh = strcmp(high, node->key);
    if (cmpLow < 0) bst_range_rec(node->left, low, high, arr, idx);
    if (cmpLow <= 0 && cmpHigh >= 0) arr[(*idx)++] = node->value;
    if (cmpHigh > 0) bst_range_rec(node->right, low, high, arr, idx);
}

EXPORT void** bst_range_query(BST *tree, const char *low, const char *high, int *out_size) {
    if (!tree || !out_size || !low || !high) return NULL;
    void **arr = malloc(sizeof(void*) * tree->size);
    int idx = 0;
    bst_range_rec(tree->root, low, high, arr, &idx);
    *out_size = idx;
    if (idx == 0) {
        free(arr);
        return NULL;
    }
    return arr;
}

EXPORT int bst_size(BST *tree) { return tree ? tree->size : 0; }

static void bst_destroy_node(BSTNode *node) {
    if (!node) return;
    bst_destroy_node(node->left);
    bst_destroy_node(node->right);
    free(node->key);
    free(node);
}

EXPORT void bst_destroy(BST *tree) {
    if (!tree) return;
    bst_destroy_node(tree->root);
    free(tree);
}

// ---------------------------------------------------------
