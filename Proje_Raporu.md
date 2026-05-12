# GAZİ ÜNİVERSİTESİ
## TEKNOLOJİ FAKÜLTESİ
## BİLGİSAYAR MÜHENDİSLİĞİ BÖLÜMÜ

**BMT210 VERİ YAPILARI PROJE ÖDEVİ RAPORU**

**2025-2026 BAHAR YARIYILI**  
**DOÇ. DR. Adem TEKEREK**

**Hazırlayanlar:**
* Elif KINALI – 24181616038
* Merve ŞEKER – 24181616027

# Kamp Alanı Rezervasyon Yönetim Sistemi

## Görev Dağılımı
Proje, grup üyeleri arasında dengeli ve denetlenebilir bir görev paylaşımıyla yürütülmüştür. Aşağıdaki tabloda her bir üyenin sorumlu olduğu modüller, geliştirme alanları ve katkı oranları özetlenmiştir.

| Üye | Sorumlu Olduğu Modüller | Katkı Alanları | Oran |
| :--- | :--- | :--- | :--- |
| **Elif KINALI** 24181616038 | C arka plan (`c_backend/*.c`), `data_structures` köprüsü (`structures.py`, `structures_python.py`), Birim ve Performans testleri (`tests/*.py`), `generate_data.py` | Kullanıcı arayüzü tasarımı, sekme bazlı GUI mimarisi, sistem akış mantığı, rezervasyon/iptal/geri al iş kuralları, kamp haritası görselleştirmesi | %50 |
| **Merve ŞEKER** 24181616027 | PyQt6 arayüzü (`gui/uygulama.py`), İş mantığı (`modules/sistem.py`), Veri modelleri (`models.py`), JSON kalıcılık katmanı (`kayitlar/`) | Veri yapılarının C dilinde implementasyonu, ctypes köprü katmanı, MaxHeap/PriorityQueue/BST/Graph algoritmaları, performans testlerinin tasarlanması ve raporlanması | %50 |

## 1. Giriş
### 1.1 Problem Tanımı
Kamp işletmeleri; farklı alan tipleri (Çadır / Karavan / Bungalov), kapasite, bakım durumu, ziyaretçi yönetimi, rezervasyon oluşturma ve iptal, ekipman stok-ödünç takibi, istatistik ve raporlama gibi süreçleri aynı anda yürütmek zorundadır. Bu süreçlerin manuel takibi; çakışma, hatalı kayıt, yanlış doluluk bilgisi ve zaman kaybı gibi sorunlara yol açmaktadır.
Bu proje, kamp işletmesi için rezervasyon ve yönetim işlemlerini tek bir sistemde, uygun veri yapılarıyla verimli şekilde gerçekleştirmeyi hedeflemektedir. Tasarım kararı verirken yalnızca işlevsellik değil, her bir veri yapısının zaman ve bellek karmaşıklığının probleme uygunluğu da göz önünde bulundurulmuştur.

### 1.2 Amaç
Projenin temel amacı, 11 farklı veri yapısını gerçek bir sektörel problem üzerinde uygulayarak: veri yapılarının problemle ilişkisini göstermek, her birinin neden seçildiğini gerekçelendirmek, alternatif veri yapılarıyla karşılaştırmalı performans analizi yapmak ve çalışan bir yazılım teslim etmektir.

### 1.3 Kapsam
Geliştirilen mimari, bir kamp alanının ihtiyaç duyacağı temel operasyonları veri yapıları odaklı olarak kapsamaktadır:
* **Ziyaretçi ve Alan Yönetimi:** Kayıtların eklenmesi, güncellenmesi, silinmesi ve mekânsal kapasite takibi.
* **Rezervasyon ve Öncelikli Bekleme Listesi:** Standart rezervasyon işlemlerinin yanı sıra dolu alanlar için VIP/Engelli öncelikli bekleme kuyruğunun yönetilmesi.
* **Mekânsal Hiyerarşi ve Rota Analizi:** Bölge-parsel hiyerarşisinin N-ary ağaç ile modellenmesi ve alanlar arası en kısa yolun Dijkstra algoritmasıyla hesaplanması.
* **Geri Alma (Undo) Mekanizması:** Yığın (Stack) tabanlı operasyon geçmişiyle son işlemin güvenle geri alınması.
* **Performans Karşılaştırma:** Aynı problem için farklı veri yapısı seçeneklerinin küçük/orta/büyük veri kümeleri üzerinde ölçülmesi.

### 1.4 Kullanılan Teknolojiler

