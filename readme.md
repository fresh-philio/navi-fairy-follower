# ✨ Navi Fairy Follower (Windows)

Ein leichtgewichtiger Desktop-Begleiter für Windows, inspiriert von **Navi** aus *The Legend of Zelda: Ocarina of Time*. Die kleine Fee schwebt als klickdurchlässiges Overlay über deinen Fenstern und der Taskleiste und folgt sanft deinem Mauszeiger.

---

## 📂 Enthaltene Dateien

Im Repository stehen drei Varianten zur Auswahl:

| Datei | Beschreibung | Empfohlen für |
| :--- | :--- | :--- |
| **`Navi Mouse Follower.exe`** | Eigenständige, portable Windows-Anwendung (entspricht der *Advanced*-Version). | Alle, die direkt loslegen wollen – **ohne Python-Installation**. |
| **`navi_follower_advanced.pyw`** | Vollversion mit weichem Glow, halbtransparenten Flügeln, Glitzerstaub & Tray-Menü. | Nutzer mit Python, die den Code selbst anpassen möchten. |
| **`navi_follower_simple.pyw`** | Minimalistische Basis-Version mit schlichter Vektor-Optik (ohne Transparenz/Partikel). | Schwächere Rechner oder als extrem schlanker Einstiegscode. |

### Unterschiede zwischen `advanced` und `simple`

* **`navi_follower_advanced.pyw` (und `.exe`)**:
  * **Optik:** Mehrschichtiger, weich auslaufender Leuchtschein (Alpha-Blending) und halbtransparente Libellenflügel im *Ocarina of Time*-Stil.
  * **Effekte:** Hinterlässt bei schnellen Mausbewegungen funkelnden Glitzerstaub.
  * **Steuerung:** Eigenes System-Tray-Icon in der Taskleiste zum Wechseln der Feen-Farben (*Navi/Blau, Ciela/Gold, Taya/Pink, Tael/Violett, Heilfee/Smaragd*) und zum sauberen Beenden.
  * **Z-Order:** Bleibt dauerhaft über der Windows-Taskleiste sichtbar.
* **`navi_follower_simple.pyw`**:
  * **Optik:** Klassische 2D-Formen ohne halbtransparente Ränder (`tkinter`).
  * **Steuerung:** Kein Tray-Icon – wird bei Bedarf über den Windows Task-Manager (`pythonw.exe`) beendet.

---

## 🚀 Installation & Start

### Option A: Portable `.exe` (Keine Installation nötig)
1. Lade die **`Navi Mouse Follower.exe`** herunter.
2. Starte sie per **Doppelklick**.
3. Unten rechts in der Windows-Taskleiste erscheint ein kleines leuchtendes Feen-Icon:
   * **Linksklick:** Schaltet direkt zur nächsten Farbe weiter.
   * **Rechtsklick:** Öffnet das Menü für die direkte Farbauswahl oder zum Beenden.

*(Hinweis: Da die `.exe` nicht digital signiert ist, zeigt Windows Defender beim ersten Start eventuell eine SmartScreen-Warnung an. Klicke dort einfach auf **Weitere Informationen → Trotzdem ausführen**.)*

### Option B: Python-Scripts (`.pyw`) ausführen
Stelle sicher, dass **Python 3** installiert ist, und installiere je nach gewünschter Version das passende Paket über die Eingabeaufforderung (`cmd`):

* **Für `navi_follower_advanced.pyw`:**
  ```bash
  pip install PyQt6
  ```
* **Für `navi_follower_simple.pyw`:**
  ```bash
  pip install pywin32
  ```

Anschließend lässt sich die jeweilige `.pyw`-Datei per **Doppelklick** starten (die Endung `.pyw` sorgt dafür, dass sich kein schwarzes Konsolenfenster öffnet).

---

## ⚙️ Optional: Zum Windows-Autostart hinzufügen

Wenn Navi automatisch beim Hochfahren von Windows starten soll:

1. Drücke **`Win + R`**, gib **`shell:startup`** ein und bestätige mit **Enter**.
2. **Wenn du die `.exe` nutzt:** Erstelle eine Verknüpfung zur `Navi Mouse Follower.exe` und ziehe sie in den geöffneten Autostart-Ordner.
3. **Wenn du die `.pyw` nutzt:**
   * Klicke im Autostart-Ordner mit Rechtsklick auf eine freie Stelle → **Neu → Verknüpfung**.
   * Gib als Speicherort den Pfad zu deiner `pythonw.exe` und dahinter den Pfad zum Script an (beides in Anführungszeichen):
     ```text
     "C:\Pfad\zu\pythonw.exe" "C:\Pfad\zum\Ordner\navi_follower_advanced.pyw"
     ```
   * Vergib einen Namen (z. B. *Navi Desktop Fee*) und klicke auf **Fertig stellen**.