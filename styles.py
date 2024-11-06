VERTICAL_TAB_BAR_STYLE = """
    QTabBar {
        background-color: #222222;
    }
    QTabBar::tab {
        height: 50px;
        width: 200px;
        margin: 5px;
        border-radius: 10px;
        background-color: #333333;
        text-align: left;
        padding: 5px;
    }
    QTabBar::tab:selected {
        background-color: #444444;
    }
    QTabBar::close-button {
        image: url(icons/closeTab.svg);
        width: 20px;
        height: 20px;
    }
    QTabBar::close-button:hover {
        background-color: #555555;
        border-radius: 8px;
    }
"""

VERTICAL_TAB_WIDGET_STYLE = """
    QTabWidget {
        background-color: #222222;
        border: none;
    }
    QTabWidget::pane {
        border: none;
        background-color: #222222;
    }
    QTabWidget::tab-bar {
        alignment: left;
        width: 200px;
    }
"""

SPLITTER_STYLE = """
    QSplitter::handle {
        background-color: #444444;
    }
    QSplitter::handle:horizontal {
        width: 2px;
    }
    QSplitter::handle:hover {
        background-color: #666666;
    }
"""