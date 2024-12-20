from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QSizePolicy, QSpacerItem
from PyQt6.QtGui import QIcon, QFontDatabase
from PyQt6.QtCore import QSize, QUrl

def load_custom_font():
    font_id = QFontDatabase.addApplicationFont("fonts/Poppins-SemiBold.ttf")
    return QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

class CustomTitleBar(QWidget):
    def __init__(self, parent, tab_widget):
        super(CustomTitleBar, self).__init__(parent)
        self.parent = parent
        self.tab_widget = tab_widget
        
        # Initialize pressing attribute
        self.pressing = False  # Add this line
        
        # Carica il font Poppins
        self.font_family = load_custom_font()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)

        btn_size = 36
        icon_size = 20

        self.btn_back = QPushButton(QIcon('icons/back.svg'), '')
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setFixedSize(btn_size, btn_size)
        self.btn_back.setIconSize(QSize(icon_size, icon_size))
        layout.addWidget(self.btn_back)

        self.btn_forward = QPushButton(QIcon('icons/forward.svg'), '')
        self.btn_forward.clicked.connect(self.go_forward)
        self.btn_forward.setFixedSize(btn_size, btn_size)
        self.btn_forward.setIconSize(QSize(icon_size, icon_size))
        layout.addWidget(self.btn_forward)

        self.btn_reload = QPushButton(QIcon('icons/reload.svg'), '')
        self.btn_reload.clicked.connect(self.reload_page)
        self.btn_reload.setFixedSize(btn_size, btn_size)
        self.btn_reload.setIconSize(QSize(icon_size, icon_size))
        layout.addWidget(self.btn_reload)

        self.btn_home = QPushButton(QIcon('icons/home.svg'), '')
        self.btn_home.clicked.connect(self.navigate_home)
        self.btn_home.setFixedSize(btn_size, btn_size)
        self.btn_home.setIconSize(QSize(icon_size, icon_size))
        layout.addWidget(self.btn_home)

        self.btn_new_tab = QPushButton(QIcon('icons/add.svg'), '')
        self.btn_new_tab.clicked.connect(self.parent.add_new_tab)
        self.btn_new_tab.setFixedSize(btn_size, btn_size)
        self.btn_new_tab.setIconSize(QSize(icon_size, icon_size))
        layout.addWidget(self.btn_new_tab)

        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setFixedHeight(36)
        self.url_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 5px 10px;
                border-radius: 18px;
                font-size: 16px;
                font-family: '{self.font_family}';
                border: 1px solid #3a3a3a;
            }}
            QLineEdit:focus {{
                border: 1px solid #4a4a4a;
            }}
        """)
        layout.addWidget(self.url_bar, 1)

        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))  # Modifica qui

        self.btn_min = QPushButton(QIcon('icons/topbar/min.svg'), '')
        self.btn_min.clicked.connect(self.parent.showMinimized)
        self.btn_min.setFixedSize(btn_size, btn_size)

        self.btn_max = QPushButton(QIcon('icons/topbar/max.svg'), '')
        self.btn_max.clicked.connect(self.maximize_restore)
        self.btn_max.setFixedSize(btn_size, btn_size)

        self.btn_close = QPushButton(QIcon('icons/topbar/close.svg'), '')
        self.btn_close.clicked.connect(self.parent.close)
        self.btn_close.setFixedSize(btn_size, btn_size)

    
        layout.addWidget(self.btn_min)
        layout.addWidget(self.btn_max)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)
        self.setFixedHeight(50)

        buttons_style = """
            QPushButton {
                border: none;
                background-color: transparent;
                border-radius: 18px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:pressed {
                background-color: #454545;
            }
        """
        for btn in [self.btn_back, self.btn_forward, self.btn_reload, self.btn_home, 
                   self.btn_new_tab, self.btn_min, self.btn_max, self.btn_close]:
            btn.setStyleSheet(buttons_style)

    def go_back(self):
        if self.current_browser():
            self.current_browser().back()

    def go_forward(self):
        if self.current_browser():
            self.current_browser().forward()

    def reload_page(self):
        if self.current_browser():
            self.current_browser().reload()


    def maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        self.windowPos = self.parent.frameGeometry().topLeft()
        
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.parent.isMaximized():
                self.parent.showNormal()
            self.parent.windowHandle().startSystemMove()

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def navigate_home(self):
        if self.current_browser():
            self.current_browser().setUrl(QUrl('about:blank'))

    def current_browser(self):
        current_index = self.tab_widget.currentIndex()
        return self.parent.page_container.widget(current_index)

    def navigate_to_url(self):
        browser = self.current_browser()
        if not browser:
            return
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'https://www.google.com/search?q=' + url
        browser.setUrl(QUrl(url))