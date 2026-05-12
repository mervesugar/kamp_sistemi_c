# Kamp Alanı Rezervasyon ve Yönetim Sistemi — Proje Raporu

**Ders:** BMT210 Veri Yapıları — Dönem Projesi  
**Kurum:** Gazi Üniversitesi, Teknoloji Fakültesi, Bilgisayar Mühendisliği Bölümü  
**Öğretim Üyesi:** Doç. Dr. Adem Tekerek  
**Yıl:** 2026  
**Programlama Dilleri:** C (Veri Yapıları) + Python (Arayüz ve İş Mantığı)

---

## 1. Problem Tanımı ve Sektörel Uygunluk

Kamp alanları; turizm, rekreasyon ve konaklama sektörlerinde yaygın olarak kullanılan tesislerdir. Bu tesislerde farklı büyüklük ve tipte (çadır, karavan, bungalov) onlarca alan bulunur. Ziyaretçilerin rezervasyon yapması, alanlara kapasiteye göre atanması, ekipmanların ödünç verilip takip edilmesi ve bakım gerektiren alanların geçici olarak kapatılması gibi süreçlerin **manuel yönetimi** ciddi hatalara ve verimsizliğe yol açmaktadır.

Bu proje; bir kamp alanında gerçekleştirilen **rezervasyon, alan atama, ekipman takibi ve öncelikli hizmet yönetimi** süreçlerini otomatikleştiren bir sistem geliştirmeyi amaçlar. Proje kapsamında her bir süreç, en uygun veri yapısı ile modellenerek performans avantajları ortaya konmuştur.

**Hedeflenen sektörler:** T.C. Orman Genel Müdürlüğü tesisleri, özel kamp işletmeleri ve doğa turizmi merkezleri.

---

## 2. Amaç ve Kapsam

Projenin temel amacı, BMT210 dersinde öğrenilen **11 farklı veri yapısını** gerçek bir sektörel problem üzerinde uygulayarak:

- Veri yapılarının problemle ilişkisini göstermek,
- Her birinin neden seçildiğini gerekçelendirmek,
- Alternatif veri yapılarıyla karşılaştırmalı performans analizi yapmak,
- Çalışan bir yazılım teslim etmektir.

---

## 3. Kullanılan Veri Yapıları

Aşağıdaki 11 veri yapısının **tamamı C dilinde** (`structures.c` — ~1200 satır) implementerilmiştir:

### 3.1. Hash Map (Karma Tablo)
- **C Fonksiyonları:** `hashmap_create`, `hashmap_insert`, `hashmap_get`, `hashmap_delete`, `hashmap_contains`
- **Kullanım:** Ziyaretçi ID ve Rezervasyon ID ile kayıtlara **O(1)** sürede erişim.
- **Gerekçe:** Binlerce kayıt içinde tek bir ID ile arama yapılacağından, dizi bazlı O(n) arama yerine hash tabanlı O(1) erişim tercih edilmiştir.

### 3.2. BST (İkili Arama Ağacı)
- **C Fonksiyonları:** `bst_create`, `bst_insert`, `bst_search`, `bst_delete`, `bst_range_query`
- **Kullanım:** Tarihe göre sıralı rezervasyon sorgulaması ve belirli bir tarih aralığındaki kayıtları çekme.
- **Gerekçe:** Sıralı veri üzerinde aralık sorgusu (range query) yapabilmek için BST'nin O(log n) karmaşıklığı tercih edilmiştir.

### 3.3. Bağlı Liste (Doubly Linked List)
- **C Fonksiyonları:** `ll_create`, `ll_append`, `ll_prepend`, `ll_remove`, `ll_to_array`
- **Kullanım:** Ziyaretçilerin geçmiş rezervasyonlarının kronolojik listesi. En son rezervasyon başa eklenir (prepend).
- **Gerekçe:** Sık ekleme-silme gerektiren dinamik veri kümeleri için sabit maliyetli O(1) baş/son ekleme sağlar.

### 3.4. Yığıt (Stack — LIFO)
- **C Fonksiyonları:** `stack_create`, `stack_push`, `stack_pop`, `stack_peek`
- **Kullanım:** Hatalı bir rezervasyon veya ekipman işleminin geri alınması (Undo mekanizması).
- **Gerekçe:** Son yapılan işlemin ilk geri alınması gerektiğinden LIFO yapısı doğal çözümdür.