| Bileşen | Teknoloji / Sürüm | Görevi |
| :--- | :--- | :--- |
| **Uygulama dili** | Python 3.12 | İş mantığı, arayüz ve köprü katmanı |
| **Arka plan dili** | C99 (MinGW GCC) | 11 veri yapısının yüksek performanslı implementasyonu |
| **Arayüz** | PyQt6 6.7 | Sekme tabanlı masaüstü kullanıcı arayüzü |
| **C/Python köprüsü** | ctypes | `structures.dll` içindeki C fonksiyonlarının Python'dan çağrılması |
| **Veri kalıcılığı** | JSON (UTF-8) | Ziyaretçi, alan, rezervasyon ve graf verilerinin diske yazılması |
| **Test çerçevesi** | unittest (Python std) | 12 test sınıfı altında 50'nin üzerinde birim testinin koşulması |
| **Yedek katman** | Saf Python | DLL bulunamadığında otomatik olarak `structures_python` modülüne geçiş |

## 2. Kullanılan Veri Yapıları
Bu bölümde projede kullanılan 11 veri yapısı; her birinin sistemdeki işlevi, seçilme gerekçesi ve alternatifine göre sağladığı avantaj ile birlikte ele alınmaktadır. Yönerge madde 4'te listelenen tüm veri yapıları (Dizi, Bağlı Liste, Yığın, Kuyruk, Öncelikli Kuyruk, Ağaç, BST, Hash Table, Graf, Heap, Set/Map) projede karşılığını bulmaktadır.

### 2.1 Veri Yapıları Genel Çözüm Özeti
| Veri Yapısı | Sistemdeki Görevi | Sağladığı Avantaj | Zaman Karmaşıklığı |
| :--- | :--- | :--- | :--- |
| **HashMap** | Ziyaretçi / Alan / Rezervasyon / Ekipman ID erişimi | Anlık erişim, liste taramasına gerek yok | Ekleme/Arama: O(1) ort. |
| **CampSet** | Bakımdaki alanların kümesi | Tekrar ekleme yok, anlık üyelik kontrolü | Kontrol/Ekleme: O(1) |
| **BST** | Tarihe göre rezervasyon sıralama ve aralık sorgusu | Sıralı yapı, aralık sorgusu (range query) verimli | Arama/Ekleme: O(log n) |
| **CampTree** | Kamp alanının mekânsal hiyerarşisi (N-ary) | Bölgesel sorgulama, alt dal hesaplama | Ekleme/Erişim: O(1) ort. |
| **MaxHeap** | En popüler alanların sıralanması (top-k) | Tepedeki en büyük değere O(1) erişim | Ekleme: O(log n), Max: O(1) |
| **PriorityQueue** | VIP/Engelli ziyaretçilerin önceliklendirilmesi | Öncelik sırasını otomatik korur, FIFO eşit öncelikte | Ekleme/Çıkarma: O(log n) |
| **Stack** | Son işlemi geri alma (Undo) | LIFO mantığıyla anlık geri al | Push/Pop: O(1) |
| **LinkedList** | Ziyaretçi rezervasyon geçmişi (çift yönlü) | Başa ekleme O(1), dinamik boyut | Ekleme: O(1), Arama: O(n) |
| **Queue** | Normal (öncelliksiz) bekleme listesi | Adil FIFO sırası | Ekleme/Çıkarma: O(1) |
| **Graph** | Alan komşulukları, rota analizi | BFS/DFS/Dijkstra ile esnek gezim | Dijkstra: O((V+E) log V) |
| **Matrix2D** (Dizi) | Alan tipi × gün doluluk istatistiği | İki boyutlu indeks, anlık okuma/yazma | Okuma/Yazma: O(1) |

### 2.2 Veri Yapılarının Detaylı Kullanımı
Aşağıda, sistemde sıklıkla başvurulan dört temel veri yapısının kod düzeyindeki kullanımı kısaca açıklanmıştır.

#### 2.2.1 HashMap — Çoklu Sözlük
Sistemde dört ayrı HashMap örneği kullanılmaktadır: `ziyaretci_map`, `alan_map`, `ekipman_map` ve `rezervasyon_map`. Her biri, ilgili nesneye ID üzerinden ortalama O(1) sürede erişim sağlar. C tarafında double hashing yerine zincirleme (separate chaining) tercih edilmiştir; kapasite varsayılan olarak 64 olarak ayarlanmış ve gerektiğinde Python katmanı dış kapsayıcıyla genişletmektedir.

#### 2.2.2 BST — Tarihe Göre Aralık Sorgusu
Rezervasyonlar, ana HashMap yanı sıra giriş tarihi anahtarıyla bir BST'ye de eklenir. Bu sayede 'belirli iki tarih arasındaki rezervasyonları getir' sorgusu O(log n + k) sürede (k = sonuç sayısı) gerçekleştirilebilmektedir. Saf liste taramasıyla karşılaştırıldığında, 1000 kayıtta yaklaşık 16 kat daha hızlı çalışmaktadır (bkz. Bölüm 6.2).

