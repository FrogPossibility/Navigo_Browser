import psutil
import threading
import time
import logging
import gc
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class PerformanceMonitor(QObject):
    performance_warning = pyqtSignal(str, int)
    
    def __init__(self, main_window=None, threshold_cpu=80, threshold_memory=85):
        super().__init__()
        self.main_window = main_window
        self.threshold_cpu = threshold_cpu
        self.threshold_memory = threshold_memory
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # Configurazione logging
        logging.basicConfig(
            filename='logs/performance.log', 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

        # Timer per azioni periodiche
        self.optimization_timer = QTimer()
        self.optimization_timer.timeout.connect(self._periodic_optimization)

    def start_monitoring(self):
        """Avvia il monitoraggio delle prestazioni"""
        try:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitor_performance)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            
            # Avvia timer ottimizzazioni
            self.optimization_timer.start(300000)  # Ogni 5 minuti
            
            logging.info("Performance monitoring started")
        except Exception as e:
            logging.error(f"Error starting performance monitoring: {e}")

    def stop_monitoring(self):
        """Ferma il monitoraggio delle prestazioni"""
        try:
            self.is_monitoring = False
            if self.monitoring_thread:
                self.monitoring_thread.join()
            
            # Ferma timer
            self.optimization_timer.stop()
            
            logging.info("Performance monitoring stopped")
        except Exception as e:
            logging.error(f"Error stopping performance monitoring: {e}")

    def _monitor_performance(self):
        """Monitora l'utilizzo di CPU e memoria"""
        while self.is_monitoring:
            try:
                cpu_usage = psutil.cpu_percent()
                memory_usage = psutil.virtual_memory().percent
                
                # Emetti segnali di warning
                if cpu_usage > self.threshold_cpu:
                    warning_msg = f"High CPU Usage: {cpu_usage}%"
                    logging.warning(warning_msg)
                    self.performance_warning.emit(warning_msg, cpu_usage)

                if memory_usage > self.threshold_memory:
                    warning_msg = f"High Memory Usage: {memory_usage}%"
                    logging.warning(warning_msg)
                    self.performance_warning.emit(warning_msg, memory_usage)

                time.sleep(60)  # Controlla ogni minuto
            except Exception as e:
                logging.error(f"Performance monitoring error: {e}")
                time.sleep(60)

    def _periodic_optimization(self):
        """Azioni periodiche di ottimizzazione"""
        try:
            # Garbage Collection
            collected = gc.collect()
            logging.info(f"Periodic Garbage Collection: {collected} objects collected")

            # Se main_window è disponibile, chiudi tab inattive
            if self.main_window:
                self._close_inactive_tabs()

        except Exception as e:
            logging.error(f"Periodic optimization error: {e}")

    def _close_inactive_tabs(self):
        """Chiudi tab inattive in modo sicuro"""
        try:
            # Verifica l'esistenza degli attributi necessari
            if not hasattr(self.main_window, 'tab_widget') or not hasattr(self.main_window, 'page_container'):
                logging.warning("Main window lacks tab_widget or page_container")
                return

            tab_widget = self.main_window.tab_widget
            page_container = self.main_window.page_container

            # Trova e chiudi tab inattive
            tabs_to_close = []
            for index in range(tab_widget.count()):
                browser = page_container.widget(index)
                # Criteri per tab inattiva (personalizza secondo necessità)
                if (browser.url().toString() == 'about:blank' or 
                    not browser.hasFocus()):
                    tabs_to_close.append(index)

            # Chiudi tab in ordine inverso per evitare problemi di indicizzazione
            for index in sorted(tabs_to_close, reverse=True):
                tab_widget.removeTab(index)
                page_container.removeWidget(page_container.widget(index))

            logging.info(f"Closed {len(tabs_to_close)} inactive tabs")

        except Exception as e:
            logging.error(f"Error closing inactive tabs: {e}")

    def set_main_window(self, main_window):
        """Imposta riferimento alla finestra principale"""
        self.main_window = main_window