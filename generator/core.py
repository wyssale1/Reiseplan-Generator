"""
Hauptmodul des Reiseplan-Generators.
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, KeepTogether

from .config import OUTPUT_DIR, PDF_MARGIN
from .utils.font_manager import setup_fonts, check_fonts_availability
from .utils.json_schema import lade_json_reiseplan
from .elements import (
    erstelle_header, erstelle_uebersicht, erstelle_flug_block, 
    erstelle_hotel_block, erstelle_aktivitaet_block, erstelle_zusatzinfo_block
)
from .apis.flight_api import hole_fluginformationen, FlightAPIException

# Logger konfigurieren
logger = logging.getLogger(__name__)


class ReiseplanGenerator:
    """
    Hauptklasse für die Generierung von Reiseplänen.
    """
    
    def __init__(self):
        """
        Initialisiert den ReiseplanGenerator.
        """
        # Stelle sicher, dass die Verzeichnisse existieren
        OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
        
        # Überprüfe, ob die benötigten Fonts verfügbar sind
        if not check_fonts_availability():
            logger.warning("Nicht alle benötigten Fonts sind verfügbar!")
        
        # Registriere Fonts
        if not setup_fonts():
            logger.warning("Nicht alle Fonts konnten registriert werden!")
        
        # Styles für PDF
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
    def _setup_styles(self):
        """
        Richtet die Styles für das PDF ein.
        """
        # Titel-Style
        self.styles.add(ParagraphStyle(
            name='Titel',
            fontName='OpenSans-Bold',
            fontSize=24,
            spaceAfter=12
        ))
        
        # Untertitel-Style
        self.styles.add(ParagraphStyle(
            name='Untertitel',
            fontName='OpenSans-Bold',
            fontSize=16,
            spaceAfter=8
        ))
        
        # Modifiziere existierenden 'Normal' Style
        self.styles['Normal'].fontName = 'OpenSans'
        self.styles['Normal'].fontSize = 11
        self.styles['Normal'].spaceAfter = 6
    
    def generiere_reiseplan(self, reiseplan_pfad: Union[str, Path]) -> Optional[str]:
        """
        Generiert einen PDF-Reiseplan aus einer JSON-Datei.
        
        Args:
            reiseplan_pfad: Pfad zur JSON-Datei mit Reisedaten
            
        Returns:
            Optional[str]: Pfad zur generierten PDF-Datei oder None bei Fehler
        """
        # Lade Reiseplan-Daten
        reiseplan_pfad = Path(reiseplan_pfad)
        reiseplan_daten = lade_json_reiseplan(reiseplan_pfad)
        
        if not reiseplan_daten:
            logger.error(f"Konnte Reiseplan-Daten nicht laden: {reiseplan_pfad}")
            return None
        
        # Ergänze Flugdaten, falls minimal
        if "fluege" in reiseplan_daten and reiseplan_daten["fluege"]:
            for i, flug in enumerate(reiseplan_daten["fluege"]):
                if self._ist_minimal_flug(flug):
                    logger.info(f"Minimal Flug gefunden: {flug['flugNr']} am {flug['flugDatum']}")
                    try:
                        ergaenzte_flugdaten = hole_fluginformationen(flug["flugNr"], flug["flugDatum"])
                        # Bewahre die Buchungsnummer, falls vorhanden
                        if "buchungsNr" in flug and flug["buchungsNr"]:
                            ergaenzte_flugdaten["buchungsNr"] = flug["buchungsNr"]
                        reiseplan_daten["fluege"][i] = ergaenzte_flugdaten
                        logger.info(f"Flugdaten erfolgreich ergänzt für Flug {flug['flugNr']}")
                    except FlightAPIException as e:
                        logger.warning(f"Konnte Flugdaten nicht ergänzen: {e}")
                        # Beibehalten der minimalen Flugdaten
                        continue
        
        # Erstelle PDF-Dateiname
        pdf_dateiname = f"{reiseplan_daten['titel'].replace(' ', '-')}.pdf"
        pdf_pfad = OUTPUT_DIR / pdf_dateiname
        
        # Erstelle PDF-Dokument
        doc = SimpleDocTemplate(
            str(pdf_pfad),
            pagesize=A4,
            rightMargin=PDF_MARGIN*cm,
            leftMargin=PDF_MARGIN*cm,
            topMargin=PDF_MARGIN*cm,
            bottomMargin=PDF_MARGIN*cm
        )
        
        # Erstelle Inhalt
        elemente = []
        
        # Header und Übersicht
        erstelle_header(elemente, reiseplan_daten, self.styles)
        erstelle_uebersicht(elemente, reiseplan_daten, self.styles)
        
        # Flüge
        if "fluege" in reiseplan_daten and reiseplan_daten["fluege"]:
            for flug in reiseplan_daten["fluege"]:
                flug_elemente = []
                erstelle_flug_block(flug_elemente, flug, self.styles)
                # Verwende KeepTogether, um zu verhindern, dass Flug-Blöcke geteilt werden
                elemente.append(KeepTogether(flug_elemente))
        
        # Hotels
        if "hotels" in reiseplan_daten and reiseplan_daten["hotels"]:
            for hotel in reiseplan_daten["hotels"]:
                hotel_elemente = []
                erstelle_hotel_block(hotel_elemente, hotel, self.styles)
                # Verwende KeepTogether, um zu verhindern, dass Hotel-Blöcke geteilt werden
                elemente.append(KeepTogether(hotel_elemente))
        
        # Aktivitäten
        if "aktivitaeten" in reiseplan_daten and reiseplan_daten["aktivitaeten"]:
            for aktivitaet in reiseplan_daten["aktivitaeten"]:
                aktivitaet_elemente = []
                erstelle_aktivitaet_block(aktivitaet_elemente, aktivitaet, self.styles)
                # Verwende KeepTogether, um zu verhindern, dass Aktivitäts-Blöcke geteilt werden
                elemente.append(KeepTogether(aktivitaet_elemente))
        
        # Zusatzinformationen
        if "zusatzinfo" in reiseplan_daten:
            zusatzinfo_elemente = []
            erstelle_zusatzinfo_block(zusatzinfo_elemente, reiseplan_daten["zusatzinfo"], self.styles)
            # Verwende KeepTogether, um zu verhindern, dass Zusatzinfo-Blöcke geteilt werden
            elemente.append(KeepTogether(zusatzinfo_elemente))
        
        # Erstelle das PDF
        try:
            doc.build(elemente)
            logger.info(f"Reiseplan erfolgreich erstellt: {pdf_pfad}")
            return str(pdf_pfad)
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des PDFs: {e}")
            return None
    
    def _ist_minimal_flug(self, flug: Dict[str, Any]) -> bool:
        """
        Überprüft, ob ein Flug nur minimal Daten enthält.
        
        Ein minimaler Flug enthält nur die Flugnummer, das Datum und optional eine Buchungsnummer.
        
        Args:
            flug: Flugdaten aus JSON
            
        Returns:
            bool: True, wenn es sich um einen minimalen Flug handelt, sonst False
        """
        # Erforderliche Felder für minimalen Flug
        minimal_required = ["flugNr", "flugDatum"]
        
        # Optional erlaubte Felder
        minimal_optional = ["buchungsNr"]
        
        # Prüfe, ob alle erforderlichen Felder vorhanden sind
        if not all(key in flug for key in minimal_required):
            return False
        
        # Prüfe, ob nur erforderliche und optionale Felder vorhanden sind
        allowed_keys = minimal_required + minimal_optional
        return all(key in allowed_keys for key in flug.keys())