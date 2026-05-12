#include "structures.h"
#include "common.h"
// 9. GRAPH (Adjacency List + Dijkstra)
// ---------------------------------------------------------
EXPORT Graph* graph_create() {
    Graph *g = malloc(sizeof(Graph));
    if (g) { g->head = NULL; g->size = 0; }
    return g;
}

static GNode* find_gnode(Graph *g, const char *id) {
    GNode *curr = g->head;
    while(curr) {
        if (strcmp(curr->id, id) == 0) return curr;
        curr = curr->next;
    }
    return NULL;
}

EXPORT void graph_add_node(Graph *g, const char *node_id) {
    if (!g || !node_id) return;
    if (find_gnode(g, node_id)) return;
    GNode *n = malloc(sizeof(GNode));
    n->id = clone_string(node_id);
    n->edges = NULL;
    n->next = g->head;
    g->head = n;
    g->size++;
}

EXPORT void graph_add_edge(Graph *g, const char *u, const char *v, int weight) {
    if (!g || !u || !v) return;
    graph_add_node(g, u);
    graph_add_node(g, v);
    
    GNode *nu = find_gnode(g, u);
    GNode *nv = find_gnode(g, v);
    
    // u -> v
    Edge *eu = malloc(sizeof(Edge));
    eu->target = clone_string(v);
    eu->weight = weight;
    eu->next = nu->edges;
    nu->edges = eu;
    
    // v -> u
    Edge *ev = malloc(sizeof(Edge));
    ev->target = clone_string(u);
    ev->weight = weight;
    ev->next = nv->edges;
    nv->edges = ev;
}

EXPORT void graph_remove_node(Graph *g, const char *node_id) {
        // Düğümü ve ona bağlı kenarları graf üzerinden temizler.
    if (!g || !node_id) return;
    GNode *curr = g->head, *prev = NULL;
    while(curr) {
        Edge *ecurr = curr->edges, *eprev = NULL;
        while(ecurr) {
            if (strcmp(ecurr->target, node_id) == 0) {
                if (eprev) eprev->next = ecurr->next;
                else curr->edges = ecurr->next;
                free(ecurr->target);
                free(ecurr);
                break;
            } else {
                eprev = ecurr;
                ecurr = ecurr->next;
            }
        }
        if (strcmp(curr->id, node_id) == 0) {
            if (prev) prev->next = curr->next;
            else g->head = curr->next;
            Edge *e = curr->edges;
            while(e) {
                Edge *nxt = e->next;
                free(e->target); free(e);
                e = nxt;
            }
            free(curr->id);
            free(curr);
            g->size--;
            curr = prev ? prev->next : g->head;
        } else {
            prev = curr;
            curr = curr->next;
        }
    }
}

EXPORT char** graph_neighbors(Graph *g, const char *node_id, int *out_size) {
    if (!g || !out_size) return NULL;
    GNode *n = find_gnode(g, node_id);
    if (!n) { *out_size = 0; return NULL; }
    int count = 0;
    Edge *e = n->edges;
    while(e) { count++; e = e->next; }
    *out_size = count;
    if (count == 0) return NULL;
    char **arr = malloc(sizeof(char*) * count);
    e = n->edges;
    for(int i=0; i<count; i++) {
        arr[i] = clone_string(e->target);
        e = e->next;
    }
    return arr;
}

EXPORT char** graph_all_nodes(Graph *g, int *out_size) {
    if (!g || !out_size) return NULL;
    *out_size = g->size;
    if (g->size == 0) return NULL;
    char **arr = malloc(sizeof(char*) * g->size);
    GNode *n = g->head;
    for(int i=0; i<g->size; i++) {
        arr[i] = clone_string(n->id);
        n = n->next;
    }
    return arr;
}


EXPORT char** graph_dijkstra(Graph *g, const char *start, const char *end, int *out_distance, int *out_size) {
    if (!g || !start || !end || !out_distance || !out_size) return NULL;
    *out_distance = -1;
    *out_size = 0;
    
    // Dijkstra algoritması kullanarak düğümler arası en kısa mesafeyi hesaplar.
    char **nodes = graph_all_nodes(g, &g->size);
    if (!nodes) return NULL;
    int v = g->size;
    int *dist = malloc(sizeof(int) * v);
    bool *visited = calloc(v, sizeof(bool));
    int *prev = malloc(sizeof(int) * v);
    
    int start_idx = -1, end_idx = -1;
    for(int i=0; i<v; i++) {
        dist[i] = 9999999;
        prev[i] = -1;
        if (strcmp(nodes[i], start) == 0) start_idx = i;
        if (strcmp(nodes[i], end) == 0) end_idx = i;
    }
    
    if (start_idx == -1 || end_idx == -1) {
        free_string_array(nodes, v); free(dist); free(visited); free(prev); return NULL;
    }
    
    dist[start_idx] = 0;
    
    for(int count=0; count<v-1; count++) {
        int u = -1;
        int min_d = 9999999;
        for(int i=0; i<v; i++) {
            if (!visited[i] && dist[i] < min_d) {
                min_d = dist[i];
                u = i;
            }
        }
        if (u == -1 || u == end_idx) break;
        visited[u] = true;
        
        GNode *nu = find_gnode(g, nodes[u]);
        Edge *e = nu->edges;
        while(e) {
            int v_idx = -1;
            for(int i=0; i<v; i++) {
                if (strcmp(nodes[i], e->target) == 0) { v_idx = i; break; }
            }
            if (v_idx != -1 && !visited[v_idx] && dist[u] != 9999999 && dist[u] + e->weight < dist[v_idx]) {
                dist[v_idx] = dist[u] + e->weight;
                prev[v_idx] = u;
            }
            e = e->next;
        }
    }
    
    if (dist[end_idx] == 9999999) {
        free_string_array(nodes, v); free(dist); free(visited); free(prev); return NULL;
    }
    
    *out_distance = dist[end_idx];
    
    // Reconstruct path
    int path_cap = 16;
    int path_len = 0;
    int *path_idx = malloc(sizeof(int) * path_cap);
    int curr = end_idx;
    while(curr != -1) {
        if (path_len == path_cap) {
            path_cap *= 2;
            path_idx = realloc(path_idx, sizeof(int) * path_cap);
        }
        path_idx[path_len++] = curr;
        curr = prev[curr];
    }
    
    *out_size = path_len;
    char **path_arr = malloc(sizeof(char*) * path_len);
    for(int i=0; i<path_len; i++) {
        path_arr[i] = clone_string(nodes[path_idx[path_len - 1 - i]]);
    }
    
    free_string_array(nodes, v); free(dist); free(visited); free(prev); free(path_idx);
    return path_arr;
}

EXPORT void graph_destroy(Graph *g) {
    if (!g) return;
    GNode *n = g->head;
    while(n) {
        Edge *e = n->edges;
        while(e) {
            Edge *next_e = e->next;
            free(e->target);
            free(e);
            e = next_e;
        }
        GNode *next_n = n->next;
        free(n->id);
        free(n);
        n = next_n;
    }
    free(g);
}

// ---------------------------------------------------------
