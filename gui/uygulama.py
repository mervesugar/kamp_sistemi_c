"""
Kamp Alanı Rezervasyon Sistemi — PyQt6 GUI
BMT210 Veri Yapıları — Gazi Üniversitesi 2026

Sekmeler:
  1. Ziyaretçiler
  2. Alanlar
  3. Rezervasyonlar
  4. Ekipman
  5. Raporlar
  6. Kamp Haritası  ← CampTree (11. veri yapısı)
"""
import sys
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from modules.sistem import KampSistemi, ALAN_TIPLERI, GUNLER

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox,
    QDoubleSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QTextEdit, QMessageBox,
    QFrame, QSplitter, QScrollArea, QDateEdit, QSlider,
    QTreeWidget, QTreeWidgetItem, QGraphicsScene, QGraphicsView
)
from PyQt6.QtCore import Qt, QDate, QTimer, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QBrush, QPainter, QPen

YESIL       = "#2d6a4f"
YESIL_ACIK  = "#52b788"
YESIL_BG    = "#d8f3dc"
KREM        = "#fefae0"
TURUNCU     = "#e76f51"
GOLGELI     = "#b7e4c7"
METIN       = "#1b1b1b"
GRIDE       = "#f0f0f0"
BEYAZ       = "#ffffff"
KIRMIZI     = "#c0392b"
MAVI        = "#2980b9"


def stil():
    return f"""
    QMainWindow, QWidget {{
        background-color: {KREM};
        color: {METIN};
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 13px;
    }}
    QTabWidget::pane {{
        border: 2px solid {YESIL};
        border-radius: 6px;
        background: {BEYAZ};
    }}
    QTabBar::tab {{
        background: {GRIDE};
        color: {METIN};
        padding: 10px 22px;
        margin-right: 3px;
        border-radius: 6px 6px 0 0;
        font-weight: bold;
        font-size: 13px;
    }}
    QTabBar::tab:selected {{
        background: {YESIL};
        color: {BEYAZ};
    }}
    QTabBar::tab:hover:!selected {{
        background: {GOLGELI};
    }}
    QPushButton {{
        background-color: {YESIL};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 18px;
        font-weight: bold;
        font-size: 13px;
    }}
    QPushButton:hover {{
        background-color: {YESIL_ACIK};
    }}
    QPushButton:pressed {{
        background-color: #1b4332;
    }}
    QPushButton#btn_red {{
        background-color: {KIRMIZI};
    }}
    QPushButton#btn_red:hover {{
        background-color: #e74c3c;
    }}
    QPushButton#btn_orange {{
        background-color: {TURUNCU};
    }}
    QPushButton#btn_orange:hover {{
        background-color: #f4a261;
    }}
    QPushButton#btn_blue {{
        background-color: {MAVI};
    }}
    QPushButton#btn_blue:hover {{
        background-color: #3498db;
    }}
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
        border: 2px solid {GOLGELI};
        border-radius: 6px;
        padding: 6px 10px;
        background: {BEYAZ};
        font-size: 13px;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
    QDoubleSpinBox:focus, QDateEdit:focus {{
        border-color: {YESIL};
    }}
    QTableWidget {{
        border: 1px solid {GOLGELI};
        border-radius: 6px;
        gridline-color: {GRIDE};
        background: {BEYAZ};
        font-size: 12px;
    }}
    QHeaderView::section {{
        background-color: {YESIL};
        color: white;
        padding: 8px;
        font-weight: bold;
        border: none;
    }}
    QTableWidget::item:selected {{
        background-color: {YESIL_BG};
        color: {METIN};
    }}
    QGroupBox {{
        border: 2px solid {GOLGELI};
        border-radius: 8px;
        margin-top: 14px;
        padding: 10px;
        font-weight: bold;
        background: {BEYAZ};
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 5px;
        color: {YESIL};
        font-size: 13px;
    }}
    QTextEdit {{
        background: #1e1e1e;
        color: #d4edda;
        font-family: 'Consolas', monospace;
        font-size: 12px;
        border-radius: 6px;
        border: 1px solid {YESIL};
    }}
    QScrollBar:vertical {{
        border: none;
        background: {GRIDE};
        width: 10px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {YESIL_ACIK};
        border-radius: 5px;
    }}
    """


def tablo_olustur(basliklar):
    t = QTableWidget()
    t.setColumnCount(len(basliklar))
    t.setHorizontalHeaderLabels(basliklar)
    t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    t.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    t.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
    t.setAlternatingRowColors(True)
    t.verticalHeader().setVisible(False)
    return t


def satir_ekle(tablo, degerler, renkler=None):
    row = tablo.rowCount()
    tablo.insertRow(row)
    for col, val in enumerate(degerler):
        item = QTableWidgetItem(str(val))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        if renkler and col < len(renkler) and renkler[col]:
            item.setForeground(QColor(renkler[col]))
        tablo.setItem(row, col, item)


def bilgi_kutusu(parent, baslik, mesaj):
    QMessageBox.information(parent, baslik, mesaj)


def hata_kutusu(parent, mesaj):
    QMessageBox.critical(parent, "Hata", mesaj)


