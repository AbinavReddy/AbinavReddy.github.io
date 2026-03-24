"""
Main orchestrator — generates all three visualizations for the Week 8 data story.
Run from the scripts/ directory:
    python main.py
"""

from static_chart import create_yearly_trends_chart
from map_viz import create_burglary_heatmap
from interactive_viz import create_district_comparison


def main():
    print("=== Week 8 Data Story — Generating Visualizations ===\n")

    print("1/3  Static chart (matplotlib) ...")
    create_yearly_trends_chart()

    print("2/3  Map (Folium) ...")
    create_burglary_heatmap()

    print("3/3  Interactive chart (Plotly) ...")
    create_district_comparison()

    print("\n=== Done! All outputs are in images/ and visualizations/ ===")


if __name__ == "__main__":
    main()
