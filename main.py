import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor, QCursor, QPixmap
from PyQt5.QtCore import Qt  # Aggiungi questa linea
from main_window import MainWindow

def set_custom_cursor(app, cursor_name='default'):
    cursor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'cursors', f'{cursor_name}.png')
    
    # Carica e ridimensiona l'immagine del cursore
    cursor_pixmap = QPixmap(cursor_path).scaled(50, 50, aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
    
    # Crea un cursore con un offset per centrarlo
    custom_cursor = QCursor(cursor_pixmap, 10, 10)
    
    # Imposta il cursore predefinito
    app.setOverrideCursor(custom_cursor)

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

    # Imposta il cursore personalizzato
    set_custom_cursor(app)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())