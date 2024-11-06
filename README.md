Web Browser Project
===================

Questo è un progetto di browser web personalizzato sviluppato in Python utilizzando PyQt5.

Caratteristiche principali:
---------------------------
1. Interfaccia utente moderna con tema scuro
2. Barra delle schede verticale personalizzata
3. Barra del titolo personalizzata con controlli di navigazione
4. Supporto per più schede
5. Pagina "Nuova scheda" personalizzata
6. Zoom predefinito personalizzabile
7. Supporto per diversi motori di ricerca

Requisiti:
----------
- Python 3.7+
- PyQt5
- PyQtWebEngine

Installazione:
--------------
1. Assicurati di avere Python installato sul tuo sistema
2. Installa le dipendenze necessarie eseguendo:
   pip install PyQt5 PyQtWebEngine

Esecuzione:
-----------
Per avviare il browser, esegui il file main.py:
python main.py

Struttura del progetto:
-----------------------
- main.py: Script principale per avviare l'applicazione
- main_window.py: Definizione della finestra principale del browser
- custom_titlebar.py: Implementazione della barra del titolo personalizzata
- custom_widgets.py: Widget personalizzati come la barra delle schede verticale
- styles.py: Definizioni degli stili CSS per i vari componenti
- blank.html: Pagina HTML per la "Nuova scheda"
- icons/: Cartella contenente le icone utilizzate nel browser
- fonts/: Cartella contenente i font personalizzati

Personalizzazione:
------------------
- Puoi modificare l'aspetto del browser modificando gli stili in styles.py
- Per cambiare il comportamento della pagina "Nuova scheda", modifica il file blank.html
- Aggiungi o rimuovi motori di ricerca modificando la variabile searchEngines in blank.html

Contribuire:
------------
Sentiti libero di contribuire al progetto aprendo issues o inviando pull requests su GitHub.

Licenza:
--------
Questo progetto è rilasciato sotto la licenza MIT. Vedi il file LICENSE per i dettagli.
