"""
Integration mit Flight-APIs für den Reiseplan-Generator.
"""

import requests
import logging
from typing import Dict, Any, Optional
import datetime

from ..config import FLIGHT_API_KEY, FLIGHT_API_URL

# Logger konfigurieren
logger = logging.getLogger(__name__)


class FlightAPIException(Exception):
    """Exception für Flight-API-Fehler."""
    pass


def hole_fluginformationen(flug_nr: str, flug_datum: str) -> Optional[Dict[str, Any]]:
    """
    Holt Fluginformationen von einer Flight-API.
    
    Args:
        flug_nr: Flugnummer (z.B. 'LX1234')
        flug_datum: Datum des Fluges im Format 'YYYY-MM-DD'
        
    Returns:
        Optional[Dict[str, Any]]: Vollständige Flugdaten oder None bei Fehler
        
    Raises:
        FlightAPIException: Bei Fehlern in der API-Integration
    """
    if not FLIGHT_API_KEY:
        logger.warning("Kein API-Schlüssel für Flight-API konfiguriert")
        raise FlightAPIException("Kein API-Schlüssel konfiguriert")
    
    try:
        logger.info(f"Rufe Flugdaten für {flug_nr} am {flug_datum} ab...")
        
        # Bereite API-Anfrage vor
        params = {
            "access_key": FLIGHT_API_KEY,
            "flight_iata": flug_nr,
            "flight_date": flug_datum
        }
        
        # Sende API-Anfrage
        response = requests.get(FLIGHT_API_URL, params=params)
        response.raise_for_status()
        
        # Verarbeite Antwort
        data = response.json()
        
        if "data" in data and len(data["data"]) > 0:
            flight_data = data["data"][0]
            
            # Extrahiere relevante Daten
            airline = flight_data["airline"]["name"]
            departure = flight_data["departure"]
            arrival = flight_data["arrival"]
            
            # Erstelle Flug-Dictionary
            return {
                "airline": airline,
                "flugNr": flug_nr,
                "abflugOrt": departure["airport"],
                "abflugCode": departure["iata"],
                "abflugZeit": departure["scheduled"],
                "ankunftOrt": arrival["airport"],
                "ankunftCode": arrival["iata"],
                "ankunftZeit": arrival["scheduled"],
                "buchungsNr": flight_data.get("flight", {}).get("number", "")
            }
        else:
            logger.warning(f"Keine Daten für Flug {flug_nr} am {flug_datum} gefunden")
            raise FlightAPIException(f"Keine Daten für Flug {flug_nr} gefunden")
            
    except requests.RequestException as e:
        logger.error(f"HTTP-Fehler bei der Flight-API-Anfrage: {e}")
        raise FlightAPIException(f"Fehler bei der API-Anfrage: {str(e)}")
    except KeyError as e:
        logger.error(f"Unerwartetes Format der Flight-API-Antwort: {e}")
        raise FlightAPIException(f"Unerwartetes Format der API-Antwort: {str(e)}")
    except Exception as e:
        logger.error(f"Unerwarteter Fehler bei der Flight-API-Integration: {e}")
        raise FlightAPIException(f"Unerwarteter Fehler: {str(e)}")