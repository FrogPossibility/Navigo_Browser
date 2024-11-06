from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QUrl

class CustomTitleBar(QWidget):
    def __init__(self, parent, tab_widget):
        super(CustomTitleBar, self).__init__(parent)
        self.parent = parent
        self.tab_widget = tab_widget
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        btn_size = 40
        icon_size = 24

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

        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setFixedWidth(800)
        self.url_bar.setStyleSheet("background-color: #333333; color: #FFFFFF; padding: 5px; border-radius: 10px; font-size: 20px;")
        layout.addWidget(self.url_bar)

        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

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

        buttons_style = "border: none; background-color: transparent;"
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
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            if self.parent.isMaximized():
                self.parent.showNormal()
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.move(self.parent.pos() + movement)
            self.start = end

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