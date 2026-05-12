# Kamp Alanı Rezervasyon ve Yönetim Sistemi

**BMT210 Veri Yapıları Dersi — Dönem Projesi**  
**Gazi Üniversitesi, Teknoloji Fakültesi, Bilgisayar Mühendisliği Bölümü — 2026**  
**Öğretim Üyesi:** Doç. Dr. Adem Tekerek

---

## Proje Yapısı

```
kamp_sistemi/
│
├── c_backend/                      ← C DİLİ KAYNAK KODLARI
│   ├── structures.h                   Header: 11 veri yapısı tip tanımları ve fonksiyon prototipleri
│   ├── structures.c                   Kaynak: Tüm veri yapılarının C implementasyonu (~1200 satır)
│   ├── structures.dll                 Derlenmiş kütüphane (Windows DLL)
│   └── build.bat                      Derleme betiği (GCC ile)
│
├── data_structures/                ← PYTHON ↔ C KÖPRÜ KATMANI
│   ├── structures.py                  ctypes ile C fonksiyonlarını çağıran Python wrapper
│   └── structures_python.py           DLL bulunamazsa kullanılan saf Python yedek implementasyon
│
├── gui/                            ← KULLANICI ARAYÜZÜ (Python / PyQt6)
│   └── uygulama.py                    5 sekmeli GUI uygulaması
│
├── modules/                        ← İŞ MANTIĞI KATMANI
│   └── sistem.py                      Rezervasyon, atama, ekipman ve raporlama işlemleri
│
├── models.py                       ← VERİ MODELLERİ
│                                      Ziyaretci, Alan, Ekipman, Rezervasyon dataclass'ları
│
├── tests/                          ← TEST DOSYALARI
│   ├── birim_testleri.py              64 birim testi (unittest)
│   └── performans_testleri.py         Karşılaştırmalı performans benchmark'ları
│
├── kayitlar/                       ← VERİ SETLERİ VE KAYITLAR (JSON)
│   ├── veri_10.json                   Küçük ölçekli test verisi
│   ├── veri_100.json                  Orta ölçekli test verisi
│   ├── veri_1000.json                 Büyük ölçekli test verisi
│   └── *.json                         Çalışma zamanı kalıcı verileri
│
├── generate_data.py                ← Örnek veri seti üretici
├── main.py                         ← GİRİŞ NOKTASI (python main.py)
├── Proje_Raporu.md                 ← Akademik Proje Raporu
└── README.md                       ← Bu dosya
```

---

## Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.10+
- PyQt6 (`pip install PyQt6`)
- GCC (yalnızca C kodunu yeniden derlemek isterseniz — DLL hazır gelmektedir)

### Çalıştırma

```bash
# 1. Uygulamayı başlat (GUI)
python main.py

# 2. Birim testlerini çalıştır (64 test — %100 başarı)
python tests/birim_testleri.py

# 3. Performans benchmark testleri
python tests/performans_testleri.py

# 4. Örnek veri seti üret (opsiyonel)
python generate_data.py
```

### C Kodunu Yeniden Derlemek (opsiyonel)

```bash
cd c_backend
build.bat
```

---

## Mimari Yaklaşım

Proje **Hibrit C/Python** mimarisi kullanır:

```
┌─────────────────────────────────────────────────┐
│          KULLANICI ARAYÜZÜ (Python/PyQt6)       │
│          gui/uygulama.py — 5 sekmeli GUI        │
└──────────────────┬──────────────────────────────┘
                   │ Python çağrıları
┌──────────────────▼──────────────────────────────┐
│           İŞ MANTIĞI (Python)                   │
│           modules/sistem.py                     │
└──────────────────┬──────────────────────────────┘
                   │ Python nesneleri
┌──────────────────▼──────────────────────────────┐
│         KÖPRÜ KATMANI (Python/ctypes)           │
│         data_structures/structures.py           │
└──────────────────┬──────────────────────────────┘
                   │ ctypes FFI çağrıları
┌──────────────────▼──────────────────────────────┐
│        VERİ YAPILARI MOTORU (C DİLİ)            │
│        c_backend/structures.c → structures.dll  │
│        malloc/free bellek yönetimi               │
│        11 veri yapısı, ~1200 satır C kodu       │
└─────────────────────────────────────────────────┘
```

