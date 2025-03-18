"""
Dienstprogramme für die Datumsformatierung und -konvertierung.
"""

import datetime
from typing import Optional


def formatiere_datum_zeit(iso_datum_zeit: str) -> str:
    """
    Formatiert einen ISO-Datum-Zeit-String in ein lesbares Format.
    
    Args:
        iso_datum_zeit: ISO-formatierter Datum-Zeit-String
        
    Returns:
        str: Formatierter Datum-Zeit-String (z.B. "01.01.2025, 14:30")
    """
    try:
        dt = datetime.datetime.fromisoformat(iso_datum_zeit)
        return dt.strftime("%d.%m.%Y, %H:%M")
    except (ValueError, TypeError):
        return iso_datum_zeit


def formatiere_zeit(iso_datum_zeit: str) -> str:
    """
    Extrahiert und formatiert die Uhrzeit aus einem ISO-Datum-Zeit-String.
    
    Args:
        iso_datum_zeit: ISO-formatierter Datum-Zeit-String
        
    Returns:
        str: Formatierter Zeit-String (z.B. "14:30")
    """
    try:
        dt = datetime.datetime.fromisoformat(iso_datum_zeit)
        return dt.strftime("%H:%M")
    except (ValueError, TypeError):
        return iso_datum_zeit


def formatiere_datum(iso_datum: str) -> str:
    """
    Formatiert ein ISO-Datum in ein lesbares Format.
    
    Args:
        iso_datum: ISO-formatierter Datum-String
        
    Returns:
        str: Formatierter Datum-String (z.B. "01.01.2025")
    """
    try:
        dt = datetime.datetime.fromisoformat(iso_datum)
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return iso_datum


def datum_zu_iso(datum: str, format_str: str = "%d.%m.%Y") -> Optional[str]:
    """
    Konvertiert einen formatierten Datum-String in einen ISO-Datum-String.
    
    Args:
        datum: Formatierter Datum-String
        format_str: Format des Eingabe-Strings
        
    Returns:
        Optional[str]: ISO-formatierter Datum-String oder None bei Fehler
    """
    try:
        dt = datetime.datetime.strptime(datum, format_str)
        return dt.date().isoformat()
    except (ValueError, TypeError):
        return None