### 3.5. Kuyruk (Queue — FIFO)
- **C Fonksiyonları:** `queue_create`, `queue_enqueue`, `queue_dequeue`, `queue_peek`
- **Kullanım:** Aynı tarihte bekleyen standart (Normal öncelikli) rezervasyonların sıralı bekleme listesi.
- **Gerekçe:** İlk gelen ilk hizmet alır mantığı (FIFO) bekleme kuyruğu için idealdir.

### 3.6. Öncelikli Kuyruk (Priority Queue)
- **C Fonksiyonları:** `pq_create`, `pq_enqueue`, `pq_dequeue`, `pq_peek`
- **Kullanım:** VIP ve engelli misafirlerin alan atanırken normal müşterilerin önüne geçmesi.
- **Gerekçe:** Basit FIFO kuyruğu öncelik ayrımı yapamaz; max-heap tabanlı PQ ile O(log n) sürede öncelikli çıkarma sağlanır.

### 3.7. Maksimum Yığın (Max Heap)
- **C Fonksiyonları:** `maxheap_create`, `maxheap_push`, `maxheap_pop`, `maxheap_top_k`
- **Kullanım:** Sistemdeki en popüler K adet kamp alanının (en çok rezervasyon yapılanlar) hızlı tespiti.
- **Gerekçe:** Bubble Sort O(n²) ile sıralama yerine, Heap Sort O(n log n) ile çok daha verimli sıralama yapılır. Büyük veri setlerinde **~200 kat** hız farkı ölçülmüştür.

### 3.8. Küme (CampSet)
- **C Fonksiyonları:** `set_create`, `set_add`, `set_remove`, `set_contains`
- **Kullanım:** Bakıma alınan alanların tekrarsız takibi ve O(1) üyelik kontrolü.
- **Gerekçe:** Bir alanın bakımda olup olmadığını her rezervasyon girişinde kontrol etmek gerekir. Dizi bazlı O(n) kontrol yerine küme ile O(1) kontrol sağlanır.

### 3.9. Graf (Graph — Adjacency List)
- **C Fonksiyonları:** `graph_create`, `graph_add_edge`, `graph_neighbors`, `graph_dijkstra`
- **Kullanım:** Kamp alanları arasındaki coğrafi komşulukların modellenmesi. BFS/DFS ile erişilebilirlik analizi, Dijkstra ile en kısa yol hesaplaması.
- **Gerekçe:** Alanlar arası ilişki ağaç veya dizide modellenemez; graf yapısı düğüm-kenar ilişkilerini doğal olarak temsil eder.

### 3.10. İki Boyutlu Dizi (Matrix 2D)
- **C Fonksiyonları:** `matrix_create`, `matrix_set`, `matrix_get`, `matrix_increment`, `matrix_row_sum`, `matrix_col_sum`
- **Kullanım:** Satır = Alan tipleri (Çadır, Karavan, Bungalov), Sütun = Haftanın günleri. Değer = o gün o tipteki doluluk sayısı.
- **Gerekçe:** Doluluk verisine indeks bazlı O(1) erişim için sabit boyutlu 2D dizi en verimli yapıdır.

### 3.11. Ağaç (Camp Tree — N-ary Tree)
- **C Fonksiyonları:** `camptree_create`, `camptree_alan_ekle`, `camptree_alan_sil`, `camptree_bolge_alanlari`, `camptree_alan_bolgesi`
- **Kullanım:** Kampın mekansal hiyerarşisi: Kök → Bölgeler (Çadır/Karavan/Bungalov) → Parseller (Alan ID).
- **Gerekçe:** Hiyerarşik organizasyon (kategori → alt eleman) ağaç yapısıyla doğal olarak modellenir; BFS/DFS gezimi ve raporlama yapılabilir.

---

## 4. Sistem Tasarımı

### 4.1. Genel Mimari