#### 2.2.3 PriorityQueue — Öncelikli Bekleme
Dolu bir alan için yeni rezervasyon talebi geldiğinde, ziyaretçi öncelik değeriyle birlikte PriorityQueue'ya eklenir (Normal=0, VIP=5, Engelli=10). C tarafındaki max-heap implementasyonu eşit önceliklerde FIFO davranışını korumak için ek bir 'counter' alanı kullanır; bu, aynı öncelik düzeyindeki ziyaretçilerin adil sırayla atanmasını garantiler.

#### 2.2.4 Graph + Dijkstra — En Kısa Rota
Kamp parselleri grafın düğümleri, aralarındaki yollar ağırlıklı kenarlar olarak modellenmiştir. `graph_dijkstra` fonksiyonu, başlangıç-bitiş düğümleri arasında en kısa mesafeyi ve geçilen yol listesini döndürür. Uygulama içerisinde 'Alanlar' sekmesinden bir A→B sorgusu yapıldığında, sonuç anında arayüzde görselleştirilir. Algoritma C tarafında dizi tabanlı O(V²) varyantıyla çalışmakta; düğüm sayısı 100'ün altında kaldığı için heap-tabanlı sürüme göre çok az fark gösterir.

## 3. Sistem Tasarımı ve Mimari
### 3.1 Mimari Genel Bakış
Proje, performans gerektiren alt seviye işlemler ile kullanıcı dostu arayüz gereksinimlerini bir arada karşılayabilmek için hibrit bir mimariyle tasarlanmıştır:
* **Arka plan (Backend - C):** Veri yapılarının tamamı C99 ile yazılmış, malloc/free hassasiyetiyle yönetilen dinamik bir kütüphane (`structures.dll`) olarak derlenmiştir.
* **Köprü (Bridge - ctypes):** Python'un yerleşik ctypes modülüyle C fonksiyonları doğrudan çağrılmakta, tip dönüşümleri (`c_char_p`, `py_object`, `c_int`) merkezi şekilde yönetilmektedir.
* **Yedek katman (Fallback):** DLL bulunamazsa `structures_python` modülü otomatik devreye girer; sistemin farklı işletim sistemlerinde derlemesiz çalışmasını sağlar.
* **İş mantığı (Logic - Python):** `modules/sistem.py` içinde rezervasyon kuralları, öncelik atamaları ve veri yönlendirmeleri yer alır.
* **Arayüz (Frontend - PyQt6):** `gui/uygulama.py` içinde sekme tabanlı masaüstü arayüz; tablolar, formlar, ağaç görünümü ve grafik sahnesi içerir.

Bu hibrit yaklaşım, C'nin hız ve düşük seviyeli bellek kontrolünü, Python'un hızlı geliştirme esnekliği ile birleştirir.

| Katman | Dil | Dosya | Sorumluluk |
| :--- | :--- | :--- | :--- |
| **Veri yapıları** | C | `c_backend/*.c` | 11 veri yapısının implementasyonu, dinamik bellek yönetimi |
| **Köprü** | Python | `data_structures/structures.py` | C kütüphanesini ctypes ile içe aktarma, tip dönüşümleri |
| **Yedek** | Python | `data_structures/structures_python.py` | DLL yokken devreye giren saf Python implementasyonu |
| **İş mantığı** | Python | `modules/sistem.py` | Rezervasyon kuralları, VIP/Engelli önceliği, sistem akışı |
| **Arayüz** | Python | `gui/uygulama.py` | PyQt6 ile sekme tabanlı masaüstü uygulaması |
| **Modeller** | Python | `models.py` | Ziyaretçi, Alan, Ekipman, Rezervasyon dataclass'ları |

### 3.2 Kullanıcı Arayüzü ve Sekme Yapısı
Arayüz, kamp alanı yöneticilerinin tüm işlemleri tek bir pencereden yönetebilmesi için sekme (tab) tabanlı tasarlanmıştır. Her sekme bir veya birden çok veri yapısının görsel karşılığını sunar.

#### 3.2.1 Ziyaretçiler Sekmesi
Yeni misafir kayıtlarının yapıldığı, mevcut ziyaretçilerin listelendiği ve öncelik durumunun (Normal / VIP / Engelli) atandığı sekmedir. Arka planda her ziyaretçi HashMap üzerinde ID anahtarıyla saklanır; arama kutusuyla ad veya ID üzerinden anlık filtreleme yapılır. 'Son İşlemi Geri Al' butonu Stack tabanlı Undo mekanizmasını tetikler.

#### 3.2.2 Alanlar Sekmesi
Çadır, karavan ve bungalov alanlarının kapasite ve bakım durumlarının takip edildiği sekmedir. Sağ alttaki 'Yol Tarifi & Graf Yönetimi' paneli, Graph veri yapısı üzerinde Dijkstra algoritmasını çalıştırarak iki parsel arası en kısa rotayı hesaplar. 'Komşu Ekle' formuyla alanlar arasına ağırlıklı kenar eklenebilir; sonuçlar siyah çıktı kutusunda görüntülenir.

