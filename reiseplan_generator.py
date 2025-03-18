#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reiseplan-Generator
Ein Tool zum Erstellen von PDF-Reiseplänen aus strukturierten JSON-Daten.
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from PIL import Image as PILImage


class ReiseplanGenerator:
    """
    Generiert PDF-Reisepläne aus JSON-Daten.
    """

    def __init__(self, basis_pfad: Optional[str] = None):
        """
        Initialisiert den ReiseplanGenerator.
        
        Args:
            basis_pfad: Basispfad für Assets und Ausgabeverzeichnisse
        """
        self.basis_pfad = Path(basis_pfad) if basis_pfad else Path.cwd()
        self.assets_pfad = self.basis_pfad / "assets"
        self.output_pfad = self.basis_pfad / "output"
        
        # Erstelle Output-Verzeichnis, falls es nicht existiert
        self.output_pfad.mkdir(exist_ok=True)
        
        # Styles für PDF
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='Titel',
            fontName='Helvetica-Bold',
            fontSize=24,
            spaceAfter=12
        ))
        self.styles.add(ParagraphStyle(
            name='Untertitel',
            fontName='Helvetica-Bold',
            fontSize=16,
            spaceAfter=8
        ))
        self.styles.add(ParagraphStyle(
            name='Normal',
            fontName='Helvetica',
            fontSize=11,
            spaceAfter=6
        ))

    def generiere_reiseplan(self, reiseplan_pfad: Union[str, Path]) -> str:
        """
        Generiert einen PDF-Reiseplan aus einer JSON-Datei.
        
        Args:
            reiseplan_pfad: Pfad zur JSON-Datei mit Reisedaten
            
        Returns:
            str: Pfad zur generierten PDF-Datei
        """
        # Lade Reiseplan-Daten
        with open(reiseplan_pfad, 'r', encoding='utf-8') as f:
            reiseplan_daten = json.load(f)
        
        # Erstelle PDF-Dateiname
        pdf_dateiname = f"{reiseplan_daten['titel'].replace(' ', '-')}.pdf"
        pdf_pfad = self.output_pfad / pdf_dateiname
        
        # Erstelle PDF-Dokument
        doc = SimpleDocTemplate(
            str(pdf_pfad),
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Erstelle Inhalt
        elemente = []
        self._erstelle_header(elemente, reiseplan_daten)
        self._erstelle_uebersicht(elemente, reiseplan_daten)
        
        # Füge Flüge hinzu
        if "fluege" in reiseplan_daten and reiseplan_daten["fluege"]:
            for flug in reiseplan_daten["fluege"]:
                self._erstelle_flug_block(elemente, flug)
        
        # Füge Hotels hinzu
        if "hotels" in reiseplan_daten and reiseplan_daten["hotels"]:
            for hotel in reiseplan_daten["hotels"]:
                self._erstelle_hotel_block(elemente, hotel)
        
        # Füge Aktivitäten hinzu
        if "aktivitaeten" in reiseplan_daten and reiseplan_daten["aktivitaeten"]:
            for aktivitaet in reiseplan_daten["aktivitaeten"]:
                self._erstelle_aktivitaet_block(elemente, aktivitaet)
        
        # Füge Zusatzinformationen hinzu
        if "zusatzinfo" in reiseplan_daten:
            self._erstelle_zusatzinfo_block(elemente, reiseplan_daten["zusatzinfo"])
        
        # Baue PDF zusammen
        doc.build(elemente)
        
        print(f"Reiseplan wurde erfolgreich generiert: {pdf_pfad}")
        return str(pdf_pfad)

    def _erstelle_header(self, elemente: List, reiseplan_daten: Dict[str, Any]) -> None:
        """
        Erstellt den Header des Reiseplans.
        
        Args:
            elemente: Liste der PDF-Elemente
            reiseplan_daten: Reiseplan-Daten aus JSON
        """
        # Logo (falls vorhanden)
        logo_pfad = self.assets_pfad / "logo.png"
        if logo_pfad.exists():
            img = Image(str(logo_pfad), width=1.5*cm, height=1.5*cm)
            elemente.append(img)
        
        # Titel
        elemente.append(Paragraph(reiseplan_daten["titel"], self.styles["Titel"]))
        
        # Datum
        start_datum = datetime.datetime.fromisoformat(reiseplan_daten["startdatum"]).strftime("%d.%m.%Y")
        end_datum = datetime.datetime.fromisoformat(reiseplan_daten["enddatum"]).strftime("%d.%m.%Y")
        datum_text = f"{start_datum} - {end_datum}"
        elemente.append(Paragraph(datum_text, self.styles["Normal"]))
        
        # Abstand
        elemente.append(Spacer(1, 0.5*cm))
        
        # Trennlinie
        elemente.append(
            Table(
                [['']], 
                colWidths=[17*cm], 
                style=TableStyle([
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.black)
                ])
            )
        )
        elemente.append(Spacer(1, 0.5*cm))

    def _erstelle_uebersicht(self, elemente: List, reiseplan_daten: Dict[str, Any]) -> None:
        """
        Erstellt die Übersicht des Reiseplans.
        
        Args:
            elemente: Liste der PDF-Elemente
            reiseplan_daten: Reiseplan-Daten aus JSON
        """
        elemente.append(Paragraph("Übersicht", self.styles["Untertitel"]))
        elemente.append(Spacer(1, 0.2*cm))
        
        elemente.append(Paragraph(f"Reiseziel: {reiseplan_daten['reiseziel']}", self.styles["Normal"]))
        
        if "reisende" in reiseplan_daten and reiseplan_daten["reisende"]:
            reisende_text = f"Reisende: {', '.join(reiseplan_daten['reisende'])}"
            elemente.append(Paragraph(reisende_text, self.styles["Normal"]))
        
        elemente.append(Spacer(1, 0.5*cm))

    def _erstelle_flug_block(self, elemente: List, flug: Dict[str, Any]) -> None:
        """
        Erstellt einen Flugblock im PDF.
        
        Args:
            elemente: Liste der PDF-Elemente
            flug: Flugdaten aus JSON
        """
        # Airline-Logo (falls vorhanden)
        airline_logo_pfad = self.assets_pfad / "airlines" / f"{flug['airline'].lower()}.png"
        if airline_logo_pfad.exists():
            img = Image(str(airline_logo_pfad), width=3*cm, height=1.5*cm)
            elemente.append(img)
            elemente.append(Spacer(1, 0.2*cm))
        
        # Trennlinie
        elemente.append(
            Table(
                [['']], 
                colWidths=[17*cm], 
                style=TableStyle([
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.black)
                ])
            )
        )
        elemente.append(Spacer(1, 0.2*cm))
        
        # Titel: Flight
        elemente.append(Paragraph("Flight", self.styles["Untertitel"]))
        elemente.append(Spacer(1, 0.2*cm))
        
        # Flugdetails als Tabelle
        flug_details = [
            ["Flugnummer:", flug["flugNr"]],
            ["Abflug:", f"{flug['abflugOrt']} ({flug['abflugCode']})"],
            ["Abflugzeit:", self._formatiere_datum_zeit(flug["abflugZeit"])],
            ["Ankunft:", f"{flug['ankunftOrt']} ({flug['ankunftCode']})"],
            ["Ankunftszeit:", self._formatiere_datum_zeit(flug["ankunftZeit"])]
        ]
        
        if "buchungsNr" in flug and flug["buchungsNr"]:
            flug_details.append(["Buchungsnummer:", flug["buchungsNr"]])
        
        flug_tabelle = Table(
            flug_details,
            colWidths=[4*cm, 13*cm],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
        )
        
        elemente.append(flug_tabelle)
        elemente.append(Spacer(1, 0.5*cm))

    def _erstelle_hotel_block(self, elemente: List, hotel: Dict[str, Any]) -> None:
        """
        Erstellt einen Hotelblock im PDF.
        
        Args:
            elemente: Liste der PDF-Elemente
            hotel: Hoteldaten aus JSON
        """
        # Hotel-Logo (falls vorhanden)
        hotel_logo_pfad = self.assets_pfad / "hotels" / f"{hotel['name'].lower().replace(' ', '-')}.png"
        if hotel_logo_pfad.exists():
            img = Image(str(hotel_logo_pfad), width=3*cm, height=1.5*cm)
            elemente.append(img)
            elemente.append(Spacer(1, 0.2*cm))
        
        # Trennlinie
        elemente.append(
            Table(
                [['']], 
                colWidths=[17*cm], 
                style=TableStyle([
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.black)
                ])
            )
        )
        elemente.append(Spacer(1, 0.2*cm))
        
        # Titel: Hotel
        elemente.append(Paragraph("Hotel", self.styles["Untertitel"]))
        elemente.append(Spacer(1, 0.2*cm))
        
        # Hoteldetails als Tabelle
        hotel_details = [
            ["Name:", hotel["name"]],
            ["Adresse:", hotel["adresse"]],
            ["Check-in:", self._formatiere_datum_zeit(hotel["checkin"])],
            ["Check-out:", self._formatiere_datum_zeit(hotel["checkout"])],
        ]
        
        if "buchungsNr" in hotel and hotel["buchungsNr"]:
            hotel_details.append(["Buchungsnummer:", hotel["buchungsNr"]])
        
        hotel_tabelle = Table(
            hotel_details,
            colWidths=[4*cm, 13*cm],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
        )
        
        elemente.append(hotel_tabelle)
        elemente.append(Spacer(1, 0.5*cm))

    def _erstelle_aktivitaet_block(self, elemente: List, aktivitaet: Dict[str, Any]) -> None:
        """
        Erstellt einen Aktivitätsblock im PDF.
        
        Args:
            elemente: Liste der PDF-Elemente
            aktivitaet: Aktivitätsdaten aus JSON
        """
        # Trennlinie
        elemente.append(
            Table(
                [['']], 
                colWidths=[17*cm], 
                style=TableStyle([
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.black)
                ])
            )
        )
        elemente.append(Spacer(1, 0.2*cm))
        
        # Titel: Aktivität
        elemente.append(Paragraph("Aktivität", self.styles["Untertitel"]))
        elemente.append(Spacer(1, 0.2*cm))
        
        # Aktivitätsdetails als Tabelle
        aktivitaet_details = [
            ["Name:", aktivitaet["name"]],
            ["Datum:", datetime.datetime.fromisoformat(aktivitaet["datum"]).strftime("%d.%m.%Y")],
            ["Zeit:", f"{self._formatiere_zeit(aktivitaet['startzeit'])} - {self._formatiere_zeit(aktivitaet['endzeit'])}"],
        ]
        
        if "ort" in aktivitaet and aktivitaet["ort"]:
            aktivitaet_details.append(["Ort:", aktivitaet["ort"]])
        
        if "buchungsNr" in aktivitaet and aktivitaet["buchungsNr"]:
            aktivitaet_details.append(["Buchungsnummer:", aktivitaet["buchungsNr"]])
        
        aktivitaet_tabelle = Table(
            aktivitaet_details,
            colWidths=[4*cm, 13*cm],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
        )
        
        elemente.append(aktivitaet_tabelle)
        elemente.append(Spacer(1, 0.5*cm))

    def _erstelle_zusatzinfo_block(self, elemente: List, zusatzinfo: Dict[str, Any]) -> None:
        """
        Erstellt einen Zusatzinfo-Block im PDF.
        
        Args:
            elemente: Liste der PDF-Elemente
            zusatzinfo: Zusatzinformationen aus JSON
        """
        # Trennlinie
        elemente.append(
            Table(
                [['']], 
                colWidths=[17*cm], 
                style=TableStyle([
                    ('LINEBELOW', (0, 0), (0, 0), 1, colors.black)
                ])
            )
        )
        elemente.append(Spacer(1, 0.2*cm))
        
        # Titel: Zusätzliche Informationen
        elemente.append(Paragraph("Zusätzliche Informationen", self.styles["Untertitel"]))
        elemente.append(Spacer(1, 0.2*cm))
        
        # Notfallkontakte
        if "notfallkontakte" in zusatzinfo and zusatzinfo["notfallkontakte"]:
            elemente.append(Paragraph("Notfallkontakte:", self.styles["Normal"]))
            
            notfallkontakte_data = []
            for kontakt in zusatzinfo["notfallkontakte"]:
                notfallkontakte_data.append([kontakt["name"], kontakt["telefon"]])
            
            notfallkontakte_tabelle = Table(
                notfallkontakte_data,
                colWidths=[8.5*cm, 8.5*cm],
                style=TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ])
            )
            
            elemente.append(notfallkontakte_tabelle)
            elemente.append(Spacer(1, 0.3*cm))
        
        # Weitere Informationen in Tabelle
        if any(key in zusatzinfo for key in ["waehrung", "zeitzone", "notizen"]):
            weitere_infos = []
            
            if "waehrung" in zusatzinfo and zusatzinfo["waehrung"]:
                weitere_infos.append(["Währung:", zusatzinfo["waehrung"]])
            
            if "zeitzone" in zusatzinfo and zusatzinfo["zeitzone"]:
                weitere_infos.append(["Zeitzone:", zusatzinfo["zeitzone"]])
            
            if weitere_infos:
                weitere_infos_tabelle = Table(
                    weitere_infos,
                    colWidths=[4*cm, 13*cm],
                    style=TableStyle([
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
                        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 12),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ])
                )
                
                elemente.append(weitere_infos_tabelle)
                elemente.append(Spacer(1, 0.3*cm))
        
        # Notizen
        if "notizen" in zusatzinfo and zusatzinfo["notizen"]:
            elemente.append(Paragraph("Notizen:", self.styles["Normal"]))
            elemente.append(Paragraph(zusatzinfo["notizen"], self.styles["Normal"]))
            elemente.append(Spacer(1, 0.3*cm))

    def _formatiere_datum_zeit(self, iso_datum_zeit: str) -> str:
        """
        Formatiert ein ISO-Datum-Zeit-String in ein lesbares Format.
        
        Args:
            iso_datum_zeit: ISO-formatierte Datum-Zeit-String
            
        Returns:
            str: Formatierter Datum-Zeit-String
        """
        try:
            dt = datetime.datetime.fromisoformat(iso_datum_zeit)
            return dt.strftime("%d.%m.%Y, %H:%M")
        except (ValueError, TypeError):
            return iso_datum_zeit

    def _formatiere_zeit(self, iso_datum_zeit: str) -> str:
        """
        Extrahiert und formatiert die Uhrzeit aus einem ISO-Datum-Zeit-String.
        
        Args:
            iso_datum_zeit: ISO-formatierte Datum-Zeit-String
            
        Returns:
            str: Formatierter Zeit-String
        """
        try:
            dt = datetime.datetime.fromisoformat(iso_datum_zeit)
            return dt.strftime("%H:%M")
        except (ValueError, TypeError):
            return iso_datum_zeit

    def hole_fluginformationen(self, flug_nr: str, datum: str) -> Optional[Dict[str, Any]]:
        """
        Optional: Holt Fluginformationen von einer API.
        
        Args:
            flug_nr: Flugnummer
            datum: Datum des Fluges
            
        Returns:
            Optional[Dict[str, Any]]: Fluginformationen oder None bei Fehler
        """
        try:
            # Hier könnte eine Integration mit einer Flug-API wie FlightAware, Skyscanner, etc. stehen
            # Beispiel (dies ist nur ein Platzhalter, Sie benötigen einen API-Key und die richtige API):
            """
            response = requests.get(
                f"https://api.flightapi.example/flight/{flug_nr}",
                params={
                    "date": datum,
                    "apiKey": "IHR_API_KEY"
                }
            )
            return response.json()
            """
            
            print(f"Fluginformationen für {flug_nr} am {datum} werden abgerufen...")
            return None  # Platzhalter
        except Exception as e:
            print(f"Fehler beim Abrufen der Fluginformationen: {e}")
            return None


# Direkter Aufruf über Kommandozeile
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Bitte geben Sie den Pfad zur Reiseplan-JSON-Datei an.")
        print("Verwendung: python reiseplan_generator.py pfad/zur/reiseplan.json")
        sys.exit(1)
    
    reiseplan_pfad = sys.argv[1]
    generator = ReiseplanGenerator()
    
    try:
        generator.generiere_reiseplan(reiseplan_pfad)
        print("Reiseplan wurde erfolgreich generiert.")
    except Exception as e:
        print(f"Fehler: {e}")
        sys.exit(1)