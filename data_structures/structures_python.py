"""
Saf Python Veri Yapıları — DLL bulunamazsa yedek olarak kullanılır.
BMT210 Veri Yapıları | Gazi Üniversitesi 2026
"""
import heapq
from collections import deque


# 1. HashMap
class _HNode:
    __slots__ = ('key', 'value', 'next')
    def __init__(self, k, v): self.key, self.value, self.next = k, v, None

class HashMap:
    def __init__(self, capacity=64):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0

    def _hash(self, key): return hash(key) % self.capacity

    def insert(self, key, value):
        idx = self._hash(key)
        n = self.buckets[idx]
        while n:
            if n.key == key: n.value = value; return
            n = n.next
        new = _HNode(key, value); new.next = self.buckets[idx]
        self.buckets[idx] = new; self.size += 1

    def get(self, key):
        n = self.buckets[self._hash(key)]
        while n:
            if n.key == key: return n.value
            n = n.next
        return None

    def delete(self, key):
        idx = self._hash(key); n, prev = self.buckets[idx], None
        while n:
            if n.key == key:
                if prev: prev.next = n.next
                else: self.buckets[idx] = n.next
                self.size -= 1; return True
            prev, n = n, n.next
        return False

    def contains(self, key): return self.get(key) is not None

    def all_keys(self):
        keys = []
        for b in self.buckets:
            n = b
            while n: keys.append(n.key); n = n.next
        return keys

    def all_values(self):
        vals = []
        for b in self.buckets:
            n = b
            while n: vals.append(n.value); n = n.next
        return vals

    def __len__(self): return self.size


# 2. BST
class _BSTNode:
    __slots__ = ('key', 'value', 'left', 'right')
    def __init__(self, k, v): self.key, self.value, self.left, self.right = k, v, None, None

class BST:
    def __init__(self): self.root = None; self.size = 0

    def insert(self, key, value): self.root = self._ins(self.root, key, value)
    def _ins(self, n, k, v):
        if n is None: self.size += 1; return _BSTNode(k, v)
        if k < n.key: n.left = self._ins(n.left, k, v)
        elif k > n.key: n.right = self._ins(n.right, k, v)
        else: n.value = v
        return n

    def search(self, key):
        n = self.root
        while n:
            if key == n.key: return n.value
            n = n.left if key < n.key else n.right
        return None

    def range_query(self, low, high):
        result = []
        def _rq(n):
            if not n: return
            if low < n.key: _rq(n.left)
            if low <= n.key <= high: result.append((n.key, n.value))
            if high > n.key: _rq(n.right)
        _rq(self.root); return result

    def inorder(self):
        result = []
        def _io(n):
            if n: _io(n.left); result.append((n.key, n.value)); _io(n.right)
        _io(self.root); return result

    def delete(self, key): self.root, d = self._del(self.root, key); self.size -= d
    def _del(self, n, k):
        if not n: return n, 0
        if k < n.key: n.left, d = self._del(n.left, k); return n, d
        if k > n.key: n.right, d = self._del(n.right, k); return n, d
        if not n.left: return n.right, 1
        if not n.right: return n.left, 1
        m = n.right
        while m.left: m = m.left
        n.key, n.value = m.key, m.value
        n.right, _ = self._del(n.right, m.key); return n, 1

    def __len__(self): return self.size


# 3. LinkedList (Doubly)
class _LLNode:
    __slots__ = ('value', 'prev', 'next')
    def __init__(self, v): self.value, self.prev, self.next = v, None, None

class LinkedList:
    def __init__(self): self.head = self.tail = None; self.size = 0

    def append(self, value):
        n = _LLNode(value)
        if self.tail: self.tail.next = n; n.prev = self.tail; self.tail = n
        else: self.head = self.tail = n
        self.size += 1

    def prepend(self, value):
        n = _LLNode(value)
        if self.head: n.next = self.head; self.head.prev = n; self.head = n
        else: self.head = self.tail = n
        self.size += 1

    def remove(self, value):
        n = self.head
        while n:
            if n.value == value:
                if n.prev: n.prev.next = n.next
                else: self.head = n.next
                if n.next: n.next.prev = n.prev
                else: self.tail = n.prev
                self.size -= 1; return True
            n = n.next
        return False

    def to_list(self):
        r, n = [], self.head
        while n: r.append(n.value); n = n.next
        return r

    def __len__(self): return self.size
    def __iter__(self):
        n = self.head
        while n: yield n.value; n = n.next