#### 3.2.3 Rezervasyonlar Sekmesi
Alan tahsisinin yapıldığı, iptal edildiği ve geri alındığı ana yönetim panelidir. Üst tabloda tüm rezervasyonlar, alt tabloda ise dolu alanlar için PriorityQueue üzerinde tutulan VIP/Engelli öncelikli bekleme listesi yer alır. Bir alan dolduğunda yeni talep otomatik olarak bekleme kuyruğuna alınır; bir iptal gerçekleştiğinde tepedeki en yüksek öncelikli ziyaretçi `pq_dequeue` ile sıradan çekilir.

#### 3.2.4 Ekipman Sekmesi
Kamp ekipmanlarının (çadır, uyku tulumu, sandalye, fener vb.) stok takibinin yapıldığı sekmedir. Her ekipman HashMap üzerinde ID anahtarıyla saklanır; 'Mevcut Stok' alanı kritik seviyenin altına düştüğünde tabloda turuncu, sıfıra düştüğünde kırmızı renkle vurgulanır. 'Ödünç Ver' ve 'İade Al' butonları stok miktarını anlık günceller.

#### 3.2.5 Kamp Haritası Sekmesi
Sistemin en görsel sekmesidir ve birden fazla veri yapısını bir arada gösterir. Sağdaki QTreeWidget paneli, CampTree (N-ary ağaç) yapısını Kök → Bölge → Parsel hiyerarşisiyle çizer; her düğümün altındaki parsel sayısı ve durumu (Müsait / Bakımda) gösterilir. Sol taraftaki QGraphicsScene paneli ise Graph yapısını çember düzeninde çizerek alanlar arası komşulukları görselleştirir; sağ alttaki zoom kaydırıcı ile yakınlaştırma yapılabilir. Alt bölgede ise CampTree'nin `bolge_raporu()` çıktısı üç ayrı tabloyla (Çadır / Karavan / Bungalov) sunulur.

#### 3.2.6 Raporlar Sekmesi
Sistemin istatistiksel özetinin sunulduğu sekmedir. Üst bandında altı stat kartı (Ziyaretçi, Alan, Ekipman, Toplam Rezervasyon, Aktif Rezervasyon, Gelir) yer alır. 'Popüler Alanlar' tablosu MaxHeap'in `top_k()` çıktısını gösterirken; 'Tarih Aralığı Sorgusu' paneli BST'nin `range_query()` fonksiyonunu kullanır. Sağda yer alan 'Performans Karşılaştırması' paneli ise dört testin (Array vs HashMap, Linear vs BST, Bubble vs Heap, List vs Set) hem metinsel çıktısını hem de bar grafiklerini üretir. Ayrıca 10/100/1000 ölçekli hazır test veri setleri tek tıkla yüklenebilir.

### 3.3 Veri Akışı
Sistemdeki bir verinin yaşam döngüsü genel olarak şu adımlarla ilerler:
1. **Girdi (Arayüz):** Kullanıcı PyQt6 formundan bir işlem başlatır (örn. yeni VIP rezervasyon).
2. **Doğrulama (İş Mantığı):** Python tarafındaki sistem modülü kapasite, bakım ve öncelik kurallarını denetler.
3. **İşlem (C Kütüphanesi):** Geçerli istek ctypes üzerinden ilgili C fonksiyonuna (`pq_enqueue`, `hashmap_insert`, `bst_insert` vb.) aktarılır.
4. **Güncelleme:** C tarafında ilgili veri yapısının belleği güncellenir; sonuç (return) kodu Python'a döner.
5. **Kalıcılık:** İşlem tamamlandığında `kayitlar/` dizinine JSON formatında yazılır; uygulama yeniden açıldığında bu dosyalardan okuma yapılır.

### 3.4 Çalıştırma Adımları
Sistemin yerel makinede çalıştırılması için aşağıdaki adımlar izlenir (Windows tabanlı geliştirme ortamında doğrulanmıştır):
1) **Bağımlılıkların kurulumu:** `pip install PyQt6`
2) **C arka planının derlenmesi:** `cd c_backend && build.bat` — MinGW GCC ile `structures.dll` üretilir. DLL üretilemezse sistem otomatik olarak saf Python katmanına düşer.
3) **Örnek veri seti üretimi (opsiyonel):** `python generate_data.py` — `kayitlar/` altında `veri_10.json`, `veri_100.json`, `veri_1000.json` oluşur.
4) **Uygulamanın başlatılması:** `python main.py`
5) **Birim testleri:** `python tests/birim_testleri.py`
6) **Performans testleri:** `python tests/performans_testleri.py`

