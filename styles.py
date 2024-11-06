VERTICAL_TAB_BAR_STYLE = """
    QTabBar {
        background-color: #1e1e1e;
    }
    QTabBar::tab {
        height: 50px;
        width: 200px;
        margin: 5px;
        border-radius: 10px;
        background-color: #2d2d2d;
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        text-align: left;
        padding: 5px 15px;
        transition: background-color 0.3s;
    }
    QTabBar::tab:selected {
        background-color: #3a3a3a;
    }
    QTabBar::tab:hover {
        background-color: #454545;
    }
    QTabBar::close-button {
        image: url(icons/closeTab.svg);
        width: 16px;
        height: 16px;
    }
    QTabBar::close-button:hover {
        background-color: #ff4444;
        border-radius: 8px;
    }
"""

VERTICAL_TAB_WIDGET_STYLE = """
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
"""

SPLITTER_STYLE = """
    QSplitter::handle {
        background-color: #3a3a3a;
    }
    QSplitter::handle:horizontal {
        width: 1px;
    }
    QSplitter::handle:hover {
        background-color: #4a4a4a;
    }
"""