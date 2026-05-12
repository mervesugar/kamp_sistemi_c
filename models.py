"""
Veri Modelleri — Kamp Alanı Rezervasyon Sistemi
"""
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Ziyaretci:
    ziyaretci_id: str
    ad: str
    soyad: str
    telefon: str
    oncelik: int = 0        # 0=Normal, 5=VIP, 10=Engelli

    @property
    def tam_ad(self):
        return f"{self.ad} {self.soyad}"

    @property
    def oncelik_adi(self):
        if self.oncelik >= 10:
            return "Engelli"
        elif self.oncelik >= 5:
            return "VIP"
        return "Normal"

    def to_dict(self):
        return {
            "ziyaretci_id": self.ziyaretci_id,
            "ad": self.ad,
            "soyad": self.soyad,
            "telefon": self.telefon,
            "oncelik": self.oncelik,
        }

    @staticmethod
    def from_dict(d):
        return Ziyaretci(**d)


@dataclass
class Alan:
    alan_id: str
    alan_tipi: str          # Çadır, Karavan, Bungalov
    kapasite: int
    fiyat: float
    rezervasyon_sayisi: int = 0
    bakimda: bool = False

    @property
    def durum(self):
        return "Bakımda" if self.bakimda else "Müsait"

    def to_dict(self):
        return {
            "alan_id": self.alan_id,
            "alan_tipi": self.alan_tipi,
            "kapasite": self.kapasite,
            "fiyat": self.fiyat,
            "rezervasyon_sayisi": self.rezervasyon_sayisi,
            "bakimda": self.bakimda,
        }

    @staticmethod
    def from_dict(d):
        return Alan(**d)


@dataclass
class Ekipman:
    ekipman_id: str
    ad: str
    toplam_stok: int
    mevcut_stok: int

    @property
    def odunc_sayisi(self):
        return self.toplam_stok - self.mevcut_stok

    def to_dict(self):
        return {
            "ekipman_id": self.ekipman_id,
            "ad": self.ad,
            "toplam_stok": self.toplam_stok,
            "mevcut_stok": self.mevcut_stok,
        }

    @staticmethod
    def from_dict(d):
        return Ekipman(**d)


@dataclass
class Rezervasyon:
    rezervasyon_id: str
    ziyaretci_id: str
    alan_id: str
    giris_tarihi: str       # "YYYY-MM-DD"
    cikis_tarihi: str
    toplam_ucret: float = 0.0
    aktif: bool = True

    def to_dict(self):
        return {
            "rezervasyon_id": self.rezervasyon_id,
            "ziyaretci_id": self.ziyaretci_id,
            "alan_id": self.alan_id,
            "giris_tarihi": self.giris_tarihi,
            "cikis_tarihi": self.cikis_tarihi,
            "toplam_ucret": self.toplam_ucret,
            "aktif": self.aktif,
        }

    @staticmethod
    def from_dict(d):
        return Rezervasyon(**d)
