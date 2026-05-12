#include "structures.h"
#include "common.h"
// 11. CAMP TREE (N-ary Tree)
// ---------------------------------------------------------
static CTNode* ctnode_create(const char *name, const char *alan_id) {
    CTNode *n = malloc(sizeof(CTNode));
    n->name = clone_string(name);
    n->alan_id = clone_string(alan_id);
    n->children = malloc(sizeof(CTNode*) * 4);
    n->child_count = 0;
    n->child_capacity = 4;
    n->parent = NULL;
    return n;
}

EXPORT CampTree* camptree_create() {
    CampTree *ct = malloc(sizeof(CampTree));
    if (ct) {
        ct->root = ctnode_create("Kamp Ana Girisi", NULL);
        ct->cadir_node = ctnode_create("Cadir Bolgesi", NULL);
        ct->karavan_node = ctnode_create("Karavan Bolgesi", NULL);
        ct->bungalov_node = ctnode_create("Bungalov Bolgesi", NULL);
        
        ct->cadir_node->parent = ct->root;
        ct->karavan_node->parent = ct->root;
        ct->bungalov_node->parent = ct->root;
        
        ct->root->children[ct->root->child_count++] = ct->cadir_node;
        ct->root->children[ct->root->child_count++] = ct->karavan_node;
        ct->root->children[ct->root->child_count++] = ct->bungalov_node;
    }
    return ct;
}

static void ctnode_add_child(CTNode *parent, CTNode *child) {
    if (parent->child_count == parent->child_capacity) {
        parent->child_capacity *= 2;
        parent->children = realloc(parent->children, sizeof(CTNode*) * parent->child_capacity);
    }
    parent->children[parent->child_count++] = child;
    child->parent = parent;
}

static CTNode* find_leaf(CTNode *node, const char *alan_id) {
    if (node->alan_id && strcmp(node->alan_id, alan_id) == 0) return node;
    for(int i=0; i<node->child_count; i++) {
        CTNode *res = find_leaf(node->children[i], alan_id);
        if (res) return res;
    }
    return NULL;
}

EXPORT bool camptree_alan_ekle(CampTree *ct, const char *alan_id, const char *alan_tipi) {
    if (!ct || !alan_id || !alan_tipi) return false;
    if (find_leaf(ct->root, alan_id)) return false; // exists
    
    CTNode *target_bolge = ct->cadir_node;
    if (strstr(alan_tipi, "Karavan")) target_bolge = ct->karavan_node;
    else if (strstr(alan_tipi, "Bungalov")) target_bolge = ct->bungalov_node;
    
    CTNode *leaf = ctnode_create(alan_id, alan_id);
    ctnode_add_child(target_bolge, leaf);
    return true;
}

EXPORT bool camptree_alan_sil(CampTree *ct, const char *alan_id) {
    if (!ct || !alan_id) return false;
    CTNode *leaf = find_leaf(ct->root, alan_id);
    if (!leaf || !leaf->parent) return false;
    
    CTNode *p = leaf->parent;
    for(int i=0; i<p->child_count; i++) {
        if (p->children[i] == leaf) {
            // shift
            for(int j=i; j<p->child_count-1; j++) {
                p->children[j] = p->children[j+1];
            }
            p->child_count--;
            free(leaf->name);
            free(leaf->alan_id);
            free(leaf->children);
            free(leaf);
            return true;
        }
    }
    return false;
}

EXPORT char** camptree_bolge_alanlari(CampTree *ct, const char *alan_tipi, int *out_size) {
    if (!ct || !out_size || !alan_tipi) return NULL;
    CTNode *target_bolge = ct->cadir_node;
    if (strstr(alan_tipi, "Karavan")) target_bolge = ct->karavan_node;
    else if (strstr(alan_tipi, "Bungalov")) target_bolge = ct->bungalov_node;
    
    *out_size = target_bolge->child_count;
    if (target_bolge->child_count == 0) return NULL;
    
    char **arr = malloc(sizeof(char*) * target_bolge->child_count);
    for(int i=0; i<target_bolge->child_count; i++) {
        arr[i] = clone_string(target_bolge->children[i]->alan_id);
    }
    return arr;
}

EXPORT char* camptree_alan_bolgesi(CampTree *ct, const char *alan_id) {
    if (!ct || !alan_id) return NULL;
    CTNode *leaf = find_leaf(ct->root, alan_id);
    if (leaf && leaf->parent) {
        return clone_string(leaf->parent->name);
    }
    return NULL;
}

EXPORT bool camptree_icerir(CampTree *ct, const char *alan_id) {
    return find_leaf(ct->root, alan_id) != NULL;
}

static void ctnode_destroy(CTNode *node) {
    if (!node) return;
    for(int i=0; i<node->child_count; i++) ctnode_destroy(node->children[i]);
    free(node->name);
    free(node->alan_id);
    free(node->children);
    free(node);
}

EXPORT void camptree_destroy(CampTree *ct) {
    if (!ct) return;
    ctnode_destroy(ct->root);
    free(ct);
}