Proje, performans gerektiren alt seviye işlemler ile kullanıcı dostu arayüz gereksinimlerini en iyi şekilde karşılayabilmek adına **hibrit bir mimari** ile tasarlanmıştır. Temel mimari yapı şu şekildedir:

- **Arka Plan (Backend - C Dili):** Veri yapılarının (Ağaç, Graf, Kuyruk, Yığıt vb.) tamamı, bellek yönetimi (malloc/free) hassasiyetiyle doğrudan **C dilinde** (`c_backend/structures.c`) geliştirilmiş ve yüksek performanslı bir dinamik kütüphane (`structures.dll` / `.so`) olarak derlenmiştir.
- **Ara Katman (Köprü - ctypes):** Python'un yerleşik `ctypes` modülü kullanılarak, C dilinde derlenmiş bu kütüphane ile Python arasında bir iletişim köprüsü kurulmuştur. Python, bellek adreslerini ve veri tiplerini dönüşümden geçirerek C fonksiyonlarını doğrudan çağırabilmektedir.
- **Ön Yüz ve İş Mantığı (Frontend & Logic - Python):** Kullanıcı arayüzü **Python (PyQt6)** ile oluşturulmuş, sistemin genel işleyişi (kurallar, kısıtlamalar, veri yönlendirmeleri) bu katmanda yönetilmiştir.

Bu hibrit yaklaşım, **C'nin hız ve düşük seviyeli bellek yönetim gücünü**, **Python'un hızlı geliştirme, esneklik ve kullanım kolaylığı** ile birleştiren etkin bir altyapı sunmaktadır.

| Katman | Dil | Dosya | Sorumluluk |
|--------|-----|-------|------------|
| **Veri Yapıları** | C | `c_backend/structures.c` | 11 veri yapısının implementasyonu, dinamik bellek yönetimi |
| **Köprü** | Python | `data_structures/structures.py` | C kütüphanesini `ctypes` ile içe aktarma, tip dönüşümleri |
| **İş Mantığı** | Python | `modules/sistem.py` | Rezervasyon kısıtlamaları, VIP/Engelli önceliği, sistem akışı |
| **Arayüz** | Python | `gui/uygulama.py` | PyQt6 ile kullanıcı etkileşimli masaüstü uygulaması |
| **Modeller** | Python | `models.py` | Ziyaretçi, Alan, Ekipman, Rezervasyon gibi temel veri nesneleri |

### 4.2. Kullanıcı Arayüzü (UI) ve Ekran Görüntüleri

Uygulamanın arayüzü, kamp alanı yöneticilerinin tüm işlemleri tek bir pencereden kolayca yönetebilmesi için **sekme (tab) tabanlı** olarak tasarlanmıştır. Ana sekmeler ve işlevleri şunlardır:

- **Ziyaretçiler:** Yeni misafir kayıtlarının yapıldığı, güncellendiği ve sistemdeki mevcut ziyaretçilerin listelendiği bölümdür.
- **Alanlar:** Kamp içindeki çadır, karavan ve bungalov alanlarının anlık kapasitelerinin ve bakım/uygunluk durumlarının takip edildiği sekmedir.
- **Rezervasyonlar:** Müşterilere alan tahsisinin yapıldığı, VIP ve Engelli misafirler için öncelikli kuyruk (Priority Queue) yapısının işlediği ve hatalı işlemlerin geri alınabildiği (Stack tabanlı Undo) ana yönetim panelidir.
- **Ekipman:** Kamp malzemelerinin (çadır, tulum, mat vb.) stok takibinin ve misafirlere zimmetlenme süreçlerinin yürütüldüğü alandır.
- **Kamp Haritası ve Raporlar:** Kamp bölgeleri arasındaki coğrafi komşulukların (Graf) görselleştirildiği, BFS/DFS arama algoritmalarıyla alan analizi yapılabildiği ve doluluk istatistiklerinin raporlandığı kısımdır.

> **NOT:** Projenin son teslim versiyonunda arayüzün kullanımını gösteren ekran görüntüleri (sekmelerin açık halleri) buraya eklenecektir.

### 4.3. Veri Akışı Özeti

Sistemdeki bir verinin yaşam döngüsü ve modüller arası akışı genel olarak aşağıdaki adımlarla gerçekleşir:

