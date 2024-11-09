import os
from PyQt6.QtCore import Qt, QUrl, QRectF, QTimer
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QStackedWidget, QPushButton, QLineEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings  # Import corretto
from PyQt6.QtGui import QPainterPath, QRegion, QIcon
from custom_widgets import VerticalTabWidget
from custom_titlebar import CustomTitleBar

from performance_monitor import PerformanceMonitor
from resource_optimizer import ResourceOptimizer, ResourceInterceptor
import logging



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Crea un profilo per le impostazioni del motore web
        profile = QWebEngineProfile.defaultProfile()



        # Inizializza monitor prestazioni
        self.performance_monitor = PerformanceMonitor(self)
        self.performance_monitor.set_main_window(self)
        
        # Avvia monitoraggio
        self.performance_monitor.start_monitoring()
        
        # Ottimizza motore web
        self.web_profile = ResourceOptimizer.optimize_web_engine()
        self.performance_monitor.set_main_window(self.web_profile)
        
        # Interceptor risorse
        self.resource_interceptor = ResourceInterceptor()
        
        
        # Timer per ottimizzazioni periodiche
        self.optimization_timer = QTimer()
        self.optimization_timer.timeout.connect(self.periodic_optimization)
        self.optimization_timer.start(300000)  # Ogni 5 minuti

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        """)
        

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Aggiungi la title bar
        self.title_bar = CustomTitleBar(self, None)
        main_layout.addWidget(self.title_bar)
        
        # Container principale
        content_container = QWidget()
        content_layout = QHBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Crea il QSplitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(2)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #444444;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #666666;
            }
        """)

        # Crea il widget delle tab
        self.tab_widget = VerticalTabWidget()
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        self.tab_widget.setMinimumWidth(50)
        self.tab_widget.setMaximumWidth(200)

        self.tab_widget.tabBar().tabMoved.connect(self.handle_tab_moved)

         # Aggiungi questa variabile per memorizzare il percorso di blank.html
        self.blank_html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blank.html')
        self.blank_html_url = QUrl.fromLocalFile(self.blank_html_path)
        
        # Container per il contenuto della pagina
        self.page_container = QStackedWidget()
        self.page_container.setMinimumWidth(400)
    
        
        # Aggiungi i widget al splitter
        self.splitter.addWidget(self.tab_widget)
        self.splitter.addWidget(self.page_container)

        # Collega il segnale splitterMoved
        self.splitter.splitterMoved.connect(self.handle_splitter_moved)

        QTimer.singleShot(50, self.set_initial_splitter_sizes)
        # Imposta le proporzioni iniziali
        self.splitter.setSizes([200, self.width() - 200])
    
        
        self.splitter.setCollapsible(0, False)

        
        content_layout.addWidget(self.splitter)
        main_layout.addWidget(content_container)
        
        # Aggiorna il riferimento al tab_widget nella title bar
        self.title_bar.tab_widget = self.tab_widget
        
        self.setCentralWidget(main_widget)


        # Aggiungi la prima tab
        self.add_new_tab()
        
        # Applica gli angoli arrotondati
        self.apply_rounded_corners()


    def add_new_tab(self, url=None):
        browser = QWebEngineView()

        self.set_default_zoom(browser)

        # Ottimizza caricamento risorse per ogni tab
        ResourceOptimizer.setup_lazy_loading(browser)
        
        # Modifica questa parte per gestire le nuove tab
        if url is None or url == '' or url == 'about:blank':
            browser.setUrl(self.blank_html_url)
        else:
            browser.setUrl(QUrl(str(url)))

        # Aggiungi questo handler per gestire i cambi di URL
        browser.urlChanged.connect(lambda qurl, b=browser: self.handle_url_change(b, qurl))

        # Implementa interceptor
        browser.page().urlChanged.connect(
            lambda url: self.check_resource_loading(url, browser)
        )

        index = self.page_container.addWidget(browser)
        
        browser.iconChanged.connect(lambda: self.update_tab_icon(browser))
        browser.urlChanged.connect(lambda qurl, browser=browser: 
            self.title_bar.url_bar.setText(qurl.toString()) if browser == self.current_browser() else None)
        browser.titleChanged.connect(lambda title: self.update_tab_title(index, title))
        
        placeholder = QWidget()
        default_icon = QIcon('icons/home.svg')
        tab_index = self.tab_widget.addTab(placeholder, default_icon, "")
        
        self.tab_widget.setCurrentIndex(tab_index)
        self.page_container.setCurrentIndex(index)
        
        return browser
    
    def handle_url_change(self, browser, qurl):
        # Quando l'URL cambia in about:blank, reindirizza a blank.html
        if qurl.toString() == 'about:blank':
            browser.setUrl(self.blank_html_url)

    def on_tab_changed(self, index):
        self.page_container.setCurrentIndex(index)

    def current_browser(self):
        return self.page_container.currentWidget()

    def close_tab(self, index):
        if self.tab_widget.count() > 1:
            browser = self.page_container.widget(index)
            self.page_container.removeWidget(browser)
            browser.deleteLater()
            self.tab_widget.removeTab(index)
        else:
            self.close()

    def update_tab_icon(self, browser):
        index = self.page_container.indexOf(browser)
        if index > -1:
            icon = browser.icon()
            if not icon.isNull():
                self.tab_widget.setTabIcon(index, icon)
            self.update_tab_title(index, browser.title())

    def update_tab_title(self, index, title):
        if index >= 0:
            truncated_title = (title[:15] + '...') if len(title) > 20 else title
            self.tab_widget.setTabText(index, truncated_title)


    def apply_rounded_corners(self):
        radius = 20
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        self.apply_rounded_corners()
        super(MainWindow, self).resizeEvent(event)

    def set_initial_splitter_sizes(self):
        total_width = self.width()
        self.splitter.setSizes([200, total_width - 200])

    def handle_splitter_moved(self, pos, index):
        sizes = self.splitter.sizes()
        if sizes[0] < 50:
            self.splitter.setSizes([50, sizes[1] + (sizes[0] - 50)])
        elif sizes[0] > 200:
            self.splitter.setSizes([200, sizes[1] + (sizes[0] - 200)])


    def set_default_zoom(self, browser):
        browser.setZoomFactor(1.0)  # Puoi regolare questo valore se necessario

    def handle_tab_moved(self, from_index, to_index):
        # Sposta anche il widget della pagina web
        widget = self.page_container.widget(from_index)
        self.page_container.removeWidget(widget)
        self.page_container.insertWidget(to_index, widget)

    def check_resource_loading(self, url, browser):
        """Verifica e blocca risorse non necessarie"""
        url_str = url.toString()
        if self.resource_interceptor.should_block_request(url_str):
            browser.page().runJavaScript(f"""
                console.log('Blocked resource: {url_str}');
            """)

    def close_inactive_tabs(self):
        """Chiude tab inattive per risparmiare risorse"""
        for index in range(self.tab_widget.count()):
            browser = self.page_container.widget(index)
            # Logica per determinare tab inattive
            if not browser.hasFocus() and browser.url().toString() == 'about:blank': self.tab_widget.removeTab(index)
            browser.deleteLater()

    def periodic_optimization(self):
        """Esegui ottimizzazioni periodiche"""
        self.performance_monitor._take_performance_action()

    def closeEvent(self, event):
        """Gestisci chiusura finestra"""
        try:
            # Ferma monitoraggio prestazioni
            self.performance_monitor.stop_monitoring()
            event.accept()
        except Exception as e:
            logging.error(f"Error during window close: {e}")
            event.accept()
