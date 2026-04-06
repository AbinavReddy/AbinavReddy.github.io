"""
Static chart module — Matplotlib.
Generates a yearly crime trend line chart showing the COVID shift,
saved as a PNG to the images/ folder.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

from config import (
    FOCUS_CRIMES, CRIME_COLORS, IMAGES_DIR,
    FONT_FAMILY, BG_COLOR, GRID_COLOR,
)
from data_loader import load_and_prepare, get_yearly_counts


def create_yearly_trends_chart():
    """Build and save the yearly crime trends static figure."""

    _, df_focus = load_and_prepare()
    yearly = get_yearly_counts(df_focus)

    fig, ax = plt.subplots(figsize=(10, 5.5))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Plot each crime type
    for crime in FOCUS_CRIMES:
        subset = yearly[yearly["Unified_Category"] == crime]
        ax.plot(
            subset["Year"], subset["Count"],
            color=CRIME_COLORS[crime],
            linewidth=2.2,
            marker="o", markersize=3.5,
            label=crime,
        )

    # COVID shading
    ax.axvspan(2020, 2021.99, color="#e63946", alpha=0.08, label="_nolegend_")
    ax.annotate(
        "COVID-19", xy=(2021, ax.get_ylim()[1] * 0.92),
        fontsize=9, color="#e63946", fontweight="bold", ha="center",
    )

    # Styling
    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Number of Incidents", fontsize=11)
    ax.set_title(
        "Yearly Crime Trends in San Francisco (2003–2024)",
        fontsize=13, fontweight="bold", pad=12,
    )
    ax.legend(frameon=True, fontsize=9, loc="upper left", framealpha=0.9)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlim(2003, 2024)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: str(int(x))))
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    ax.grid(axis="y", color=GRID_COLOR, linewidth=0.6)
    ax.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()

    out_path = os.path.join(IMAGES_DIR, "yearly_crime_trends.png")
    fig.savefig(out_path, dpi=180, bbox_inches="tight", facecolor=BG_COLOR)
    plt.close(fig)
    print(f"  ✓ Static chart saved → {out_path}")
    return out_path


if __name__ == "__main__":
    create_yearly_trends_chart()