1. **Girdi (Arayüz):** Kullanıcı, PyQt6 arayüzündeki formlar aracılığıyla bir işlem (örn. yeni bir VIP rezervasyon talebi) başlatır.
2. **Doğrulama (İş Mantığı):** Python tarafındaki sistem modülü bu isteği alır; kapasite kontrolü, alan müsaitliği ve müşteri önceliği gibi iş kurallarını denetler.
3. **İşlem (C Kütüphanesi):** Geçerli olan istek, `ctypes` üzerinden parametreler formatlanarak (tip dönüşümleri yapılarak) C kütüphanesindeki hedef veri yapısı fonksiyonuna (örn. `pq_enqueue` veya `hashmap_insert`) aktarılır.
4. **Güncelleme ve Yanıt:** C tarafında ilgili veri yapısının belleği güncellenir ve işlemin başarılı/başarısız olma durumu Python'a sonuç (return) kodu olarak döndürülür. Python bu durumu arayüze yansıtarak tabloları anlık olarak yeniler.
5. **Veri Kalıcılığı:** İşlemler tamamlandığında veya uygulama kapatıldığında, hafızadaki son durum Python üzerinden `kayitlar/` dizinine **JSON** formatında yazılarak kaydedilir. Sistemin sonraki açılışında bu dosyalar okunup C tarafındaki veri yapıları tekrar ayağa kaldırılır.

---

## 5. Algoritmik Yaklaşım

### 5.1. Rezervasyon Oluşturma Akışı
1. **HashMap** ile ziyaretçi ID kontrolü — O(1)
2. **CampSet** ile alanın bakımda olup olmadığı kontrolü — O(1)
3. **Matrix2D** ile doluluk durumu kontrolü — O(1)
4. **PriorityQueue** ile öncelikli atama (VIP > Normal) — O(log n)
5. **BST** ile tarih bazlı kayıt ekleme — O(log n)
6. **LinkedList** ile ziyaretçi geçmişine ekleme — O(1)
7. **Stack** ile geri alma kaydı oluşturma — O(1)

### 5.2. Raporlama
- **MaxHeap** ile en popüler K alan — O(n log n)
- **Matrix2D** satır/sütun toplamları ile doluluk analizi — O(n)
- **Graph** BFS/DFS ile alan erişilebilirlik raporu — O(V+E)
- **CampTree** hiyerarşi yazımı ile organizasyon raporu

---

## 6. Test Senaryoları

### 6.1. Birim Testleri
Python `unittest` modülü ile **64 birim testi** yazılmış ve C fonksiyonlarına bağlı olarak çalıştırılmıştır. Tüm testler **%100 başarı** ile geçmiştir.

| Veri Yapısı | Test Sayısı | Başarı |
|-------------|-------------|--------|
| HashMap | 8 | ✅ 8/8 |
| BST | 7 | ✅ 7/7 |
| LinkedList | 6 | ✅ 6/6 |
| Stack | 5 | ✅ 5/5 |
| Queue | 4 | ✅ 4/4 |
| PriorityQueue | 3 | ✅ 3/3 |
| MaxHeap | 4 | ✅ 4/4 |
| CampSet | 4 | ✅ 4/4 |
| Graph | 5 | ✅ 5/5 |
| Matrix2D | 6 | ✅ 6/6 |
| CampTree | 9 | ✅ 9/9 |
| Entegrasyon | 3 | ✅ 3/3 |
| **Toplam** | **64** | **✅ 64/64** |

### 6.2. Veri Setleri
Testler 3 farklı ölçekte çalıştırılmıştır:

| Ölçek | Rezervasyon | Alan | Ziyaretçi | Amaç |
|-------|------------|------|-----------|------|
| Küçük | 10 | 5 | 5 | Manuel doğrulama |
| Orta | 100 | 20 | 20 | Normal yoğunluk simülasyonu |
| Büyük | 1000 | 50 | 200 | Algoritmik karmaşıklık farkının gözlenmesi |

---

## 7. Performans Karşılaştırmaları

C dilinde implemente edilen veri yapıları, alternatif basit yaklaşımlarla karşılaştırılmıştır. Ölçümler `tests/performans_testleri.py` ile yapılmıştır.

