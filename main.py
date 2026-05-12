"""
Kamp Alanı Rezervasyon Sistemi
Giriş noktası: python main.py → GUI açılır.
"""
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui.uygulama import AnaUygulama


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Kamp Alanı Rezervasyon Sistemi")
    app.setOrganizationName("Gazi Üniversitesi BMT210")

    pencere = AnaUygulama()
    pencere.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
