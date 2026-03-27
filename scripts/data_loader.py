"""
Data loading and preprocessing module.
Reads the SF crime CSV and provides filtered, clean DataFrames
for the other visualization modules to consume.
"""

import pandas as pd
from config import DATA_PATH, YEAR_MIN, YEAR_MAX, FOCUS_CRIMES


DISTRICT_NAME_MAP = {
    "BAYVIEW": "Bayview",
    "CENTRAL": "Central",
    "INGLESIDE": "Ingleside",
    "MISSION": "Mission",
    "NORTHERN": "Northern",
    "PARK": "Park",
    "RICHMOND": "Richmond",
    "SOUTHERN": "Southern",
    "TARAVAL": "Taraval",
    "TENDERLOIN": "Tenderloin",
    "OUT OF SF": "Out of SF",
    "OUT OF SAN FRANCISCO": "Out of SF",
}


def load_raw_data():
    """Load the full CSV with parsed dates."""
    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["Incident_Date"],
        dtype={"Police_District": "category", "Unified_Category": "category"},
    )
    return df


def filter_full_years(df):
    """Keep only complete calendar years."""
    return df[(df["Year"] >= YEAR_MIN) & (df["Year"] <= YEAR_MAX)].copy()


def filter_focus_crimes(df):
    """Keep only rows matching the focus crime categories."""
    return df[df["Unified_Category"].isin(FOCUS_CRIMES)].copy()


def normalize_district_names(df):
    """Normalize district labels so categories are consistent across all outputs."""
    out = df.copy()
    norm = (
        out["Police_District"]
        .astype(str)
        .str.strip()
        .str.upper()
    )
    out["Police_District"] = norm.map(DISTRICT_NAME_MAP).fillna("Unknown")
    return out


def get_yearly_counts(df):
    """Return a DataFrame with yearly counts per crime category."""
    counts = (
        df.groupby(["Year", "Unified_Category"])
        .size()
        .reset_index(name="Count")
    )
    return counts


def get_district_counts(df, year_range):
    """Return crime counts per district and category for a year range."""
    subset = df[df["Year"].isin(year_range)]
    counts = (
        subset.groupby(["Police_District", "Unified_Category"])
        .size()
        .reset_index(name="Count")
    )
    return counts


def get_geo_data(df, year_range, crime_type):
    """Return lat/lon points for a specific crime type and year range."""
    subset = df[
        (df["Year"].isin(year_range))
        & (df["Unified_Category"] == crime_type)
        & df["Latitude"].notna()
        & df["Longitude"].notna()
    ]
    return subset[["Latitude", "Longitude"]].copy()


def load_and_prepare():
    """One-call convenience: load, filter years, filter focus crimes."""
    df = load_raw_data()
    df = filter_full_years(df)
    df = normalize_district_names(df)
    df_focus = filter_focus_crimes(df)
    return df, df_focus
