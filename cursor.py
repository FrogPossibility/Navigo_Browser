import os
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtCore import Qt

class CustomCursor:
    def __init__(self):
        # Percorso della cartella dei cursori
        self.cursor_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cursors')
        
        # Dizionario per memorizzare i cursori
        self.cursors = {}
        
        # Carica tutti i cursori
        self.load_cursors()

    def load_cursors(self):
        cursor_files = {
            'default': 'icons/cursors/default.png',
            'pointer': 'icons/cursors/pointer.png',
            'text': 'icons/cursors/text.png',
            'resize': 'icons/cursors/resize.png',
            'wait': 'icons/cursors/default.png'
        }
        
        for cursor_name, file_name in cursor_files.items():
            file_path = os.path.join(self.cursor_path, file_name)
            if os.path.exists(file_path):
                pixmap = QPixmap(file_path)
                # Puoi specificare il punto di hotspot per ogni cursore
                # Il punto di hotspot è la posizione esatta del click nel cursore
                hotspot_x = hotspot_y = 0
                
                # Regola il punto di hotspot in base al tipo di cursore
                if cursor_name == 'pointer':
                    hotspot_x = 5
                    hotspot_y = 0
                elif cursor_name == 'text':
                    hotspot_x = 16
                    hotspot_y = 16
                
                self.cursors[cursor_name] = QCursor(pixmap, hotspot_x, hotspot_y)

    def apply_cursors(self, app):
        # Imposta il cursore predefinito
        if 'default' in self.cursors:
            app.setOverrideCursor(self.cursors['default'])
        
        # Imposta gli stili CSS per i diversi elementi dell'interfaccia
        app.setStyleSheet("""
            QPushButton { cursor: pointer; }
            QLineEdit { cursor: text; }
            QSplitter::handle { cursor: resize; }
        """)

def set_custom_cursors(app):
    cursor_manager = CustomCursor()
    cursor_manager.apply_cursors(app)