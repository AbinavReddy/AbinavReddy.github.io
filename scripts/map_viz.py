"""
Map visualization module — Folium.
Creates a side-by-side heatmap comparison of burglary hotspots
before COVID (2017-2019) vs during COVID (2020-2021).
"""

import folium
from folium.plugins import HeatMap
import os

from config import (
    PRE_COVID_YEARS, COVID_YEARS, VIZ_DIR,
)
from data_loader import load_and_prepare, get_geo_data


def create_burglary_heatmap():
    """Build a Folium heatmap showing burglary concentration during COVID."""

    df, _ = load_and_prepare()

    # Get geo points for burglary in the two periods
    pre_points = get_geo_data(df, PRE_COVID_YEARS, "Burglary")
    covid_points = get_geo_data(df, COVID_YEARS, "Burglary")

    # Sample down to keep file size reasonable (max 15k points per layer)
    if len(pre_points) > 15000:
        pre_points = pre_points.sample(15000, random_state=42)
    if len(covid_points) > 15000:
        covid_points = covid_points.sample(15000, random_state=42)

    # Center on San Francisco
    sf_center = [37.76, -122.44]

    m = folium.Map(location=sf_center, zoom_start=12, tiles="cartodbpositron")

    # Pre-COVID layer (blue)
    pre_heat = HeatMap(
        pre_points[["Latitude", "Longitude"]].values.tolist(),
        name="Pre-COVID (2017–2019)",
        radius=10, blur=12, max_zoom=13,
        gradient={0.2: "#457b9d", 0.5: "#1d3557", 0.8: "#e63946", 1.0: "#e63946"},
    )
    pre_heat.add_to(m)

    # COVID layer (red) — hidden by default so user can toggle
    covid_fg = folium.FeatureGroup(name="During COVID (2020–2021)", show=False)
    HeatMap(
        covid_points[["Latitude", "Longitude"]].values.tolist(),
        radius=10, blur=12, max_zoom=13,
        gradient={0.2: "#f4a261", 0.5: "#e76f51", 0.8: "#e63946", 1.0: "#9b2226"},
    ).add_to(covid_fg)
    covid_fg.add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)

    out_path = os.path.join(VIZ_DIR, "burglary_heatmap.html")
    m.save(out_path)
    print(f"  ✓ Folium map saved  → {out_path}")
    return out_path


if __name__ == "__main__":
    create_burglary_heatmap()