# 4. Stack
class Stack:
    def __init__(self): self._data = []
    def push(self, item): self._data.append(item)
    def pop(self):
        if not self._data: raise IndexError("Stack boş")
        return self._data.pop()
    def peek(self): return self._data[-1] if self._data else None
    def is_empty(self): return len(self._data) == 0
    def __len__(self): return len(self._data)


# 5. Queue
class Queue:
    def __init__(self): self._data = deque()
    def enqueue(self, item): self._data.append(item)
    def dequeue(self):
        if not self._data: raise IndexError("Kuyruk boş")
        return self._data.popleft()
    def peek(self): return self._data[0] if self._data else None
    def is_empty(self): return len(self._data) == 0
    def to_list(self): return list(self._data)
    def __len__(self): return len(self._data)


# 6. PriorityQueue
class PriorityQueue:
    def __init__(self): self._heap = []; self._cnt = 0
    def enqueue(self, item, priority):
        heapq.heappush(self._heap, (-priority, self._cnt, item)); self._cnt += 1
    def dequeue(self):
        if not self._heap: raise IndexError("PQ boş")
        return heapq.heappop(self._heap)[2]
    def peek(self): return self._heap[0][2] if self._heap else None
    def is_empty(self): return len(self._heap) == 0
    def to_list(self): return [x[2] for x in sorted(self._heap)]
    def remove_item(self, item):
        for i, (_, _, it) in enumerate(self._heap):
            if it == item: del self._heap[i]; heapq.heapify(self._heap); return True
        return False
    def __len__(self): return len(self._heap)


# 7. MaxHeap
class MaxHeap:
    def __init__(self): self._data = []
    def push(self, value, item): heapq.heappush(self._data, (-value, item))
    def pop(self):
        if not self._data: raise IndexError("Heap boş")
        neg, item = heapq.heappop(self._data); return -neg, item
    def top_k(self, k):
        snap = list(self._data); result = []
        for _ in range(min(k, len(snap))):
            if not snap: break
            neg, item = heapq.heappop(snap); result.append((-neg, item))
        return result
    def is_empty(self): return len(self._data) == 0
    def __len__(self): return len(self._data)


# 8. CampSet
class CampSet:
    def __init__(self): self._data = set()
    def add(self, aid): self._data.add(aid)
    def remove(self, aid): self._data.discard(aid)
    def contains(self, aid): return aid in self._data
    def all(self): return list(self._data)
    def __len__(self): return len(self._data)


# 9. Graph
class Graph:
    def __init__(self): self._adj = {}

    def add_node(self, nid):
        if nid not in self._adj: self._adj[nid] = {}

    def add_edge(self, u, v, weight=1):
        self.add_node(u); self.add_node(v)
        self._adj[u][v] = weight; self._adj[v][u] = weight

    def remove_node(self, nid):
        if nid in self._adj:
            for nb in list(self._adj[nid]): self._adj[nb].pop(nid, None)
            del self._adj[nid]

    def neighbors(self, nid): return list(self._adj.get(nid, {}).keys())

    def bfs(self, start):
        if start not in self._adj: return []
        visited, q, r = {start}, deque([start]), []
        while q:
            n = q.popleft(); r.append(n)
            for nb in self._adj[n]:
                if nb not in visited: visited.add(nb); q.append(nb)
        return r

    def dfs(self, start):
        if start not in self._adj: return []
        visited, r = set(), []
        def _d(n):
            visited.add(n); r.append(n)
            for nb in self._adj[n]:
                if nb not in visited: _d(nb)
        _d(start); return r

    def all_nodes(self): return list(self._adj.keys())

    def dijkstra(self, start, end):
        if start not in self._adj or end not in self._adj: return float('inf'), []
        dist = {n: float('inf') for n in self._adj}; dist[start] = 0
        prev = {n: None for n in self._adj}; pq = [(0, start)]
        while pq:
            d, u = heapq.heappop(pq)
            if u == end: break
            if d > dist[u]: continue
            for nb, w in self._adj[u].items():
                nd = d + w
                if nd < dist[nb]: dist[nb] = nd; prev[nb] = u; heapq.heappush(pq, (nd, nb))
        path, c = [], end
        while c: path.insert(0, c); c = prev[c]
        return (dist[end], path) if dist[end] < float('inf') else (float('inf'), [])

    def __len__(self): return len(self._adj)


