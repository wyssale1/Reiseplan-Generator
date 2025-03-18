# Reiseplan-Generator

Ein elegantes Tool zur Erstellung von PDF-Reiseplänen aus strukturierten JSON-Daten. Mit diesem Generator können Sie professionelle Reisedokumente mit Flug-, Hotel- und Aktivitätsinformationen erstellen und verwalten.

## 🌟 Funktionen

- 📋 Erstellung von strukturierten Reiseplänen aus JSON-Daten
- 🛫 Übersichtliche Darstellung von Flugdetails
- 🏨 Hotelaufenthalte mit Check-in/Check-out Informationen
- 🗓️ Aktivitätsplanung mit Zeit und Ort
- 🖼️ Integration von Logos (Airlines, Hotels)
- 📱 Zusatzinformationen (Währung, Zeitzone, Notfallkontakte)

## 🚀 Technologie-Stack

- **Python 3.8+**: Moderne, lesbare Programmierung
- **ReportLab**: Robuste Bibliothek zur PDF-Generierung
- **Pillow**: Zur Verarbeitung von Bildern
- **Requests**: Für optional API-Integrationen

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/reiseplan-generator.git
cd reiseplan-generator

# Abhängigkeiten installieren
pip install -r requirements.txt

# Ordnerstruktur vorbereiten
mkdir -p assets/airlines assets/hotels data output
```

## 🔧 Verwendung

### 1. Reiseplan-Daten erstellen

Erstellen Sie eine JSON-Datei mit Ihrer Reiseplanstruktur und speichern Sie diese im `data/`-Verzeichnis:

```json
{
  "titel": "London Geschäftsreise",
  "startdatum": "2025-04-10",
  "enddatum": "2025-04-15",
  "reiseziel": "London, Vereinigtes Königreich",
  "reisende": ["Max Mustermann"],
  
  "fluege": [
    {
      "airline": "SWISS",
      "flugNr": "LX12",
      "abflugOrt": "Zürich",
      "abflugCode": "ZRH",
      "abflugZeit": "2025-04-10T18:55:00",
      "ankunftOrt": "London City",
      "ankunftCode": "LCY", 
      "ankunftZeit": "2025-04-10T20:00:00",
      "buchungsNr": "ABCDEF"
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
- Speichern Sie Hotel-Logos unter `assets/hotels/` (z.B. `shangri-la-london.png`)

### 3. PDF generieren

```bash
# Über das CLI-Modul
python cli.py data/reiseplan-london.json

# Alternativ direkt über das Hauptmodul
python reiseplan_generator.py data/reiseplan-london.json
```

Das generierte PDF wird im `output/`-Verzeichnis gespeichert.

## 📁 Projektstruktur

```
reiseplan-generator/
├── reiseplan_generator.py   # Hauptmodul mit PDF-Generierungsfunktionen
├── cli.py                   # Command Line Interface
├── requirements.txt         # Python-Abhängigkeiten
├── assets/                  # Bilder und andere Assets
│   ├── logo.png             # Ihr persönliches Logo
│   ├── airlines/            # Airline-Logos
│   └── hotels/              # Hotel-Logos
├── data/                    # JSON-Daten für Reisepläne
└── output/                  # Generierte PDF-Dokumente
```

## 🔄 Erweiterte Funktionen

### API-Integration für Flugdaten

Die Methode `hole_fluginformationen()` kann mit APIs wie FlightAware, Amadeus oder Skyscanner verbunden werden, um automatisch aktuelle Flugdaten zu laden:

```python
# In reiseplan_generator.py
def hole_fluginformationen(self, flug_nr, datum):
    api_key = os.environ.get("FLIGHTAPI_KEY")
    url = f"https://api.flightaware.com/v2/flights/{flug_nr}"
    response = requests.get(url, headers={"Authorization": f"Bearer {api_key}"})
    return response.json()
```

### GUI-Oberfläche hinzufügen

Mit Python-Bibliotheken wie tkinter, PyQt oder Streamlit können Sie leicht eine grafische Benutzeroberfläche erstellen:

```python
# Beispiel für ein einfaches Streamlit-Interface
import streamlit as st
from reiseplan_generator import ReiseplanGenerator

st.title("Reiseplan-Generator")
uploaded_file = st.file_uploader("JSON-Reiseplan hochladen", type="json")

if uploaded_file is not None:
    generator = ReiseplanGenerator()
    pdf_path = generator.generiere_reiseplan(uploaded_file)
    st.success(f"PDF erfolgreich generiert: {pdf_path}")
```

## 🤝 Beitragen

Beiträge sind willkommen! So können Sie beitragen:

1. Fork des Projekts
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request öffnen

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.