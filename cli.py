#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reiseplan-Generator CLI
Command Line Interface für den Reiseplan-Generator.
"""

import os
import sys
import argparse
from pathlib import Path
import logging

from generator.core import ReiseplanGenerator
from generator.config import BASE_DIR
from generator.utils.logging_setup import setup_logging


def main():
    """
    Hauptfunktion für die CLI des Reiseplan-Generators.
    """
    # Logger konfigurieren
    logger = setup_logging()
    
    # Parser für Kommandozeilenargumente
    parser = argparse.ArgumentParser(
        description="Generiert PDF-Reisepläne aus JSON-Daten."
    )
    
    parser.add_argument(
        "reiseplan_pfad",
        help="Pfad zur JSON-Datei mit Reisedaten"
    )
    
    parser.add_argument(
        "--debug",
        help="Aktiviert den Debug-Modus mit ausführlicher Protokollierung",
        action="store_true"
    )
    
    parser.add_argument(
        "--open",
        help="Öffnet das generierte PDF nach der Erstellung",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Debug-Modus
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug-Modus wurde aktiviert")
    
    # Überprüfe, ob die Reiseplan-Datei existiert
    reiseplan_pfad = Path(args.reiseplan_pfad)
    if not reiseplan_pfad.exists():
        logger.error(f"Fehler: Die angegebene Datei '{reiseplan_pfad}' existiert nicht.")
        sys.exit(1)
    
    # Initialisiere den Generator
    generator = ReiseplanGenerator()
    
    try:
        # Generiere den Reiseplan
        pdf_pfad = generator.generiere_reiseplan(reiseplan_pfad)
        
        if pdf_pfad:
            logger.info(f"Reiseplan wurde erfolgreich generiert: {pdf_pfad}")
            
            # Wenn --open Option gesetzt ist, versuche das PDF zu öffnen
            if args.open:
                oeffne_pdf(pdf_pfad)
        else:
            logger.error("Fehler beim Generieren des Reiseplans.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Unerwarteter Fehler beim Generieren des Reiseplans: {e}")
        sys.exit(1)


def oeffne_pdf(pdf_pfad: str):
    """
    Öffnet ein PDF-Dokument mit dem Standardprogramm des Betriebssystems.
    
    Args:
        pdf_pfad: Pfad zur PDF-Datei
    """
    if sys.platform.startswith('darwin'):  # macOS
        os.system(f"open '{pdf_pfad}'")
    elif sys.platform.startswith('win'):   # Windows
        os.system(f'start "" "{pdf_pfad}"')
    elif sys.platform.startswith('linux'): # Linux
        os.system(f"xdg-open '{pdf_pfad}'")
    else:
        print(f"Konnte PDF nicht automatisch öffnen. Datei hier finden: {pdf_pfad}")


if __name__ == "__main__":
    main()