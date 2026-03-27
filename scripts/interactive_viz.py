"""
Interactive Plotly visualization module.
Creates a grouped bar chart comparing crime counts by district
across three periods: pre-COVID, during-COVID, post-COVID.
Users can toggle crime types and periods via the legend.
"""

import plotly.express as px
import pandas as pd
import os

from config import (
    FOCUS_CRIMES, CRIME_COLORS,
    PRE_COVID_YEARS, COVID_YEARS, POST_COVID_YEARS,
    VIZ_DIR, FONT_FAMILY, BG_COLOR,
)
from data_loader import load_and_prepare


EXPECTED_DISTRICTS = [
    "Bayview", "Central", "Ingleside", "Mission", "Northern",
    "Park", "Richmond", "Southern", "Taraval", "Tenderloin",
]


def _label_period(year):
    if year in PRE_COVID_YEARS:
        return "Pre-COVID (2017–19)"
    if year in COVID_YEARS:
        return "COVID (2020–21)"
    if year in POST_COVID_YEARS:
        return "Post-COVID (2022–24)"
    return None


def create_district_comparison():
    """Build an interactive Plotly chart: crime shift by district and period."""

    _, df_focus = load_and_prepare()

    # Keep only the three comparison periods
    all_years = list(PRE_COVID_YEARS) + list(COVID_YEARS) + list(POST_COVID_YEARS)
    df_period = df_focus[df_focus["Year"].isin(all_years)].copy()
    df_period["Period"] = df_period["Year"].apply(_label_period)

    # Annualize: total count / number of years in period — fair comparison
    period_lengths = {
        "Pre-COVID (2017–19)": len(list(PRE_COVID_YEARS)),
        "COVID (2020–21)": len(list(COVID_YEARS)),
        "Post-COVID (2022–24)": len(list(POST_COVID_YEARS)),
    }

    counts = (
        df_period
        .groupby(["Police_District", "Period", "Unified_Category"])
        .size()
        .reset_index(name="TotalCount")
    )
    counts["YearsInPeriod"] = counts["Period"].map(period_lengths)
    counts["AvgYearlyCount"] = (counts["TotalCount"] / counts["YearsInPeriod"]).round(0).astype(int)

    # Sort periods in chronological order
    period_order = ["Pre-COVID (2017–19)", "COVID (2020–21)", "Post-COVID (2022–24)"]
    counts["Period"] = pd.Categorical(counts["Period"], categories=period_order, ordered=True)

    # Keep only core SF districts and enforce stable district ordering.
    counts = counts[counts["Police_District"].isin(EXPECTED_DISTRICTS)].copy()
    counts["Police_District"] = pd.Categorical(
        counts["Police_District"], categories=EXPECTED_DISTRICTS, ordered=True
    )

    observed = set(counts["Police_District"].dropna().astype(str).unique())
    missing = [d for d in EXPECTED_DISTRICTS if d not in observed]
    if missing:
        print(f"  ! Warning: missing districts in filtered data: {', '.join(missing)}")

    fig = px.bar(
        counts,
        x="Police_District",
        y="AvgYearlyCount",
        color="Unified_Category",
        facet_col="Period",
        barmode="group",
        color_discrete_map=CRIME_COLORS,
        labels={
            "AvgYearlyCount": "Avg. Yearly Incidents",
            "Police_District": "District",
            "Unified_Category": "Crime Type",
        },
        title="How Crime Shifted Across SF Districts: Before, During, and After COVID",
        facet_col_spacing=0.055,
        category_orders={
            "Period": period_order,
            "Police_District": EXPECTED_DISTRICTS,
        },
    )

    fig.update_layout(
        font_family=FONT_FAMILY,
        plot_bgcolor=BG_COLOR,
        paper_bgcolor="white",
        height=620,
        margin=dict(t=90, b=145, l=75, r=35),
        legend=dict(
            title="Crime Type",
            orientation="h",
            yanchor="top", y=-0.18,
            xanchor="center", x=0.5,
        ),
    )
    fig.update_xaxes(tickangle=-35, automargin=True, title_standoff=8)
    fig.update_yaxes(automargin=True, title_standoff=12, tickformat=",")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    out_path = os.path.join(VIZ_DIR, "district_comparison.html")
    fig.write_html(out_path, include_plotlyjs="cdn")
    print(f"  ✓ Plotly chart saved → {out_path}")
    return out_path


if __name__ == "__main__":
    create_district_comparison()
