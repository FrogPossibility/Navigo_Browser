from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineSettings
from PyQt6.QtCore import QTimer

class ResourceOptimizer:
    @staticmethod
    def optimize_web_engine():
        """Ottimizza le impostazioni del motore web"""
        
        # Configurazione profilo
        profile = QWebEngineProfile.defaultProfile()
        settings = profile.settings()
        
        # Impostazioni valide  # Carica automaticamente le immagini # Supporto per modalità a schermo intero

        # Nota: Non ci sono impostazioni per LocalStorage in QWebEngineSettings in PyQt6

        # Configurazione della cache
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)  # Cache su disco
        
        return profile

    @staticmethod
    def setup_lazy_loading(browser):
        """Implementa caricamento lazy delle risorse"""
        def preload_critical_resources():
            # Logica di precaricamento risorse critiche
            browser.page().runJavaScript("""
                // Ottimizza caricamento risorse
                document.querySelectorAll('img').forEach(img => {
                    img.loading = 'lazy';
                });
            """)
        
        # Carica risorse dopo un breve ritardo
        QTimer.singleShot(1000, preload_critical_resources)

class ResourceInterceptor:
    """Interceptor per bloccare risorse non necessarie"""
    def __init__(self):
        self.blocked_domains = [
            'doubleclick.net', 
            'googlesyndication.com', 
            'ads.twitter.com'
        ]

    def should_block_request(self, url):
        """Determina se bloccare una richiesta"""
        return any(domain in url for domain in self.blocked_domains)