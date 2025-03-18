"""
Funktionen zum Erstellen von PDF-Elementen für den Reiseplan-Generator.
"""

import datetime
from typing import Dict, Any, List
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image

from .config import AIRLINES_DIR, HOTELS_DIR, ASSETS_DIR
from .utils.date_utils import formatiere_datum_zeit, formatiere_zeit


def erstelle_header(elemente: List, reiseplan_daten: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> None:
    """
    Erstellt den Header des Reiseplans.
    
    Args:
        elemente: Liste der PDF-Elemente
        reiseplan_daten: Reiseplan-Daten aus JSON
        styles: Styles für die PDF-Formatierung
    """
    # Logo (falls vorhanden)
    logo_pfad = ASSETS_DIR / "logo.png"
    if logo_pfad.exists():
        img = Image(str(logo_pfad), width=1.5*cm, height=1.5*cm)
        elemente.append(img)
    
    # Titel
    elemente.append(Paragraph(reiseplan_daten["titel"], styles["Titel"]))
    
    # Datum
    start_datum = datetime.datetime.fromisoformat(reiseplan_daten["startdatum"]).strftime("%d.%m.%Y")
    end_datum = datetime.datetime.fromisoformat(reiseplan_daten["enddatum"]).strftime("%d.%m.%Y")
    datum_text = f"{start_datum} - {end_datum}"
    elemente.append(Paragraph(datum_text, styles["Normal"]))
    
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


def erstelle_uebersicht(elemente: List, reiseplan_daten: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> None:
    """
    Erstellt die Übersicht des Reiseplans.
    
    Args:
        elemente: Liste der PDF-Elemente
        reiseplan_daten: Reiseplan-Daten aus JSON
        styles: Styles für die PDF-Formatierung
    """
    elemente.append(Paragraph("Übersicht", styles["Untertitel"]))
    elemente.append(Spacer(1, 0.2*cm))
    
    elemente.append(Paragraph(f"Reiseziel: {reiseplan_daten['reiseziel']}", styles["Normal"]))
    
    if "reisende" in reiseplan_daten and reiseplan_daten["reisende"]:
        reisende_text = f"Reisende: {', '.join(reiseplan_daten['reisende'])}"
        elemente.append(Paragraph(reisende_text, styles["Normal"]))
    
    elemente.append(Spacer(1, 0.5*cm))


def erstelle_flug_block(elemente: List, flug: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> None:
    """
    Erstellt einen Flugblock im PDF.
    
    Args:
        elemente: Liste der PDF-Elemente
        flug: Flugdaten aus JSON
        styles: Styles für die PDF-Formatierung
    """
    # Airline-Logo (falls vorhanden)
    if "airline" in flug:
        airline_name = flug["airline"].lower().replace(' ', '-')
        airline_logo_pfad = AIRLINES_DIR / f"{airline_name}.png"
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
    elemente.append(Paragraph("Flight", styles["Untertitel"]))
    elemente.append(Spacer(1, 0.2*cm))
    
    # Flugdetails als Tabelle
    flug_details = [
        ["Flugnummer:", flug["flugNr"]]
    ]
    
    # Flugdatum hinzufügen (für minimale Flüge)
    if "flugDatum" in flug:
        flug_details.append(["Datum:", flug["flugDatum"]])
    
    # Füge optionale Felder hinzu, falls vorhanden
    if "abflugOrt" in flug and "abflugCode" in flug:
        flug_details.append(["Abflug:", f"{flug['abflugOrt']} ({flug['abflugCode']})"])
    
    if "abflugZeit" in flug:
        flug_details.append(["Abflugzeit:", formatiere_datum_zeit(flug["abflugZeit"])])
    
    if "ankunftOrt" in flug and "ankunftCode" in flug:
        flug_details.append(["Ankunft:", f"{flug['ankunftOrt']} ({flug['ankunftCode']})"])
    
    if "ankunftZeit" in flug:
        flug_details.append(["Ankunftszeit:", formatiere_datum_zeit(flug["ankunftZeit"])])
    
    if "buchungsNr" in flug and flug["buchungsNr"]:
        flug_details.append(["Buchungsnummer:", flug["buchungsNr"]])
    
    flug_tabelle = Table(
        flug_details,
        colWidths=[4*cm, 13*cm],
        style=TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'OpenSans-Bold'),  # Open Sans Bold für Labels
            ('FONTNAME', (1, 0), (1, -1), 'OpenSans'),      # Open Sans für Inhalte
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


def erstelle_hotel_block(elemente: List, hotel: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> None:
    """
    Erstellt einen Hotelblock im PDF.
    
    Args:
        elemente: Liste der PDF-Elemente
        hotel: Hoteldaten aus JSON
        styles: Styles für die PDF-Formatierung
    """
    # Hotel-Logo (falls vorhanden)
    hotel_logo_pfad = HOTELS_DIR / f"{hotel['name'].lower().replace(' ', '-')}.png"
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
    elemente.append(Paragraph("Hotel", styles["Untertitel"]))
    elemente.append(Spacer(1, 0.2*cm))
    
    # Hoteldetails als Tabelle
    hotel_details = [
        ["Name:", hotel["name"]],
        ["Adresse:", hotel["adresse"]],
        ["Check-in:", formatiere_datum_zeit(hotel["checkin"])],
        ["Check-out:", formatiere_datum_zeit(hotel["checkout"])],
    ]
    
    if "buchungsNr" in hotel and hotel["buchungsNr"]:
        hotel_details.append(["Buchungsnummer:", hotel["buchungsNr"]])
    
    hotel_tabelle = Table(
        hotel_details,
        colWidths=[4*cm, 13*cm],
        style=TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (0, -1), 'OpenSans-Bold'),  # Open Sans Bold für Labels
            ('FONTNAME', (1, 0), (1, -1), 'OpenSans'),      # Open Sans für Inhalte
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


def erstelle_aktivitaet_block(elemente: List, aktivitaet: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> None:
    """
    Erstellt einen Aktivitätsblock im PDF.
    
    Args:
        elemente: Liste der PDF-Elemente
        aktivitaet: Aktivitätsdaten aus JSON
        styles: Styles für die PDF-Formatierung
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
    elemente.append(Paragraph("Aktivität", styles["Untertitel"]))
    elemente.append(Spacer(1, 0.2*cm))
    
    # Aktivitätsdetails als Tabelle
    aktivitaet_details = [
        ["Name:", aktivitaet["name"]],
        ["Datum:", datetime.datetime.fromisoformat(aktivitaet["datum"]).strftime("%d.%m.%Y")],
        ["Zeit:", f"{formatiere_zeit(aktivitaet['startzeit'])} - {formatiere_zeit(aktivitaet['endzeit'])}"],
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
            ('FONTNAME', (0, 0), (0, -1), 'OpenSans-Bold'),  # Open Sans Bold für Labels
            ('FONTNAME', (1, 0), (1, -1), 'OpenSans'),      # Open Sans für Inhalte
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


def erstelle_zusatzinfo_block(elemente: List, zusatzinfo: Dict[str, Any], styles: Dict[str, ParagraphStyle]) -> None:
    """
    Erstellt einen Zusatzinfo-Block im PDF.
    
    Args:
        elemente: Liste der PDF-Elemente
        zusatzinfo: Zusatzinformationen aus JSON
        styles: Styles für die PDF-Formatierung
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
    elemente.append(Paragraph("Zusätzliche Informationen", styles["Untertitel"]))
    elemente.append(Spacer(1, 0.2*cm))
    
    # Notfallkontakte
    if "notfallkontakte" in zusatzinfo and zusatzinfo["notfallkontakte"]:
        elemente.append(Paragraph("Notfallkontakte:", styles["Normal"]))
        
        notfallkontakte_data = []
        for kontakt in zusatzinfo["notfallkontakte"]:
            notfallkontakte_data.append([kontakt["name"], kontakt["telefon"]])
        
        notfallkontakte_tabelle = Table(
            notfallkontakte_data,
            colWidths=[8.5*cm, 8.5*cm],
            style=TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('FONTNAME', (0, 0), (-1, -1), 'OpenSans'),  # Open Sans für Kontakte
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
                    ('FONTNAME', (0, 0), (0, -1), 'OpenSans-Bold'),  # Open Sans Bold für Labels
                    ('FONTNAME', (1, 0), (1, -1), 'OpenSans'),      # Open Sans für Inhalte
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
        elemente.append(Paragraph("Notizen:", styles["Normal"]))
        elemente.append(Paragraph(zusatzinfo["notizen"], styles["Normal"]))
        elemente.append(Spacer(1, 0.3*cm))