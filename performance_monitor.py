import psutil
import threading
import time
import logging
import gc
from PyQt5.QtCore import QObject, pyqtSignal

class PerformanceMonitor(QObject):
    performance_warning = pyqtSignal(str, int)
    
    def __init__(self, threshold_cpu=80, threshold_memory=85):
        super().__init__()
        self.threshold_cpu = threshold_cpu
        self.threshold_memory = threshold_memory
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # Configurazione logging
        logging.basicConfig(
            filename='browser_performance.log', 
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

    def start_monitoring(self):
        """Avvia il monitoraggio delle prestazioni"""
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitor_performance)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        logging.info("Performance monitoring started")

    def stop_monitoring(self):
        """Ferma il monitoraggio delle prestazioni"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logging.info("Performance monitoring stopped")

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
                    self._take_performance_action()

                if memory_usage > self.threshold_memory:
                    warning_msg = f"High Memory Usage: {memory_usage}%"
                    logging.warning(warning_msg)
                    self.performance_warning.emit(warning_msg, memory_usage)
                    self._take_performance_action()

                time.sleep(60)  # Controlla ogni minuto
            except Exception as e:
                logging.error(f"Performance monitoring error: {e}")
                time.sleep(60)

    def _take_performance_action(self):
        """Azioni per mitigare alto utilizzo risorse"""
        # Garbage Collection forzata
        gc.collect()
        
        # Rilascia risorse non utilizzate
        try:
            # Chiudi tab non attive
            if hasattr(self, 'main_window'):
                self.main_window.close_inactive_tabs()
            
            # Libera cache del browser
            if hasattr(self, 'web_profile'):
                self.web_profile.clearHttpCache()
        except Exception as e:
            logging.error(f"Performance mitigation error: {e}")

    def set_main_window(self, main_window):
        """Imposta riferimento alla finestra principale"""
        self.main_window = main_window

    def set_web_profile(self, web_profile):
        """Imposta profilo web per pulizia cache"""
        self.web_profile = web_profile