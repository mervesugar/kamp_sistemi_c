"""
C Veri Yapıları Köprü Katmanı — ctypes ile structures.dll'e bağlanır.
DLL bulunamazsa saf Python yedek implementasyona geçer.
BMT210 Veri Yapıları | Gazi Üniversitesi 2026
"""
import os, ctypes, ast
from collections import deque

USE_C = False
_lib = None

try:
    dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "c_backend", "structures.dll"))
    if not os.path.exists(dll_path):
        raise FileNotFoundError(f"DLL bulunamadi: {dll_path}")
    _lib = ctypes.CDLL(dll_path)
    USE_C = True
    print("=" * 63)
    print("[BİLGİ] C arka planı başarıyla yüklendi (structures.dll).")
    print("[BİLGİ] Tüm veri yapıları C dilinde çalışmaktadır.")
    print("=" * 63)
except Exception as e:
    print("=" * 63)
    print(f"[UYARI] C arka planı yüklenemedi: {e}")
    print("[BİLGİ] Saf Python veri yapıları kullanılıyor...")
    print("=" * 63)

if not USE_C:
    from .structures_python import *
else:
    # CTYPES TİP TANIMLARI
    VP  = ctypes.c_void_p
    CP  = ctypes.c_char_p
    IP  = ctypes.POINTER(ctypes.c_int)
    CI  = ctypes.c_int
    CB  = ctypes.c_bool
    PO  = ctypes.py_object
    PPO = ctypes.POINTER(ctypes.py_object)
    PCP = ctypes.POINTER(ctypes.c_char_p)

    def _sig(fn, args, res=None):
        fn.argtypes = args
        if res is not None: fn.restype = res

    # LinkedList
    _sig(_lib.ll_create,   [],          VP)
    _sig(_lib.ll_append,   [VP, CP])
    _sig(_lib.ll_prepend,  [VP, CP])
    _sig(_lib.ll_remove,   [VP, CP],    CB)
    _sig(_lib.ll_size,     [VP],        CI)
    _sig(_lib.ll_to_array, [VP, IP],    PCP)

    # Stack
    _sig(_lib.stack_create,   [],        VP)
    _sig(_lib.stack_push,     [VP, CP])
    _sig(_lib.stack_pop,      [VP],      VP)
    _sig(_lib.stack_peek,     [VP],      VP)
    _sig(_lib.stack_is_empty, [VP],      CB)
    _sig(_lib.stack_size,     [VP],      CI)

    # Queue
    _sig(_lib.queue_create,   [],        VP)
    _sig(_lib.queue_enqueue,  [VP, CP])
    _sig(_lib.queue_dequeue,  [VP],      VP)
    _sig(_lib.queue_peek,     [VP],      VP)
    _sig(_lib.queue_is_empty, [VP],      CB)
    _sig(_lib.queue_size,     [VP],      CI)
    _sig(_lib.queue_to_array, [VP, IP],  PCP)

    # HashMap
    _sig(_lib.hashmap_create,     [CI],      VP)
    _sig(_lib.hashmap_insert,     [VP, CP, PO])
    _sig(_lib.hashmap_get,        [VP, CP],  VP)
    _sig(_lib.hashmap_delete,     [VP, CP],  CB)
    _sig(_lib.hashmap_contains,   [VP, CP],  CB)
    _sig(_lib.hashmap_size,       [VP],      CI)
    _sig(_lib.hashmap_all_keys,   [VP, IP],  PCP)
    _sig(_lib.hashmap_all_values, [VP, IP],  PPO)

    # BST
    _sig(_lib.bst_create,      [],           VP)
    _sig(_lib.bst_insert,      [VP, CP, PO])
    _sig(_lib.bst_search,      [VP, CP],     VP)
    _sig(_lib.bst_delete,      [VP, CP])
    _sig(_lib.bst_size,        [VP],         CI)
    _sig(_lib.bst_range_query, [VP, CP, CP, IP], PPO)

    # PriorityQueue
    _sig(_lib.pq_create,   [CI],       VP)
    _sig(_lib.pq_enqueue,  [VP, PO, CI])
    _sig(_lib.pq_dequeue,  [VP],       VP)
    _sig(_lib.pq_peek,     [VP],       VP)
    _sig(_lib.pq_is_empty, [VP],       CB)
    _sig(_lib.pq_size,     [VP],       CI)
    _sig(_lib.pq_to_array, [VP, IP],   PPO)

    # MaxHeap
    _sig(_lib.maxheap_create,   [CI],       VP)
    _sig(_lib.maxheap_push,     [VP, CI, PO])
    _sig(_lib.maxheap_pop,      [VP],       VP)
    _sig(_lib.maxheap_is_empty, [VP],       CB)
    _sig(_lib.maxheap_size,     [VP],       CI)
    _sig(_lib.maxheap_top_k,    [VP, CI, IP], PPO)

    # CampSet
    _sig(_lib.set_create,   [CI],       VP)
    _sig(_lib.set_add,      [VP, CP])
    _sig(_lib.set_remove,   [VP, CP])
    _sig(_lib.set_contains, [VP, CP],   CB)
    _sig(_lib.set_size,     [VP],       CI)
    _sig(_lib.set_to_array, [VP, IP],   PCP)

    # Graph
    _sig(_lib.graph_create,      [],                         VP)
    _sig(_lib.graph_add_node,    [VP, CP])
    _sig(_lib.graph_add_edge,    [VP, CP, CP, CI])
    _sig(_lib.graph_remove_node, [VP, CP])
    _sig(_lib.graph_neighbors,   [VP, CP, IP],               PCP)
    _sig(_lib.graph_all_nodes,   [VP, IP],                   PCP)
    _sig(_lib.graph_dijkstra,    [VP, CP, CP, IP, IP],       PCP)

    # Matrix2D
    _sig(_lib.matrix_create,    [CI, CI, CI], VP)
    _sig(_lib.matrix_set,       [VP, CI, CI, CI])
    _sig(_lib.matrix_get,       [VP, CI, CI], CI)
    _sig(_lib.matrix_increment, [VP, CI, CI, CI])
    _sig(_lib.matrix_row_sum,   [VP, CI],     CI)
    _sig(_lib.matrix_col_sum,   [VP, CI],     CI)

    # CampTree
    _sig(_lib.camptree_create,         [],           VP)
    _sig(_lib.camptree_alan_ekle,      [VP, CP, CP], CB)
    _sig(_lib.camptree_alan_sil,       [VP, CP],     CB)
    _sig(_lib.camptree_bolge_alanlari, [VP, CP, IP], PCP)
    _sig(_lib.camptree_alan_bolgesi,   [VP, CP],     VP)
    _sig(_lib.camptree_icerir,         [VP, CP],     CB)

    # Free helpers
    _sig(_lib.free_string_array, [PCP, CI])
    _sig(_lib.free_string,       [VP])

    # YARDIMCI FONKSİYONLAR
    def _c_str(s): return str(s).encode('utf-8')

    def _parse_val(s):
        if s is None: return None
        try: return ast.literal_eval(s)
        except (ValueError, SyntaxError): return s

    def _p_str(b):
        if not b: return None
        return _parse_val(b.decode('utf-8'))

    def _p_str_free(ptr):
        if not ptr: return None
        s = ctypes.cast(ptr, CP).value.decode('utf-8')
        _lib.free_string(VP(ptr))
        return _parse_val(s)

    def _str_arr(arr, size):
        """C'den dönen char** dizisini Python listesine çevirir ve belleği serbest bırakır."""
        if not arr: return []
        res = [_p_str(arr[i]) for i in range(size)]
        _lib.free_string_array(ctypes.cast(arr, PCP), size)
        return res

    # PYTHON WRAPPER SINIFLARI

    class HashMap:
        def __init__(self, capacity=64):
            self._c = _lib.hashmap_create(capacity)
            self._refs = {}

        def insert(self, key, value):
            self._refs[key] = value
            _lib.hashmap_insert(self._c, _c_str(key), PO(value))

        def get(self, key):
            res = _lib.hashmap_get(self._c, _c_str(key))
            return ctypes.cast(res, PO).value if res else None

        def delete(self, key):
            r = _lib.hashmap_delete(self._c, _c_str(key))
            if r: self._refs.pop(key, None)
            return r

        def contains(self, key): return _lib.hashmap_contains(self._c, _c_str(key))

        def all_keys(self):
            sz = ctypes.c_int()
            arr = _lib.hashmap_all_keys(self._c, ctypes.byref(sz))
            return _str_arr(arr, sz.value)

        def all_values(self):
            sz = ctypes.c_int()
            arr = _lib.hashmap_all_values(self._c, ctypes.byref(sz))
            if not arr: return []
            res = [arr[i] for i in range(sz.value)]
            _lib.free_string(ctypes.cast(arr, VP))
            return res

        def __len__(self): return _lib.hashmap_size(self._c)

    class BST:
        def __init__(self):
            self._c = _lib.bst_create()
            self._refs = {}

        def insert(self, key, value):
            self._refs[key] = value
            _lib.bst_insert(self._c, _c_str(key), PO(value))

        def search(self, key):
            res = _lib.bst_search(self._c, _c_str(key))
            return ctypes.cast(res, PO).value if res else None

        def delete(self, key):
            _lib.bst_delete(self._c, _c_str(key))
            self._refs.pop(key, None)

        def range_query(self, low, high):
            sz = ctypes.c_int()
            arr = _lib.bst_range_query(self._c, _c_str(low), _c_str(high), ctypes.byref(sz))
            if not arr: return []
            result = []
            for i in range(sz.value):
                v = arr[i]
                for k, rv in self._refs.items():
                    if rv == v: result.append((k, v)); break
            _lib.free_string(ctypes.cast(arr, VP))
            return result

        def inorder(self):
            return sorted(self._refs.items())

        def __len__(self): return _lib.bst_size(self._c)

    class LinkedList:
        def __init__(self): self._c = _lib.ll_create()
        def append(self, v): _lib.ll_append(self._c, _c_str(v))
        def prepend(self, v): _lib.ll_prepend(self._c, _c_str(v))
        def remove(self, v): return _lib.ll_remove(self._c, _c_str(v))

        def to_list(self):
            sz = ctypes.c_int()
            arr = _lib.ll_to_array(self._c, ctypes.byref(sz))
            return _str_arr(arr, sz.value)

        def __iter__(self): return iter(self.to_list())
        def __len__(self): return _lib.ll_size(self._c)

    class Stack:
        def __init__(self): self._c = _lib.stack_create()
        def push(self, item): _lib.stack_push(self._c, _c_str(item))
        def pop(self):
            if self.is_empty(): raise IndexError("Stack boş")
            return _p_str_free(_lib.stack_pop(self._c))
        def peek(self):
            return None if self.is_empty() else _p_str_free(_lib.stack_peek(self._c))
        def is_empty(self): return _lib.stack_is_empty(self._c)
        def __len__(self): return _lib.stack_size(self._c)

    class Queue:
        def __init__(self): self._c = _lib.queue_create()
        def enqueue(self, item): _lib.queue_enqueue(self._c, _c_str(item))
        def dequeue(self):
            if self.is_empty(): raise IndexError("Queue boş")
            return _p_str_free(_lib.queue_dequeue(self._c))
        def peek(self):
            return None if self.is_empty() else _p_str_free(_lib.queue_peek(self._c))
        def is_empty(self): return _lib.queue_is_empty(self._c)
        def to_list(self):
            sz = ctypes.c_int()
            arr = _lib.queue_to_array(self._c, ctypes.byref(sz))
            return _str_arr(arr, sz.value)
        def __len__(self): return _lib.queue_size(self._c)

    class PriorityQueue:
        def __init__(self):
            self._c = _lib.pq_create(16)
            self._refs = []        # [(item, priority), ...]

        def enqueue(self, item, priority):
            self._refs.append((item, priority))
            _lib.pq_enqueue(self._c, PO(item), priority)

        def dequeue(self):
            if self.is_empty(): raise IndexError("PQ boş")
            res = _lib.pq_dequeue(self._c)
            item = ctypes.cast(res, PO).value if res else None
            # _refs listesinden eşleşen ilk kaydı kaldır
            for i, (it, _) in enumerate(self._refs):
                if it == item:
                    del self._refs[i]
                    break
            return item

        def peek(self): return None if self.is_empty() else _lib.pq_peek(self._c)
        def is_empty(self): return _lib.pq_is_empty(self._c)

        def to_list(self):
            sz = ctypes.c_int()
            arr = _lib.pq_to_array(self._c, ctypes.byref(sz))
            if not arr: return []
            res = [arr[i] for i in range(sz.value)]
            _lib.free_string(ctypes.cast(arr, VP))
            return res

        def remove_item(self, item):
            """Belirtilen öğeyi kuyruktan çıkarır — C PQ'yu yeniden oluşturur."""
            # _refs'te bu item'ı bul
            idx = None
            for i, (it, _) in enumerate(self._refs):
                if it == item:
                    idx = i
                    break
            if idx is None:
                return False
            # Eşleşen kaydı çıkar
            del self._refs[idx]
            # C PQ'yu kalan elemanlarla yeniden oluştur
            self._c = _lib.pq_create(max(16, len(self._refs) + 1))
            for it, pr in self._refs:
                _lib.pq_enqueue(self._c, PO(it), pr)
            return True

        def __len__(self): return _lib.pq_size(self._c)

    class MaxHeap:
        def __init__(self):
            self._c = _lib.maxheap_create(16)
            self._refs = []; self._vals = {}

        def push(self, value, item):
            self._refs.append(item); self._vals[item] = value
            _lib.maxheap_push(self._c, value, PO(item))

        def pop(self):
            if self.is_empty(): raise IndexError("Heap boş")
            res = _lib.maxheap_pop(self._c)
            item = ctypes.cast(res, PO).value if res else None
            if item in self._refs: self._refs.remove(item)
            return self._vals.get(item, -1), item

        def top_k(self, k):
            sz = ctypes.c_int()
            arr = _lib.maxheap_top_k(self._c, k, ctypes.byref(sz))
            if not arr: return []
            res = [(self._vals.get(arr[i], -1), arr[i]) for i in range(sz.value)]
            _lib.free_string(ctypes.cast(arr, VP))
            return res

        def is_empty(self): return _lib.maxheap_is_empty(self._c)
        def __len__(self): return _lib.maxheap_size(self._c)

    class CampSet:
        def __init__(self): self._c = _lib.set_create(16)
        def add(self, aid): _lib.set_add(self._c, _c_str(aid))
        def remove(self, aid): _lib.set_remove(self._c, _c_str(aid))
        def contains(self, aid): return _lib.set_contains(self._c, _c_str(aid))
        def all(self):
            sz = ctypes.c_int()
            arr = _lib.set_to_array(self._c, ctypes.byref(sz))
            return _str_arr(arr, sz.value)
        def __len__(self): return _lib.set_size(self._c)

    class Graph:
        def __init__(self): self._c = _lib.graph_create()
        def add_node(self, nid): _lib.graph_add_node(self._c, _c_str(nid))
        def add_edge(self, u, v, weight=1): _lib.graph_add_edge(self._c, _c_str(u), _c_str(v), weight)
        def remove_node(self, nid): _lib.graph_remove_node(self._c, _c_str(nid))

        def neighbors(self, nid):
            sz = ctypes.c_int()
            arr = _lib.graph_neighbors(self._c, _c_str(nid), ctypes.byref(sz))
            return _str_arr(arr, sz.value)

        def all_nodes(self):
            sz = ctypes.c_int()
            arr = _lib.graph_all_nodes(self._c, ctypes.byref(sz))
            return _str_arr(arr, sz.value)

        def bfs(self, start):
            if start not in self.all_nodes(): return []
            visited, q, r = {start}, deque([start]), []
            while q:
                n = q.popleft(); r.append(n)
                for nb in self.neighbors(n):
                    if nb not in visited: visited.add(nb); q.append(nb)
            return r

        def dfs(self, start):
            if start not in self.all_nodes(): return []
            visited, r = set(), []
            def _d(n):
                visited.add(n); r.append(n)
                for nb in self.neighbors(n):
                    if nb not in visited: _d(nb)
            _d(start); return r

        def dijkstra(self, start, end):
            dist = ctypes.c_int(); sz = ctypes.c_int()
            arr = _lib.graph_dijkstra(self._c, _c_str(start), _c_str(end), ctypes.byref(dist), ctypes.byref(sz))
            if dist.value == -1 or not arr: return float('inf'), []
            res = _str_arr(arr, sz.value)
            return dist.value, res

    class Matrix2D:
        def __init__(self, rows, cols, default=0):
            self.rows, self.cols = rows, cols
            self._c = _lib.matrix_create(rows, cols, default)

        def set(self, r, c, v): _lib.matrix_set(self._c, r, c, v)
        def get(self, r, c):
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols: return None
            return _lib.matrix_get(self._c, r, c)
        def increment(self, r, c, amt=1): _lib.matrix_increment(self._c, r, c, amt)
        def row_sum(self, r): return _lib.matrix_row_sum(self._c, r)
        def col_sum(self, c): return _lib.matrix_col_sum(self._c, c)
        def to_list(self):
            return [[self.get(r, c) for c in range(self.cols)] for r in range(self.rows)]

    class CampTree:
        def __init__(self): self._c = _lib.camptree_create()
        def alan_ekle(self, aid, tipi): return _lib.camptree_alan_ekle(self._c, _c_str(aid), _c_str(tipi))
        def alan_sil(self, aid): return _lib.camptree_alan_sil(self._c, _c_str(aid))

        def bolge_alanlari(self, tipi):
            sz = ctypes.c_int()
            arr = _lib.camptree_bolge_alanlari(self._c, _c_str(tipi), ctypes.byref(sz))
            return _str_arr(arr, sz.value)

        def alan_bolgesi(self, aid):
            val = _p_str_free(_lib.camptree_alan_bolgesi(self._c, _c_str(aid)))
            if val and "Karavan" in val: return "Karavan Bölgesi"
            if val and ("Cadir" in val or "Çadır" in val): return "Çadır Bölgesi"
            if val and "Bungalov" in val: return "Bungalov Bölgesi"
            return val

        def icerir(self, aid): return _lib.camptree_icerir(self._c, _c_str(aid))
        def bolge_alan_sayisi(self, tipi): return len(self.bolge_alanlari(tipi))

        def tum_bolgeler(self):
            return {f"{t} Bölgesi": self.bolge_alanlari(t) for t in ["Çadır", "Karavan", "Bungalov"]}

        def __len__(self):
            return sum(self.bolge_alan_sayisi(t) for t in ["Çadır", "Karavan", "Bungalov"])

        def bfs(self):
            r = [(0, "Kamp Ana Girişi")]
            bl = [("Çadır", "Çadır Bölgesi"), ("Karavan", "Karavan Bölgesi"), ("Bungalov", "Bungalov Bölgesi")]
            for _, ad in bl: r.append((1, ad))
            for tip, _ in bl:
                for a in self.bolge_alanlari(tip): r.append((2, a))
            return r

        def dfs(self, node=None, seviye=0):
            r = [(0, "Kamp Ana Girişi")]
            bl = [("Çadır", "Çadır Bölgesi"), ("Karavan", "Karavan Bölgesi"), ("Bungalov", "Bungalov Bölgesi")]
            for tip, ad in bl:
                r.append((1, ad))
                for a in self.bolge_alanlari(tip): r.append((2, a))
            return r

        def hiyerarsi_yazdir(self):
            lines = ["Kamp Ana Girişi", "Çadır Bölgesi", "Karavan Bölgesi", "Bungalov Bölgesi"]
            for a in self.bolge_alanlari("Çadır") + self.bolge_alanlari("Karavan") + self.bolge_alanlari("Bungalov"):
                lines.append(a)
            return lines
