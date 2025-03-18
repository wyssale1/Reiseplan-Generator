#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Reiseplan-Generator CLI
Command Line Interface für den Reiseplan-Generator
"""

import os
import sys
import argparse
from pathlib import Path

from reiseplan_generator import ReiseplanGenerator


def main():
    # Parser für Kommandozeilenargumente
    parser = argparse.ArgumentParser(
        description="Generiert PDF-Reisepläne aus JSON-Daten."
    )
    
    parser.add_argument(
        "reiseplan_pfad",
        help="Pfad zur JSON-Datei mit Reisedaten"
    )
    
    parser.add_argument(
        "--output-dir",
        help="Pfad zum Ausgabeverzeichnis (Standard: ./output)",
        default="./output"
    )
    
    parser.add_argument(
        "--assets-dir",
        help="Pfad zum Assets-Verzeichnis (Standard: ./assets)",
        default="./assets"
    )
    
    # Optional: API-Integration aktivieren
    parser.add_argument(
        "--api-integration",
        help="Aktiviert die API-Integration für Fluginformationen",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    # Überprüfe, ob die Reiseplan-Datei existiert
    reiseplan_pfad = Path(args.reiseplan_pfad)
    if not reiseplan_pfad.exists():
        print(f"Fehler: Die angegebene Datei '{reiseplan_pfad}' existiert nicht.")
        sys.exit(1)
    
    # Basis-Pfad ist das aktuelle Verzeichnis
    basis_pfad = Path.cwd()
    
    # Erstelle die Assets- und Output-Verzeichnisse, falls sie nicht existieren
    assets_pfad = Path(args.assets_dir)
    assets_pfad.mkdir(exist_ok=True)
    
    output_pfad = Path(args.output_dir)
    output_pfad.mkdir(exist_ok=True)
    
    # Überprüfe, ob die Assets-Unterverzeichnisse existieren und erstelle sie ggf.
    (assets_pfad / "airlines").mkdir(exist_ok=True)
    (assets_pfad / "hotels").mkdir(exist_ok=True)
    
    # Initialisiere den Generator
    generator = ReiseplanGenerator(basis_pfad=basis_pfad)
    
    try:
        # Generiere den Reiseplan
        pdf_pfad = generator.generiere_reiseplan(reiseplan_pfad)
        print(f"Reiseplan wurde erfolgreich generiert: {pdf_pfad}")
        
        # Wenn auf einem Desktop-System, versuche das PDF zu öffnen
        if sys.platform.startswith('darwin'):  # macOS
            os.system(f"open '{pdf_pfad}'")
        elif sys.platform.startswith('win'):  # Windows
            os.system(f'start "" "{pdf_pfad}"')
        elif sys.platform.startswith('linux'):  # Linux
            os.system(f"xdg-open '{pdf_pfad}'")
    except Exception as e:
        print(f"Fehler beim Generieren des Reiseplans: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()