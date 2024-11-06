from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor

def set_custom_cursors(window):
    """
    Imposta i cursori personalizzati per diversi elementi della finestra
    """
    # Cursore predefinito per la finestra principale
    window.setCursor(Qt.ArrowCursor)

    # Cursore per la barra degli URL
    if hasattr(window.title_bar, 'url_bar'):
        window.title_bar.url_bar.setCursor(Qt.IBeamCursor)

    # Cursore per i pulsanti
    buttons = [
        window.title_bar.btn_back,
        window.title_bar.btn_forward,
        window.title_bar.btn_reload,
        window.title_bar.btn_home,
        window.title_bar.btn_new_tab,
        window.title_bar.btn_min,
        window.title_bar.btn_max,
        window.title_bar.btn_close
    ]
    
    for button in buttons:
        button.setCursor(Qt.PointingHandCursor)

    # Cursore per le tab
    window.tab_widget.setCursor(Qt.ArrowCursor)
    
    # Cursore per il contenuto web
    for i in range(window.page_container.count()):
        browser = window.page_container.widget(i)
        if browser:
            browser.setCursor(Qt.ArrowCursor)

    # Cursore per lo splitter
    window.splitter.handle(1).setCursor(Qt.SplitHCursor)

def apply_cursors(window):
    """
    Applica i cursori personalizzati alla finestra
    """
    set_custom_cursors(window)