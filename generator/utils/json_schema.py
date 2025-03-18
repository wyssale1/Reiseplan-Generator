"""
JSON-Schema-Validierung für Reiseplan-Daten.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

# Logger konfigurieren
logger = logging.getLogger(__name__)

# Definiere das Schema für einen Flug
FLUG_SCHEMA = {
    "required": ["flugNr", "flugDatum"],
    "optional": ["airline", "abflugOrt", "abflugCode", "abflugZeit", 
                 "ankunftOrt", "ankunftCode", "ankunftZeit", "buchungsNr"]
}

# Definiere das Schema für ein Hotel
HOTEL_SCHEMA = {
    "required": ["name", "adresse", "checkin", "checkout"],
    "optional": ["buchungsNr"]
}

# Definiere das Schema für eine Aktivität
AKTIVITAET_SCHEMA = {
    "required": ["name", "datum", "startzeit", "endzeit"],
    "optional": ["ort", "buchungsNr"]
}

# Definiere das Schema für den gesamten Reiseplan
REISEPLAN_SCHEMA = {
    "required": ["titel", "startdatum", "enddatum", "reiseziel"],
    "optional": ["reisende", "fluege", "hotels", "aktivitaeten", "zusatzinfo"]
}


def validiere_reiseplan(reiseplan_daten: Dict[str, Any]) -> List[str]:
    """
    Validiert die Reiseplan-Daten gegen das Schema.
    
    Args:
        reiseplan_daten: Die zu validierenden Reiseplan-Daten
        
    Returns:
        List[str]: Liste von Fehlermeldungen, leer wenn keine Fehler gefunden wurden
    """
    fehler = []
    
    # Prüfe erforderliche Felder für den Reiseplan
    for feld in REISEPLAN_SCHEMA["required"]:
        if feld not in reiseplan_daten:
            fehler.append(f"Erforderliches Feld '{feld}' fehlt im Reiseplan")
    
    # Prüfe Flüge, falls vorhanden
    if "fluege" in reiseplan_daten and reiseplan_daten["fluege"]:
        for i, flug in enumerate(reiseplan_daten["fluege"]):
            for feld in FLUG_SCHEMA["required"]:
                if feld not in flug:
                    fehler.append(f"Erforderliches Feld '{feld}' fehlt in Flug #{i+1}")
    
    # Prüfe Hotels, falls vorhanden
    if "hotels" in reiseplan_daten and reiseplan_daten["hotels"]:
        for i, hotel in enumerate(reiseplan_daten["hotels"]):
            for feld in HOTEL_SCHEMA["required"]:
                if feld not in hotel:
                    fehler.append(f"Erforderliches Feld '{feld}' fehlt in Hotel #{i+1}")
    
    # Prüfe Aktivitäten, falls vorhanden
    if "aktivitaeten" in reiseplan_daten and reiseplan_daten["aktivitaeten"]:
        for i, aktivitaet in enumerate(reiseplan_daten["aktivitaeten"]):
            for feld in AKTIVITAET_SCHEMA["required"]:
                if feld not in aktivitaet:
                    fehler.append(f"Erforderliches Feld '{feld}' fehlt in Aktivität #{i+1}")
    
    return fehler


def lade_json_reiseplan(datei_pfad: Path) -> Optional[Dict[str, Any]]:
    """
    Lädt und validiert eine JSON-Reiseplan-Datei.
    
    Args:
        datei_pfad: Pfad zur JSON-Datei
        
    Returns:
        Optional[Dict[str, Any]]: Validierte Reiseplan-Daten oder None bei Fehler
    """
    try:
        with open(datei_pfad, 'r', encoding='utf-8') as f:
            reiseplan_daten = json.load(f)
        
        # Validiere die Daten
        fehler = validiere_reiseplan(reiseplan_daten)
        if fehler:
            for fehler_msg in fehler:
                logger.error(fehler_msg)
            return None
        
        return reiseplan_daten
    except json.JSONDecodeError as e:
        logger.error(f"Fehler beim Parsen der JSON-Datei: {e}")
        return None
    except Exception as e:
        logger.error(f"Fehler beim Laden der Reiseplan-Datei: {e}")
        return None