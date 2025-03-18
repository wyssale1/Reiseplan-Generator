# Reiseplan-Generator

Ein modernes Tool zur Erstellung von PDF-Reiseplänen aus strukturierten JSON-Daten. Mit diesem Generator können Sie professionelle Reisedokumente mit Flug-, Hotel- und Aktivitätsinformationen erstellen und verwalten.

## 🌟 Funktionen

- 📋 Erstellung von strukturierten Reiseplänen aus JSON-Daten
- 🛫 Übersichtliche Darstellung von Flugdetails
- 🏨 Hotelaufenthalte mit Check-in/Check-out Informationen
- 🗓️ Aktivitätsplanung mit Zeit und Ort
- 🖼️ Integration von Logos (Airlines, Hotels)
- 📱 Zusatzinformationen (Währung, Zeitzone, Notfallkontakte)

## 🚀 Technologie-Stack

- **TypeScript**: Für typsichere Entwicklung
- **Vite**: Moderne Build-Umgebung 
- **PDFKit**: Zur PDF-Generierung
- **Moment.js**: Für Datums- und Zeitformatierung
- **Axios**: Für API-Integrationen (optional)

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/yourusername/reiseplan-generator.git
cd reiseplan-generator

# Abhängigkeiten installieren
npm install

# Build erstellen
npm run build
```

## 🔧 Verwendung

### 1. Reiseplan-Daten erstellen

Erstellen Sie eine JSON-Datei mit Ihrer Reiseplanstruktur:

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

### 2. PDF generieren

```bash
# PDF aus der JSON-Datei generieren
npm run generate -- ./data/reiseplan-london.json
```

Das generierte PDF wird im `output`-Verzeichnis gespeichert.

## 📁 Projektstruktur

```
reiseplan-generator/
├── src/                  # Quellcode
│   ├── main.ts           # Hauptlogik
│   ├── cli.ts            # Kommandozeilen-Interface
│   └── types.ts          # TypeScript-Definitionen
├── assets/               # Bilder und Assets
│   ├── logo.png          
│   ├── airlines/         # Airline-Logos
│   └── hotels/           # Hotel-Logos
├── data/                 # JSON-Reisepläne
├── output/               # Generierte PDFs
├── package.json          
├── tsconfig.json        
└── vite.config.ts       
```

## 🔄 Erweiterte Funktionen

### API-Integration für Flugdaten

Die Funktion `holeFluginformationen()` kann mit APIs wie FlightAware oder Amadeus verbunden werden, um automatisch aktuelle Flugdaten zu laden.

```typescript
// API-Key in einer .env-Datei konfigurieren
// API-Endpoint in holeFluginformationen() anpassen
```

### Anpassbare Layouts

Sie können das PDF-Layout durch Ändern der entsprechenden Funktionen in `main.ts` anpassen.

## 🤝 Beitragen

Beiträge sind willkommen! So können Sie beitragen:

1. Fork des Projekts
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request öffnen

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die [LICENSE](LICENSE) Datei für Details.

## 📬 Kontakt

Ihr Name - [@IhrTwitterHandle](https://twitter.com/IhrTwitterHandle) - ihre.email@example.com

Projekt-Link: [https://github.com/yourusername/reiseplan-generator](https://github.com/yourusername/reiseplan-generator)