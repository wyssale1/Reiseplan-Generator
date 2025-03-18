"""
Konfigurationseinstellungen für den Reiseplan-Generator.
"""

import os
from pathlib import Path

# Basis-Verzeichnisse
BASE_DIR = Path(os.getenv('REISEPLAN_BASE_DIR', Path.cwd()))
ASSETS_DIR = Path(os.getenv('REISEPLAN_ASSETS_DIR', BASE_DIR / 'assets'))
OUTPUT_DIR = Path(os.getenv('REISEPLAN_OUTPUT_DIR', BASE_DIR / 'output'))
FONTS_DIR = ASSETS_DIR / 'fonts'
AIRLINES_DIR = ASSETS_DIR / 'airlines'
HOTELS_DIR = ASSETS_DIR / 'hotels'

# API Konfiguration
FLIGHT_API_KEY = os.getenv('FLIGHT_API_KEY')
FLIGHT_API_URL = 'http://api.aviationstack.com/v1/flights'

# PDF Einstellungen
PDF_MARGIN = 2  # in cm

# Debug-Modus
DEBUG = os.getenv('REISEPLAN_DEBUG', 'False').lower() in ('true', '1', 't')

# Logging
LOG_LEVEL = os.getenv('REISEPLAN_LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('REISEPLAN_LOG_FILE', BASE_DIR / 'reiseplan_generator.log')