"""
Konfiguration des Loggings für den Reiseplan-Generator.
"""

import logging
import sys
from pathlib import Path

from ..config import LOG_LEVEL, LOG_FILE, DEBUG


def setup_logging():
    """
    Konfiguriert das Logging für den Reiseplan-Generator.
    """
    # Bestimme das Log-Level
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    log_level = level_map.get(LOG_LEVEL.upper(), logging.INFO)
    
    # Erstelle den Logger
    logger = logging.getLogger('reiseplan_generator')
    logger.setLevel(log_level)
    
    # Verhindere Dopplung der Log-Meldungen
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Formatter für Log-Meldungen
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Füge einen Handler für die Konsole hinzu
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Füge einen Handler für die Log-Datei hinzu
    if LOG_FILE:
        log_file = Path(LOG_FILE)
        log_file.parent.mkdir(exist_ok=True, parents=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Logge Debugging-Infos, wenn der Debug-Modus aktiviert ist
    if DEBUG:
        logger.debug("Debug-Modus ist aktiviert")
    
    return logger