## 4. Algoritmik Yaklaşım
Bu bölümde sistemin temel senaryolardaki algoritmik akışı, ilgili veri yapılarıyla birlikte adım adım açıklanmaktadır.

### 4.1 Yeni Rezervasyon Oluşturma
Kullanıcı arayüzden ziyaretçi, alan ve tarihleri seçip 'Rezervasyon Oluştur' butonuna bastığında sistem aşağıdaki adımları izler:
1. **Doğrulama:** Ziyaretçi nesnesine HashMap üzerinden O(1) sürede erişilir; alanın bakım durumu CampSet'e O(1) sorgusuyla teyit edilir.
2. **Çoklu indeksleme:** Yeni Rezervasyon nesnesi `rezervasyon_map`'e (HashMap) eklenirken aynı anda giriş tarihi anahtarıyla BST'ye O(log n) maliyetle insert edilir.
3. **Analitik güncelleme:** İlgili alanın rezervasyon sayısı bir artırılır ve MaxHeap'e push edilir; en popüler alan her zaman tepede kalır.
4. **Güvenlik:** İşlem türü ve hedef ID, geri alma için Stack'e push edilir.
5. **Kalıcılık:** Tüm değişiklikler JSON'a yazılır.

### 4.2 Müsait Parsel Kalmaması ve Bekleme Kuyruğu
İstenen tarih aralığında uygun alan bulunamazsa, ziyaretçi bekleme listesine alınır. Bu işlemde standart Queue yerine PriorityQueue kullanılır:
1. Ziyaretçinin öncelik skoru okunur (Normal=0, VIP=5, Engelli=10).
2. Talep PriorityQueue'ya O(log n) sürede eklenir; max-heap özelliği en yüksek öncelikli kişiyi tepede tutar.
3. Bir parsel boşaldığında `pq_dequeue` ile tepedeki talep çekilerek atama yapılır.
4. Eşit öncelik durumunda 'counter' alanı sayesinde FIFO davranışı korunur; geç gelen bir VIP, daha önce gelen aynı seviyedeki bir VIP'i geçemez.

### 4.3 Mekânsal Hiyerarşi ve Rota Analizi
Kamp Haritası sekmesi iki ayrı veri yapısını birlikte kullanır:
* **Ağaç gezimi (CampTree):** Kök → Bölge → Parsel hiyerarşisi BFS ile gezilerek QTreeWidget üzerinde gösterilir. İşlem O(V+E) sürelidir.
* **Graf çizimi (Graph):** Alanlar düğüm, aralarındaki yollar kenar olarak çember düzeninde QGraphicsScene içine yerleştirilir.
* **Dijkstra ile en kısa yol:** Kullanıcı A→B sorgusu yaptığında `graph_dijkstra` çağrılır. Algoritma şu adımları izler:
  1. Tüm düğümlerin uzaklığı sonsuz, başlangıç düğümünün uzaklığı 0 olarak başlatılır.
  2. Her iterasyonda ziyaret edilmemiş ve en küçük uzaklığa sahip düğüm seçilir.
  3. Bu düğümün komşuları gevşetilir (relax); yeni daha kısa yol bulunursa `prev[]` dizisi güncellenir.
  4. Hedef düğüme ulaşıldığında `prev[]` üzerinden geri yürüyerek yol yeniden inşa edilir.
  * Algoritma C tarafında dizi tabanlı seçim ile çalışır; düğüm sayısı küçük olduğu için heap-tabanlı varyanta gerek duyulmamıştır.

### 4.4 Hatalı İşlemi Geri Alma (Undo)
* **LIFO yaklaşımı:** Personel 'Geri Al' butonuna bastığında, operasyon belleğini tutan Stack üzerinden en üstteki kayıt pop edilir.
* **Ters işlem:** Çekilen komutun türüne göre (örn. `ziyaretci_ekle` → `ziyaretci_sil`) ilgili HashMap, BST ve diğer yapılar bir önceki güvenli durumuna döndürülür.
* **Çoklu geri alma:** Stack boş kalana kadar sırayla geri alma desteklenir.

## 5. Test Senaryoları
### 5.1 Birim Testleri
Tüm veri yapılarının doğruluğu, `tests/birim_testleri.py` içindeki 12 ayrı test sınıfı altında toplam 50'nin üzerinde test senaryosu ile doğrulanmıştır. Testler Python'un standart unittest çerçevesi ile yazılmıştır.

