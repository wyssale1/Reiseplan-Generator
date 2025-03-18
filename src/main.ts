// src/main.ts
import fs from 'fs';
import path from 'path';
import PDFDocument from 'pdfkit';
import axios from 'axios';
import moment from 'moment';
import { Reiseplan, Flug, Hotel, Aktivitaet, Zusatzinfo } from './types';

// Konfiguration
moment.locale('de');
const ASSETS_PATH = path.join(__dirname, '../assets');
const TEMPLATES_PATH = path.join(__dirname, '../templates');
const OUTPUT_PATH = path.join(__dirname, '../output');

// Erstelle Output-Verzeichnis, falls es nicht existiert
if (!fs.existsSync(OUTPUT_PATH)) {
  fs.mkdirSync(OUTPUT_PATH);
}

/**
 * Hauptfunktion zum Generieren des Reiseplans
 * @param reiseplanPfad - Pfad zur JSON-Datei des Reiseplans
 */
export async function generiereReiseplan(reiseplanPfad: string): Promise<string> {
  try {
    // Lade Reiseplan-Daten
    const reiseplanDaten: Reiseplan = JSON.parse(fs.readFileSync(reiseplanPfad, 'utf8'));
    
    // Erstelle PDF-Dokument
    const doc = new PDFDocument({
      size: 'A4',
      margins: { top: 50, bottom: 50, left: 50, right: 50 }
    });
    
    // Definiere Ausgabepfad
    const ausgabePfad = path.join(OUTPUT_PATH, `${reiseplanDaten.titel.replace(/\s+/g, '-')}.pdf`);
    const ausgabeStream = fs.createWriteStream(ausgabePfad);
    
    // Pipe PDF-Dokument in Ausgabedatei
    doc.pipe(ausgabeStream);
    
    // Generiere PDF-Inhalt
    await erstellePDF(doc, reiseplanDaten);
    
    // Finalisiere PDF
    doc.end();
    
    console.log(`Reiseplan wurde erfolgreich generiert: ${ausgabePfad}`);
    return ausgabePfad;
  } catch (error) {
    console.error('Fehler beim Generieren des Reiseplans:', error);
    throw error;
  }
}

/**
 * Erstellt den PDF-Inhalt basierend auf den Reiseplan-Daten
 * @param doc - PDFKit-Dokument
 * @param daten - Reiseplan-Daten aus JSON
 */
async function erstellePDF(doc: PDFKit.PDFDocument, daten: Reiseplan): Promise<void> {
  // Titel und Header
  erstelleHeader(doc, daten);
  
  // Übersicht
  erstelleUebersicht(doc, daten);
  
  // Jeder Reisetag bzw. jedes Element
  let yPosition = 200;
  
  // Flüge
  if (daten.fluege && daten.fluege.length > 0) {
    for (const flug of daten.fluege) {
      yPosition = await erstelleFlugBlock(doc, flug, yPosition);
      yPosition += 30; // Abstand zwischen Blöcken
      
      // Neue Seite, wenn nicht genug Platz
      if (yPosition > 700) {
        doc.addPage();
        yPosition = 50;
      }
    }
  }
  
  // Hotels
  if (daten.hotels && daten.hotels.length > 0) {
    for (const hotel of daten.hotels) {
      yPosition = erstelleHotelBlock(doc, hotel, yPosition);
      yPosition += 30; // Abstand zwischen Blöcken
      
      // Neue Seite, wenn nicht genug Platz
      if (yPosition > 700) {
        doc.addPage();
        yPosition = 50;
      }
    }
  }
  
  // Aktivitäten
  if (daten.aktivitaeten && daten.aktivitaeten.length > 0) {
    for (const aktivitaet of daten.aktivitaeten) {
      yPosition = erstelleAktivitaetBlock(doc, aktivitaet, yPosition);
      yPosition += 30; // Abstand zwischen Blöcken
      
      // Neue Seite, wenn nicht genug Platz
      if (yPosition > 700) {
        doc.addPage();
        yPosition = 50;
      }
    }
  }
  
  // Weitere Informationen
  if (daten.zusatzinfo) {
    yPosition = erstelleZusatzinfoBlock(doc, daten.zusatzinfo, yPosition);
  }
}

/**
 * Erstellt den Header des Reiseplans
 * @param doc - PDFKit-Dokument
 * @param daten - Reiseplan-Daten
 */
function erstelleHeader(doc: PDFKit.PDFDocument, daten: Reiseplan): void {
  // Logo (falls vorhanden)
  const logoPfad = path.join(ASSETS_PATH, 'logo.png');
  if (fs.existsSync(logoPfad)) {
    doc.image(logoPfad, 50, 50, { width: 50 });
  }
  
  // Titel
  doc.font('Helvetica-Bold')
     .fontSize(24)
     .text(daten.titel, 120, 60);
  
  // Datum
  doc.font('Helvetica')
     .fontSize(12)
     .text(`${moment(daten.startdatum).format('DD.MM.YYYY')} - ${moment(daten.enddatum).format('DD.MM.YYYY')}`, 120, 90);
  
  // Linie
  doc.moveTo(50, 120)
     .lineTo(550, 120)
     .stroke();
}