- **C katmanı:** Tüm veri yapılarının algoritmik implementasyonu. Bellek yönetimi (malloc/free), pointer manipülasyonu ve performans optimizasyonu burada yapılır.
- **Python katmanı:** Kullanıcı arayüzü, iş mantığı ve veri dönüşümleri. C fonksiyonlarını `ctypes` ile çağırır.

---

## 11 Veri Yapısı ve Kullanım Alanları

| # | Veri Yapısı | C Fonksiyonları | Projede Kullanım | Karmaşıklık |
|---|-------------|-----------------|------------------|-------------|
| 1 | **HashMap** | `hashmap_create/insert/get/delete` | Ziyaretçi/Rezervasyon ID ile O(1) kayıt erişimi | O(1) ort. |
| 2 | **BST** | `bst_create/insert/search/range_query` | Tarih bazlı sıralı sorgu ve aralık arama | O(log n) |
| 3 | **Linked List** | `ll_create/append/prepend/remove` | Ziyaretçi rezervasyon geçmişi (dinamik liste) | O(1) ekle |
| 4 | **Stack** | `stack_create/push/pop/peek` | İşlem geri alma (Undo) — LIFO | O(1) |
| 5 | **Queue** | `queue_create/enqueue/dequeue` | Bekleme listesi — FIFO sıralı hizmet | O(1) |
| 6 | **Priority Queue** | `pq_create/enqueue/dequeue` | VIP/Engelli öncelikli alan atama | O(log n) |
| 7 | **Max Heap** | `maxheap_create/push/pop/top_k` | En popüler K alan sıralaması | O(log n) |
| 8 | **CampSet** | `set_create/add/remove/contains` | Bakımdaki alanların O(1) kontrol kümesi | O(1) |
| 9 | **Graph** | `graph_create/add_edge/dijkstra` | Alan komşulukları, BFS/DFS, en kısa yol | O(V+E) |
| 10 | **Matrix 2D** | `matrix_create/set/get/increment` | Alan tipi × gün doluluk matrisi | O(1) erişim |
| 11 | **Camp Tree** | `camptree_create/alan_ekle/alan_sil` | Mekansal hiyerarşi (N-ary ağaç) | O(1) erişim |

---

## GUI Sekmeleri

| Sekme | Özellikler |
|-------|-----------|
| **Ziyaretçiler** | Ekle / Güncelle / Sil / Ara / Öncelik Atama (Normal, VIP, Engelli) |
| **Alanlar** | Ekle / Sil / Bakıma Al / Bakımdan Çıkar / Komşuluk Tanımla |
| **Rezervasyonlar** | Oluştur / İptal / Stack ile Geri Al / BST Tarih Sorgusu |
| **Ekipman** | Stok Yönetimi / Ödünç Ver / İade Al |
| **Raporlar** | 6 İstatistik Kartı / Popüler Alanlar / Performans Testleri |

---

## Performans Karşılaştırmaları

Küçük (10), Orta (100) ve Büyük (1000) veri setleri üzerinde ölçüm yapılmıştır:

| Karşılaştırma | Küçük (10) | Orta (100) | Büyük (1000) | Sonuç |
|---------------|-----------|-----------|-------------|-------|
| Array vs **HashMap** arama | 0.41 µs | 1.81 µs | 15.72 vs **1.57 µs** | HashMap **~10x** hızlı |
| Lineer vs **BST** arama | 0.36 µs | 1.43 µs | 12.70 vs **1.99 µs** | BST **~6x** hızlı |
| Bubble Sort vs **Heap Sort** | 9.80 µs | 384 µs | 11411 vs **53.6 µs** | Heap **~212x** hızlı |
| Liste vs **Set** kontrol | 0.25 µs | 0.71 µs | 5.21 vs **0.19 µs** | Set **~27x** hızlı |

---

## Veri Kalıcılığı

Tüm veriler `kayitlar/` klasöründe JSON formatında saklanır.  
Program kapanınca otomatik kaydedilir, açılınca yüklenir.