| Test Sınıfı | Veri Yapısı | Doğrulanan Senaryo (Özet) |
| :--- | :--- | :--- |
| **TestHashMap** | HashMap | Ekleme, güncelleme, silme, all_keys/all_values, contains kontrolü |
| **TestBST** | BST | Arama, sıralı dolaşım (inorder), aralık sorgusu, silme |
| **TestLinkedList** | LinkedList | Append, prepend, remove, iter; çift yönlü bağlantı doğrulaması |
| **TestStack** | Stack | LIFO sırası, peek, boş stack hatası |
| **TestQueue** | Queue | FIFO sırası, peek, boş queue hatası |
| **TestPriorityQueue** | PriorityQueue | Öncelik sırası, eşit öncelikte FIFO davranışı |
| **TestMaxHeap** | MaxHeap | En büyük elemanın doğru pop'u, top_k() yıkıcı olmama |
| **TestCampSet** | CampSet | Add/contains/remove, olmayan eleman silme güvenliği |
| **TestGraph** | Graph | Komşuluk, BFS/DFS gezimi, düğüm silme, bağlantısız bileşen |
| **TestMatrix2D** | Matrix2D | Set/get, increment, row_sum/col_sum, sınır dışı kontrol |
| **TestCampTree** | CampTree | Alan ekleme, silme, bölge sorgusu, BFS/DFS, mükerrer ID engeli |
| **TestLinkedListGecmis** | LinkedList | Ziyaretçi geçmişinde LIFO senaryosu (prepend tabanlı) |

Tüm testler başarıyla geçmiş, herhangi bir hata veya başarısızlık (failure) gözlenmemiştir. Bu durum, hem C tarafındaki implementasyonların hem de saf Python yedeğinin davranışsal olarak birbirine denk olduğunu göstermektedir.

### 5.2 Sınır ve Fonksiyonel Senaryolar
Sistemin hata toleransını ve kararlılığını ölçmek için birim testlerin ötesinde, gerçek kullanıcı akışlarını taklit eden sınır (edge case) testleri de manuel olarak koşulmuştur.

#### 5.2.1 Öncelikli Müşteri Ataması (Fonksiyonel)
* **Girdi:** Kamp kapasitesi doluyken sisteme önce Normal, sonra VIP, sonra Engelli statüsünde üç müşterinin bekleme listesine alınması.
* **Adımlar:** Üç talebi sırayla ekle → bir parseli iptal ederek boşalt → atama tetikle.
* **Beklenen:** Atama yapıldığında önce Engelli (öncelik=10), sonra VIP (öncelik=5) atanır; Normal müşteri bekleme listesinde kalır.
* **İlgili veri yapıları:** PriorityQueue, MaxHeap.

#### 5.2.2 Dolu veya Bakımdaki Alana İşlem (Sınır)
* **Girdi:** Yöneticinin 'Bakımda' olarak işaretlediği bir parsele yeni rezervasyon denenmesi.
* **Adımlar:** Arayüzden bakımdaki bir parseli seç → tarih aralığını gir → 'Rezervasyon Oluştur'.
* **Beklenen:** Sistem işlemi reddeder, çökmez, 'Rezervasyon oluşturulamadı. Alan bakımda olabilir.' uyarısı verilir.
* **İlgili veri yapıları:** CampSet, HashMap, Matrix2D.

#### 5.2.3 Seçim Yapılmadan İşlem (Sınır)
* **Girdi:** Hiçbir kayıt seçilmeden 'Sil', 'Güncelle' veya 'Bakıma Al' butonuna basılması.
* **Beklenen:** Sistem NullReference hatasına düşmez, kullanıcıya 'Önce kayıt seçin' uyarısı verir.
* **İlgili veri yapıları:** HashMap (anahtar null geldiği için işlem engellenir).

#### 5.2.4 Dijkstra ile Erişilemeyen Nokta (Sınır)
* **Girdi:** Birbirine kenarla bağlanmamış iki alan arasında yol tarifi istenmesi.
* **Beklenen:** Algoritma sonsuz mesafe döndürür; arayüz 'gidilebilecek bir yol bulunamadı' mesajı gösterir.
* **İlgili veri yapıları:** Graph.

#### 5.2.5 Geri Alma Stack'inin Boş Olması (Sınır)
* **Girdi:** Hiçbir işlem yapılmamışken 'Geri Al' butonuna basılması.
* **Beklenen:** Stack boş olduğu için işlem yapılmaz, durum çubuğunda bilgi mesajı görünür.
* **İlgili veri yapıları:** Stack.

## 6. Performans Karşılaştırmaları
Performans testleri `tests/performans_testleri.py` betiği ile çalıştırılmıştır. Her test üç veri boyutunda (küçük: 10, orta: 100, büyük: 500-1000) tekrarlanmış; ölçüm değerleri en az 1000 tekrar ortalamasına dayanmaktadır. Aşağıdaki tablolarda elde edilen gerçek ölçüm sonuçları yer almaktadır.

### 6.1 Test 1: Array O(n) vs HashMap O(1) — Rezervasyon Arama
Rezervasyon ID'siyle kayıt bulma senaryosunda liste taraması ile HashMap karşılaştırılmıştır.

