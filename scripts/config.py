"""
Shared configuration for the Week 8 data story project.
Central place for paths, constants, and style settings used across all modules.
"""

import os

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "merged_crime_data_2003_2025.csv")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
VIZ_DIR = os.path.join(BASE_DIR, "visualizations")

# --- Data Filters ---
# Full years only (2025 is partial)
YEAR_MIN = 2003
YEAR_MAX = 2024

# Focus crimes used throughout the story
FOCUS_CRIMES = [
    "Assault", "Burglary", "Larceny/Theft",
    "Robbery", "Vehicle Theft",
]

# Periods for before/during/after COVID comparison
PRE_COVID_YEARS = range(2017, 2020)     # 2017-2019
COVID_YEARS = range(2020, 2022)         # 2020-2021
POST_COVID_YEARS = range(2022, 2025)    # 2022-2024

# --- Color Palette (consistent across all figures) ---
CRIME_COLORS = {
    "Assault":       "#e63946",
    "Burglary":      "#457b9d",
    "Larceny/Theft": "#f4a261",
    "Robbery":       "#2a9d8f",
    "Vehicle Theft": "#264653",
}

# Accent colors for period annotations
PERIOD_COLORS = {
    "pre_covid":  "#6c757d",
    "covid":      "#e63946",
    "post_covid": "#2a9d8f",
}

# --- Plot Style ---
FONT_FAMILY = "'Helvetica Neue', Helvetica, Arial, sans-serif"
BG_COLOR = "#fafafa"
GRID_COLOR = "#e0e0e0"
