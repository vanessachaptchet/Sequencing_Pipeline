Parfait 👍
Voici **TOUT le contenu du README**, **clé en main**.
👉 Tu **copies–colles exactement** ceci dans `README.md`.
👉 **Tu ne modifies rien** si tu ne veux pas.

---

````markdown
# Sequencing Run Processing Pipeline (Prototype)

## Kontext und Ziel
Dieses Projekt wurde im Rahmen einer technischen Aufgabe für die Position  
**Junior Bioinformatiker / Data Scientist** entwickelt.

Ziel dieser Aufgabe ist die Konzeption und Implementierung einer einfachen,
aber robusten Verarbeitungskomponente für Sequenzierläufe mit Fokus auf:

- saubere und nachvollziehbare Code-Struktur  
- robuste Fehlerbehandlung  
- klare Statusberichterstattung  
- gute Wartbarkeit und Erweiterbarkeit  

Der Schwerpunkt liegt nicht auf biologischer Komplexität, sondern auf
Software-Engineering-Prinzipien, wie sie in bioinformatischen Pipelines
im Produktionsumfeld angewendet werden.

---

## Grundlegender Ansatz
Die Pipeline verarbeitet Sequenzierdaten in einer klaren Hierarchie:

- Das **Input-Verzeichnis** enthält mehrere Sequenzierläufe (Runs)
- Jeder **Run** besteht aus mehreren FASTQ-Dateien (Samples)
- Jedes Sample wird **unabhängig** verarbeitet
- Fehler auf Sample-Ebene stoppen **nicht** den gesamten Run

Durch diesen Ansatz ist die Pipeline robust gegenüber fehlerhaften oder
inkompletten Eingabedaten und kann auch **Teilergebnisse** korrekt verarbeiten.
Runs können daher den Status **SUCCESS**, **FAILED** oder **PARTIAL** annehmen.

---

## Projektstruktur
Der Code ist modular aufgebaut, um Verantwortlichkeiten klar zu trennen:

- `main.py`  
  Einstiegspunkt der Anwendung.  
  Verarbeitet Kommandozeilenargumente, initialisiert das Logging und steuert
  den gesamten Ablauf der Pipeline.

- `processor/run_scanner.py`  
  Erkennt Sequenzierläufe und FASTQ-Dateien im Input-Verzeichnis.

- `processor/fastq_utils.py`  
  Liest FASTQ-Dateien und berechnet einfache technische Metriken
  (z. B. Anzahl der Reads, durchschnittliche Read-Länge).

- `processor/sample_processor.py`  
  Verarbeitet einzelne FASTQ-Samples und kapselt die Sample-spezifische
  Fehlerbehandlung.

- `processor/output_writer.py`  
  Aggregiert die Ergebnisse auf Run-Ebene und erzeugt strukturierte
  JSON-Ausgabedateien.

- `processor/logging_utils.py`  
  Konfiguriert das Logging für Konsolenausgabe und Logdateien.

---

## Ausführung der Pipeline

```bash
python main.py --input input --outdir output --log logs/pipeline.log
````

### Annahmen zum Input

* `--input` enthält ein Verzeichnis pro Sequenzierlauf (z. B. `20251212_run001`)
* FASTQ-Dateien können sich in Unterverzeichnissen befinden (rekursive Suche)
* Unterstützte Dateiformate:

  * `.fastq`
  * `.fq`
  * `.fastq.gz`
  * `.fq.gz`
* Technische Verzeichnisse (z. B. `output`, `logs`, `processor`) werden
  bei der Run-Erkennung ignoriert

---

## Ausgaben

### Run-Übersicht (erforderlich)

Die Datei `output/status_overview.json` enthält eine Übersicht pro Run mit:

* `run_id`
* `num_samples`
* `run_status` (SUCCESS / FAILED / PARTIAL)
* `failed_samples`

Diese Datei eignet sich für ein schnelles Monitoring oder die Weiterverarbeitung
in nachgelagerten Systemen.

### Detaillierter Bericht (Nachvollziehbarkeit)

Die Datei `output/status_detailed.json` enthält detaillierte Informationen
auf Sample-Ebene:

* Sample-ID
* Verarbeitungsstatus
* berechnete Metriken bei erfolgreicher Verarbeitung
* Fehlermeldung bei fehlgeschlagenen Samples

---

## Fehlerbehandlungsstrategie

* Jedes FASTQ-Sample wird unabhängig verarbeitet
* Beschädigte oder unvollständige FASTQ-Dateien führen zu einem FAILED-Sample
* Fehler werden mit Run-ID und Sample-ID geloggt
* Der Run-Status wird wie folgt bestimmt:

  * **SUCCESS**: alle Samples erfolgreich verarbeitet
  * **FAILED**: alle Samples fehlgeschlagen
  * **PARTIAL**: Mischung aus erfolgreichen und fehlgeschlagenen Samples

Dieser Ansatz stellt sicher, dass Probleme transparent sichtbar sind
und nutzbare Ergebnisse nicht verloren gehen.

---

## Monitoring und Produktionsaspekte (konzeptionell)

In einer produktiven Umgebung könnten unter anderem folgende Metriken
überwacht werden:

* Anzahl verarbeiteter Runs und Samples
* Anteil FAILED und PARTIAL Runs
* Häufigkeit bestimmter Fehlertypen (z. B. beschädigte FASTQ-Dateien)
* Verarbeitungsdauer pro Run und pro Sample

Mögliche Alarmierungsstrategien:

* Alarm bei Überschreiten definierter Fehlerraten
* Alarm, wenn Runs ungewöhnlich lange in Bearbeitung bleiben

Geeignete Werkzeuge:

* **Prometheus + Grafana** für Metriken und Dashboards
* **ELK / EFK Stack** für zentrales Logging
* Benachrichtigungen über E-Mail, Slack oder PagerDuty

---

## Mögliche Erweiterungen

* Ergänzung von Unit-Tests für FASTQ-Verarbeitung und Statuslogik
* Parallele Verarbeitung großer Runs
* Optionale CSV-Ausgabe zusätzlich zu JSON
* Integritätsprüfungen (z. B. Checksummen)
* Bereitstellung der Pipeline über Docker oder Conda

