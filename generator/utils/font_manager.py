"""
Funktionen für das Font-Management mit lokal gespeicherten Fonts.
"""

import os
import logging
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ..config import FONTS_DIR

# Logger konfigurieren
logger = logging.getLogger(__name__)


def setup_fonts() -> bool:
    """
    Registriert die lokal gespeicherten Fonts für den Reiseplan-Generator.
    
    Returns:
        bool: True, wenn alle Fonts erfolgreich geladen wurden, sonst False
    """
    # Stelle sicher, dass das Fonts-Verzeichnis existiert
    FONTS_DIR.mkdir(exist_ok=True, parents=True)
    
    success = True
    
    # OpenSans Regular
    if not register_font('OpenSans', str(FONTS_DIR / 'OpenSans-Regular.ttf')):
        success = False
    
    # OpenSans Bold
    if not register_font('OpenSans-Bold', str(FONTS_DIR / 'OpenSans-Bold.ttf')):
        success = False
    
    return success


def register_font(font_name: str, font_path: str) -> bool:
    """
    Registriert eine lokale Font bei ReportLab.
    
    Args:
        font_name: Name der Font für ReportLab
        font_path: Pfad zur Font-Datei
        
    Returns:
        bool: True bei Erfolg, False bei Fehler
    """
    font_path_obj = Path(font_path)
    
    # Überprüfe, ob die Font-Datei existiert
    if not font_path_obj.exists():
        logger.error(f"Font-Datei nicht gefunden: {font_path}")
        logger.error(f"Bitte OpenSans-Fonts im Verzeichnis {FONTS_DIR} bereitstellen")
        return False
    
    # Registriere Font bei ReportLab
    try:
        pdfmetrics.registerFont(TTFont(font_name, font_path))
        logger.info(f"Font {font_name} wurde erfolgreich registriert")
        return True
    except Exception as e:
        logger.error(f"Fehler beim Registrieren der Font {font_name}: {e}")
        return False


def check_fonts_availability() -> bool:
    """
    Überprüft, ob die benötigten Fonts im Fonts-Verzeichnis vorhanden sind.
    
    Returns:
        bool: True, wenn alle benötigten Fonts verfügbar sind, sonst False
    """
    required_fonts = [
        ('OpenSans-Regular.ttf', 'OpenSans Regular'),
        ('OpenSans-Bold.ttf', 'OpenSans Bold')
    ]
    
    missing_fonts = []
    
    for font_file, font_name in required_fonts:
        font_path = FONTS_DIR / font_file
        if not font_path.exists():
            missing_fonts.append(font_name)
    
    if missing_fonts:
        logger.warning(f"Die folgenden Fonts fehlen: {', '.join(missing_fonts)}")
        logger.warning(f"Bitte stellen Sie die Font-Dateien im Verzeichnis {FONTS_DIR} bereit")
        return False
    
    return True