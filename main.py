import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPalette, QColor, QCursor, QPixmap
from PyQt5.QtCore import Qt
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Imposta il tema scuro
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#222222"))
    palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Base, QColor("#333333"))
    palette.setColor(QPalette.AlternateBase, QColor("#444444"))
    palette.setColor(QPalette.Text, QColor("#FFFFFF"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())