| Veri Boyutu | Array O(n) | HashMap O(1) | Hız Oranı |
| :--- | :--- | :--- | :--- |
| **10 kayıt** | ≈ 0.25 µs | ≈ 0.30 µs | ≈ 0.8x |
| **100 kayıt** | ≈ 3.44 µs | ≈ 0.31 µs | ≈ 11x |
| **1000 kayıt** | ≈ 14.38 µs | ≈ 0.28 µs | ≈ 51x |

Yorum: Küçük veri kümelerinde (N=10) Array daha hızlı görünmektedir; bunun nedeni hash hesaplama ve fonksiyon çağrı maliyetlerinin baskın olmasıdır. Veri büyüdükçe HashMap'in sabit O(1) erişim avantajı belirginleşir: 1000 kayıtta yaklaşık 51 kat daha hızlıdır. Bu davranış, kuramsal beklentilerle birebir örtüşmektedir.

### 6.2 Test 2: Lineer Arama O(n) vs BST Arama O(log n) — Tarih Sorgusu
Tarih bazlı rezervasyon sorgusunda sıralı liste taraması ile BST karşılaştırılmıştır.

| Veri Boyutu | Lineer O(n) | BST O(log n) | Hız Oranı |
| :--- | :--- | :--- | :--- |
| **10 kayıt** | ≈ 0.29 µs | ≈ 0.24 µs | ≈ 1.2x |
| **100 kayıt** | ≈ 1.33 µs | ≈ 0.42 µs | ≈ 3.1x |
| **1000 kayıt** | ≈ 11.26 µs | ≈ 0.68 µs | ≈ 16.5x |

Yorum: Küçük veri setlerinde fark sınırlıyken, BST'nin avantajı veri büyüdükçe belirginleşmektedir. 1000 kayıtta BST yaklaşık 16 kat daha hızlıdır. Ek olarak BST, aralık sorgusu (`range_query`) işleminde ek döngüye gerek duymadan doğrudan alt ağaç budaması yapabilmektedir; bu, sıralı liste için mümkün olsa da BST'de uygulanması çok daha doğaldır.

### 6.3 Test 3: Bubble Sort O(n²) vs Heap Sort O(n log n)
Rezervasyon sayısına göre alan sıralaması senaryosunda Bubble Sort ile heapq tabanlı Heap Sort karşılaştırılmıştır.

| Veri Boyutu | Bubble Sort O(n²) | Heap Sort O(n log n) | Hız Oranı |
| :--- | :--- | :--- | :--- |
| **10 eleman** | ≈ 8.81 µs | ≈ 5.66 µs | ≈ 1.6x |
| **100 eleman** | ≈ 479.85 µs | ≈ 22.57 µs | ≈ 21x |
| **500 eleman** | ≈ 9 359 µs | ≈ 105.58 µs | ≈ 89x |

Yorum: Bubble Sort'un O(n²) karmaşıklığı 500 elemanda Heap Sort'a göre yaklaşık 89 kat daha yavaş çalışmaktadır. MaxHeap tabanlı `top_k()` yaklaşımı, tüm listeyi sıralamadan yalnızca ilk K elemanı bulabildiği için Raporlar sekmesindeki 'Popüler Alanlar' kartında bu avantaj pratik kazanca dönüşmektedir.

### 6.4 Test 4: Liste O(n) vs CampSet O(1) — Bakım Durumu Kontrolü
Bakımdaki alan ID'sinin var olup olmadığını kontrol etme senaryosunda liste taraması ile küme tabanlı arama karşılaştırılmıştır.

| Veri Boyutu | Liste O(n) | CampSet O(1) | Hız Oranı |
| :--- | :--- | :--- | :--- |
| **10 eleman** | ≈ 0.279 µs | ≈ 0.064 µs | ≈ 4x |
| **100 eleman** | ≈ 1.506 µs | ≈ 0.061 µs | ≈ 25x |
| **1000 eleman** | ≈ 14.437 µs | ≈ 0.067 µs | ≈ 217x |

Yorum: CampSet, hash tabanlı yapısı sayesinde veri boyutundan bağımsız sabit O(1) kontrol süresi sağlamaktadır. 1000 elemanda liste taramasından yaklaşık 217 kat daha hızlıdır. Bakım durumu kontrolü her rezervasyon talebinde çağrıldığı için, bu fark sistem genelinde kümülatif olarak büyük kazanç yaratmaktadır.

### 6.5 Genel Değerlendirme
Dört performans testinin tamamı, kuramsal karmaşıklık sınıflarının pratikte de geçerli olduğunu göstermiştir. Sonuçlar aşağıdaki ilkeleri doğrulamıştır:
* Hash tabanlı yapılar (HashMap, CampSet) küçük N için ek maliyet getirse de N büyüdükçe büyük avantaj sağlar.
* Logaritmik karmaşıklık (BST), lineer aramaya göre veri büyüdükçe orantılı şekilde hızlanır.
* Karesel karmaşıklık (Bubble Sort) küçük N'lerde tolere edilebilir, ancak N=500'de bile büyük dezavantaja dönüşür.
* Veri yapısı seçimi, yalnızca işlevsellik değil ölçeklenebilirlik açısından da kritik bir karardır.

