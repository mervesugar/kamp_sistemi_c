"""
Birim Testleri — Kamp Alanı Rezervasyon Sistemi
BMT210 — Gazi Üniversitesi 2026

Çalıştırmak için:
    python tests/birim_testleri.py
"""
import sys
import os
import tempfile
import shutil
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from data_structures.structures import (
    HashMap, BST, LinkedList, Stack, Queue,
    PriorityQueue, MaxHeap, CampSet, Graph, Matrix2D, CampTree
)


# 1. HashMap

class TestHashMap(unittest.TestCase):

    def setUp(self):
        self.hm = HashMap()

    def test_insert_and_get(self):
        self.hm.insert("key1", "val1")
        self.assertEqual(self.hm.get("key1"), "val1")

    def test_update_existing_key(self):
        self.hm.insert("k", 1)
        self.hm.insert("k", 99)
        self.assertEqual(self.hm.get("k"), 99)

    def test_get_nonexistent(self):
        self.assertIsNone(self.hm.get("yok"))

    def test_delete_existing(self):
        self.hm.insert("x", 10)
        self.assertTrue(self.hm.delete("x"))
        self.assertIsNone(self.hm.get("x"))

    def test_delete_nonexistent(self):
        self.assertFalse(self.hm.delete("yok"))

    def test_size(self):
        for i in range(5):
            self.hm.insert(f"k{i}", i)
        self.assertEqual(len(self.hm), 5)

    def test_contains(self):
        self.hm.insert("abc", 1)
        self.assertTrue(self.hm.contains("abc"))
        self.assertFalse(self.hm.contains("xyz"))

    def test_all_keys_values(self):
        self.hm.insert("a", 1)
        self.hm.insert("b", 2)
        self.assertIn("a", self.hm.all_keys())
        self.assertIn(2, self.hm.all_values())


# 2. BST

class TestBST(unittest.TestCase):

    def setUp(self):
        self.bst = BST()
        for k in [5, 3, 7, 1, 4, 6, 9]:
            self.bst.insert(k, f"v{k}")

    def test_search_existing(self):
        self.assertEqual(self.bst.search(5), "v5")
        self.assertEqual(self.bst.search(1), "v1")

    def test_search_nonexistent(self):
        self.assertIsNone(self.bst.search(99))

    def test_inorder_sorted(self):
        keys = [k for k, _ in self.bst.inorder()]
        self.assertEqual(keys, sorted(keys))

    def test_range_query(self):
        result = self.bst.range_query(3, 7)
        keys = [k for k, _ in result]
        self.assertIn(3, keys)
        self.assertIn(7, keys)
        self.assertNotIn(1, keys)
        self.assertNotIn(9, keys)

    def test_delete(self):
        self.bst.delete(5)
        self.assertIsNone(self.bst.search(5))

    def test_size(self):
        self.assertEqual(len(self.bst), 7)

    def test_update(self):
        self.bst.insert(3, "updated")
        self.assertEqual(self.bst.search(3), "updated")


# 3. LinkedList

class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.ll = LinkedList()

    def test_append(self):
        self.ll.append(1)
        self.ll.append(2)
        self.assertEqual(self.ll.to_list(), [1, 2])

    def test_prepend(self):
        self.ll.append(2)
        self.ll.prepend(1)
        self.assertEqual(self.ll.to_list()[0], 1)

    def test_remove(self):
        self.ll.append(1)
        self.ll.append(2)
        self.assertTrue(self.ll.remove(1))
        self.assertNotIn(1, self.ll.to_list())

    def test_remove_nonexistent(self):
        self.assertFalse(self.ll.remove(99))

    def test_size(self):
        for i in range(4):
            self.ll.append(i)
        self.assertEqual(len(self.ll), 4)

    def test_iter(self):
        self.ll.append("a")
        self.ll.append("b")
        items = list(self.ll)
        self.assertEqual(items, ["a", "b"])


# 4. Stack

