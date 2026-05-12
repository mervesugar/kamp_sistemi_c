"""
Performans Testleri - Kamp Alani Rezervasyon Sistemi
BMT210 Veri Yapilari - Gazi Universitesi 2026

Yonerge Madde 6: Kucuk, orta ve buyuk olcekli veri kumeleri ile testler;
islem surelerini ve gozlenen farklar tablo ile raporlanir.

Calistirmak icin:
    python tests/performans_testleri.py
"""
import sys
import os
import time
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from data_structures.structures import HashMap, BST, Stack, PriorityQueue, MaxHeap


# ================================================================
# Yardimci fonksiyonlar
# ================================================================

def sure_ol(fn, *args, **kwargs):
    """Fonksiyonun calisma suresini mikrosaniye cinsinden dondurur."""
    baslangic = time.perf_counter()
    fn(*args, **kwargs)
    return (time.perf_counter() - baslangic) * 1_000_000  # us


def tablo_yazdir(baslik, sutunlar, satirlar):
    """Basit ASCII tablo ciktisi."""
    genislikler = [max(len(str(s[i])) for s in [sutunlar] + satirlar) for i in range(len(sutunlar))]
    ayrac = "+" + "+".join("-" * (g + 2) for g in genislikler) + "+"
    print("")
    print("-" * 60)
    print("  " + baslik)
    print("-" * 60)
    print(ayrac)
    print("| " + " | ".join(str(sutunlar[i]).ljust(genislikler[i]) for i in range(len(sutunlar))) + " |")
    print(ayrac)
    for satir in satirlar:
        print("| " + " | ".join(str(satir[i]).ljust(genislikler[i]) for i in range(len(satir))) + " |")
    print(ayrac)


# ================================================================
# TEST 1: Array (Lineer Arama) vs HashMap (O(1) Erisim)
# Yonerge: arama suresi, erisim kolayligi karsilastirmasi
# ================================================================