def onay_kutusu(parent, mesaj):
    reply = QMessageBox.question(
        parent, "Onay", mesaj,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes


class BarChartWidget(QWidget):
    def __init__(self, title, labels, data1, data1_label, data2, data2_label):
        super().__init__()
        self.title = title
        self.labels = labels
        self.data1 = data1
        self.data1_label = data1_label
        self.data2 = data2
        self.data2_label = data2_label
        self.setMinimumHeight(280)
        self.setMinimumWidth(300)

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QColor, QFont, QPen
        from PyQt6.QtCore import Qt, QRectF
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Arka plan
        painter.fillRect(0, 0, w, h, QColor(BEYAZ))
        painter.setPen(QPen(QColor(GOLGELI), 1))
        painter.drawRect(0, 0, w-1, h-1)
        
        # Başlık
        painter.setPen(QPen(QColor(METIN)))
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        painter.drawText(0, 10, w, 25, Qt.AlignmentFlag.AlignCenter, self.title)
        
        if not self.data1 or not self.data2:
            return
            
        max_val = max(max(self.data1), max(self.data2))
        if max_val <= 0: max_val = 1
        
        pad_top = 60
        pad_bot = 40
        pad_left = 60
        pad_right = 20
        
        graph_w = w - pad_left - pad_right
        graph_h = h - pad_top - pad_bot
        
        # Eksenler
        painter.setPen(QPen(QColor("#aaaaaa"), 2))
        painter.drawLine(pad_left, pad_top, pad_left, h - pad_bot)
        painter.drawLine(pad_left, h - pad_bot, w - pad_right, h - pad_bot)
        
        # Legend (Gösterge) - Sol tarafa hizalandı
        painter.setFont(QFont("Segoe UI", 9))
        leg_x = pad_left
        leg_y = 35
        
        painter.fillRect(leg_x, leg_y, 12, 12, QColor(KIRMIZI))
        painter.drawText(leg_x + 18, leg_y, 70, 12, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.data1_label)
        
        painter.fillRect(leg_x + 95, leg_y, 12, 12, QColor(MAVI))
        painter.drawText(leg_x + 113, leg_y, 70, 12, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.data2_label)
        
        # Barlar
        n = len(self.labels)
        bar_group_w = graph_w / n
        bar_w = bar_group_w * 0.35
        if bar_w > 40: bar_w = 40
        
        def fmt(v):
            if v == 0: return "0"
            if v < 0.01: return f"{v:.4f}"
            if v < 0.1: return f"{v:.3f}"
            if v < 10: return f"{v:.2f}"
            return f"{v:.1f}"

        for i in range(n):
            cx = pad_left + i * bar_group_w + bar_group_w / 2
            
            # X ekseni etiketi
            painter.setPen(QPen(QColor(METIN)))
            painter.drawText(int(cx - bar_group_w/2), int(h - pad_bot + 10), int(bar_group_w), 20, Qt.AlignmentFlag.AlignCenter, f"N={self.labels[i]}")
            
            # Yükseklik hesaplamaları
            v1 = self.data1[i]
            v2 = self.data2[i]
            bh1 = ((v1 ** 0.5) / (max_val ** 0.5)) * graph_h
            bh2 = ((v2 ** 0.5) / (max_val ** 0.5)) * graph_h
            if v1 > 0 and bh1 < 4: bh1 = 4
            if v2 > 0 and bh2 < 4: bh2 = 4
            
            bx1 = cx - bar_w - 2
            by1 = h - pad_bot - bh1
            bx2 = cx + 2
            by2 = h - pad_bot - bh2
            
            # Yazı çakışmasını engellemek için dinamik yükseklik ayarı (Staggering)
            by1_text = by1 - 15
            by2_text = by2 - 15
            if abs(by1_text - by2_text) < 16:
                if by1_text < by2_text:
                    by2_text = by1_text - 16
                else:
                    by1_text = by2_text - 16
            
            # Bar 1 (Kırmızı)
            painter.fillRect(QRectF(bx1, by1, bar_w, bh1), QColor(KIRMIZI))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(int(bx1-20), int(by1_text), int(bar_w+40), 15, Qt.AlignmentFlag.AlignCenter, fmt(v1))
            
            # Bar 2 (Mavi)
            painter.fillRect(QRectF(bx2, by2, bar_w, bh2), QColor(MAVI))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(int(bx2-20), int(by2_text), int(bar_w+40), 15, Qt.AlignmentFlag.AlignCenter, fmt(v2))


# ANA PENCERE

class AnaUygulama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sistem = KampSistemi()
        self.sistem.ornek_veri_yukle()

        self.setWindowTitle("Kamp Alanı Rezervasyon Sistemi  |  BMT210")
        self.setMinimumSize(1100, 750)
        self.setStyleSheet(stil())

        merkez = QWidget()
        self.setCentralWidget(merkez)
        ana_layout = QVBoxLayout(merkez)
        ana_layout.setContentsMargins(12, 12, 12, 12)
        ana_layout.setSpacing(8)

        # Başlık
        baslik = QLabel("Kamp Alanı Rezervasyon ve Yönetim Sistemi")
        baslik.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        baslik.setStyleSheet(f"color: {YESIL}; padding: 6px 0;")
        baslik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ana_layout.addWidget(baslik)

        # Sekmeler
        self.sekmeler = QTabWidget()
        ana_layout.addWidget(self.sekmeler)

        self._ziyaretci_sekmesi()
        self._alan_sekmesi()
        self._rezervasyon_sekmesi()
        self._ekipman_sekmesi()
        self._kamp_haritasi_sekmesi()
        self._rapor_sekmesi()
        self.statusBar().hide()

    def _durum(self, mesaj):
        self.statusBar().showMessage(mesaj, 4000)

    # 1. ZİYARETÇİ SEKMESİ

    def _ziyaretci_sekmesi(self):
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setSpacing(12)

        # Sol: form
        form_grup = QGroupBox("Yeni Ziyaretçi Ekle / Güncelle")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.z_ad = QLineEdit()
        self.z_soyad = QLineEdit()
        self.z_tel = QLineEdit()
        self.z_oncelik = QComboBox()
        self.z_oncelik.addItems(["Normal (0)", "VIP (5)", "Engelli (10)"])

        form_layout.addRow("Ad:", self.z_ad)
        form_layout.addRow("Soyad:", self.z_soyad)
        form_layout.addRow("Telefon:", self.z_tel)
        form_layout.addRow("Öncelik:", self.z_oncelik)

        btn_ekle = QPushButton("Ziyaretçi Ekle")
        btn_guncelle = QPushButton("Güncelle")
        btn_guncelle.setObjectName("btn_blue")
        btn_sil = QPushButton("Sil")
        btn_sil.setObjectName("btn_red")
        btn_geri = QPushButton("Son İşlemi Geri Al")
        btn_geri.setObjectName("btn_orange")

        btn_ekle.clicked.connect(self._ziyaretci_ekle)
        btn_guncelle.clicked.connect(self._ziyaretci_guncelle)
        btn_sil.clicked.connect(self._ziyaretci_sil)
        btn_geri.clicked.connect(self._geri_al)

        btn_layout = QVBoxLayout()
        for b in [btn_ekle, btn_guncelle, btn_sil, btn_geri]:
            btn_layout.addWidget(b)
        btn_layout.addStretch()

        form_grup.setLayout(form_layout)

        sol = QVBoxLayout()
        sol.addWidget(form_grup)
        sol.addLayout(btn_layout)
        sol.addStretch()

        # Sağ: tablo
        sag = QVBoxLayout()
        ust = QHBoxLayout()
        ara_label = QLabel("Ara:")
        self.z_ara = QLineEdit()
        self.z_ara.setPlaceholderText("Ad veya ID ile ara...")
        self.z_ara.textChanged.connect(self._ziyaretci_listele)
        ust.addWidget(ara_label)
        ust.addWidget(self.z_ara)
        sag.addLayout(ust)

        self.z_tablo = tablo_olustur(["ID", "Ad", "Soyad", "Telefon", "Öncelik"])
        self.z_tablo.clicked.connect(self._ziyaretci_sec)
        sag.addWidget(self.z_tablo)

        layout.addLayout(sol, 1)
        layout.addLayout(sag, 3)

        self.sekmeler.addTab(w, "Ziyaretçiler")
        self._ziyaretci_listele()

    def _ziyaretci_listele(self):
        self.z_tablo.setRowCount(0)
        filtre = self.z_ara.text().lower() if hasattr(self, 'z_ara') else ""
        onc_renk = {"Normal": None, "VIP": MAVI, "Engelli": TURUNCU}
        for z in self.sistem.tum_ziyaretciler():
            if filtre and filtre not in z.ad.lower() and filtre not in z.soyad.lower() and filtre not in z.ziyaretci_id.lower():
                continue
            r = onc_renk.get(z.oncelik_adi)
            satir_ekle(self.z_tablo,
                       [z.ziyaretci_id, z.ad, z.soyad, z.telefon, z.oncelik_adi],
                       [None, None, None, None, r])

    def _ziyaretci_sec(self):
        row = self.z_tablo.currentRow()
        if row < 0:
            return
        self.z_ad.setText(self.z_tablo.item(row, 1).text())
        self.z_soyad.setText(self.z_tablo.item(row, 2).text())
        self.z_tel.setText(self.z_tablo.item(row, 3).text())
        onc_map = {"Normal": 0, "VIP": 1, "Engelli": 2}
        onc = self.z_tablo.item(row, 4).text()
        self.z_oncelik.setCurrentIndex(onc_map.get(onc, 0))

    def _ziyaretci_ekle(self):
        ad = self.z_ad.text().strip()
        soyad = self.z_soyad.text().strip()
        tel = self.z_tel.text().strip()
        if not ad or not soyad:
            hata_kutusu(self, "Ad ve soyad zorunludur.")
            return
        onc_deger = [0, 5, 10][self.z_oncelik.currentIndex()]
        z = self.sistem.ziyaretci_ekle(ad, soyad, tel, onc_deger)
        self._ziyaretci_listele()
        self._durum(f"Ziyaretçi eklendi: {z.tam_ad}  ({z.ziyaretci_id})")

    def _ziyaretci_guncelle(self):
        row = self.z_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Güncellenecek ziyaretçiyi seçin.")
            return
        zid = self.z_tablo.item(row, 0).text()
        onc_deger = [0, 5, 10][self.z_oncelik.currentIndex()]
        self.sistem.ziyaretci_guncelle(zid,
            ad=self.z_ad.text().strip() or None,
            soyad=self.z_soyad.text().strip() or None,
            telefon=self.z_tel.text().strip() or None,
            oncelik=onc_deger)
        self._ziyaretci_listele()
        self._durum(f"Ziyaretçi güncellendi: {zid}")

    def _ziyaretci_sil(self):
        row = self.z_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Silinecek ziyaretçiyi seçin.")
            return
        zid = self.z_tablo.item(row, 0).text()
        ad = self.z_tablo.item(row, 1).text()
        if not onay_kutusu(self, f"{ad} adlı ziyaretçiyi silmek istiyor musunuz?"):
            return
        self.sistem.ziyaretci_sil(zid)
        self._ziyaretci_listele()
        self._durum(f"Ziyaretçi silindi: {zid}")

    def _geri_al(self):
        sonuc = self.sistem.son_islemi_geri_al()
        self._ziyaretci_listele()
        self._alan_listele()
        self._rezervasyon_listele()
        self._ekipman_listele()
        if sonuc == "Geri alınacak işlem yok.":
            bilgi_kutusu(self, "Stack Boş", sonuc)
        else:
            self._durum(sonuc)

    # 2. ALAN SEKMESİ

    def _alan_sekmesi(self):
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setSpacing(12)

        form_grup = QGroupBox("Yeni Alan Ekle")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.a_tip = QComboBox()
        self.a_tip.addItems(ALAN_TIPLERI)
        self.a_kap = QSpinBox()
        self.a_kap.setRange(1, 50)
        self.a_kap.setValue(4)
        self.a_fiyat = QDoubleSpinBox()
        self.a_fiyat.setRange(0, 99999)
        self.a_fiyat.setValue(200)
        self.a_fiyat.setPrefix("₺")

        form_layout.addRow("Alan Tipi:", self.a_tip)
        form_layout.addRow("Kapasite:", self.a_kap)
        form_layout.addRow("Gecelik Fiyat:", self.a_fiyat)

        btn_ekle = QPushButton("Alan Ekle")
        btn_bakim = QPushButton("Bakıma Al")
        btn_bakim.setObjectName("btn_orange")
        btn_bakimdan = QPushButton("Bakımdan Çıkar")
        btn_bakimdan.setObjectName("btn_blue")
        btn_sil = QPushButton("Alanı Sil")
        btn_sil.setObjectName("btn_red")

        btn_ekle.clicked.connect(self._alan_ekle)
        btn_bakim.clicked.connect(self._bakima_al)
        btn_bakimdan.clicked.connect(self._bakimdan_cikart)
        btn_sil.clicked.connect(self._alan_sil)

        form_grup.setLayout(form_layout)

        sol = QVBoxLayout()
        sol.addWidget(form_grup)
        for b in [btn_ekle, btn_bakim, btn_bakimdan, btn_sil]:
            sol.addWidget(b)
        sol.addStretch()

        sag = QVBoxLayout()
        self.a_tablo = tablo_olustur(["ID", "Tip", "Kapasite", "Fiyat (₺)", "Rezervasyon", "Durum"])
        sag.addWidget(self.a_tablo)

        # GRAF / DİJKSTRA PANELİ
        graf_grup = QGroupBox("Yol Tarifi & Graf Yönetimi (Dijkstra En Kısa Yol)")
        graf_layout = QHBoxLayout()
        
        yol_layout = QFormLayout()
        self.yol_baslangic = QComboBox()
        self.yol_bitis = QComboBox()
        yol_layout.addRow("Nereden:", self.yol_baslangic)
        yol_layout.addRow("Nereye:", self.yol_bitis)
        btn_yol = QPushButton("En Kısa Yolu Bul")
        btn_yol.setObjectName("btn_blue")
        btn_yol.clicked.connect(self._yol_tarifi_bul)
        yol_layout.addRow("", btn_yol)
        
        komsu_layout = QFormLayout()
        self.komsu1 = QComboBox()
        self.komsu2 = QComboBox()
        self.komsu_mesafe = QSpinBox()
        self.komsu_mesafe.setRange(1, 9999)
        self.komsu_mesafe.setValue(1)
        komsu_layout.addRow("Alan 1:", self.komsu1)
        komsu_layout.addRow("Alan 2:", self.komsu2)
        komsu_layout.addRow("Mesafe:", self.komsu_mesafe)
        btn_komsu = QPushButton("Komşu Ekle")
        btn_komsu.setObjectName("btn_orange")
        btn_komsu.clicked.connect(self._komsu_ekle)
        komsu_layout.addRow("", btn_komsu)
        
        self.yol_sonuc = QTextEdit()
        self.yol_sonuc.setReadOnly(True)
        self.yol_sonuc.setMaximumHeight(80)
        self.yol_sonuc.setPlaceholderText("Yol tarifi sonucu burada görünecek...")
        
        graf_layout.addLayout(yol_layout)
        graf_layout.addLayout(komsu_layout)
        
        graf_ana = QVBoxLayout()
        graf_ana.addLayout(graf_layout)
        graf_ana.addWidget(self.yol_sonuc)
        graf_grup.setLayout(graf_ana)
        
        sag.addWidget(graf_grup)

        layout.addLayout(sol, 1)
        layout.addLayout(sag, 3)

        self.sekmeler.addTab(w, "Alanlar")
        self._alan_listele()
        self._alan_combo_yenile()

    def _alan_listele(self):
        self.a_tablo.setRowCount(0)
        for a in self.sistem.tum_alanlar():
            renk = KIRMIZI if a.bakimda else YESIL
            satir_ekle(self.a_tablo,
                       [a.alan_id, a.alan_tipi, a.kapasite,
                        f"{a.fiyat:.0f}", a.rezervasyon_sayisi, a.durum],
                       [None, None, None, None, None, renk])

    def _alan_sec(self):
        row = self.a_tablo.currentRow()
        if row < 0:
            return
        tip = self.a_tablo.item(row, 1).text()
        idx = ALAN_TIPLERI.index(tip) if tip in ALAN_TIPLERI else 0
        self.a_tip.setCurrentIndex(idx)

    def _alan_ekle(self):
        tip = self.a_tip.currentText()
        kap = self.a_kap.value()
        fiyat = self.a_fiyat.value()
        a = self.sistem.alan_ekle(tip, kap, fiyat)
        self._alan_listele()
        self._agac_guncelle()
        self._alan_combo_yenile()
        self._rezervasyon_listele()  # Otomatik rezervasyon olursa tablo güncellensin
        self._durum(f"Alan eklendi: {a.alan_id}  ({tip})")

    def _alan_sil(self):
        row = self.a_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Silinecek alanı seçin.")
            return
        aid = self.a_tablo.item(row, 0).text()
        if not onay_kutusu(self, f"{aid} alanını silmek istiyor musunuz?"):
            return
        self.sistem.alan_sil(aid)
        self._alan_listele()
        self._agac_guncelle()
        self._alan_combo_yenile()
        self._durum(f"Alan silindi: {aid}")

    def _bakima_al(self):
        row = self.a_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Alan seçin.")
            return
        aid = self.a_tablo.item(row, 0).text()
        self.sistem.bakima_al(aid)
        self._alan_listele()
        self._durum(f"{aid} bakıma alındı.")

    def _alan_combo_yenile(self):
        if not hasattr(self, 'yol_baslangic'): return
        self.yol_baslangic.clear()
        self.yol_bitis.clear()
        self.komsu1.clear()
        self.komsu2.clear()
        for a in self.sistem.tum_alanlar():
            metin = f"{a.alan_id} ({a.alan_tipi})"
            self.yol_baslangic.addItem(metin, a.alan_id)
            self.yol_bitis.addItem(metin, a.alan_id)
            self.komsu1.addItem(metin, a.alan_id)
            self.komsu2.addItem(metin, a.alan_id)

    def _yol_tarifi_bul(self):
        bas = self.yol_baslangic.currentData()
        bit = self.yol_bitis.currentData()
        if not bas or not bit:
            return
        mesafe, yol = self.sistem.yol_tarifi_al(bas, bit)
        if mesafe == float('inf'):
            self.yol_sonuc.setText(f"{bas} alanından {bit} alanına gidilebilecek bir yol bulunamadı.")
        else:
            yol_metni = " ➔ ".join(yol)
            self.yol_sonuc.setText(f"En Kısa Yol Bulundu! Toplam Mesafe: {mesafe} birim\nRota: {yol_metni}")

    def _komsu_ekle(self):
        a1 = self.komsu1.currentData()
        a2 = self.komsu2.currentData()
        mesafe = self.komsu_mesafe.value()
        if a1 == a2:
            hata_kutusu(self, "Aynı alana komşu eklenemez.")
            return
        if self.sistem.komsu_ekle(a1, a2, mesafe):
            self._durum(f"Komşu eklendi: {a1} <-> {a2} (Mesafe: {mesafe})")
            self.yol_sonuc.setText(f"Bağlantı kuruldu: {a1} ve {a2} arası mesafe {mesafe} olarak ayarlandı. Lütfen rotanızı tekrar hesaplayın.")
        else:
            hata_kutusu(self, "Komşu eklenirken bir hata oluştu.")

    def _bakimdan_cikart(self):
        row = self.a_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Alan seçin.")
            return
        aid = self.a_tablo.item(row, 0).text()
        self.sistem.bakimdan_cikart(aid)
        self._alan_listele()
        self._rezervasyon_listele()  # Otomatik rezervasyon olursa tablo güncellensin
        self._durum(f"{aid} bakımdan çıkarıldı.")

    # 3. REZERVASYON SEKMESİ

    def _rezervasyon_sekmesi(self):
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setSpacing(12)

        form_grup = QGroupBox("Yeni Rezervasyon Oluştur")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.r_ziyaretci = QComboBox()
        self.r_alan = QComboBox()
        self.r_giris = QDateEdit()
        self.r_giris.setCalendarPopup(True)
        self.r_giris.setDate(QDate.currentDate())
        self.r_cikis = QDateEdit()
        self.r_cikis.setCalendarPopup(True)
        self.r_cikis.setDate(QDate.currentDate().addDays(3))

        form_layout.addRow("Ziyaretçi:", self.r_ziyaretci)
        form_layout.addRow("Alan:", self.r_alan)
        form_layout.addRow("Giriş Tarihi:", self.r_giris)
        form_layout.addRow("Çıkış Tarihi:", self.r_cikis)

        btn_olustur = QPushButton("Rezervasyon Oluştur")
        btn_iptal = QPushButton("İptal Et")
        btn_iptal.setObjectName("btn_red")
        btn_geri = QPushButton("Geri Al (Stack)")
        btn_geri.setObjectName("btn_orange")
        btn_yenile = QPushButton("Listeleri Yenile")
        btn_yenile.setObjectName("btn_blue")

        btn_olustur.clicked.connect(self._rezervasyon_olustur)
        btn_iptal.clicked.connect(self._rezervasyon_iptal)
        btn_geri.clicked.connect(self._geri_al)
        btn_yenile.clicked.connect(self._combo_yenile)

        form_grup.setLayout(form_layout)

        sol = QVBoxLayout()
        sol.addWidget(form_grup)
        for b in [btn_olustur, btn_iptal, btn_geri, btn_yenile]:
            sol.addWidget(b)
        sol.addStretch()

        sag = QVBoxLayout()

        # Filtre
        filtre_layout = QHBoxLayout()
        self.r_sadece_aktif = QComboBox()
        self.r_sadece_aktif.addItems(["Tüm Rezervasyonlar", "Sadece Aktif"])
        self.r_sadece_aktif.currentIndexChanged.connect(self._rezervasyon_listele)
        filtre_layout.addWidget(QLabel("Görüntüle:"))
        filtre_layout.addWidget(self.r_sadece_aktif)
        filtre_layout.addStretch()
        sag.addLayout(filtre_layout)

        self.r_tablo = tablo_olustur(["ID", "Ziyaretçi", "Alan", "Giriş", "Çıkış", "Ücret (₺)", "Durum"])
        sag.addWidget(self.r_tablo)

        # --- BEKLEME LİSTESİ ---
        bekleme_label = QLabel("Bekleme Listesi (Priority Queue - VIP/Engelli Öncelikli)")
        bekleme_label.setStyleSheet(f"color: {TURUNCU}; font-weight: bold; margin-top: 10px; font-size: 14px;")
        sag.addWidget(bekleme_label)
        self.b_tablo = tablo_olustur(["Talep ID", "Ziyaretçi", "Alan Tipi", "Giriş", "Çıkış"])
        sag.addWidget(self.b_tablo)

        layout.addLayout(sol, 1)
        layout.addLayout(sag, 3)

        self.sekmeler.addTab(w, "Rezervasyonlar")
        self._combo_yenile()
        self._rezervasyon_listele()

    def _combo_yenile(self):
        self.r_ziyaretci.clear()
        for z in self.sistem.tum_ziyaretciler():
            self.r_ziyaretci.addItem(f"{z.tam_ad} ({z.ziyaretci_id})", z.ziyaretci_id)
        self.r_alan.clear()
        for a in self.sistem.musait_alanlar():
            self.r_alan.addItem(f"{a.alan_id} — {a.alan_tipi} (₺{a.fiyat:.0f}/gece)", a.alan_id)
        # Tabloları da yenile ki güncel durum görünsün
        self._rezervasyon_listele()

    def _rezervasyon_listele(self):
        self.r_tablo.setRowCount(0)
        sadece_aktif = self.r_sadece_aktif.currentIndex() == 1
        for r in self.sistem.tum_rezervasyonlar(sadece_aktif):
            z = self.sistem.ziyaretci_bul(r.ziyaretci_id)
            ad = z.tam_ad if z else r.ziyaretci_id
            durum = "Aktif" if r.aktif else "İptal"
            renk = YESIL if r.aktif else KIRMIZI
            satir_ekle(self.r_tablo,
                       [r.rezervasyon_id, ad, r.alan_id,
                        r.giris_tarihi, r.cikis_tarihi,
                        f"{r.toplam_ucret:.0f}", durum],
                       [None, None, None, None, None, None, renk])
        self._bekleme_listele()

    def _bekleme_listele(self):
        if not hasattr(self, 'b_tablo'): return
        self.b_tablo.setRowCount(0)
        bekleyenler = self.sistem.oncelik_kuyrugu.to_list()
        for b in bekleyenler:
            z = self.sistem.ziyaretci_bul(b["ziyaretci_id"])
            ad = f"{z.tam_ad} ({z.oncelik_adi})" if z else b["ziyaretci_id"]
            satir_ekle(self.b_tablo, [b["id"], ad, b["alan_tipi"], b["giris"], b["cikis"]])

    def _rezervasyon_olustur(self):
        if self.r_ziyaretci.count() == 0 or self.r_alan.count() == 0:
            hata_kutusu(self, "Ziyaretçi veya müsait alan yok. Önce ekleyin.")
            return
        zid = self.r_ziyaretci.currentData()
        aid = self.r_alan.currentData()
        giris = self.r_giris.date().toString("yyyy-MM-dd")
        cikis = self.r_cikis.date().toString("yyyy-MM-dd")
        if giris >= cikis:
            hata_kutusu(self, "Çıkış tarihi giriş tarihinden sonra olmalıdır.")
            return
        r = self.sistem.rezervasyon_olustur(zid, aid, giris, cikis)
        if r == "DOLU":
            a = self.sistem.alan_bul(aid)
            if onay_kutusu(self, f"Seçilen {a.alan_tipi} alanı kapasiteye ulaşmış durumda.\n"
                                 f"Ziyaretçiyi '{a.alan_tipi}' bekleme listesine (Priority Queue) eklemek ister misiniz?"):
                self.sistem.bekleme_listesine_ekle(zid, a.alan_tipi, giris, cikis)
                self._bekleme_listele()
                self._durum("Ziyaretçi bekleme listesine alındı.")
            return

        if not r:
            hata_kutusu(self, "Rezervasyon oluşturulamadı. Alan bakımda olabilir.")
            return
        self._rezervasyon_listele()
        self._alan_listele()
        self._rapor_guncelle()
        self._durum(f"Rezervasyon oluşturuldu: {r.rezervasyon_id}  |  ₺{r.toplam_ucret:.0f}")

    def _rezervasyon_iptal(self):
        row = self.r_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "İptal edilecek rezervasyonu seçin.")
            return
        rid = self.r_tablo.item(row, 0).text()
        if not onay_kutusu(self, f"{rid} rezervasyonunu iptal etmek istiyor musunuz?"):
            return
        self.sistem.rezervasyon_iptal(rid)
        self._rezervasyon_listele()
        self._alan_listele()
        self._rapor_guncelle()
        self._durum(f"Rezervasyon iptal edildi: {rid}")

    # 4. EKİPMAN SEKMESİ

    def _ekipman_sekmesi(self):
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setSpacing(12)

        form_grup = QGroupBox("Ekipman Yönetimi")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        self.e_ad = QLineEdit()
        self.e_stok = QSpinBox()
        self.e_stok.setRange(1, 999)
        self.e_stok.setValue(10)
        self.e_adet = QSpinBox()
        self.e_adet.setRange(1, 99)
        self.e_adet.setValue(1)
        self.e_adet.setToolTip("Kaç adet ekipman ödünç verileceğini veya iade alınacağını belirler.")

        form_layout.addRow("Ekipman Adı:", self.e_ad)
        form_layout.addRow("Başlangıç Stok:", self.e_stok)
        form_layout.addRow("Ödünç/İade Adedi:", self.e_adet)

        btn_ekle = QPushButton("Ekipman Ekle")
        btn_odunc = QPushButton("📤  Ödünç Ver")
        btn_odunc.setObjectName("btn_orange")
        btn_iade = QPushButton("📥  İade Al")
        btn_iade.setObjectName("btn_blue")
        btn_sil = QPushButton("Sil")
        btn_sil.setObjectName("btn_red")

        btn_ekle.clicked.connect(self._ekipman_ekle)
        btn_odunc.clicked.connect(self._ekipman_odunc)
        btn_iade.clicked.connect(self._ekipman_iade)
        btn_sil.clicked.connect(self._ekipman_sil)

        form_grup.setLayout(form_layout)

        sol = QVBoxLayout()
        sol.addWidget(form_grup)
        for b in [btn_ekle, btn_odunc, btn_iade, btn_sil]:
            sol.addWidget(b)
        sol.addStretch()

        sag = QVBoxLayout()
        self.e_tablo = tablo_olustur(["ID", "Ekipman Adı", "Toplam Stok", "Mevcut Stok", "Ödünç Sayısı"])
        self.e_tablo.clicked.connect(self._ekipman_sec)
        sag.addWidget(self.e_tablo)

        layout.addLayout(sol, 1)
        layout.addLayout(sag, 3)

        self.sekmeler.addTab(w, "Ekipman")
        self._ekipman_listele()

    def _ekipman_listele(self):
        self.e_tablo.setRowCount(0)
        for e in self.sistem.tum_ekipmanlar():
            renk = KIRMIZI if e.mevcut_stok == 0 else (TURUNCU if e.mevcut_stok < 3 else None)
            satir_ekle(self.e_tablo,
                       [e.ekipman_id, e.ad, e.toplam_stok, e.mevcut_stok, e.odunc_sayisi],
                       [None, None, None, renk, None])

    def _ekipman_sec(self):
        row = self.e_tablo.currentRow()
        if row < 0:
            return
        self.e_ad.setText(self.e_tablo.item(row, 1).text())

    def _ekipman_ekle(self):
        ad = self.e_ad.text().strip()
        if not ad:
            hata_kutusu(self, "Ekipman adı zorunludur.")
            return
        e = self.sistem.ekipman_ekle(ad, self.e_stok.value())
        self._ekipman_listele()
        self._durum(f"Ekipman eklendi: {e.ad}")

    def _ekipman_odunc(self):
        row = self.e_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Ekipman seçin.")
            return
        eid = self.e_tablo.item(row, 0).text()
        adet = self.e_adet.value()
        if self.sistem.ekipman_odunc_ver(eid, adet):
            self._ekipman_listele()
            self._durum(f"{adet} adet ödünç verildi: {eid}")
        else:
            hata_kutusu(self, "Yeterli stok yok.")

    def _ekipman_iade(self):
        row = self.e_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Ekipman seçin.")
            return
        eid = self.e_tablo.item(row, 0).text()
        self.sistem.ekipman_iade_al(eid, self.e_adet.value())
        self._ekipman_listele()
        self._durum(f"İade alındı: {eid}")

    def _ekipman_sil(self):
        row = self.e_tablo.currentRow()
        if row < 0:
            hata_kutusu(self, "Ekipman seçin.")
            return
        eid = self.e_tablo.item(row, 0).text()
        ad = self.e_tablo.item(row, 1).text()
        if not onay_kutusu(self, f"'{ad}' ekipmanını silmek istiyor musunuz?"):
            return
        self.sistem.ekipman_sil(eid)
        self._ekipman_listele()
        self._durum(f"Ekipman silindi: {eid}")

    # 6. KAMP HARİTASI SEKMESİ  (CampTree — 11. yapı)

    def _kamp_haritasi_sekmesi(self):
        w = QWidget()
        ana = QVBoxLayout(w)
        ana.setSpacing(10)

        # ── Başlık açıklaması ─────────────────────────────────
        aciklama = QLabel(
            " CampTree — N-ary Ağaç  |  "
            "Kök: Kamp Ana Girişi  →  Dal: Bölgeler  →  Yaprak: Parseller"
        )
        aciklama.setStyleSheet(
            f"background:{YESIL}; color:white; font-weight:bold; "
            "padding:8px 14px; border-radius:6px; font-size:13px;"
        )
        aciklama.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ana.addWidget(aciklama)

        # ── Ana yatay bölünme ─────────────────────────────────
        ust = QHBoxLayout()
        ust.setSpacing(12)

        # SOL PANEL — Görsel QTreeWidget ağaç
        hiy_grup = QGroupBox("🌳  Ağaç Hiyerarşisi  —  Görsel Ağaç (CampTree)")
        hiy_grup.setStyleSheet(
            f"QGroupBox {{ background:{BEYAZ}; }} "
            f"QGroupBox::title {{ color:{YESIL}; font-size:13px; font-weight:bold; }}"
        )
        hiy_layout = QVBoxLayout()

        self.agac_widget = QTreeWidget()
        self.agac_widget.setColumnCount(3)
        self.agac_widget.setHeaderLabels(["Düğüm", "Tür", "Parsel Sayısı"])
        self.agac_widget.setAnimated(True)
        self.agac_widget.setAlternatingRowColors(True)
        self.agac_widget.setMinimumHeight(240)
        self.agac_widget.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.agac_widget.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.agac_widget.header().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.agac_widget.setStyleSheet(f"""
            QTreeWidget {{
                background: {BEYAZ};
                border: 2px solid {YESIL};
                border-radius: 8px;
                font-size: 13px;
                padding: 4px;
            }}
            QTreeWidget::item {{
                padding: 5px 4px;
                border-radius: 4px;
            }}
            QTreeWidget::item:hover {{
                background: {YESIL_BG};
            }}
            QTreeWidget::item:selected {{
                background: {YESIL_ACIK};
                color: white;
            }}
            QTreeWidget::branch:has-children:!has-siblings:closed,
            QTreeWidget::branch:closed:has-children:has-siblings {{
                border-image: none;
                image: none;
            }}
            QHeaderView::section {{
                background: {YESIL};
                color: white;
                font-weight: bold;
                font-size: 12px;
                padding: 6px;
                border: none;
            }}
        """)

        btn_yenile = QPushButton("Ağacı Yenile")
        btn_yenile.clicked.connect(self._agac_guncelle)

        hiy_layout.addWidget(self.agac_widget)
        hiy_layout.addWidget(btn_yenile)
        hiy_grup.setLayout(hiy_layout)

        # SOL PANEL — Graf Çizimi (Alanlar Arası Komşuluklar)
        graf_grup = QGroupBox("🕸️  Kamp Haritası Grafiği (Ağırlıklı Komşuluklar)")
        graf_grup.setStyleSheet(
            f"QGroupBox {{ background:{BEYAZ}; }} "
            f"QGroupBox::title {{ color:{YESIL}; font-size:13px; font-weight:bold; }}"
        )
        graf_layout = QVBoxLayout()

        self.graf_scene = QGraphicsScene()
        self.graf_view = QGraphicsView(self.graf_scene)
        self.graf_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.graf_view.setMinimumHeight(300)

        # Alt butonlar
        graf_btn_layout = QHBoxLayout()
        btn_graf_yenile = QPushButton("Haritayı Yenile")
        btn_graf_yenile.clicked.connect(self._graf_haritasi_guncelle)

        # Zoom slider: 🔍−  [███████]  🔍+
        zoom_layout = QHBoxLayout()
        zoom_layout.setSpacing(4)
        lbl_zoom_out = QLabel("🔍−")
        lbl_zoom_out.setStyleSheet("font-size: 15px; padding: 0 2px;")
        lbl_zoom_in = QLabel("🔍+")
        lbl_zoom_in.setStyleSheet("font-size: 15px; padding: 0 2px;")
        self.graf_zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.graf_zoom_slider.setRange(10, 300)   # %10 — %300
        self.graf_zoom_slider.setValue(100)
        self.graf_zoom_slider.setFixedWidth(160)
        self.graf_zoom_slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                background: {GOLGELI};
                height: 6px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {YESIL};
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }}
        """)
        self.graf_zoom_slider.valueChanged.connect(self._graf_zoom_degisti)
        zoom_layout.addWidget(lbl_zoom_out)
        zoom_layout.addWidget(self.graf_zoom_slider)
        zoom_layout.addWidget(lbl_zoom_in)

        graf_btn_layout.addWidget(btn_graf_yenile)
        graf_btn_layout.addStretch()
        graf_btn_layout.addLayout(zoom_layout)

        graf_layout.addWidget(self.graf_view)
        graf_layout.addLayout(graf_btn_layout)
        graf_grup.setLayout(graf_layout)

        # Graf sola(2), Ağaç sağa(1)
        ust.addWidget(graf_grup, 2)
        ust.addWidget(hiy_grup, 1)

        ana.addLayout(ust)

        # ── Bölge tabloları ───────────────────────────────────
        bolge_grup = QGroupBox(" Bölge Bazlı Alan Raporu  (bolge_raporu)")
        bolge_grup.setStyleSheet(
            f"QGroupBox {{ background:{BEYAZ}; }} "
            f"QGroupBox::title {{ color:{YESIL}; font-size:13px; font-weight:bold; }}"
        )
        bolge_ana = QHBoxLayout()
        bolge_ana.setSpacing(10)

        BOLGELER = [
            ("⛺  Çadır Bölgesi",    "Çadır Bölgesi",    YESIL),
            ("🚐  Karavan Bölgesi",  "Karavan Bölgesi",  MAVI),
            ("Bungalov Bölgesi", "Bungalov Bölgesi", TURUNCU),
        ]
        self.bolge_tablolar = {}

        for etiket, anahtar, renk in BOLGELER:
            grup = QGroupBox(etiket)
            grup.setStyleSheet(
                f"QGroupBox {{ background:#f8fffe; border:2px solid {renk}; "
                f"border-radius:8px; margin-top:14px; padding:8px; font-weight:bold; }} "
                f"QGroupBox::title {{ subcontrol-origin:margin; left:12px; "
                f"padding:0 5px; color:{renk}; font-size:13px; }}"
            )
            g_layout = QVBoxLayout()
            tbl = tablo_olustur(["Alan ID", "Kap.", "Fiyat (₺)", "Rez.", "Durum"])
            self.bolge_tablolar[anahtar] = tbl
            g_layout.addWidget(tbl)
            grup.setLayout(g_layout)
            bolge_ana.addWidget(grup)

        bolge_grup.setLayout(bolge_ana)
        ana.addWidget(bolge_grup)

        self.sekmeler.addTab(w, "Kamp Haritası")
        self._agac_guncelle()

    def _agac_guncelle(self):
        """CampTree görünümlerini tümünü yeniler."""
        self._graf_haritasi_guncelle()
        if not hasattr(self, 'agac_widget'):
            return

        # ── 1) Görsel QTreeWidget ──────────────────────────────
        self.agac_widget.clear()
        agac = self.sistem.mekan_agaci

        # ── Kök düğüm
        kok = QTreeWidgetItem(self.agac_widget)
        kok.setText(0, f"Kamp Ana Girişi")
        kok.setText(1, "Kök")
        kok.setText(2, f"{len(agac)} parsel")
        kok.setFont(0, QFont("Segoe UI", 12, QFont.Weight.Bold))
        kok.setForeground(0, QBrush(QColor(YESIL)))
        kok.setForeground(1, QBrush(QColor(YESIL)))
        kok.setForeground(2, QBrush(QColor(YESIL)))

        # ── Bölge ve ikon eşleşmeleri
        BOLGE_IKON = {
            "Çadır Bölgesi":   ("⛺", "#2d6a4f", "Dal"),
            "Karavan Bölgesi": ("🚐", "#2980b9", "Dal"),
            "Bungalov Bölgesi":("", "#e76f51", "Dal"),
        }
        ALAN_IKON = {
            "Çadır Bölgesi":   ("", "#52b788"),
            "Karavan Bölgesi": ("", "#5dade2"),
            "Bungalov Bölgesi":("", "#f0a070"),
        }

        rapor = agac.tum_bolgeler()

        for bolge_adi, alan_listesi in rapor.items():
            ikon, renk, tur = BOLGE_IKON.get(bolge_adi, ("📁", METIN, "Dal"))

            # Dal düğümü
            dal = QTreeWidgetItem(kok)
            dal.setText(0, f"{ikon}  {bolge_adi}")
            dal.setText(1, tur)
            dal.setText(2, f"{len(alan_listesi)} parsel")
            dal.setFont(0, QFont("Segoe UI", 11, QFont.Weight.Bold))
            dal.setForeground(0, QBrush(QColor(renk)))
            dal.setForeground(2, QBrush(QColor(renk)))

            a_ikon, a_renk = ALAN_IKON.get(bolge_adi, ("", METIN))

            for alan_id in alan_listesi:
                a = self.sistem.alan_map.get(alan_id)
                durum_ikon = "" if (a and a.bakimda) else ""
                d_renk = KIRMIZI if (a and a.bakimda) else "#27ae60"

                # Yaprak düğüm
                yaprak = QTreeWidgetItem(dal)
                yaprak.setText(0, f"{a_ikon}  {alan_id}")
                yaprak.setText(1, "Yaprak")
                yaprak.setText(2, f"{durum_ikon} {'Bakımda' if (a and a.bakimda) else 'Müsait'}")
                yaprak.setFont(0, QFont("Segoe UI", 10))
                yaprak.setForeground(0, QBrush(QColor(a_renk)))
                yaprak.setForeground(2, QBrush(QColor(d_renk)))

        self.agac_widget.expandAll()

        # ── 2) Bölge tabloları ─────────────────────────────────
        bolge_raporu = self.sistem.bolge_raporu()
        for bolge_adi, tbl in self.bolge_tablolar.items():
            tbl.setRowCount(0)
            for a_dict in bolge_raporu.get(bolge_adi, []):
                durum = "Bakımda" if a_dict["bakimda"] else "Müsait"
                renk = KIRMIZI if a_dict["bakimda"] else YESIL
                satir_ekle(
                    tbl,
                    [
                        a_dict["alan_id"],
                        a_dict["kapasite"],
                        f"{a_dict['fiyat']:.0f}",
                        a_dict["rezervasyon_sayisi"],
                        durum,
                    ],
                    [None, None, None, None, renk],
                )

    def _graf_haritasi_guncelle(self):
        if not hasattr(self, 'graf_scene'):
            return
        self.graf_scene.clear()

        graf = self.sistem.alan_grafi
        dugumler = graf.all_nodes()
        if not dugumler:
            return

        import math
        merkez_x, merkez_y = 0, 0
        n = len(dugumler)
        yaricap = max(160, n * 14)
        aci_artisi = 2 * math.pi / n if n > 0 else 0

        dugum_kordinatlari = {}
        for i, dugum in enumerate(dugumler):
            aci = i * aci_artisi - math.pi / 2
            x = merkez_x + math.cos(aci) * yaricap
            y = merkez_y + math.sin(aci) * yaricap
            dugum_kordinatlari[dugum] = (x, y)

        cizilen_kenarlar = set()
        for dugum in dugumler:
            x1, y1 = dugum_kordinatlari[dugum]
            komsular = graf.neighbors(dugum)
            for komsu in komsular:
                kenar = tuple(sorted([dugum, komsu]))
                if kenar not in cizilen_kenarlar and komsu in dugum_kordinatlari:
                    x2, y2 = dugum_kordinatlari[komsu]
                    self.graf_scene.addLine(x1, y1, x2, y2, QPen(QColor("#2d6a4f"), 2))
                    cizilen_kenarlar.add(kenar)

        for dugum, (x, y) in dugum_kordinatlari.items():
            r = 22
            self.graf_scene.addEllipse(x - r, y - r, 2*r, 2*r, QPen(QColor("#1e1e1e"), 2), QBrush(QColor("#f4a261")))
            # Etiket — dairenin içinde, ortalanmış
            txt = self.graf_scene.addText(dugum, QFont("Segoe UI", 7, QFont.Weight.Bold))
            txt.setDefaultTextColor(QColor("#1b1b1b"))
            txt_w = txt.boundingRect().width()
            txt_h = txt.boundingRect().height()
            txt.setPos(x - txt_w / 2, y - txt_h / 2)
            txt.setZValue(1)

        # Sahneyi görünüme sığdır
        self._graf_sigdir()

    def _graf_sigdir(self):
        """Graf sahnesini görünüme sığdırır."""
        if not hasattr(self, 'graf_view') or not hasattr(self, 'graf_scene'):
            return
        rect = self.graf_scene.itemsBoundingRect()
        rect.adjust(-30, -30, 30, 30)  # kenar boşluğu
        self.graf_view.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
        if hasattr(self, 'graf_zoom_slider'):
            self.graf_zoom_slider.blockSignals(True)
            self.graf_zoom_slider.setValue(100)
            self.graf_zoom_slider.blockSignals(False)

    def _graf_zoom_degisti(self, value):
        """Zoom slider değiştiğinde çağrılır."""
        self._graf_sigdir_internal()
        factor = value / 100.0
        self.graf_view.scale(factor, factor)

    def _graf_sigdir_internal(self):
        """Slider için dahili sığdırma (slider değerini değiştirmez)."""
        if not hasattr(self, 'graf_view') or not hasattr(self, 'graf_scene'):
            return
        self.graf_view.resetTransform()
        rect = self.graf_scene.itemsBoundingRect()
        rect.adjust(-30, -30, 30, 30)
        self.graf_view.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)

    # 5. RAPOR SEKMESİ

    def _rapor_sekmesi(self):
        w = QWidget()
        ana = QVBoxLayout(w)
        ana.setSpacing(10)

        # ── Test Verisi Yükle ──────────────────────────
        test_grup = QGroupBox("Test Verisi Yükle (10 / 100 / 1000 Rezervasyon)")
        test_grup.setStyleSheet(f"QGroupBox {{ background: {YESIL_BG}; border-radius: 5px; }} QLabel {{ background: transparent; }}")
        test_layout = QHBoxLayout()

        self.test_boyut = QComboBox()
        self.test_boyut.addItems(["10 Rezervasyon", "100 Rezervasyon", "1000 Rezervasyon"])
        self.test_boyut.setFixedWidth(200)

        btn_yukle = QPushButton("Veriyi Yükle")
        btn_yukle.setObjectName("btn_blue")
        btn_yukle.clicked.connect(self._test_verisi_yukle)

        btn_temizle = QPushButton("Mevcut Veriyi Temizle")
        btn_temizle.setObjectName("btn_red")
        btn_temizle.clicked.connect(self._veri_temizle)

        self.test_sonuc = QLabel("")
        self.test_sonuc.setStyleSheet(f"color: {YESIL}; font-weight: bold; padding-left: 10px; background: transparent;")

        test_layout.addWidget(QLabel("Ölçek:"))
        test_layout.addWidget(self.test_boyut)
        test_layout.addWidget(btn_yukle)
        test_layout.addWidget(btn_temizle)
        test_layout.addWidget(self.test_sonuc)
        test_layout.addStretch()
        test_grup.setLayout(test_layout)
        ana.addWidget(test_grup)

        # Stat kartlar
        kart_layout = QHBoxLayout()
        self.stat_kartlar = {}
        for isim in ["Ziyaretçi", "Alan", "Ekipman", "Toplam Rez.", "Aktif Rez.", "Gelir (₺)"]:
            frame = QFrame()
            frame.setStyleSheet(f"""
                QFrame {{
                    background: {YESIL};
                    border-radius: 10px;
                    padding: 6px;
                }}
            """)
            fl = QVBoxLayout(frame)
            lbl_isim = QLabel(isim)
            lbl_isim.setStyleSheet("color: white; font-size: 11px; font-weight: bold;")
            lbl_isim.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_deger = QLabel("0")
            lbl_deger.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
            lbl_deger.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fl.addWidget(lbl_isim)
            fl.addWidget(lbl_deger)
            self.stat_kartlar[isim] = lbl_deger
            kart_layout.addWidget(frame)
        ana.addLayout(kart_layout)

        # İki sütun
        alt = QHBoxLayout()

        # Sol: Popüler alanlar + BST sorgü
        sol = QVBoxLayout()

        populer_grup = QGroupBox("🏆 Popüler Alanlar (MaxHeap)")
        pg = QVBoxLayout()
        self.populer_tablo = tablo_olustur(["Alan ID", "Tip", "Rezervasyon Sayısı"])
        pg.addWidget(self.populer_tablo)
        populer_grup.setLayout(pg)
        sol.addWidget(populer_grup)

        bst_grup = QGroupBox("📅 Tarih Aralığı Sorgusu (BST)")
        bg = QVBoxLayout()
        bst_filtre = QHBoxLayout()
        self.bst_baslangic = QDateEdit()
        self.bst_baslangic.setCalendarPopup(True)
        self.bst_baslangic.setDate(QDate(2025, 1, 1))
        self.bst_bitis = QDateEdit()
        self.bst_bitis.setCalendarPopup(True)
        self.bst_bitis.setDate(QDate(2025, 12, 31))
        btn_bst = QPushButton("🔍 Sorgula")
        btn_bst.clicked.connect(self._bst_sorgula)
        bst_filtre.addWidget(QLabel("Başlangıç:"))
        bst_filtre.addWidget(self.bst_baslangic)
        bst_filtre.addWidget(QLabel("Bitiş:"))
        bst_filtre.addWidget(self.bst_bitis)
        bst_filtre.addWidget(btn_bst)
        bg.addLayout(bst_filtre)
        self.bst_tablo = tablo_olustur(["Rezervasyon ID", "Ziyaretçi", "Alan", "Tarih", "Ücret (₺)"])
        bg.addWidget(self.bst_tablo)
        bst_grup.setLayout(bg)
        sol.addWidget(bst_grup)

        # Sağ: Performans log
        sag = QVBoxLayout()
        perf_grup = QGroupBox("⚡ Performans Karşılaştırması")
        pg2 = QVBoxLayout()
        btn_perf = QPushButton("Testleri Çalıştır (Grafikleri Oluştur)")
        btn_perf.clicked.connect(self._performans_testleri)
        pg2.addWidget(btn_perf)
        
        self.perf_sekmeler = QTabWidget()
        
        self.perf_log = QTextEdit()
        self.perf_log.setReadOnly(True)
        self.perf_log.setMinimumHeight(350)
        self.perf_sekmeler.addTab(self.perf_log, "Test Çıktıları")
        
        self.grafikler_widget = QWidget()
        self.grafikler_layout = QVBoxLayout(self.grafikler_widget)
        self.grafikler_layout.setSpacing(15)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.grafikler_widget)
        self.perf_sekmeler.addTab(scroll, "Grafiksel Analiz")
        
        pg2.addWidget(self.perf_sekmeler)
        perf_grup.setLayout(pg2)
        sag.addWidget(perf_grup)

        alt.addLayout(sol, 3)
        alt.addLayout(sag, 2)
        ana.addLayout(alt)

        self.sekmeler.addTab(w, "Raporlar")
        self._rapor_guncelle()

    def _rapor_guncelle(self):
        stats = self.sistem.istatistikler()
        mapping = {
            "Ziyaretçi": stats["toplam_ziyaretci"],
            "Alan": stats["toplam_alan"],
            "Ekipman": stats["toplam_ekipman"],
            "Toplam Rez.": stats["toplam_rezervasyon"],
            "Aktif Rez.": stats["aktif_rezervasyon"],
            "Gelir (₺)": f"{stats['toplam_gelir']:.0f}",
        }
        for isim, deger in mapping.items():
            if isim in self.stat_kartlar:
                self.stat_kartlar[isim].setText(str(deger))

        # Popüler alanlar
        self.populer_tablo.setRowCount(0)
        for a, sayi in self.sistem.populer_alanlar(5):
            satir_ekle(self.populer_tablo, [a.alan_id, a.alan_tipi, sayi])

    def _sistemi_sifirla(self):
        """Tüm veri yapılarını sıfırdan başlatır — tekrarlı import bloğunu merkezileştirir."""
        from data_structures.structures import (
            HashMap, BST, LinkedList, Stack,
            MaxHeap, CampSet, Graph, CampTree
        )
        s = self.sistem
        s.ziyaretci_map   = HashMap()
        s.alan_map        = HashMap()
        s.ekipman_map     = HashMap()
        s.rezervasyon_map = HashMap()
        s.rezervasyon_bst = BST()
        s.gecmis_listesi  = LinkedList()
        s.islem_stack     = Stack()
        s.bakim_set       = CampSet()
        s.alan_grafi      = Graph()
        s.popülerlik_heap = MaxHeap()
        s.mekan_agaci     = CampTree()

    def _test_verisi_yukle(self):
        import subprocess
        boyut_map = {"10 Rezervasyon": 10, "100 Rezervasyon": 100, "1000 Rezervasyon": 1000}
        n = boyut_map[self.test_boyut.currentText()]
        dosya = os.path.join(ROOT, "kayitlar", f"veri_{n}.json")

        if not os.path.exists(dosya):
            script = os.path.join(ROOT, "generate_data.py")
            subprocess.run([sys.executable, script], cwd=ROOT)

        if not os.path.exists(dosya):
            hata_kutusu(self, f"veri_{n}.json bulunamadı.")
            return

        import json
        with open(dosya, encoding="utf-8") as f:
            veri = json.load(f)

        from models import Ziyaretci, Alan, Rezervasyon, Ekipman
        self._sistemi_sifirla()
        s = self.sistem

        for d in veri.get("ziyaretciler", []):
            z = Ziyaretci.from_dict(d)
            s.ziyaretci_map.insert(z.ziyaretci_id, z)

        for d in veri.get("alanlar", []):
            a = Alan.from_dict(d)
            s.alan_map.insert(a.alan_id, a)
            s.alan_grafi.add_node(a.alan_id)
            s.mekan_agaci.alan_ekle(a.alan_id, a.alan_tipi)
            if a.bakimda:
                s.bakim_set.add(a.alan_id)

        for d in veri.get("ekipmanlar", []):
            e = Ekipman.from_dict(d)
            s.ekipman_map.insert(e.ekipman_id, e)

        for d in veri.get("rezervasyonlar", []):
            r = Rezervasyon.from_dict(d)
            s.rezervasyon_map.insert(r.rezervasyon_id, r)
            s.rezervasyon_bst.insert(r.giris_tarihi, r.rezervasyon_id)

        graf_data = veri.get("graf_yollari", {})
        if isinstance(graf_data, dict):
            eklenen = set()
            for u, komsular in graf_data.items():
                if isinstance(komsular, dict):
                    for v, w in komsular.items():
                        kenar = tuple(sorted([u, v]))
                        if kenar not in eklenen:
                            s.alan_grafi.add_edge(u, v, int(w))
                            eklenen.add(kenar)

        s._heap_yenile()
        s._kaydet()
        self._tum_tablolari_guncelle()

        stats = s.istatistikler()
        self.test_sonuc.setText(
            f"{n} rezervasyon yüklendi  |  "
            f"{stats['toplam_ziyaretci']} ziyaretçi  |  "
            f"{stats['toplam_alan']} alan  |  "
            f"{stats['toplam_ekipman']} ekipman türü"
        )

    def _veri_temizle(self):
        if not onay_kutusu(self, "Tüm mevcut veriyi silmek istiyor musunuz?"):
            return
        self._sistemi_sifirla()
        self.sistem._kaydet()
        self._tum_tablolari_guncelle()
        self.test_sonuc.setText("Veri temizlendi")
        self._durum("Tüm veri silindi.")

    def _tum_tablolari_guncelle(self):
        self._ziyaretci_listele()
        self._alan_listele()
        self._rezervasyon_listele()
        self._ekipman_listele()
        self._combo_yenile()
        self._alan_combo_yenile()
        self._rapor_guncelle()
        self._agac_guncelle()

    def _bst_sorgula(self):
        baslangic = self.bst_baslangic.date().toString("yyyy-MM-dd")
        bitis = self.bst_bitis.date().toString("yyyy-MM-dd")
        rezervasyonlar = self.sistem.tarih_araligi_rezervasyonlar(baslangic, bitis)
        self.bst_tablo.setRowCount(0)
        for r in rezervasyonlar:
            z = self.sistem.ziyaretci_bul(r.ziyaretci_id)
            ad = z.tam_ad if z else r.ziyaretci_id
            satir_ekle(self.bst_tablo,
                       [r.rezervasyon_id, ad, r.alan_id, r.giris_tarihi, f"{r.toplam_ucret:.0f}"])

    def _performans_testleri(self):
        import random, time
        from data_structures.structures import HashMap

        log = self.perf_log
        log.clear()

        def yaz(s):
            log.append(s)
            QApplication.processEvents()

        try:
            OLCEKLER = [10, 100, 1000]

            data_arama_n = []; data_arama_arr = []; data_arama_hm = []
            data_pq_n = []; data_pq_sort = []; data_pq_pq = []
            data_sort_n = []; data_sort_bubble = []; data_sort_heap = []
            data_set_n = []; data_set_arr = []; data_set_set = []

            yaz("=" * 62)
            yaz("  PERFORMANS KARŞILAŞTIRMA TESTLERİ")
            yaz("  BMT210 — Gazi Üniversitesi 2026")
            yaz("=" * 62)

            # ── TEST 1: Array vs HashMap ──────────────────────────
            yaz("\n📌 TEST 1: Array Arama vs HashMap  —  O(n) vs O(1)")
            yaz(f"  {'N':>8}  {'Array (ms)':>12}  {'HashMap (ms)':>13}  {'Hız Farkı':>10}")
            yaz("  " + "-" * 50)
            for N in OLCEKLER:
                data = [(f"K{i}", i) for i in range(N)]
                aranan = f"K{N // 2}"
                tekrar = max(10, 2000 // N)

                t0 = time.perf_counter()
                for _ in range(tekrar):
                    for k, v in data:
                        if k == aranan:
                            break
                sure_arr = (time.perf_counter() - t0) / tekrar * 1000

                hm = HashMap(capacity=N * 2)
                for k, v in data:
                    hm.insert(k, v)
                t0 = time.perf_counter()
                for _ in range(tekrar):
                    hm.get(aranan)
                sure_hm = (time.perf_counter() - t0) / tekrar * 1000

                kat = sure_arr / max(sure_hm, 0.0001)
                yaz(f"  {N:>8}  {sure_arr:>12.4f}  {sure_hm:>13.4f}  {kat:>9.1f}x")
                QApplication.processEvents()

                data_arama_n.append(str(N))
                data_arama_arr.append(sure_arr)
                data_arama_hm.append(sure_hm)
                
            yaz("  → Veri büyüdükçe Array O(n) yavaşlarken HashMap sabit kalır.")

            # ── TEST 2: Sıralı Liste vs Priority Queue ────────────
            yaz("\n📌 TEST 2: Sıralı Liste vs Priority Queue  —  O(n log n) vs O(log n)")
            yaz(f"  {'N':>8}  {'Sort (ms)':>12}  {'PQ push (ms)':>13}  {'Hız Farkı':>10}")
            yaz("  " + "-" * 50)
            for N in OLCEKLER:
                liste = [(random.randint(0, 10), f"Z{i}") for i in range(N)]
                tekrar = max(5, 500 // N)

                t0 = time.perf_counter()
                for _ in range(tekrar):
                    sorted(liste, key=lambda x: x[0], reverse=True)
                sure_sort = (time.perf_counter() - t0) / tekrar * 1000

                from data_structures.structures import PriorityQueue as _PQ
                t0 = time.perf_counter()
                for _ in range(tekrar):
                    p = _PQ()
                    for onc, item in liste:
                        p.enqueue(item, onc)
                    p.dequeue()
                sure_pq = (time.perf_counter() - t0) / tekrar * 1000

                kat = sure_sort / max(sure_pq, 0.0001)
                yaz(f"  {N:>8}  {sure_sort:>12.4f}  {sure_pq:>13.4f}  {kat:>9.1f}x")
                QApplication.processEvents()
                
                data_pq_n.append(str(N))
                data_pq_sort.append(sure_sort)
                data_pq_pq.append(sure_pq)
                
            yaz("  -> PQ her seferinde tüm listeyi sıralamaz, heap özelliğini korur.")

            # ── TEST 3: Bubble Sort vs Heap Sort ──────────────────
            yaz("\n📌 TEST 3: Bubble Sort vs Heap Sort  —  O(n²) vs O(n log n)")
            yaz(f"  {'N':>8}  {'Bubble (ms)':>12}  {'Heap (ms)':>13}  {'Hız Farkı':>10}")
            yaz("  " + "-" * 50)
            import heapq as hq
            for N in OLCEKLER:
                arr = [random.randint(0, 10000) for _ in range(N)]

                t0 = time.perf_counter()
                b = arr[:]
                for i in range(len(b)):
                    for j in range(len(b) - i - 1):
                        if b[j] > b[j+1]:
                            b[j], b[j+1] = b[j+1], b[j]
                sure_bubble = (time.perf_counter() - t0) * 1000
                QApplication.processEvents()

                t0 = time.perf_counter()
                h = arr[:]
                hq.heapify(h)
                [hq.heappop(h) for _ in range(len(h))]
                sure_heap = (time.perf_counter() - t0) * 1000

                kat = sure_bubble / max(sure_heap, 0.0001)
                yaz(f"  {N:>8}  {sure_bubble:>12.4f}  {sure_heap:>13.4f}  {kat:>9.1f}x")
                QApplication.processEvents()
                
                data_sort_n.append(str(N))
                data_sort_bubble.append(sure_bubble)
                data_sort_heap.append(sure_heap)
                
            yaz("  → N büyüdükçe fark dramatik artar: O(n²) ile O(n log n) arasındaki uçurum.")

            # ── TEST 4: Array vs Set ──────────────────────────────
            yaz("\n📌 TEST 4: Array vs Set  —  O(n) vs O(1)  (Bakım Alan Kontrolü)")
            yaz(f"  {'N':>8}  {'Array (ms)':>12}  {'Set (ms)':>13}  {'Hız Farkı':>10}")
            yaz("  " + "-" * 50)
            for N in OLCEKLER:
                items = [f"A{i}" for i in range(N)]
                aranan2 = f"A{N - 1}"
                tekrar = max(10, 2000 // N)

                t0 = time.perf_counter()
                for _ in range(tekrar):
                    _ = aranan2 in items
                sure_arr = (time.perf_counter() - t0) / tekrar * 1000

                s2 = set(items)
                t0 = time.perf_counter()
                for _ in range(tekrar):
                    _ = aranan2 in s2
                sure_set = (time.perf_counter() - t0) / tekrar * 1000

                kat = sure_arr / max(sure_set, 0.0001)
                yaz(f"  {N:>8}  {sure_arr:>12.4f}  {sure_set:>13.4f}  {kat:>9.1f}x")
                QApplication.processEvents()
                
                data_set_n.append(str(N))
                data_set_arr.append(sure_arr)
                data_set_set.append(sure_set)
                
            yaz("  → Set hash tabanlıdır; N ne kadar büyürse Array o kadar geride kalır.")

            # ── Grafikleri Çiz ──────────────────────────────
            while self.grafikler_layout.count():
                item = self.grafikler_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            c1 = BarChartWidget("Arama (Array vs HashMap) [ms]", data_arama_n, data_arama_arr, "Array", data_arama_hm, "HashMap")
            self.grafikler_layout.addWidget(c1)
            
            c2 = BarChartWidget("Sıralama (List Sort vs PriorityQueue) [ms]", data_pq_n, data_pq_sort, "Sort", data_pq_pq, "PQ")
            self.grafikler_layout.addWidget(c2)
            
            c3 = BarChartWidget("Sıralama (Bubble vs Heap Sort) [ms]", data_sort_n, data_sort_bubble, "Bubble", data_sort_heap, "Heap")
            self.grafikler_layout.addWidget(c3)
            
            c4 = BarChartWidget("Üyelik Kontrolü (Array vs Set) [ms]", data_set_n, data_set_arr, "Array", data_set_set, "Set")
            self.grafikler_layout.addWidget(c4)
            
            yaz("\n" + "=" * 62)
            yaz("  Tüm testler ve grafikler oluşturuldu!")
            yaz("=" * 62)

        except Exception as e:
            import traceback
            yaz(f"\nHata: {e}")
            yaz(traceback.format_exc())