## 7. Sonuç ve Değerlendirme
### 7.1 Sonuç
Geliştirilen 'Kamp Alanı Rezervasyon Yönetim Sistemi' projesi, başlangıçta belirlenen tüm hedeflere başarıyla ulaşmıştır. Ziyaretçi yönetimi, alan tahsisi, öncelikli bekleme listesi, kamp haritası üzerinde Dijkstra ile yön bulma ve geri alma mekanizması gibi karmaşık işlemler, doğru veri yapıları seçilerek optimize edilmiş ve performanslı çalışan bir yapıya kavuşturulmuştur. PyQt6 ile hazırlanan arayüz sayesinde BFS/DFS gezimleri, BST aralık sorguları ve PriorityQueue atamaları kullanıcı tarafından görsel olarak takip edilebilir hale gelmiştir.
11 farklı veri yapısının tamamı; hem birim testlerle hem de gerçek veri kümeleri üzerindeki performans testleriyle doğrulanmıştır. C ve Python katmanlarının ctypes üzerinden köprülenmesi, performansı korurken geliştirme hızını artıran bir yaklaşım olarak değerli bir mühendislik tecrübesi sağlamıştır.

### 7.2 Güçlü Yönler
* **Modüler mimari:** arayüz, iş mantığı ve veri yapıları net bir şekilde ayrılmıştır.
* **Hibrit C/Python yaklaşımı:** hız ve esneklik bir arada sunulmuştur.
* **Otomatik yedek (fallback):** DLL yokken saf Python katmanına geçiş, taşınabilirliği artırır.
* **Kapsamlı test altyapısı:** 12 birim test sınıfı, 5 sınır senaryo, 4 performans testi.
* **Veri yapılarının çeşitliliği:** yönergedeki tüm 11 veri yapısı projeye organik biçimde yerleştirilmiştir.

### 7.3 Sınırlılıklar
* JSON tabanlı kalıcılık eşzamanlı çok kullanıcılı senaryolar için uygun değildir.
* BST dengelenmediği için en kötü durumda O(n) davranışa düşebilir (AVL veya Red-Black ağacıyla geliştirilebilir).
* Dijkstra implementasyonu dizi tabanlıdır; çok büyük graflarda min-heap tabanlı sürüm tercih edilmelidir.
* Rezervasyon çakışma kontrolü şu an alan-tarih bazlıdır; saat bazlı ince ayar yapılmamıştır.

### 7.4 Gelecek Çalışmalar
* SQLite veya başka bir hafif veritabanına geçiş ile çok kullanıcılı destek.
* AVL/Red-Black ağaç ile BST'nin dengelenmesi.
* Dijkstra'nın min-heap tabanlı O((V+E) log V) sürümüne geçilmesi.
* Kullanıcı rolleri (yönetici/personel/müşteri) ve oturum yönetimi.
* Web tabanlı dashboard ile uzaktan izleme ve raporlama.

## 8. Kaynakça
[1] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms, 3rd ed. Cambridge, MA, USA: MIT Press, 2009.
[2] M. T. Goodrich, R. Tamassia, and M. H. Goldwasser, Data Structures and Algorithms in Python. Hoboken, NJ, USA: John Wiley & Sons, 2013.
[3] Python Software Foundation, "Python 3.12 Documentation," [Online]. Available: https://docs.python.org/3/. [Accessed: May 12, 2026].
[4] Riverbank Computing, "PyQt6 Reference Guide," PyQt6 Documentation. [Online]. Available: https://www.riverbankcomputing.com/static/Docs/PyQt6/. [Accessed: May 12, 2026].
[5] Python Software Foundation, "json — JSON encoder and decoder," [Online]. Available: https://docs.python.org/3/library/json.html. [Accessed: May 12, 2026].
[6] Python Software Foundation, "heapq — Heap queue algorithm," [Online]. Available: https://docs.python.org/3/library/heapq.html. [Accessed: May 12, 2026].
[7] Python Software Foundation, "ctypes — A foreign function library for Python," [Online]. Available: https://docs.python.org/3/library/ctypes.html. [Accessed: May 12, 2026].
[8] R. Sedgewick and K. Wayne, Algorithms, 4th ed. Boston, MA, USA: Addison-Wesley Professional, 2011.
[9] I. Sommerville, Software Engineering, 10th ed. Boston, MA, USA: Pearson, 2015.
[10] E. W. Dijkstra, "A note on two problems in connexion with graphs," Numerische Mathematik, vol. 1, no. 1, pp. 269–271, 1959.
