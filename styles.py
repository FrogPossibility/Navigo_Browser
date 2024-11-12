VERTICAL_TAB_BAR_STYLE = """
    QTabBar {
        background-color: #222222; /* Sfondo scuro */
        border: none;  /* Rimuovere bordi */
    }
    QTabBar::tab {
        height: 50px;
        width: 200px;
        margin: 5px; /* Aggiungere margine per separazione */
        border-radius: 10px; /* Arrotondare gli angoli */
        background-color: #333333; /* Colore di base per le schede */
        color: #ffffff; /* Colore del testo */
        font-size: 14px;
        font-weight: bold;
        text-align: left;
        padding: 5px 15px;
        transition: background-color 0.3s; /* Transizione per hover */
    }
    QTabBar::tab:selected {
        background-color: #444444; /* Colore per scheda selezionata */
    }
    QTabBar::tab:hover {
        background-color: #454545; /* Colore al passaggio del mouse */
    }
    QTabBar::close-button {
        image: url(icons/closeTab.svg);
        width: 16px;
        height: 16px;
        margin-right: 5px; /* Spaziatura per il pulsante */
    }
    QTabBar::close-button:hover {
        background-color: #ff4444; /* Colore di hover per il pulsante */
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
        background-color: #1e1e1e; /* Colore di sfondo */
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