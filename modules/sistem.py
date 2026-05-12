"""
Sistem Motoru — tüm iş mantığı burada.
GUI ve testler bu modülü kullanır.
"""
import json
import os
import sys
import uuid
from datetime import date, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from models import Ziyaretci, Alan, Ekipman, Rezervasyon
from data_structures.structures import (
    HashMap, BST, LinkedList, Stack, Queue,
    PriorityQueue, MaxHeap, CampSet, Graph, Matrix2D, CampTree
)

KAYIT_DIR = os.path.join(ROOT, "kayitlar")
ALAN_TIPLERI = ["Çadır", "Karavan", "Bungalov"]
GUNLER = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]


class KampSistemi:
    def __init__(self):
        # ── Veri yapıları ──
        self.ziyaretci_map = HashMap()      # id → Ziyaretci
        self.alan_map = HashMap()           # id → Alan
        self.ekipman_map = HashMap()        # id → Ekipman
        self.rezervasyon_map = HashMap()    # id → Rezervasyon

        self.rezervasyon_bst = BST()        # tarih → rezervasyon_id
        self.gecmis_listesi = LinkedList()  # (ziyaretci_id, rezervasyon_id)

        self.islem_stack = Stack()          # geri alma
        self.bekleme_kuyrugu = Queue()      # bekleyen talep
        self.oncelik_kuyrugu = PriorityQueue()

        self.popülerlik_heap = MaxHeap()    # (sayı, alan_id)
        self.bakim_set = CampSet()          # bakımdaki alan_id'ler

        self.alan_grafi = Graph()           # komşu alanlar
        self.doluluk_matrisi = Matrix2D(3, 7)  # tip × gün
        self.mekan_agaci = CampTree()       # mekansal hiyerarşi (11. yapı)

        os.makedirs(KAYIT_DIR, exist_ok=True)
        self._yukle()
        self._heap_yenile()

    # ZİYARETÇİ

    def ziyaretci_ekle(self, ad, soyad, telefon, oncelik=0):
        zid = "Z" + str(uuid.uuid4())[:6].upper()
        z = Ziyaretci(zid, ad, soyad, telefon, oncelik)
        self.ziyaretci_map.insert(zid, z)
        self.islem_stack.push(("ziyaretci_sil", zid))
        self._kaydet()
        return z

    def ziyaretci_guncelle(self, zid, ad=None, soyad=None, telefon=None, oncelik=None):
        z = self.ziyaretci_map.get(zid)
        if not z:
            return False
        eski = Ziyaretci(z.ziyaretci_id, z.ad, z.soyad, z.telefon, z.oncelik)
        if ad: z.ad = ad
        if soyad: z.soyad = soyad
        if telefon: z.telefon = telefon
        if oncelik is not None: z.oncelik = oncelik
        self.ziyaretci_map.insert(zid, z)
        self.islem_stack.push(("ziyaretci_geri", eski))
        self._kaydet()
        return True

    def ziyaretci_sil(self, zid):
        z = self.ziyaretci_map.get(zid)
        if not z:
            return False
        self.islem_stack.push(("ziyaretci_geri", z))
        self.ziyaretci_map.delete(zid)
        self._kaydet()
        return True

    def tum_ziyaretciler(self):
        return self.ziyaretci_map.all_values()

    def ziyaretci_bul(self, zid):
        return self.ziyaretci_map.get(zid)

    # ALAN

    def alan_ekle(self, alan_tipi, kapasite, fiyat):
        aid = "A" + str(uuid.uuid4())[:6].upper()
        a = Alan(aid, alan_tipi, kapasite, fiyat)
        self.alan_map.insert(aid, a)
        self.alan_grafi.add_node(aid)
        self.mekan_agaci.alan_ekle(aid, alan_tipi)   # ağaca ekle
        self.islem_stack.push(("alan_sil", aid))
        self._kaydet()
        self.bekleme_listesini_isle()
        return a

    def alan_sil(self, aid):
        a = self.alan_map.get(aid)
        if not a:
            return False
        self.islem_stack.push(("alan_geri", a))
        self.alan_map.delete(aid)
        self.alan_grafi.remove_node(aid)
        self.mekan_agaci.alan_sil(aid)   # ağaçtan kaldır
        self.bakim_set.remove(aid)
        self._kaydet()
        return True

    def bakima_al(self, aid):
        a = self.alan_map.get(aid)
        if not a:
            return False
        a.bakimda = True
        self.bakim_set.add(aid)
        self._kaydet()
        return True

    def bakimdan_cikart(self, aid):
        a = self.alan_map.get(aid)
        if not a:
            return False
        a.bakimda = False
        self.bakim_set.remove(aid)
        self._kaydet()
        self.bekleme_listesini_isle()
        return True

    def tum_alanlar(self):
        return self.alan_map.all_values()

    def alan_bul(self, aid):
        return self.alan_map.get(aid)

    def musait_alanlar(self):
        return [a for a in self.tum_alanlar() if not a.bakimda]

    def yol_tarifi_al(self, baslangic_id, bitis_id):
        return self.alan_grafi.dijkstra(baslangic_id, bitis_id)

    def komsu_ekle(self, aid1, aid2, mesafe=1):
        a1 = self.alan_map.get(aid1)
        a2 = self.alan_map.get(aid2)
        if a1 and a2:
            self.alan_grafi.add_edge(aid1, aid2, mesafe)
            self._kaydet()
            return True
        return False

    # EKİPMAN

    def ekipman_ekle(self, ad, stok):
        eid = "E" + str(uuid.uuid4())[:6].upper()
        e = Ekipman(eid, ad, stok, stok)
        self.ekipman_map.insert(eid, e)
        self.islem_stack.push(("ekipman_sil", eid))
        self._kaydet()
        return e

    def ekipman_odunc_ver(self, eid, adet=1):
        e = self.ekipman_map.get(eid)
        if not e or e.mevcut_stok < adet:
            return False
        e.mevcut_stok -= adet
        self.islem_stack.push(("ekipman_iade", (eid, adet)))
        self._kaydet()
        return True

    def ekipman_iade_al(self, eid, adet=1):
        e = self.ekipman_map.get(eid)
        if not e:
            return False
        e.mevcut_stok = min(e.toplam_stok, e.mevcut_stok + adet)
        self._kaydet()
        return True

    def ekipman_sil(self, eid):
        e = self.ekipman_map.get(eid)
        if not e:
            return False
        self.islem_stack.push(("ekipman_geri", e))
        self.ekipman_map.delete(eid)
        self._kaydet()
        return True

    def tum_ekipmanlar(self):
        return self.ekipman_map.all_values()

    # REZERVASYON

    def rezervasyon_olustur(self, ziyaretci_id, alan_id, giris, cikis):
        z = self.ziyaretci_map.get(ziyaretci_id)
        a = self.alan_map.get(alan_id)
        if not z or not a or a.bakimda:
            return None
        
        # Kapasite kontrolü
        if a.rezervasyon_sayisi >= a.kapasite:
            return "DOLU"

        rid = "R" + str(uuid.uuid4())[:8].upper()
        try:
            g = datetime.strptime(giris, "%Y-%m-%d").date()
            c = datetime.strptime(cikis, "%Y-%m-%d").date()
            gun_sayisi = max(1, (c - g).days)
        except Exception:
            gun_sayisi = 1

        ucret = gun_sayisi * a.fiyat
        r = Rezervasyon(rid, ziyaretci_id, alan_id, giris, cikis, ucret)

        self.rezervasyon_map.insert(rid, r)
        self.rezervasyon_bst.insert(giris, rid)
        self.gecmis_listesi.prepend((ziyaretci_id, rid))

        a.rezervasyon_sayisi += 1
        self.islem_stack.push(("rezervasyon_iptal", rid))

        # Doluluk matrisi güncelle
        tip_idx = ALAN_TIPLERI.index(a.alan_tipi) if a.alan_tipi in ALAN_TIPLERI else 0
        try:
            gun_idx = g.weekday()
            self.doluluk_matrisi.increment(tip_idx, gun_idx)
        except Exception:
            pass

        self._heap_yenile()
        self._kaydet()
        return r

    def rezervasyon_iptal(self, rid):
        r = self.rezervasyon_map.get(rid)
        if not r or not r.aktif:
            return False
        r.aktif = False
        a = self.alan_map.get(r.alan_id)
        if a:
            a.rezervasyon_sayisi = max(0, a.rezervasyon_sayisi - 1)
        self.islem_stack.push(("rezervasyon_geri_al", rid))
        self._heap_yenile()
        self._kaydet()
        
        # Biri iptal edince bekleme listesini kontrol et
        self.bekleme_listesini_isle()
        return True

    def son_islemi_geri_al(self):
        if self.islem_stack.is_empty():
            return "Geri alınacak işlem yok."
        islem, veri = self.islem_stack.pop()

        if islem == "ziyaretci_sil":
            self.ziyaretci_map.delete(veri)
            self._kaydet()
            return f"Ziyaretçi silindi: {veri}"
        elif islem == "ziyaretci_geri":
            self.ziyaretci_map.insert(veri.ziyaretci_id, veri)
            self._kaydet()
            return f"Ziyaretçi geri yüklendi: {veri.tam_ad}"
        elif islem == "alan_sil":
            self.alan_map.delete(veri)
            self._kaydet()
            return f"Alan silindi: {veri}"
        elif islem == "alan_geri":
            self.alan_map.insert(veri.alan_id, veri)
            self.alan_grafi.add_node(veri.alan_id)
            self.mekan_agaci.alan_ekle(veri.alan_id, veri.alan_tipi)  # ağaca geri yükle
            self._kaydet()
            return f"Alan geri yüklendi: {veri.alan_id}"
        elif islem == "rezervasyon_iptal":
            r = self.rezervasyon_map.get(veri)
            if r:
                r.aktif = False
                a = self.alan_map.get(r.alan_id)
                if a:
                    a.rezervasyon_sayisi = max(0, a.rezervasyon_sayisi - 1)
            self._kaydet()
            return f"Rezervasyon iptal edildi: {veri}"
        elif islem == "rezervasyon_geri_al":
            r = self.rezervasyon_map.get(veri)
            if r:
                r.aktif = True
                a = self.alan_map.get(r.alan_id)
                if a:
                    a.rezervasyon_sayisi += 1
            self._kaydet()
            return f"Rezervasyon geri alındı: {veri}"
        elif islem == "ekipman_iade":
            eid, adet = veri
            e = self.ekipman_map.get(eid)
            if e:
                e.mevcut_stok = min(e.toplam_stok, e.mevcut_stok + adet)
            self._kaydet()
            return f"Ekipman iade geri alındı: {eid}"
        elif islem == "ekipman_sil":
            self.ekipman_map.delete(veri)
            self._kaydet()
            return f"Ekipman silindi: {veri}"
        elif islem == "ekipman_geri":
            self.ekipman_map.insert(veri.ekipman_id, veri)
            self._kaydet()
            return f"Ekipman geri yüklendi: {veri.ad}"
        return "Bilinmeyen işlem."

    def tum_rezervasyonlar(self, sadece_aktif=False):
        rvs = self.rezervasyon_map.all_values()
        if sadece_aktif:
            rvs = [r for r in rvs if r.aktif]
        return rvs

    def tarih_araligi_rezervasyonlar(self, baslangic, bitis):
        """BST range_query kullanarak tarih aralığındaki rezervasyonlar."""
        pairs = self.rezervasyon_bst.range_query(baslangic, bitis)
        result = []
        for _, rid in pairs:
            r = self.rezervasyon_map.get(rid)
            if r:
                result.append(r)
        return result

    # BEKLEME LİSTESİ (Priority Queue)

    def bekleme_listesine_ekle(self, ziyaretci_id, alan_tipi, giris, cikis):
        z = self.ziyaretci_map.get(ziyaretci_id)
        if not z:
            return False
        
        talep = {
            "id": str(uuid.uuid4())[:6].upper(),
            "ziyaretci_id": ziyaretci_id,
            "alan_tipi": alan_tipi,
            "giris": giris,
            "cikis": cikis,
            "eklenme_zamani": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.oncelik_kuyrugu.enqueue(talep, z.oncelik)
        self._kaydet() # Kuyruğu da kaydetmek istersen json'a eklenebilir, şimdilik memory'de
        return True

    def bekleme_listesini_isle(self):
        bekleyenler = self.oncelik_kuyrugu.to_list()
        islem_yapildi = False
        
        for talep in bekleyenler:
            # Bu talep için uygun alan var mı?
            uygun_alan = None
            for a in self.musait_alanlar():
                if a.alan_tipi == talep["alan_tipi"] and a.rezervasyon_sayisi < a.kapasite:
                    uygun_alan = a
                    break
            
            if uygun_alan:
                r = self.rezervasyon_olustur(talep["ziyaretci_id"], uygun_alan.alan_id, talep["giris"], talep["cikis"])
                if r and r != "DOLU":
                    self.oncelik_kuyrugu.remove_item(talep)
                    islem_yapildi = True
        return islem_yapildi

    # RAPORLAR / İSTATİSTİK

    def istatistikler(self):
        rezervasyonlar = self.tum_rezervasyonlar()
        aktif = [r for r in rezervasyonlar if r.aktif]
        toplam_gelir = sum(r.toplam_ucret for r in aktif)
        return {
            "toplam_ziyaretci": len(self.ziyaretci_map),
            "toplam_alan": len(self.alan_map),
            "toplam_ekipman": len(self.ekipman_map),
            "toplam_rezervasyon": len(rezervasyonlar),
            "aktif_rezervasyon": len(aktif),
            "toplam_gelir": toplam_gelir,
            "bakimdaki_alan": len(self.bakim_set),
        }

    def bolge_raporu(self) -> dict:
        """
        CampTree kullanarak bölge bazlı alan raporu üretir.

        Döndürür:
        {
            "Çadır Bölgesi":    [{"alan_id":..., "kapasite":..., "fiyat":..., "bakimda":...}, ...],
            "Karavan Bölgesi":  [...],
            "Bungalov Bölgesi": [...],
        }
        """
        tip_map = {
            "Çadır Bölgesi":    "Çadır",
            "Karavan Bölgesi":  "Karavan",
            "Bungalov Bölgesi": "Bungalov",
        }
        rapor = {}
        for bolge_adi, alan_id_listesi in self.mekan_agaci.tum_bolgeler().items():
            alanlar = []
            for aid in alan_id_listesi:
                a = self.alan_map.get(aid)
                if a:
                    alanlar.append({
                        "alan_id":          a.alan_id,
                        "kapasite":         a.kapasite,
                        "fiyat":            a.fiyat,
                        "rezervasyon_sayisi": a.rezervasyon_sayisi,
                        "bakimda":          a.bakimda,
                    })
            rapor[bolge_adi] = alanlar
        return rapor

    def mekan_hiyerarsisi(self) -> list:
        """
        CampTree.hiyerarsi_yazdir() çağrısıyla ağaç yapısını
        metin satırları listesi olarak döndürür.
        Raporlama ekranında veya terminalde göstermek için kullanılır.
        """
        return self.mekan_agaci.hiyerarsi_yazdir()

    def populer_alanlar(self, k=5):
        """MaxHeap kullanarak en popüler k alanı döndürür."""
        heap = MaxHeap()
        for a in self.tum_alanlar():
            heap.push(a.rezervasyon_sayisi, a.alan_id)
        top = heap.top_k(k)
        result = []
        for sayi, aid in top:
            a = self.alan_map.get(aid)
            if a:
                result.append((a, sayi))
        return result

    def _heap_yenile(self):
        self.popülerlik_heap = MaxHeap()
        for a in self.tum_alanlar():
            self.popülerlik_heap.push(a.rezervasyon_sayisi, a.alan_id)

    # ÖRNEK VERİ

    def ornek_veri_yukle(self):
        """Demo amaçlı örnek veriler."""
        if len(self.ziyaretci_map) > 0:
            return  # Zaten veri var

        # Ziyaretçiler
        z1 = self.ziyaretci_ekle("Ahmet", "Yılmaz", "0532-111-1111", 0)
        z2 = self.ziyaretci_ekle("Fatma", "Kaya", "0533-222-2222", 5)     # VIP
        z3 = self.ziyaretci_ekle("Mehmet", "Demir", "0534-333-3333", 10)  # Engelli
        z4 = self.ziyaretci_ekle("Ayşe", "Çelik", "0535-444-4444", 0)
        z5 = self.ziyaretci_ekle("Ali", "Şahin", "0536-555-5555", 5)      # VIP

        # Alanlar (10 adet)
        a1 = self.alan_ekle("Çadır", 4, 150.0)
        a2 = self.alan_ekle("Çadır", 6, 200.0)
        a3 = self.alan_ekle("Çadır", 3, 120.0)
        a4 = self.alan_ekle("Karavan", 4, 350.0)
        a5 = self.alan_ekle("Karavan", 6, 450.0)
        a6 = self.alan_ekle("Karavan", 2, 300.0)
        a7 = self.alan_ekle("Bungalov", 2, 600.0)
        a8 = self.alan_ekle("Bungalov", 4, 800.0)
        a9 = self.alan_ekle("Bungalov", 3, 700.0)
        a10 = self.alan_ekle("Çadır", 8, 250.0)

        import random
        # Graf komşulukları (halka + çapraz bağlantılar)
        self.alan_grafi.add_edge(a1.alan_id, a2.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a2.alan_id, a3.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a3.alan_id, a4.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a4.alan_id, a5.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a5.alan_id, a6.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a6.alan_id, a7.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a7.alan_id, a8.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a8.alan_id, a9.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a9.alan_id, a10.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a10.alan_id, a1.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a1.alan_id, a5.alan_id, random.randint(0, 300))
        self.alan_grafi.add_edge(a3.alan_id, a7.alan_id, random.randint(0, 300))

        # Bakım
        self.bakima_al(a8.alan_id)

        # Ekipmanlar
        self.ekipman_ekle("Çadır (2 Kişilik)", 10)
        self.ekipman_ekle("Uyku Tulumu", 20)
        self.ekipman_ekle("Kamp Sandalyesi", 15)
        self.ekipman_ekle("Kamp Masası", 8)
        self.ekipman_ekle("Fener", 25)

        # Rezervasyonlar
        self.rezervasyon_olustur(z1.ziyaretci_id, a1.alan_id, "2025-06-01", "2025-06-05")
        self.rezervasyon_olustur(z2.ziyaretci_id, a4.alan_id, "2025-06-10", "2025-06-15")
        self.rezervasyon_olustur(z3.ziyaretci_id, a7.alan_id, "2025-06-20", "2025-06-22")
        self.rezervasyon_olustur(z4.ziyaretci_id, a2.alan_id, "2025-07-01", "2025-07-07")
        self.rezervasyon_olustur(z5.ziyaretci_id, a5.alan_id, "2025-07-10", "2025-07-12")
        self.rezervasyon_olustur(z1.ziyaretci_id, a9.alan_id, "2025-07-20", "2025-07-25")

    # JSON KAYIT / YÜKLEME

    def _graf_adj_dict(self):
        """Graf komşuluk bilgisini JSON'a uygun dict olarak üretir (C ve Python uyumlu)."""
        if hasattr(self.alan_grafi, '_adj'):
            return self.alan_grafi._adj
        # C backend — all_nodes / neighbors ile oluştur
        adj = {}
        for node in self.alan_grafi.all_nodes():
            adj[node] = {}
            for nb in self.alan_grafi.neighbors(node):
                adj[node][nb] = 1  # ağırlık bilgisi C'den alınamıyorsa varsayılan 1
        return adj

    def _kaydet(self):
        os.makedirs(KAYIT_DIR, exist_ok=True)
        try:
            with open(os.path.join(KAYIT_DIR, "ziyaretciler.json"), "w", encoding="utf-8") as f:
                json.dump([z.to_dict() for z in self.tum_ziyaretciler()], f, ensure_ascii=False, indent=2)
            with open(os.path.join(KAYIT_DIR, "alanlar.json"), "w", encoding="utf-8") as f:
                json.dump([a.to_dict() for a in self.tum_alanlar()], f, ensure_ascii=False, indent=2)
            with open(os.path.join(KAYIT_DIR, "ekipmanlar.json"), "w", encoding="utf-8") as f:
                json.dump([e.to_dict() for e in self.tum_ekipmanlar()], f, ensure_ascii=False, indent=2)
            with open(os.path.join(KAYIT_DIR, "rezervasyonlar.json"), "w", encoding="utf-8") as f:
                json.dump([r.to_dict() for r in self.tum_rezervasyonlar()], f, ensure_ascii=False, indent=2)
            with open(os.path.join(KAYIT_DIR, "graf_yollari.json"), "w", encoding="utf-8") as f:
                json.dump(self._graf_adj_dict(), f, ensure_ascii=False, indent=2)
        except Exception as ex:
            print(f"Kayıt hatası: {ex}")

    def _yukle(self):
        def _oku(dosya):
            yol = os.path.join(KAYIT_DIR, dosya)
            if os.path.exists(yol):
                try:
                    with open(yol, encoding="utf-8") as f:
                        icerik = f.read().strip()
                        if not icerik:
                            return [] if dosya != "graf_yollari.json" else {}
                        return json.loads(icerik)
                except (json.JSONDecodeError, ValueError):
                    return [] if dosya != "graf_yollari.json" else {}
            return [] if dosya != "graf_yollari.json" else {}

        for d in _oku("ziyaretciler.json"):
            z = Ziyaretci.from_dict(d)
            self.ziyaretci_map.insert(z.ziyaretci_id, z)

        for d in _oku("alanlar.json"):
            a = Alan.from_dict(d)
            self.alan_map.insert(a.alan_id, a)
            self.alan_grafi.add_node(a.alan_id)
            self.mekan_agaci.alan_ekle(a.alan_id, a.alan_tipi)  # ağaca yükle
            if a.bakimda:
                self.bakim_set.add(a.alan_id)

        for d in _oku("ekipmanlar.json"):
            e = Ekipman.from_dict(d)
            self.ekipman_map.insert(e.ekipman_id, e)

        for d in _oku("rezervasyonlar.json"):
            r = Rezervasyon.from_dict(d)
            self.rezervasyon_map.insert(r.rezervasyon_id, r)
            self.rezervasyon_bst.insert(r.giris_tarihi, r.rezervasyon_id)

        graf_data = _oku("graf_yollari.json")
        if isinstance(graf_data, dict):
            eklenen = set()
            for u, komsular in graf_data.items():
                if isinstance(komsular, dict):
                    for v, w in komsular.items():
                        kenar = tuple(sorted([u, v]))
                        if kenar not in eklenen:
                            self.alan_grafi.add_edge(u, v, int(w))
                            eklenen.add(kenar)