def test_array_vs_hashmap():
    print("")
    print("=" * 60)
    print("  TEST 1: Array (Lineer Arama) vs HashMap (O(1) Erisim)")
    print("  Senaryo: Rezervasyon ID ile kayit bulma")
    print("=" * 60)

    veri_boyutlari = [10, 100, 1000]
    satirlar = []

    for n in veri_boyutlari:
        anahtarlar = [f"R{i:05d}" for i in range(n)]
        degerler = [f"Rezervasyon_{i}" for i in range(n)]
        hedef = anahtarlar[n // 2]

        # Array (liste) - lineer arama O(n)
        liste = list(zip(anahtarlar, degerler))

        def array_ara():
            for k, v in liste:
                if k == hedef:
                    return v

        # HashMap - O(1) ortalama
        hm = HashMap(capacity=max(64, n * 2))
        for k, v in zip(anahtarlar, degerler):
            hm.insert(k, v)

        tekrar = 1000
        array_sure = sum(sure_ol(array_ara) for _ in range(tekrar)) / tekrar
        hashmap_sure = sum(sure_ol(hm.get, hedef) for _ in range(tekrar)) / tekrar

        hiz_orani = array_sure / hashmap_sure if hashmap_sure > 0 else float("inf")
        satirlar.append([
            n,
            f"{array_sure:.2f} us",
            f"{hashmap_sure:.2f} us",
            f"~{hiz_orani:.1f}x"
        ])

    tablo_yazdir(
        "Arama Suresi Karsilastirmasi (1000 tekrar ortalamasi)",
        ["Veri Boyutu", "Array O(n)", "HashMap O(1)", "Hiz Orani"],
        satirlar
    )
    print("  >> Yorum: Veri buyudukce Array O(n) davranisi belirginlesir;")
    print("     HashMap sabit O(1) erisim suresini korur.")


# ================================================================
# TEST 2: Lineer Arama vs BST Arama
# Yonerge: O(n) vs O(log n) karsilastirmasi
# ================================================================

def test_lineer_vs_bst():
    print("")
    print("=" * 60)
    print("  TEST 2: Lineer Arama vs BST Arama")
    print("  Senaryo: Tarih bazli rezervasyon sorgulama")
    print("=" * 60)

    veri_boyutlari = [10, 100, 1000]
    satirlar = []

    for n in veri_boyutlari:
        tarihler = sorted([f"2025-{(i % 12)+1:02d}-{(i % 28)+1:02d}" for i in range(n)])
        hedef = tarihler[n // 2]

        # Lineer arama - O(n)
        def lineer_ara():
            for t in tarihler:
                if t == hedef:
                    return t

        # BST - O(log n)
        bst = BST()
        for i, t in enumerate(tarihler):
            bst.insert(t, f"R{i:05d}")

        tekrar = 1000
        lineer_sure = sum(sure_ol(lineer_ara) for _ in range(tekrar)) / tekrar
        bst_sure = sum(sure_ol(bst.search, hedef) for _ in range(tekrar)) / tekrar

        hiz_orani = lineer_sure / bst_sure if bst_sure > 0 else float("inf")
        satirlar.append([
            n,
            f"{lineer_sure:.2f} us",
            f"{bst_sure:.2f} us",
            f"~{hiz_orani:.1f}x"
        ])

    tablo_yazdir(
        "Arama Suresi Karsilastirmasi (1000 tekrar ortalamasi)",
        ["Veri Boyutu", "Lineer Arama O(n)", "BST Arama O(log n)", "Hiz Orani"],
        satirlar
    )
    print("  >> Yorum: BST sirali yapida her aramada veriyi yariya boler;")
    print("     buyuk veri setlerinde O(log n) avantaji belirginlesir.")


# ================================================================
# TEST 3: Bubble Sort vs Heap Sort
# Yonerge: siralama verimliligi karsilastirmasi
# ================================================================

def bubble_sort(lst):
    n = len(lst)
    lst = lst[:]
    for i in range(n):
        for j in range(0, n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
    return lst


def heap_sort(lst):
    import heapq
    return list(heapq.nsmallest(len(lst), lst))


def test_bubble_vs_heap():
    print("")
    print("=" * 60)
    print("  TEST 3: Bubble Sort O(n^2) vs Heap Sort O(n log n)")
    print("  Senaryo: Rezervasyon sayisina gore alan siralamasi")
    print("=" * 60)

    veri_boyutlari = [10, 100, 500]
    satirlar = []

    for n in veri_boyutlari:
        veri = [random.randint(0, 1000) for _ in range(n)]

        bubble_sure = sure_ol(bubble_sort, veri)
        heap_sure = sure_ol(heap_sort, veri)

        hiz_orani = bubble_sure / heap_sure if heap_sure > 0 else float("inf")
        satirlar.append([
            n,
            f"{bubble_sure:.2f} us",
            f"{heap_sure:.2f} us",
            f"~{hiz_orani:.1f}x"
        ])

    tablo_yazdir(
        "Siralama Suresi Karsilastirmasi",
        ["Veri Boyutu", "Bubble Sort O(n^2)", "Heap Sort O(n log n)", "Hiz Orani"],
        satirlar
    )
    print("  >> Yorum: Bubble Sort n-kare ile orantili buyur;")
    print("     Heap Sort (MaxHeap) n log n ile cok daha olceklenebilir.")


# ================================================================
# TEST 4: Liste vs Set - Eleman Varlik Kontrolu
# Yonerge: bellek ve erisim karsilastirmasi
# ================================================================

def test_liste_vs_set():
    print("")
    print("=" * 60)
    print("  TEST 4: Liste vs Set - Eleman Varlik Kontrolu")
    print("  Senaryo: Bakimdaki alan ID'sinin kontrolu (CampSet)")
    print("=" * 60)

    veri_boyutlari = [10, 100, 1000]
    satirlar = []

    for n in veri_boyutlari:
        elemanlar = [f"A{i:04d}" for i in range(n)]
        hedef = elemanlar[n // 2]

        liste = list(elemanlar)
        kume = set(elemanlar)

        tekrar = 10_000
        liste_sure = sum(sure_ol(lambda: hedef in liste) for _ in range(tekrar)) / tekrar
        set_sure = sum(sure_ol(lambda: hedef in kume) for _ in range(tekrar)) / tekrar

        hiz_orani = liste_sure / set_sure if set_sure > 0 else float("inf")
        satirlar.append([
            n,
            f"{liste_sure:.3f} us",
            f"{set_sure:.3f} us",
            f"~{hiz_orani:.1f}x"
        ])

    tablo_yazdir(
        "Uyelik Kontrolu Karsilastirmasi (10.000 tekrar ortalamasi)",
        ["Veri Boyutu", "Liste O(n)", "Set O(1)", "Hiz Orani"],
        satirlar
    )
    print("  >> Yorum: CampSet (Set tabanli) bakim kontrolunde O(1) saglar;")
    print("     liste tabanli kontrol n ile dogru orantili yavaslar.")


# ================================================================
# ANA CALISTIRICI
# ================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Kamp Sistemi - Performans Benchmark Testleri")
    print("  BMT210 Veri Yapilari | Gazi Universitesi 2026")
    print("=" * 60)
    print("  Veri Boyutlari: Kucuk (10), Orta (100), Buyuk (500-1000)")

    test_array_vs_hashmap()
    test_lineer_vs_bst()
    test_bubble_vs_heap()
    test_liste_vs_set()

    print("")
    print("=" * 60)
    print("  Tum performans testleri tamamlandi.")
    print("  Sonuclar yonerge Madde 6 kapsaminda uretilmistir.")
    print("=" * 60)
