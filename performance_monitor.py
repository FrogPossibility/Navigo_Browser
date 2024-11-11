import psutil
import threading
import time
import logging
import gc
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from PyQt6.QtWebEngineCore import QWebEngineProfile

class PerformanceMonitor(QObject):
    def _periodic_optimization(self):
        """Azioni periodiche di ottimizzazione"""
        try:
            # Garbage Collection più aggressiva
            gc.collect(2)  # Raccolta più profonda
            
            # Chiudi tab inattive
            if self.main_window:
                self._close_inactive_tabs()
            
            # Libera risorse WebEngine
            self._cleanup_webengine_resources()

        except Exception as e:
            logging.error(f"Periodic optimization error: {e}")

    def _cleanup_webengine_resources(self):
        """Pulizia risorse WebEngine"""
        try:
            # Svuota cache
            profile = QWebEngineProfile.defaultProfile()
            profile.clearAllVisitedLinks()
            profile.clearHttpCache()
            
            # Chiudi pagine non visibili
            if hasattr(self.main_window, 'page_container'):
                page_container = self.main_window.page_container
                for i in range(page_container.count()):
                    browser = page_container.widget(i)
                    if not browser.isVisible():
                        browser.page().setWebChannel(None)
                        browser.page().deleteLater()

        except Exception as e:
            logging.error(f"WebEngine resource cleanup error: {e}")

    def _close_inactive_tabs(self):
        """Chiudi tab inattive con criteri più rigorosi"""
        try:
            tab_widget = self.main_window.tab_widget
            page_container = self.main_window.page_container

            tabs_to_close = []
            for index in range(tab_widget.count()):
                browser = page_container.widget(index)
                
                # Criteri più severi per tab inattive
                if (
                    browser.url().toString() == 'about:blank' or 
                    not browser.hasFocus() or
                    (time.time() - getattr(browser, 'last_activity', 0) > 3600)  # Inattivo da più di un'ora
                ):
                    tabs_to_close.append(index)

            # Chiudi tab in ordine inverso
            for index in sorted(tabs_to_close, reverse=True):
                tab_widget.removeTab(index)
                page_container.removeWidget(page_container.widget(index))

            logging.info(f"Closed {len(tabs_to_close)} inactive tabs")

        except Exception as e:
            logging.error(f"Error closing inactive tabs: {e}")