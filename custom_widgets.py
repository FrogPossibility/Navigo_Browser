from PyQt5.QtWidgets import QTabBar, QTabWidget, QStylePainter, QStyleOptionTab
from PyQt5.QtCore import QSize, QRect, QRectF, Qt
from PyQt5.QtGui import QPainterPath, QColor, QFontDatabase, QFont
from styles import VERTICAL_TAB_BAR_STYLE, VERTICAL_TAB_WIDGET_STYLE
from custom_titlebar import load_custom_font

class VerticalTabBar(QTabBar):
    def __init__(self, parent=None):
        super(VerticalTabBar, self).__init__(parent)
        self.font_family = load_custom_font()
        self.setMinimumWidth(100)  # Modifica questa linea
        self.setExpanding(True)
        self.setStyleSheet(f"""
            QTabBar {{
                background-color: #222222;
            }}
            QTabBar::tab {{
                height: 50px;
                width: 200px;
                margin: 5px;
                border-radius: 10px;
                background-color: #333333;
                text-align: left;
                padding: 5px;
                font-family: '{self.font_family}';
            }}
            QTabBar::tab:selected {{
                background-color: #444444;
            }}
            QTabBar::close-button {{
                image: url(icons/closeTab.svg);
                width: 20px;
                height: 20px;
            }}
            QTabBar::close-button:hover {{
                background-color: #555555;
                border-radius: 8px;
            }}
        """)

    def tabSizeHint(self, index):
        width = max(100, self.width())  # Assicura una larghezza minima di 100px
        return QSize(width, 50)

    def paintEvent(self, event):
        painter = QStylePainter(self)
        
        for index in range(self.count()):
            option = QStyleOptionTab()
            self.initStyleOption(option, index)
            tab_rect = self.tabRect(index)
            
            # Background della tab
            path = QPainterPath()
            path.addRoundedRect(QRectF(tab_rect), 10, 10)
            painter.fillPath(path, QColor("#333333") if index != self.currentIndex() else QColor("#444444"))
            
            # Icona
            if not self.tabIcon(index).isNull():
                icon_rect = QRect(tab_rect.left() + 5, tab_rect.top() + 15, 20, 20)
                self.tabIcon(index).paint(painter, icon_rect)
            
            # Testo con il nuovo font
            text = self.tabText(index)
            text_rect = QRect(tab_rect.left() + 30, tab_rect.top(), tab_rect.width() - 60, tab_rect.height())
            painter.setPen(Qt.white)
            painter.setFont(QFont(self.font_family))  # Imposta il font per il testo
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, text)
            
            # Pulsante di chiusura
            close_button = self.tabButton(index, QTabBar.RightSide)
            if close_button:
                close_rect = QRect(tab_rect.right() - 25, tab_rect.top() + 15, 20, 20)
                close_button.setGeometry(close_rect)
                close_button.show()

class VerticalTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(VerticalTabWidget, self).__init__(parent)
        self.setTabBar(VerticalTabBar())
        self.setTabPosition(QTabWidget.West)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setMinimumWidth(100)
        self.setMaximumWidth(200)
        self.setStyleSheet("""
            QTabWidget {
                background-color: #1e1e1e;
                border: none;
            }
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabWidget::tab-bar {
                alignment: left;
                width: 200px;
            }
        """)