class TestStack(unittest.TestCase):

    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)

    def test_peek(self):
        s = Stack()
        s.push("x")
        self.assertEqual(s.peek(), "x")
        self.assertEqual(len(s), 1)  # peek silmez

    def test_empty_pop(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(1)
        self.assertFalse(s.is_empty())

    def test_lifo_order(self):
        s = Stack()
        for i in range(5):
            s.push(i)
        order = [s.pop() for _ in range(5)]
        self.assertEqual(order, [4, 3, 2, 1, 0])


# 5. Queue

class TestQueue(unittest.TestCase):

    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        self.assertEqual(q.dequeue(), "a")  # FIFO

    def test_empty_dequeue(self):
        q = Queue()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek(self):
        q = Queue()
        q.enqueue(10)
        self.assertEqual(q.peek(), 10)

    def test_fifo_order(self):
        q = Queue()
        for i in range(5):
            q.enqueue(i)
        order = [q.dequeue() for _ in range(5)]
        self.assertEqual(order, [0, 1, 2, 3, 4])


# 6. PriorityQueue

class TestPriorityQueue(unittest.TestCase):

    def test_priority_order(self):
        pq = PriorityQueue()
        pq.enqueue("Normal", 0)
        pq.enqueue("VIP", 5)
        pq.enqueue("Engelli", 10)
        self.assertEqual(pq.dequeue(), "Engelli")

    def test_equal_priority_fifo(self):
        pq = PriorityQueue()
        pq.enqueue("A", 3)
        pq.enqueue("B", 3)
        first = pq.dequeue()
        self.assertEqual(first, "A")  # FIFO for equal priority

    def test_empty_check(self):
        pq = PriorityQueue()
        self.assertTrue(pq.is_empty())


# 7. MaxHeap

class TestMaxHeap(unittest.TestCase):

    def test_pop_max(self):
        h = MaxHeap()
        h.push(3, "c")
        h.push(10, "a")
        h.push(7, "b")
        val, item = h.pop()
        self.assertEqual(val, 10)

    def test_top_k(self):
        h = MaxHeap()
        for i in range(10):
            h.push(i, f"item{i}")
        top = h.top_k(3)
        vals = [v for v, _ in top]
        self.assertEqual(vals, [9, 8, 7])

    def test_empty(self):
        h = MaxHeap()
        self.assertTrue(h.is_empty())

    def test_top_k_does_not_modify_heap(self):
        h = MaxHeap()
        for i in range(5):
            h.push(i, f"i{i}")
        size_before = len(h)
        h.top_k(3)
        self.assertEqual(len(h), size_before)


# 8. CampSet

class TestCampSet(unittest.TestCase):

    def test_add_contains(self):
        s = CampSet()
        s.add("A1")
        self.assertTrue(s.contains("A1"))

    def test_remove(self):
        s = CampSet()
        s.add("A2")
        s.remove("A2")
        self.assertFalse(s.contains("A2"))

    def test_remove_nonexistent(self):
        s = CampSet()
        s.remove("yok")  # discard — hata fırlatmamalı

    def test_all(self):
        s = CampSet()
        s.add("A1")
        s.add("A2")
        self.assertEqual(len(s.all()), 2)


# 9. Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = Graph()
        self.g.add_edge("A", "B")
        self.g.add_edge("B", "C")
        self.g.add_edge("C", "D")

    def test_neighbors(self):
        nb = self.g.neighbors("B")
        self.assertIn("A", nb)
        self.assertIn("C", nb)

    def test_bfs(self):
        result = self.g.bfs("A")
        self.assertEqual(result[0], "A")
        self.assertIn("D", result)

    def test_dfs(self):
        result = self.g.dfs("A")
        self.assertIn("D", result)

    def test_remove_node(self):
        self.g.remove_node("C")
        self.assertNotIn("C", self.g.all_nodes())
        self.assertNotIn("C", self.g.neighbors("B"))

    def test_bfs_disconnected(self):
        self.g.add_node("X")
        result = self.g.bfs("A")
        self.assertNotIn("X", result)


# 10. Matrix2D

class TestMatrix2D(unittest.TestCase):

    def test_set_get(self):
        m = Matrix2D(3, 7)
        m.set(0, 0, 5)
        self.assertEqual(m.get(0, 0), 5)

    def test_increment(self):
        m = Matrix2D(3, 7)
        m.increment(1, 3)
        m.increment(1, 3)
        self.assertEqual(m.get(1, 3), 2)

    def test_row_sum(self):
        m = Matrix2D(3, 7)
        m.set(0, 0, 10)
        m.set(0, 3, 5)
        self.assertEqual(m.row_sum(0), 15)

    def test_col_sum(self):
        m = Matrix2D(3, 7)
        m.set(0, 2, 3)
        m.set(1, 2, 7)
        self.assertEqual(m.col_sum(2), 10)

    def test_out_of_bounds(self):
        m = Matrix2D(3, 7)
        self.assertIsNone(m.get(10, 10))

    def test_to_list(self):
        m = Matrix2D(2, 3)
        lst = m.to_list()
        self.assertEqual(len(lst), 2)
        self.assertEqual(len(lst[0]), 3)


# 11. CampTree (N-ary Ağaç — Mekansal Hiyerarşi)

class TestCampTree(unittest.TestCase):

    def setUp(self):
        self.tree = CampTree()
        self.tree.alan_ekle("A001", "Çadır")
        self.tree.alan_ekle("A002", "Çadır")
        self.tree.alan_ekle("A003", "Karavan")
        self.tree.alan_ekle("A004", "Bungalov")

    def test_alan_ekleme(self):
        """Yeni alan doğru bölgeye yerleştirilmeli."""
        self.assertTrue(self.tree.icerir("A001"))
        self.assertTrue(self.tree.icerir("A003"))

    def test_bolge_alanlari(self):
        """Bölge sorgulaması doğru alan ID'lerini döndermeli."""
        cadir = self.tree.bolge_alanlari("Çadır")
        self.assertIn("A001", cadir)
        self.assertIn("A002", cadir)
        self.assertNotIn("A003", cadir)

    def test_alan_bolgesi(self):
        """Alan ID'ye göre bölge adı döndürmeli."""
        self.assertEqual(self.tree.alan_bolgesi("A003"), "Karavan Bölgesi")
        self.assertEqual(self.tree.alan_bolgesi("A004"), "Bungalov Bölgesi")

    def test_alan_silme(self):
        """Silinen alan artık ağaçta olmamalı."""
        self.tree.alan_sil("A001")
        self.assertFalse(self.tree.icerir("A001"))
        self.assertEqual(len(self.tree.bolge_alanlari("Çadır")), 1)

    def test_mukerrer_ekleme_engeli(self):
        """Aynı ID iki kez eklenememeli."""
        result = self.tree.alan_ekle("A001", "Çadır")
        self.assertFalse(result)

    def test_toplam_boyut(self):
        """len() toplam yaprak sayısını döndermeli."""
        self.assertEqual(len(self.tree), 4)

    def test_bfs_gezimi(self):
        """BFS kökten başlamalı ve tüm düğümleri kapsamalı."""
        bfs = self.tree.bfs()
        isimler = [ad for _, ad in bfs]
        self.assertEqual(isimler[0], "Kamp Ana Girişi")
        self.assertIn("A001", isimler)
        self.assertIn("Çadır Bölgesi", isimler)

    def test_dfs_gezimi(self):
        """DFS pre-order tüm düğümleri kapsamalı."""
        dfs = self.tree.dfs()
        isimler = [ad for _, ad in dfs]
        self.assertIn("A003", isimler)
        self.assertIn("Bungalov Bölgesi", isimler)

    def test_hiyerarsi_yazdir(self):
        """Metin çıktısı beklenen bölge adlarını içermeli."""
        satirlar = self.tree.hiyerarsi_yazdir()
        birlesik = "\n".join(satirlar)
        self.assertIn("Kamp Ana Girişi", birlesik)
        self.assertIn("Çadır Bölgesi", birlesik)
        self.assertIn("A001", birlesik)


# 12. LinkedList — Ziyaretçi Geçmiş Senaryosu

class TestLinkedListGecmis(unittest.TestCase):
    """Rezervasyon geçmişi senaryosu: prepend + LIFO sorgu"""

    def test_gecmis_sirasi(self):
        """En son rezervasyon başa eklenmeli (en yeni = baş)."""
        ll = LinkedList()
        ll.prepend(("Z001", "R001"))
        ll.prepend(("Z001", "R002"))
        ll.prepend(("Z001", "R003"))
        gecmis = ll.to_list()
        self.assertEqual(gecmis[0], ("Z001", "R003"))   # en yeni
        self.assertEqual(gecmis[-1], ("Z001", "R001"))  # en eski

    def test_gecmis_silme(self):
        """Rezervasyon iptal edilince geçmişten de kaldırılmalı."""
        ll = LinkedList()
        ll.prepend(("Z001", "R001"))
        ll.prepend(("Z002", "R002"))
        ll.remove(("Z001", "R001"))
        self.assertNotIn(("Z001", "R001"), ll.to_list())

    def test_bos_gecmis(self):
        """Boş listede to_list() boş dönmeli."""
        ll = LinkedList()
        self.assertEqual(ll.to_list(), [])


# ÇALIŞTIRICI

if __name__ == "__main__":
    print("=" * 60)
    print("  Kamp Sistemi — Birim Testleri")
    print("  BMT210 | Gazi Üniversitesi 2026")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    test_siniflar = [
        TestHashMap, TestBST, TestLinkedList, TestStack, TestQueue,
        TestPriorityQueue, TestMaxHeap, TestCampSet, TestGraph, TestMatrix2D,
        TestCampTree, TestLinkedListGecmis
    ]
    for cls in test_siniflar:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("\n" + "=" * 60)
    toplam = result.testsRun
    basari = toplam - len(result.failures) - len(result.errors)
    print(f"  Toplam: {toplam} test  |  OK: {basari}  |  HATA: {len(result.failures) + len(result.errors)}")
    print("=" * 60)
