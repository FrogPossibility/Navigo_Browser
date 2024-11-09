import sys
import os
import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt, QTimer
from main_window import MainWindow
import gc

class PerformanceOptimizedApp(QApplication):
    def __init__(self, argv):
        # Imposta attributi DPI PRIMA di creare l'applicazione
        #QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        #QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        super().__init__(argv)
        
        # Impostazioni per ridurre il consumo di risorse
        #self.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

def setup_logging():
    """Configura il logging per l'applicazione"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'navigo_browser.log')),
            logging.StreamHandler()
        ]
    )

def setup_performance_optimizations(app, window):
    """Configura ottimizzazioni di performance"""
    # Garbage Collection periodica
    def periodic_gc():
        collected = gc.collect()
        logging.info(f"Garbage Collection: collected {collected} objects")

    # Timer per garbage collection ogni 5 minuti
    gc_timer = QTimer()
    gc_timer.timeout.connect(periodic_gc)
    gc_timer.start(300000)  # 5 minuti

    # Gestione memoria
    app.setQuitOnLastWindowClosed(True)

def configure_dark_theme(app):
    """Configura il tema scuro dell'applicazione"""
    palette = QPalette()
    
    # Definizione colori tema scuro
    dark_palette = {
        QPalette.ColorRole.Window: QColor("#222222"),
        QPalette.ColorRole.WindowText: QColor("#FFFFFF"),
        QPalette.ColorRole.Base: QColor("#333333"),
        QPalette.ColorRole.AlternateBase: QColor("#444444"),
        QPalette.ColorRole.Text: QColor("#FFFFFF"),
        QPalette.ColorRole.Button: QColor("#2D2D2D"),
        QPalette.ColorRole.ButtonText: QColor("#FFFFFF"),
        QPalette.ColorRole.BrightText: QColor("#FFFFFF"),
        QPalette.ColorRole.Highlight: QColor("#666666"),
        QPalette.ColorRole.HighlightedText: QColor("#FFFFFF")
    }
    
    # Applica colori
    for role, color in dark_palette.items():
        palette.setColor(role, color)
    
    app.setPalette(palette)
    app.setStyle('Fusion')  # Stile che supporta bene i temi personalizzati

def main():
    """Punto di ingresso principale dell'applicazione"""


    try:
        # Configurazione logging
        setup_logging()
        logging.info("Avvio Navigo Browser")

         # Crea cartella logs se non esiste
        os.makedirs('logs', exist_ok=True)

        # Configurazione logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/navigo_browser.log'),
                logging.StreamHandler()
            ]
        )

        # Creazione applicazione ottimizzata
        app = PerformanceOptimizedApp(sys.argv)
        
        # Configurazione tema scuro
        configure_dark_theme(app)

        # Creazione finestra principale
        window = MainWindow()
        window.show()

        # Configurazione ottimizzazioni
        setup_performance_optimizations(app, window)

        # Gestore eccezioni globale
        sys.excepthook = global_exception_handler

        # Avvio applicazione
        exit_code = app.exec()
        logging.info(f"Chiusura Navigo Browser. Exit Code: {exit_code}")
        
        return exit_code

    except Exception as e:
        logging.critical(f"Errore critico durante l'avvio: {e}", exc_info=True)
        return 1

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Gestore eccezioni globale"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )

if __name__ == "__main__":
    # Imposta il percorso di lavoro alla directory dello script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Esegui l'applicazione
    sys.exit(main())