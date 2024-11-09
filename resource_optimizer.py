from PyQt5.QtWebEngineWidgets import QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QTimer

class ResourceOptimizer:
    @staticmethod
    def optimize_web_engine():
        """Ottimizza le impostazioni del motore web"""
        settings = QWebEngineSettings.globalSettings()
        
        # Ottimizzazioni di base
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, False)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, False)
        
        # Configurazione profilo
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100 MB
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        
        return profile

    @staticmethod
    def setup_lazy_loading(browser):
        def preload_critical_resources():
            browser.page().runJavaScript("""
                document.querySelectorAll('img').forEach(img => {
                    img.loading = 'lazy';
                });
            """)
        
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