### 7.1. Arama: Array (O(n)) vs HashMap (O(1))

| Veri Boyutu | Array Arama | HashMap Arama | Hız Farkı |
|-------------|------------|---------------|-----------|
| 10 | 0.41 µs | 1.53 µs | ~0.3x |
| 100 | 1.81 µs | 1.71 µs | ~1.1x |
| **1000** | **15.72 µs** | **1.57 µs** | **~10x** |

**Yorum:** Küçük verilerde fark önemsiz, ancak veri büyüdükçe Array O(n) ile orantılı yavaşlarken HashMap sabit O(1) süresini korur.

### 7.2. Sıralama: Bubble Sort (O(n²)) vs Heap Sort (O(n log n))

| Veri Boyutu | Bubble Sort | Heap Sort | Hız Farkı |
|-------------|------------|-----------|-----------|
| 10 | 9.80 µs | 880.30 µs | ~0.01x |
| 100 | 384.90 µs | 11.60 µs | ~33x |
| **500** | **11411 µs** | **53.60 µs** | **~212x** |

**Yorum:** Bubble Sort n² ile orantılı büyürken, MaxHeap tabanlı sıralama n log n ile çok daha ölçeklenebilirdir.

### 7.3. Üyelik Kontrolü: Liste (O(n)) vs Set (O(1))

| Veri Boyutu | Liste Kontrol | Set Kontrol | Hız Farkı |
|-------------|--------------|-------------|-----------|
| 10 | 0.247 µs | 0.200 µs | ~1.2x |
| 100 | 0.706 µs | 0.198 µs | ~3.6x |
| **1000** | **5.206 µs** | **0.190 µs** | **~27x** |

**Yorum:** CampSet (hash tabanlı küme) bakım kontrolünde sabit O(1) sağlar; liste tabanlı kontrol veri boyutuyla doğru orantılı yavaşlar.

---

## 8. Sonuç ve Değerlendirme

Bu projede BMT210 dersi kapsamında öğrenilen **11 temel veri yapısı**, gerçek bir kamp alanı yönetim problemine başarıyla uygulanmıştır. Proje sürecinde elde edilen temel kazanımlar:

1. **Veri yapılarının doğru seçiminin önemi:** Her bir veri yapısı, çözdüğü probleme göre bilinçli olarak seçilmiş ve gerekçelendirilmiştir. Yanlış veri yapısı kullanımının (örneğin sıralama için Bubble Sort yerine Heap Sort) performansta **200 kata varan** farklar yaratabileceği deneysel olarak gösterilmiştir.

2. **C dilinin avantajları:** Düşük seviyeli bellek yönetimi (malloc/free) ve pointer kullanımı ile veri yapılarının nasıl çalıştığı derinden anlaşılmıştır.

3. **Hibrit mimari başarısı:** C'nin performans gücü ile Python'un geliştirme hızı ve zengin kütüphane desteği etkin biçimde birleştirilmiştir.

4. **Test kültürü:** 64 birim testi ile kodun doğruluğu; 3 farklı ölçekteki veri setiyle performansı sistematik olarak doğrulanmıştır.

---

## 9. Grup Üyelerinin Görev Dağılımı

### 👤 1. Kişi — [AD SOYAD]
- **C Veri Yapıları:** HashMap, BST, Linked List, CampSet, Matrix2D
- **Sistem Modülü:** Ziyaretçi ekleme/silme/güncelleme, alan yönetimi
- **Arayüz:** Ziyaretçiler ve Alanlar sekmeleri (PyQt6)
- **Rapor:** Problem tanımı, veri yapıları açıklamaları, README

### 👤 2. Kişi — [AD SOYAD]
- **C Veri Yapıları:** Priority Queue, Queue, Stack, Max Heap, Graph, Camp Tree
- **Sistem Modülü:** Rezervasyon sıraya alma, geri alma, BFS/DFS komşuluk analizi
- **Test:** `birim_testleri.py` ve `performans_testleri.py`
- **Arayüz:** Rezervasyonlar, Ekipman ve Raporlar sekmeleri (PyQt6)
- **Rapor:** Performans karşılaştırmaları, sonuç ve değerlendirme