/**
 * Erstellt die Übersicht des Reiseplans
 * @param doc - PDFKit-Dokument
 * @param daten - Reiseplan-Daten
 */
function erstelleUebersicht(doc: PDFKit.PDFDocument, daten: Reiseplan): void {
  doc.font('Helvetica-Bold')
     .fontSize(14)
     .text('Übersicht', 50, 140);
  
  doc.font('Helvetica')
     .fontSize(12)
     .text(`Reiseziel: ${daten.reiseziel}`, 50, 165);
  
  if (daten.reisende) {
    doc.text(`Reisende: ${daten.reisende.join(', ')}`, 50, 180);
  }
}

/**
 * Erstellt einen Flugblock im PDF
 * @param doc - PDFKit-Dokument
 * @param flug - Flugdaten
 * @param yPosition - Y-Position im Dokument
 * @returns - Neue Y-Position nach dem Block
 */
async function erstelleFlugBlock(doc: PDFKit.PDFDocument, flug: Flug, yPosition: number): Promise<number> {
  // Fluglogo (falls vorhanden)
  const airlineLogo = path.join(ASSETS_PATH, 'airlines', `${flug.airline.toLowerCase()}.png`);
  if (fs.existsSync(airlineLogo)) {
    doc.image(airlineLogo, 50, yPosition, { width: 80 });
    yPosition += 40;
  }
  
  // Trennlinie
  doc.rect(50, yPosition, 500, 1).fill('#000000');
  yPosition += 15;

  // Titel: Flight
  doc.font('Helvetica-Bold')
     .fontSize(16)
     .text('Flight', 50, yPosition);
  yPosition += 25;
  
  // Flugdetails als Tabelle
  doc.font('Helvetica-Bold').fontSize(12).text('Flugnummer:', 50, yPosition);
  doc.font('Helvetica').text(flug.flugNr, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Abflug:', 50, yPosition);
  doc.font('Helvetica').text(`${flug.abflugOrt} (${flug.abflugCode})`, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Abflugzeit:', 50, yPosition);
  doc.font('Helvetica').text(`${moment(flug.abflugZeit).format('DD.MM.YYYY, HH:mm')}`, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Ankunft:', 50, yPosition);
  doc.font('Helvetica').text(`${flug.ankunftOrt} (${flug.ankunftCode})`, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Ankunftszeit:', 50, yPosition);
  doc.font('Helvetica').text(`${moment(flug.ankunftZeit).format('DD.MM.YYYY, HH:mm')}`, 150, yPosition);
  yPosition += 20;
  
  if (flug.buchungsNr) {
    doc.font('Helvetica-Bold').text('Buchungsnummer:', 50, yPosition);
    doc.font('Helvetica').text(flug.buchungsNr, 150, yPosition);
    yPosition += 20;
  }
  
  // Trennlinie am Ende
  doc.rect(50, yPosition + 10, 500, 1).fill('#000000');
  
  return yPosition + 20;
}

/**
 * Erstellt einen Hotelblock im PDF
 * @param doc - PDFKit-Dokument
 * @param hotel - Hoteldaten
 * @param yPosition - Y-Position im Dokument
 * @returns - Neue Y-Position nach dem Block
 */
function erstelleHotelBlock(doc: PDFKit.PDFDocument, hotel: Hotel, yPosition: number): number {
  // Hotellogo (falls vorhanden)
  const hotelLogo = path.join(ASSETS_PATH, 'hotels', `${hotel.name.toLowerCase().replace(/\s+/g, '-')}.png`);
  if (fs.existsSync(hotelLogo)) {
    doc.image(hotelLogo, 50, yPosition, { width: 80 });
    yPosition += 40;
  }
  
  // Trennlinie
  doc.rect(50, yPosition, 500, 1).fill('#000000');
  yPosition += 15;

  // Titel: Hotel
  doc.font('Helvetica-Bold')
     .fontSize(16)
     .text('Hotel', 50, yPosition);
  yPosition += 25;
  
  // Hoteldetails als Tabelle
  doc.font('Helvetica-Bold').fontSize(12).text('Name:', 50, yPosition);
  doc.font('Helvetica').text(hotel.name, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Adresse:', 50, yPosition);
  doc.font('Helvetica').text(hotel.adresse, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Check-in:', 50, yPosition);
  doc.font('Helvetica').text(`${moment(hotel.checkin).format('DD.MM.YYYY, HH:mm')}`, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Check-out:', 50, yPosition);
  doc.font('Helvetica').text(`${moment(hotel.checkout).format('DD.MM.YYYY, HH:mm')}`, 150, yPosition);
  yPosition += 20;
  
  if (hotel.buchungsNr) {
    doc.font('Helvetica-Bold').text('Buchungsnummer:', 50, yPosition);
    doc.font('Helvetica').text(hotel.buchungsNr, 150, yPosition);
    yPosition += 20;
  }
  
  // Trennlinie am Ende
  doc.rect(50, yPosition + 10, 500, 1).fill('#000000');
  
  return yPosition + 20;
}

/**
 * Erstellt einen Aktivitätsblock im PDF
 * @param doc - PDFKit-Dokument
 * @param aktivitaet - Aktivitätsdaten
 * @param yPosition - Y-Position im Dokument
 * @returns - Neue Y-Position nach dem Block
 */
function erstelleAktivitaetBlock(doc: PDFKit.PDFDocument, aktivitaet: Aktivitaet, yPosition: number): number {
  // Trennlinie
  doc.rect(50, yPosition, 500, 1).fill('#000000');
  yPosition += 15;

  // Titel: Aktivität
  doc.font('Helvetica-Bold')
     .fontSize(16)
     .text('Aktivität', 50, yPosition);
  yPosition += 25;
  
  // Aktivitätsdetails
  doc.font('Helvetica-Bold').fontSize(12).text('Name:', 50, yPosition);
  doc.font('Helvetica').text(aktivitaet.name, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Datum:', 50, yPosition);
  doc.font('Helvetica').text(`${moment(aktivitaet.datum).format('DD.MM.YYYY')}`, 150, yPosition);
  yPosition += 20;
  
  doc.font('Helvetica-Bold').text('Zeit:', 50, yPosition);
  doc.font('Helvetica').text(`${moment(aktivitaet.startzeit).format('HH:mm')} - ${moment(aktivitaet.endzeit).format('HH:mm')}`, 150, yPosition);
  yPosition += 20;
  
  if (aktivitaet.ort) {
    doc.font('Helvetica-Bold').text('Ort:', 50, yPosition);
    doc.font('Helvetica').text(aktivitaet.ort, 150, yPosition);
    yPosition += 20;
  }
  
  if (aktivitaet.buchungsNr) {
    doc.font('Helvetica-Bold').text('Buchungsnummer:', 50, yPosition);
    doc.font('Helvetica').text(aktivitaet.buchungsNr, 150, yPosition);
    yPosition += 20;
  }
  
  // Trennlinie am Ende
  doc.rect(50, yPosition + 10, 500, 1).fill('#000000');
  
  return yPosition + 20;
}

/**
 * Erstellt einen Zusatzinfo-Block im PDF
 * @param doc - PDFKit-Dokument
 * @param zusatzinfo - Zusatzinformationen
 * @param yPosition - Y-Position im Dokument
 * @returns - Neue Y-Position nach dem Block
 */
function erstelleZusatzinfoBlock(doc: PDFKit.PDFDocument, zusatzinfo: Zusatzinfo, yPosition: number): number {
  // Trennlinie
  doc.rect(50, yPosition, 500, 1).fill('#000000');
  yPosition += 15;

  // Titel: Zusätzliche Informationen
  doc.font('Helvetica-Bold')
     .fontSize(16)
     .text('Zusätzliche Informationen', 50, yPosition);
  yPosition += 25;
  
  // Zusatzinfos
  if (zusatzinfo.notfallkontakte) {
    doc.font('Helvetica-Bold').fontSize(12).text('Notfallkontakte:', 50, yPosition);
    yPosition += 20;
    
    for (const kontakt of zusatzinfo.notfallkontakte) {
      doc.font('Helvetica').text(`${kontakt.name}: ${kontakt.telefon}`, 70, yPosition);
      yPosition += 15;
    }
    yPosition += 10;
  }
  
  if (zusatzinfo.waehrung) {
    doc.font('Helvetica-Bold').fontSize(12).text('Währung:', 50, yPosition);
    doc.font('Helvetica').text(zusatzinfo.waehrung, 150, yPosition);
    yPosition += 20;
  }
  
  if (zusatzinfo.zeitzone) {
    doc.font('Helvetica-Bold').fontSize(12).text('Zeitzone:', 50, yPosition);
    doc.font('Helvetica').text(zusatzinfo.zeitzone, 150, yPosition);
    yPosition += 20;
  }
  
  if (zusatzinfo.notizen) {
    doc.font('Helvetica-Bold').fontSize(12).text('Notizen:', 50, yPosition);
    yPosition += 15;
    doc.font('Helvetica').text(zusatzinfo.notizen, 70, yPosition, { width: 480 });
    yPosition += 60; // Platz für Notizen
  }
  
  // Trennlinie am Ende
  doc.rect(50, yPosition + 10, 500, 1).fill('#000000');
  
  return yPosition + 20;
}

// Optional: API-Integration für Flugdaten
export async function holeFluginformationen(flugNr: string, datum: string): Promise<any | null> {
  try {
    // Hier könnte eine Integration mit einer Flug-API wie FlightAware, Skyscanner, etc. stehen
    // Beispiel (dies ist nur ein Platzhalter, Sie benötigen einen API-Key und die richtige API):
    /*
    const response = await axios.get(`https://api.flightapi.example/flight/${flugNr}`, {
      params: {
        date: datum,
        apiKey: 'IHR_API_KEY'
      }
    });
    return response.data;
    */
    
    console.log(`Fluginformationen für ${flugNr} am ${datum} werden abgerufen...`);
    return null; // Platzhalter
  } catch (error) {
    console.error('Fehler beim Abrufen der Fluginformationen:', error);
    return null;
  }
}