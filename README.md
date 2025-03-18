# Reiseplan-Generator

Ein elegantes Tool zur Erstellung von PDF-Reiseplänen aus strukturierten JSON-Daten. Mit diesem Generator können Sie professionelle Reisedokumente mit Flug-, Hotel- und Aktivitätsinformationen erstellen und verwalten.

## 🌟 Funktionen

- 📋 Erstellung von strukturierten Reiseplänen aus JSON-Daten
- 🛫 Automatische Ergänzung von Flugdetails mit minimalen Eingaben (nur Flugnummer und Datum)
- 🏨 Hotelaufenthalte mit Check-in/Check-out Informationen
- 🗓️ Aktivitätsplanung mit Zeit und Ort
- 🖼️ Integration von Logos (Airlines, Hotels)
- 📱 Zusatzinformationen (Währung, Zeitzone, Notfallkontakte)
- 🖊️ Modulare Struktur mit Open Sans Font

## 🚀 Technologie-Stack

- **Python 3.8+**: Moderne, lesbare Programmierung
- **ReportLab**: Robuste Bibliothek zur PDF-Generierung
- **Requests**: Für API-Integrationen mit Flugdaten

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/reiseplan-generator.git
cd reiseplan-generator

# Virtuelle Umgebung erstellen und aktivieren
python3 -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Ordnerstruktur vorbereiten
mkdir -p assets/airlines assets/hotels assets/fonts data output
```

### Schriften einrichten

Für optimale Ergebnisse sollten Sie die OpenSans-Schriftarten im Verzeichnis `assets/fonts` bereitstellen:

1. Laden Sie die OpenSans-Schriften herunter:
   - [OpenSans-Regular.ttf](https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Regular.ttf)
   - [OpenSans-Bold.ttf](https://github.com/googlefonts/opensans/raw/main/fonts/ttf/OpenSans-Bold.ttf)

2. Legen Sie diese Dateien im Verzeichnis `assets/fonts` ab:
   ```bash
   cp OpenSans-Regular.ttf OpenSans-Bold.ttf assets/fonts/
   ```

## 🔧 Verwendung

### 1. Reiseplan-Daten erstellen

Erstellen Sie eine JSON-Datei mit Ihrer Reiseplanstruktur. Mit der Flight-API-Integration können Sie minimale Flugdaten angeben:

```json
{
  "titel": "Geschäftsreise Frankfurt",
  "startdatum": "2025-05-15",
  "enddatum": "2025-05-17",
  "reiseziel": "Frankfurt, Deutschland",
  "reisende": ["Max Mustermann"],
  
  "fluege": [
    {
      "flugNr": "LX1070",
      "flugDatum": "2025-05-15",
      "buchungsNr": "ABC123"
    },
    {
      "flugNr": "LX1071",
      "flugDatum": "2025-05-17",
      "buchungsNr": "ABC123"
    }
  ],
  
  "hotels": [...],
  "aktivitaeten": [...],
  "zusatzinfo": {...}
}
```

### 2. Logos hinzufügen (optional)

- Fügen Sie Ihr persönliches Logo als `assets/logo.png` hinzu
- Speichern Sie Airline-Logos unter `assets/airlines/` (z.B. `swiss.png`)
- Speichern Sie Hotel-Logos unter `assets/hotels/` (z.B. `steigenberger-airport-hotel.png`)

### 3. PDF generieren

```bash
# Über das CLI-Modul
python cli.py data/reiseplan-minimal.json

# Mit automatischem Öffnen des PDFs
python cli.py data/reiseplan-minimal.json --open

# Mit Debug-Modus für ausführliche Logs
python cli.py data/reiseplan-minimal.json --debug
```

Das generierte PDF wird im `output/`-Verzeichnis gespeichert.

## 📁 Projektstruktur

```
reiseplan-generator/
├── reiseplan_generator/       # Hauptpaket
│   ├── __init__.py            # Paket-Initialisierung
│   ├── core.py                # Hauptgenerator-Klasse
│   ├── elements.py            # PDF-Element-Funktionen
│   ├── config.py              # Konfigurationseinstellungen
│   ├── __main__.py            # Einstiegspunkt für Paket-Ausführung
│   ├── apis/                  # API-Integrationen
│   │   ├── __init__.py
│   │   └── flight_api.py      # Fluginformationen-API
│   └── utils/                 # Hilfsfunktionen
│       ├── __init__.py
│       ├── date_utils.py      # Datums-Hilfsfunktionen
│       ├── font_manager.py    # Font-Management
│       ├── json_schema.py     # JSON-Schema-Validierung
│       └── logging_setup.py   # Logging-Konfiguration
├── cli.py                     # Command Line Interface
├── requirements.txt           # Python-Abhängigkeiten
├── README.md                  # Projektdokumentation
├── assets/                    # Assets-Verzeichnis
│   ├── logo.png               # Ihr persönliches Logo
│   ├── airlines/              # Airline-Logos
│   ├── hotels/                # Hotel-Logos
│   └── fonts/                 # Schriftarten
│       ├── OpenSans-Regular.ttf
│       └── OpenSans-Bold.ttf
├── data/                      # JSON-Daten für Reisepläne
└── output/                    # Generierte PDF-Dokumente
```

## 🔄 Flight API Integration

Um die vollständige Flight-API-Funktionalität zu nutzen, müssen Sie einen API-Schlüssel für einen Flugdatendienst wie Aviation Stack erhalten:

1. Registrieren Sie sich für einen API-Schlüssel bei [aviationstack.com](https://aviationstack.com/)
2. Setzen Sie den API-Schlüssel als Umgebungsvariable:

```bash
export FLIGHT_API_KEY=Ihr_API_Schlüssel
```

Ohne API-Schlüssel werden minimale Flugdaten unverändert übernommen.

## 🤝 Mitwirken

Beiträge sind willkommen! So können Sie beitragen:

1. Fork des Projekts erstellen
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request öffnen

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.