# 10. Matrix2D
class Matrix2D:
    def __init__(self, rows, cols, default=0):
        self.rows, self.cols = rows, cols
        self._data = [[default] * cols for _ in range(rows)]

    def set(self, r, c, v):
        if 0 <= r < self.rows and 0 <= c < self.cols: self._data[r][c] = v
    def get(self, r, c):
        return self._data[r][c] if 0 <= r < self.rows and 0 <= c < self.cols else None
    def increment(self, r, c, amt=1):
        if 0 <= r < self.rows and 0 <= c < self.cols: self._data[r][c] += amt
    def row_sum(self, r): return sum(self._data[r])
    def col_sum(self, c): return sum(self._data[r][c] for r in range(self.rows))
    def to_list(self): return [row[:] for row in self._data]


# 11. CampTree (N-ary)
class _TreeNode:
    __slots__ = ('name', 'alan_id', 'children', 'parent')
    def __init__(self, name, alan_id=None):
        self.name, self.alan_id, self.children, self.parent = name, alan_id, [], None
    @property
    def is_leaf(self): return self.alan_id is not None

class CampTree:
    BOLGE_MAP = {"Çadır": "Çadır Bölgesi", "Karavan": "Karavan Bölgesi", "Bungalov": "Bungalov Bölgesi"}

    def __init__(self):
        self.root = _TreeNode("Kamp Ana Girişi")
        self._bolge_nodes = {}
        for ad in ["Çadır Bölgesi", "Karavan Bölgesi", "Bungalov Bölgesi"]:
            n = _TreeNode(ad); n.parent = self.root
            self.root.children.append(n); self._bolge_nodes[ad] = n
        self._alan_nodes = {}

    def alan_ekle(self, alan_id, alan_tipi):
        if alan_id in self._alan_nodes: return False
        bolge = self._bolge_nodes[self.BOLGE_MAP.get(alan_tipi, "Çadır Bölgesi")]
        y = _TreeNode(alan_id, alan_id=alan_id); y.parent = bolge
        bolge.children.append(y); self._alan_nodes[alan_id] = y; return True

    def alan_sil(self, alan_id):
        n = self._alan_nodes.get(alan_id)
        if not n: return False
        if n.parent: n.parent.children.remove(n)
        del self._alan_nodes[alan_id]; return True

    def bolge_alanlari(self, alan_tipi):
        bn = self._bolge_nodes.get(self.BOLGE_MAP.get(alan_tipi, alan_tipi))
        return [c.alan_id for c in bn.children if c.is_leaf] if bn else []

    def tum_bolgeler(self):
        return {ad: [c.alan_id for c in n.children if c.is_leaf] for ad, n in self._bolge_nodes.items()}

    def alan_bolgesi(self, alan_id):
        n = self._alan_nodes.get(alan_id)
        return n.parent.name if n and n.parent else None

    def bolge_alan_sayisi(self, alan_tipi): return len(self.bolge_alanlari(alan_tipi))
    def icerir(self, alan_id): return alan_id in self._alan_nodes

    def bfs(self):
        r, q = [], deque([(self.root, 0)])
        while q:
            n, lvl = q.popleft(); r.append((lvl, n.name))
            for c in n.children: q.append((c, lvl + 1))
        return r

    def dfs(self, node=None, seviye=0):
        if node is None: node = self.root
        r = [(seviye, node.name)]
        for c in node.children: r.extend(self.dfs(c, seviye + 1))
        return r

    def hiyerarsi_yazdir(self):
        lines = []
        def _y(n, pre="", last=True):
            bag = "└── " if last else "├── "
            if not n.parent: lines.append(f"🏕️  {n.name}")
            elif not n.is_leaf: lines.append(f"{pre}{bag}{n.name}  ({len(n.children)} parsel)")
            else: lines.append(f"{pre}{bag}📍 {n.name}")
            cp = pre + ("    " if last else "│   ")
            for i, c in enumerate(n.children): _y(c, cp, i == len(n.children) - 1)
        _y(self.root); return lines

    def __len__(self): return len(self._alan_nodes)