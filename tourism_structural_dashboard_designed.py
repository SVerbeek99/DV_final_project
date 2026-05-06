"""
Tourism & Structural Transformation Explorer — designed Dash version
--------------------------------------------------------------------
Place these files in the same folder as this script:
- employmentdata.csv
- tourism15indicators.csv

Run:
    pip install dash plotly pandas numpy
    python tourism_structural_dashboard_designed.py

Open:
    http://127.0.0.1:8050
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html


# -----------------------------------------------------------------------------
# 1. File paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
EMPLOYMENT_CSV = BASE_DIR / "employmentdata.csv"
TOURISM_CSV = BASE_DIR / "tourism15indicators.csv"

if not EMPLOYMENT_CSV.exists():
    EMPLOYMENT_CSV = Path("/mnt/data/employmentdata.csv")
if not TOURISM_CSV.exists():
    TOURISM_CSV = Path("/mnt/data/tourism15indicators.csv")


# -----------------------------------------------------------------------------
# 2. Metadata and style
# -----------------------------------------------------------------------------
REGION_MAP = {
    "Spain": "Europe",
    "France": "Europe",
    "Croatia": "Europe",
    "Iceland": "Europe",
    "Thailand": "Asia",
    "Indonesia": "Asia",
    "United Arab Emirates": "Middle East",
    "Morocco": "Africa",
    "South Africa": "Africa",
    "Dominican Republic": "Latin America & Caribbean",
    "Mexico": "Latin America & Caribbean",
    "Argentina": "Latin America & Caribbean",
    "Chile": "Latin America & Caribbean",
    "Colombia": "Latin America & Caribbean",
    "United States": "North America",
}

REGION_COLORS = {
    "Europe": "#A78BFA",
    "Asia": "#22D3EE",
    "Middle East": "#34D399",
    "Africa": "#FBBF24",
    "Latin America & Caribbean": "#FB7185",
    "North America": "#60A5FA",
    "Other": "#94A3B8",
}

SECTOR_COLORS = {
    "Services": "#22C55E",
    "Industry": "#F97316",
    "Agriculture": "#38BDF8",
    "Tourism": "#E879F9",
}

THEME = {
    "paper": "#111827",
    "card": "#172033",
    "card2": "#1F2937",
    "grid": "#334155",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
    "accent": "#F97316",
    "accent2": "#22D3EE",
}

SERIES_RENAME = {
    # Employment structure
    "Employment in services, male (% of male employment) (modeled ILO estimate)": "services_male",
    "Employment in services, female (% of female employment) (modeled ILO estimate)": "services_female",
    "Employment in industry, male (% of male employment) (modeled ILO estimate)": "industry_male",
    "Employment in industry, female (% of female employment) (modeled ILO estimate)": "industry_female",
    "Employment in agriculture, male (% of male employment) (modeled ILO estimate)": "agriculture_male",
    "Employment in agriculture, female (% of female employment) (modeled ILO estimate)": "agriculture_female",
    "Agriculture, forestry, and fishing, value added (current US$)": "agriculture_value_added_usd",
    "Industry (including construction), value added (current US$)": "industry_value_added_usd",
    # Tourism, development, social outcomes
    "International tourism, receipts (% of total exports)": "tourism_receipts_pct_exports",
    "Urban population (% of total population)": "urban_population_pct",
    "GDP per capita (current US$)": "gdp_per_capita_current_usd",
    "Poverty headcount ratio at national poverty lines (% of population)": "poverty_headcount_pct",
    "Gini index": "gini_index",
}

VAR_LABELS = {
    "tourism_receipts_pct_exports": "Tourism receipts (% of total exports)",
    "urban_population_pct": "Urban population (% of total)",
    "gdp_per_capita_current_usd": "GDP per capita (current US$)",
    "poverty_headcount_pct": "Poverty headcount (% of population)",
    "gini_index": "GINI index",
    "services_male": "Services employment, male (%)",
    "services_female": "Services employment, female (%)",
    "services_avg": "Services employment, gender-average (%)",
    "industry_male": "Industry employment, male (%)",
    "industry_female": "Industry employment, female (%)",
    "industry_avg": "Industry employment, gender-average (%)",
    "agriculture_male": "Agriculture employment, male (%)",
    "agriculture_female": "Agriculture employment, female (%)",
    "agriculture_avg": "Agriculture employment, gender-average (%)",
    "service_dominance_index": "Service dominance index",
    "agriculture_value_added_usd": "Agriculture value added (current US$)",
    "industry_value_added_usd": "Industry value added (current US$)",
}

SECTOR_OPTIONS = [
    {"label": "Services employment, gender-average", "value": "services_avg"},
    {"label": "Industry employment, gender-average", "value": "industry_avg"},
    {"label": "Agriculture employment, gender-average", "value": "agriculture_avg"},
    {"label": "Services employment, male", "value": "services_male"},
    {"label": "Services employment, female", "value": "services_female"},
    {"label": "Industry employment, male", "value": "industry_male"},
    {"label": "Industry employment, female", "value": "industry_female"},
    {"label": "Agriculture employment, male", "value": "agriculture_male"},
    {"label": "Agriculture employment, female", "value": "agriculture_female"},
]

OUTCOME_OPTIONS = [
    {"label": "Poverty headcount", "value": "poverty_headcount_pct"},
    {"label": "GINI index", "value": "gini_index"},
    {"label": "GDP per capita", "value": "gdp_per_capita_current_usd"},
    {"label": "Urban population", "value": "urban_population_pct"},
]


# -----------------------------------------------------------------------------
# 3. Data loading and transformation
# -----------------------------------------------------------------------------
def read_wdi_wide(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Could not find {path}. Put the CSV in the same folder as this script.")

    raw = pd.read_csv(path)
    raw = raw[raw["Country Code"].astype(str).str.match(r"^[A-Z]{3}$", na=False)].copy()
    raw = raw[raw["Series Name"].isin(SERIES_RENAME.keys())].copy()

    year_cols = [c for c in raw.columns if re.match(r"^\d{4} \[YR\d{4}\]$", c)]
    long_df = raw.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        value_vars=year_cols,
        var_name="year_raw",
        value_name="value",
    )
    long_df["year"] = long_df["year_raw"].str.extract(r"(\d{4})").astype(int)
    long_df["indicator"] = long_df["Series Name"].map(SERIES_RENAME)
    long_df["value"] = pd.to_numeric(long_df["value"].replace("..", np.nan), errors="coerce")
    return long_df[["Country Name", "Country Code", "year", "indicator", "value"]]


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    needed = [
        "services_male", "services_female", "industry_male", "industry_female",
        "agriculture_male", "agriculture_female",
    ]
    for col in needed:
        if col not in df.columns:
            df[col] = np.nan

    df["services_avg"] = df[["services_male", "services_female"]].mean(axis=1)
    df["industry_avg"] = df[["industry_male", "industry_female"]].mean(axis=1)
    df["agriculture_avg"] = df[["agriculture_male", "agriculture_female"]].mean(axis=1)
    df["service_dominance_index"] = df["services_avg"] - (df["industry_avg"] + df["agriculture_avg"])

    if "gdp_per_capita_current_usd" in df.columns:
        df["log_gdp_per_capita"] = np.log10(
            df["gdp_per_capita_current_usd"].where(df["gdp_per_capita_current_usd"] > 0)
        )
    return df


def build_dataset() -> pd.DataFrame:
    employment_long = read_wdi_wide(EMPLOYMENT_CSV)
    tourism_long = read_wdi_wide(TOURISM_CSV)
    long_df = pd.concat([employment_long, tourism_long], ignore_index=True)

    wide = (
        long_df.pivot_table(
            index=["Country Name", "Country Code", "year"],
            columns="indicator",
            values="value",
            aggfunc="first",
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )

    wide = add_derived_columns(wide)
    wide["region"] = wide["Country Name"].map(REGION_MAP).fillna("Other")
    return wide.sort_values(["Country Name", "year"])


def tourism_groups(series: pd.Series) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    out = pd.Series("No tourism data", index=s.index, dtype="object")
    valid = s.dropna()
    if len(valid) >= 3:
        q1, q2 = valid.quantile([1 / 3, 2 / 3])
        out[s <= q1] = "Low tourism dependence"
        out[(s > q1) & (s <= q2)] = "Medium tourism dependence"
        out[s > q2] = "High tourism dependence"
    elif len(valid) > 0:
        out[s.notna()] = "Tourism data available"
    return out


def latest_snapshot(df: pd.DataFrame, year: int, countries: Iterable[str]) -> pd.DataFrame:
    base_cols = ["Country Name", "Country Code", "region"]
    variable_cols = [c for c in df.columns if c not in base_cols + ["year"]]

    rows: List[Dict[str, object]] = []
    for country in countries:
        sub = df[(df["Country Name"] == country) & (df["year"] <= year)].sort_values("year")
        if sub.empty:
            continue
        row: Dict[str, object] = {
            "Country Name": country,
            "Country Code": sub["Country Code"].dropna().iloc[-1],
            "region": sub["region"].dropna().iloc[-1],
            "selected_year": year,
        }
        for var in variable_cols:
            valid = sub[["year", var]].dropna()
            if valid.empty:
                row[var] = np.nan
                row[f"{var}_source_year"] = np.nan
            else:
                row[var] = valid[var].iloc[-1]
                row[f"{var}_source_year"] = int(valid["year"].iloc[-1])
        rows.append(row)

    snap = pd.DataFrame(rows)
    if not snap.empty:
        snap = add_derived_columns(snap)
        snap["tourism_group"] = tourism_groups(snap.get("tourism_receipts_pct_exports", pd.Series(index=snap.index)))
    return snap


def exact_snapshot(df: pd.DataFrame, year: int, countries: Iterable[str]) -> pd.DataFrame:
    snap = df[(df["year"] == year) & (df["Country Name"].isin(countries))].copy()
    if not snap.empty:
        snap["selected_year"] = year
        snap = add_derived_columns(snap)
        snap["tourism_group"] = tourism_groups(snap.get("tourism_receipts_pct_exports", pd.Series(index=snap.index)))
        for c in [col for col in snap.columns if col not in ["Country Name", "Country Code", "region", "year", "selected_year"]]:
            snap[f"{c}_source_year"] = year
    return snap


def get_snapshot(df: pd.DataFrame, year: int, countries: Iterable[str], mode: str) -> pd.DataFrame:
    if mode == "exact":
        return exact_snapshot(df, year, countries)
    return latest_snapshot(df, year, countries)


def source_year(row: pd.Series, var: str) -> str:
    value = row.get(f"{var}_source_year", np.nan)
    if pd.isna(value):
        return "n/a"
    return str(int(value))


# -----------------------------------------------------------------------------
# 4. Load data
# -----------------------------------------------------------------------------
df = build_dataset()
COUNTRIES = [str(c) for c in sorted(df["Country Name"].dropna().unique())]
YEARS = [int(y) for y in sorted(df["year"].dropna().unique())]
DEFAULT_COUNTRIES = [
    c for c in ["Spain", "Thailand", "Morocco", "Dominican Republic", "Mexico", "South Africa", "Indonesia", "Croatia", "Colombia"]
    if c in COUNTRIES
]
DEFAULT_FOCUS_COUNTRY = "Thailand" if "Thailand" in COUNTRIES else COUNTRIES[0]
DEFAULT_YEAR = 2020 if 2020 in YEARS else max(YEARS)


# -----------------------------------------------------------------------------
# 5. Figure helpers
# -----------------------------------------------------------------------------
def base_layout(fig: go.Figure, title: str | None = None) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=THEME["card"],
        plot_bgcolor=THEME["card"],
        font=dict(color=THEME["text"], family="Inter, Segoe UI, Arial, sans-serif"),
        title=dict(text=title, font=dict(size=18, color="#F9FAFB"), x=0.02, xanchor="left") if title else None,
        margin=dict(l=30, r=30, t=70, b=40),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(bgcolor="#0F172A", font_size=12, font_family="Inter, Arial"),
    )
    fig.update_xaxes(gridcolor=THEME["grid"], zerolinecolor="#64748B")
    fig.update_yaxes(gridcolor=THEME["grid"], zerolinecolor="#64748B")
    return fig


def empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font=dict(size=16, color=THEME["text"]))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return base_layout(fig)


def add_regression_line(fig: go.Figure, plot_df: pd.DataFrame, x: str, y: str) -> go.Figure:
    sub = plot_df[[x, y]].dropna()
    if len(sub) < 3:
        return fig
    xvals = sub[x].astype(float).to_numpy()
    yvals = sub[y].astype(float).to_numpy()
    if np.nanstd(xvals) == 0:
        return fig
    slope, intercept = np.polyfit(xvals, yvals, 1)
    xs = np.linspace(np.nanmin(xvals), np.nanmax(xvals), 100)
    ys = slope * xs + intercept
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            name="trend",
            line=dict(color="#F8FAFC", dash="dash", width=2),
            hoverinfo="skip",
        )
    )
    return fig


def normalize_marker_size(series: pd.Series, min_size: float = 8, max_size: float = 28) -> pd.Series:
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0 or s.max() == s.min():
        return pd.Series(min_size + 4, index=s.index)
    return min_size + (s - s.min()) * (max_size - min_size) / (s.max() - s.min())


def latest_year_for_country(var: str, country: str) -> str:
    sub = df[df["Country Name"] == country][["year", var]].dropna()
    if sub.empty:
        return "n/a"
    return str(int(sub["year"].iloc[-1]))


# -----------------------------------------------------------------------------
# 6. Figures
# -----------------------------------------------------------------------------
def fig_tourism_vs_sector(snap: pd.DataFrame, sector_var: str) -> go.Figure:
    plot_df = snap.dropna(subset=["tourism_receipts_pct_exports", sector_var]).copy()
    if plot_df.empty:
        return empty_figure("No data available for this selection.")

    fig = px.scatter(
        plot_df,
        x="tourism_receipts_pct_exports",
        y=sector_var,
        color="region",
        size="gdp_per_capita_current_usd",
        hover_name="Country Name",
        custom_data=["Country Name"],
        labels={
            "tourism_receipts_pct_exports": VAR_LABELS["tourism_receipts_pct_exports"],
            sector_var: VAR_LABELS.get(sector_var, sector_var),
            "region": "Region",
            "gdp_per_capita_current_usd": VAR_LABELS["gdp_per_capita_current_usd"],
        },
        color_discrete_map=REGION_COLORS,
        size_max=42,
    )
    fig.update_traces(
        marker=dict(line=dict(color="#F9FAFB", width=1.2), opacity=0.9),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Tourism receipts: %{x:.2f}%<br>"
            f"{VAR_LABELS.get(sector_var, sector_var)}: %{{y:.2f}}%<br>"
            "<extra></extra>"
        ),
    )
    fig = add_regression_line(fig, plot_df, "tourism_receipts_pct_exports", sector_var)
    return base_layout(fig, f"Tourism dependence vs {VAR_LABELS.get(sector_var, sector_var)}")


def fig_tourism_vs_outcome(snap: pd.DataFrame, outcome_var: str) -> go.Figure:
    plot_df = snap.dropna(subset=["tourism_receipts_pct_exports", outcome_var]).copy()
    if plot_df.empty:
        return empty_figure("No outcome data available for this selection.")

    fig = px.scatter(
        plot_df,
        x="tourism_receipts_pct_exports",
        y=outcome_var,
        color="region",
        size="services_avg",
        hover_name="Country Name",
        custom_data=["Country Name"],
        labels={
            "tourism_receipts_pct_exports": VAR_LABELS["tourism_receipts_pct_exports"],
            outcome_var: VAR_LABELS.get(outcome_var, outcome_var),
            "services_avg": VAR_LABELS["services_avg"],
            "region": "Region",
        },
        color_discrete_map=REGION_COLORS,
        size_max=42,
    )
    fig.update_traces(
        marker=dict(line=dict(color="#F9FAFB", width=1.2), opacity=0.9),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Tourism receipts: %{x:.2f}%<br>"
            f"{VAR_LABELS.get(outcome_var, outcome_var)}: %{{y:.2f}}<br>"
            "<extra></extra>"
        ),
    )
    fig = add_regression_line(fig, plot_df, "tourism_receipts_pct_exports", outcome_var)
    return base_layout(fig, f"Tourism dependence vs {VAR_LABELS.get(outcome_var, outcome_var)}")


def fig_country_trajectory_triangle(country: str) -> go.Figure:
    cdf = df[df["Country Name"] == country].copy().sort_values("year")
    cdf = cdf.dropna(subset=["services_avg", "industry_avg", "agriculture_avg"])
    if cdf.empty:
        return empty_figure("No employment-composition data available for this country.")

    marker_size = normalize_marker_size(cdf.get("tourism_receipts_pct_exports", pd.Series(index=cdf.index)), 8, 22)
    marker_size = marker_size.fillna(10)
    hover = []
    for _, r in cdf.iterrows():
        tourism_text = "n/a" if pd.isna(r.get("tourism_receipts_pct_exports", np.nan)) else f"{r['tourism_receipts_pct_exports']:.2f}% of exports"
        gdp_text = "n/a" if pd.isna(r.get("gdp_per_capita_current_usd", np.nan)) else f"${r['gdp_per_capita_current_usd']:,.0f}"
        hover.append(
            f"<b>{country}</b><br>"
            f"Year: {int(r['year'])}<br>"
            f"Services: {r['services_avg']:.1f}%<br>"
            f"Industry: {r['industry_avg']:.1f}%<br>"
            f"Agriculture: {r['agriculture_avg']:.1f}%<br>"
            f"Tourism receipts: {tourism_text}<br>"
            f"GDP per capita: {gdp_text}"
        )

    fig = go.Figure()
    fig.add_trace(
        go.Scatterternary(
            a=cdf["services_avg"],
            b=cdf["industry_avg"],
            c=cdf["agriculture_avg"],
            mode="lines+markers",
            text=hover,
            hovertemplate="%{text}<extra></extra>",
            line=dict(color="#E879F9", width=3),
            marker=dict(
                size=marker_size,
                color=cdf["year"],
                colorscale="Turbo",
                showscale=True,
                colorbar=dict(title="Year", thickness=12),
                line=dict(color="#F8FAFC", width=1.1),
                opacity=0.95,
            ),
            name=country,
        )
    )

    # Emphasize start and end points.
    first = cdf.iloc[0]
    last = cdf.iloc[-1]
    fig.add_trace(
        go.Scatterternary(
            a=[first["services_avg"], last["services_avg"]],
            b=[first["industry_avg"], last["industry_avg"]],
            c=[first["agriculture_avg"], last["agriculture_avg"]],
            mode="markers+text",
            text=["Start", "Latest"],
            textposition=["bottom center", "top center"],
            marker=dict(size=[13, 16], color=["#38BDF8", "#F97316"], line=dict(color="#F8FAFC", width=1.2)),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_layout(
        ternary=dict(
            bgcolor=THEME["card"],
            sum=100,
            aaxis=dict(title="Services", gridcolor="#475569", linecolor="#64748B", tickfont=dict(size=10)),
            baxis=dict(title="Industry", gridcolor="#475569", linecolor="#64748B", tickfont=dict(size=10)),
            caxis=dict(title="Agriculture", gridcolor="#475569", linecolor="#64748B", tickfont=dict(size=10)),
        )
    )
    return base_layout(fig, f"Structural pathway in the employment triangle: {country}")


def fig_composition_triangle(snap: pd.DataFrame) -> go.Figure:
    plot_df = snap.dropna(subset=["services_avg", "industry_avg", "agriculture_avg"]).copy()
    if plot_df.empty:
        return empty_figure("No sector-composition data available for selected countries.")

    marker_size = normalize_marker_size(plot_df.get("tourism_receipts_pct_exports", pd.Series(index=plot_df.index)), 9, 26)
    marker_size = marker_size.fillna(11)
    hover = []
    for _, r in plot_df.iterrows():
        tourism_text = "n/a" if pd.isna(r.get("tourism_receipts_pct_exports", np.nan)) else f"{r['tourism_receipts_pct_exports']:.2f}% ({source_year(r, 'tourism_receipts_pct_exports')})"
        hover.append(
            f"<b>{r['Country Name']}</b><br>"
            f"Region: {r['region']}<br>"
            f"Services: {r['services_avg']:.1f}%<br>"
            f"Industry: {r['industry_avg']:.1f}%<br>"
            f"Agriculture: {r['agriculture_avg']:.1f}%<br>"
            f"Tourism receipts: {tourism_text}"
        )

    fig = go.Figure()
    for region, rdf in plot_df.groupby("region"):
        idx = rdf.index
        fig.add_trace(
            go.Scatterternary(
                a=rdf["services_avg"],
                b=rdf["industry_avg"],
                c=rdf["agriculture_avg"],
                mode="markers+text",
                text=rdf["Country Name"],
                textposition="top center",
                hovertext=[hover[plot_df.index.get_loc(i)] for i in idx],
                hovertemplate="%{hovertext}<extra></extra>",
                marker=dict(
                    size=marker_size.loc[idx],
                    color=REGION_COLORS.get(region, REGION_COLORS["Other"]),
                    line=dict(color="#F8FAFC", width=1.1),
                    opacity=0.9,
                ),
                name=region,
            )
        )

    fig.update_layout(
        ternary=dict(
            bgcolor=THEME["card"],
            sum=100,
            aaxis=dict(title="Services", gridcolor="#475569", linecolor="#64748B", tickfont=dict(size=10)),
            baxis=dict(title="Industry", gridcolor="#475569", linecolor="#64748B", tickfont=dict(size=10)),
            caxis=dict(title="Agriculture", gridcolor="#475569", linecolor="#64748B", tickfont=dict(size=10)),
        )
    )
    return base_layout(fig, "Employment composition landscape")


def fig_shift_dotplot(df_selected: pd.DataFrame, countries: List[str]) -> go.Figure:
    rows = []
    for country in countries:
        cdf = df_selected[df_selected["Country Name"] == country].sort_values("year")
        cdf = cdf.dropna(subset=["services_avg", "industry_avg", "agriculture_avg"])
        if cdf.empty:
            continue
        first = cdf.iloc[0]
        last = cdf.iloc[-1]
        rows.extend([
            {"Country Name": country, "Sector": "Services", "Change": last["services_avg"] - first["services_avg"]},
            {"Country Name": country, "Sector": "Industry", "Change": last["industry_avg"] - first["industry_avg"]},
            {"Country Name": country, "Sector": "Agriculture", "Change": last["agriculture_avg"] - first["agriculture_avg"]},
        ])
    shift = pd.DataFrame(rows)
    if shift.empty:
        return empty_figure("No structural shift data available.")

    service_order = (
        shift[shift["Sector"] == "Services"].sort_values("Change", ascending=True)["Country Name"].tolist()
    )
    fig = go.Figure()
    symbols = {"Services": "circle", "Industry": "diamond", "Agriculture": "square"}

    for sector in ["Services", "Industry", "Agriculture"]:
        sdf = shift[shift["Sector"] == sector]
        fig.add_trace(
            go.Scatter(
                x=sdf["Change"],
                y=sdf["Country Name"],
                mode="markers",
                name=sector,
                marker=dict(
                    size=14,
                    symbol=symbols[sector],
                    color=SECTOR_COLORS[sector],
                    line=dict(color="#F8FAFC", width=1),
                ),
                hovertemplate="<b>%{y}</b><br>Sector: " + sector + "<br>Change: %{x:.1f} percentage points<extra></extra>",
            )
        )

    # subtle zero-origin lollipops for readability
    for _, r in shift.iterrows():
        fig.add_shape(
            type="line",
            x0=0,
            x1=r["Change"],
            y0=r["Country Name"],
            y1=r["Country Name"],
            line=dict(color="rgba(148,163,184,0.25)", width=1),
            layer="below",
        )

    fig.add_vline(x=0, line_width=1.4, line_dash="dash", line_color="#CBD5E1")
    fig.update_yaxes(categoryorder="array", categoryarray=service_order)
    fig.update_xaxes(title="Change in employment share, percentage points", zeroline=False)
    fig.update_yaxes(title="")
    return base_layout(fig, "Structural shift scoreboard: first year to latest year")


def fig_coverage_matrix(df_selected: pd.DataFrame, countries: List[str]) -> go.Figure:
    variables = [
        "tourism_receipts_pct_exports",
        "services_avg",
        "industry_avg",
        "agriculture_avg",
        "gdp_per_capita_current_usd",
        "urban_population_pct",
        "poverty_headcount_pct",
        "gini_index",
    ]
    rows = []
    for country in countries:
        cdf = df_selected[df_selected["Country Name"] == country]
        total = len(cdf)
        for var in variables:
            available = cdf[var].notna().sum() if var in cdf else 0
            pct = 100 * available / total if total else 0
            if pct == 0:
                category = 0
            elif pct < 40:
                category = 1
            elif pct < 80:
                category = 2
            else:
                category = 3
            rows.append({"Country": country, "Indicator": VAR_LABELS.get(var, var), "Coverage": pct, "Category": category, "Text": f"{pct:.0f}%"})
    cov = pd.DataFrame(rows)
    if cov.empty:
        return empty_figure("No coverage information available.")

    z = cov.pivot(index="Indicator", columns="Country", values="Category")
    text = cov.pivot(index="Indicator", columns="Country", values="Text")
    colorscale = [
        [0.00, "#7F1D1D"], [0.249, "#7F1D1D"],
        [0.25, "#B45309"], [0.499, "#B45309"],
        [0.50, "#CA8A04"], [0.749, "#CA8A04"],
        [0.75, "#16A34A"], [1.00, "#16A34A"],
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=z.values,
            x=z.columns,
            y=z.index,
            text=text.values,
            texttemplate="%{text}",
            textfont=dict(color="#F8FAFC", size=10),
            colorscale=colorscale,
            zmin=0,
            zmax=3,
            showscale=False,
            hovertemplate="<b>%{x}</b><br>%{y}<br>Coverage: %{text}<extra></extra>",
        )
    )
    fig.update_xaxes(tickangle=35)
    return base_layout(fig, "Data coverage matrix — explicit missingness")


# -----------------------------------------------------------------------------
# 7. Dash app
# -----------------------------------------------------------------------------
app = Dash(__name__)
app.title = "Tourism & Structural Transformation"

CARD_STYLE = {
    "background": "linear-gradient(180deg, #1F2937 0%, #111827 100%)",
    "border": "1px solid rgba(148,163,184,0.22)",
    "borderRadius": "18px",
    "padding": "14px",
    "boxShadow": "0 18px 38px rgba(0,0,0,0.24)",
}

CONTROL_STYLE = {
    "background": "#0F172A",
    "border": "1px solid rgba(148,163,184,0.25)",
    "borderRadius": "18px",
    "padding": "16px",
}

app.layout = html.Div(
    style={
        "fontFamily": "Inter, Segoe UI, Arial, sans-serif",
        "padding": "22px",
        "background": "radial-gradient(circle at top left, #1E3A8A 0%, #111827 28%, #030712 100%)",
        "minHeight": "100vh",
        "color": THEME["text"],
    },
    children=[
        html.Div(
            style={"display": "flex", "alignItems": "flex-end", "justifyContent": "space-between", "gap": "16px", "marginBottom": "18px"},
            children=[
                html.Div([
                    html.Div("DATA VISUALIZATION PROJECT", style={"letterSpacing": "0.18em", "fontSize": "11px", "color": THEME["accent2"], "fontWeight": 700}),
                    html.H1("Tourism & Structural Transformation", style={"margin": "5px 0 3px", "fontSize": "34px", "lineHeight": "1.05"}),
                    html.Div(
                        "Exploring whether tourism-led development is associated with a service-oriented employment shift, "
                        "and whether this transformation coincides with broader development outcomes.",
                        style={"fontSize": "15px", "maxWidth": "980px", "color": "#CBD5E1"},
                    ),
                ]),
                html.Div("Exploratory · linked views · country comparison", style={"fontSize": "12px", "color": "#CBD5E1", "border": "1px solid rgba(148,163,184,0.35)", "borderRadius": "999px", "padding": "8px 12px", "whiteSpace": "nowrap"}),
            ],
        ),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1.4fr 1fr", "gap": "16px", "marginBottom": "16px"},
            children=[
                html.Div(
                    style=CONTROL_STYLE,
                    children=[
                        html.Div("Controls", style={"fontWeight": 700, "marginBottom": "10px", "color": "#F8FAFC"}),
                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px"},
                            children=[
                                html.Div([
                                    html.Label("Selected countries", style={"fontSize": "12px", "color": "#CBD5E1"}),
                                    dcc.Dropdown(
                                        id="countries",
                                        options=[{"label": c, "value": c} for c in COUNTRIES],
                                        value=DEFAULT_COUNTRIES,
                                        multi=True,
                                        style={"color": "#111827"},
                                    ),
                                ]),
                                html.Div([
                                    html.Label("Focus country", style={"fontSize": "12px", "color": "#CBD5E1"}),
                                    dcc.Dropdown(
                                        id="focus_country",
                                        options=[{"label": c, "value": c} for c in COUNTRIES],
                                        value=DEFAULT_FOCUS_COUNTRY,
                                        clearable=False,
                                        style={"color": "#111827"},
                                    ),
                                    html.Small("Click a country in the first scatter to update this view.", style={"color": THEME["muted"]}),
                                ]),
                                html.Div([
                                    html.Label("Comparison year", style={"fontSize": "12px", "color": "#CBD5E1"}),
                                    dcc.Slider(
                                        id="year",
                                        min=min(YEARS),
                                        max=max(YEARS),
                                        step=1,
                                        value=DEFAULT_YEAR,
                                        marks={int(y): str(int(y)) for y in YEARS if int(y) in [min(YEARS), 2010, 2015, 2020, max(YEARS)]},
                                        tooltip={"placement": "bottom", "always_visible": False},
                                    ),
                                ]),
                                html.Div([
                                    html.Label("Data mode", style={"fontSize": "12px", "color": "#CBD5E1"}),
                                    dcc.RadioItems(
                                        id="mode",
                                        options=[
                                            {"label": "Latest available up to selected year", "value": "latest"},
                                            {"label": "Exact selected year only", "value": "exact"},
                                        ],
                                        value="latest",
                                        labelStyle={"display": "block", "margin": "3px 0", "fontSize": "13px"},
                                    ),
                                ]),
                            ],
                        ),
                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px", "marginTop": "12px"},
                            children=[
                                html.Div([
                                    html.Label("Sector variable", style={"fontSize": "12px", "color": "#CBD5E1"}),
                                    dcc.Dropdown(id="sector_var", options=SECTOR_OPTIONS, value="services_avg", clearable=False, style={"color": "#111827"}),
                                ]),
                                html.Div([
                                    html.Label("Outcome variable", style={"fontSize": "12px", "color": "#CBD5E1"}),
                                    dcc.Dropdown(id="outcome_var", options=OUTCOME_OPTIONS, value="poverty_headcount_pct", clearable=False, style={"color": "#111827"}),
                                ]),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="kpi_cards",
                    style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "12px"},
                ),
            ],
        ),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px"},
            children=[
                html.Div(dcc.Graph(id="tourism_sector_scatter", config={"displayModeBar": False}), style=CARD_STYLE),
                html.Div(dcc.Graph(id="tourism_outcome_scatter", config={"displayModeBar": False}), style=CARD_STYLE),
            ],
        ),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px", "marginTop": "16px"},
            children=[
                html.Div(dcc.Graph(id="trajectory_triangle", config={"displayModeBar": False}), style=CARD_STYLE),
                html.Div(dcc.Graph(id="composition_triangle", config={"displayModeBar": False}), style=CARD_STYLE),
            ],
        ),

        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "16px", "marginTop": "16px"},
            children=[
                html.Div(dcc.Graph(id="structural_shift", config={"displayModeBar": False}), style=CARD_STYLE),
                html.Div(dcc.Graph(id="coverage_matrix", config={"displayModeBar": False}), style=CARD_STYLE),
            ],
        ),

        html.Div(
            style={"fontSize": "12px", "color": "#94A3B8", "marginTop": "16px", "paddingBottom": "8px"},
            children=(
                "Methodological note: the dashboard supports exploratory analysis. It visualizes associations and structural patterns, "
                "not causal proof that tourism directly causes sectoral decline, poverty, or inequality."
            ),
        ),
    ],
)


# -----------------------------------------------------------------------------
# 8. Callbacks
# -----------------------------------------------------------------------------
@app.callback(
    Output("focus_country", "value"),
    Input("tourism_sector_scatter", "clickData"),
    State("focus_country", "value"),
    prevent_initial_call=True,
)
def update_focus_country_from_click(click_data, current_value):
    if click_data and click_data.get("points"):
        custom = click_data["points"][0].get("customdata")
        if custom:
            return custom[0]
    return current_value


@app.callback(
    Output("tourism_sector_scatter", "figure"),
    Output("tourism_outcome_scatter", "figure"),
    Output("trajectory_triangle", "figure"),
    Output("composition_triangle", "figure"),
    Output("structural_shift", "figure"),
    Output("coverage_matrix", "figure"),
    Output("kpi_cards", "children"),
    Input("countries", "value"),
    Input("year", "value"),
    Input("mode", "value"),
    Input("sector_var", "value"),
    Input("outcome_var", "value"),
    Input("focus_country", "value"),
)
def update_dashboard(countries, year, mode, sector_var, outcome_var, focus_country):
    if not countries:
        countries = COUNTRIES
    year = int(year)
    snap = get_snapshot(df, year, countries, mode)
    selected_df = df[df["Country Name"].isin(countries)].copy()

    # KPI cards
    available_tourism = snap["tourism_receipts_pct_exports"].notna().sum() if "tourism_receipts_pct_exports" in snap else 0
    avg_services = snap["services_avg"].mean() if "services_avg" in snap else np.nan
    avg_tourism = snap["tourism_receipts_pct_exports"].mean() if "tourism_receipts_pct_exports" in snap else np.nan
    focus_latest = latest_year_for_country("tourism_receipts_pct_exports", focus_country)

    kpis = [
        ("Countries", f"{len(countries)}", "active comparison set"),
        ("Tourism data", f"{available_tourism}/{len(countries)}", "countries with values"),
        ("Avg. services share", "n/a" if pd.isna(avg_services) else f"{avg_services:.1f}%", "selected snapshot"),
        ("Focus tourism year", focus_latest, focus_country),
    ]
    kpi_children = [
        html.Div(
            style={
                "background": "linear-gradient(135deg, rgba(249,115,22,0.16), rgba(34,211,238,0.10))",
                "border": "1px solid rgba(148,163,184,0.25)",
                "borderRadius": "18px",
                "padding": "14px",
                "minHeight": "84px",
            },
            children=[
                html.Div(label, style={"fontSize": "12px", "color": "#CBD5E1"}),
                html.Div(value, style={"fontSize": "26px", "fontWeight": 800, "margin": "3px 0", "color": "#F8FAFC"}),
                html.Div(sub, style={"fontSize": "11px", "color": "#94A3B8"}),
            ],
        )
        for label, value, sub in kpis
    ]

    return (
        fig_tourism_vs_sector(snap, sector_var),
        fig_tourism_vs_outcome(snap, outcome_var),
        fig_country_trajectory_triangle(focus_country),
        fig_composition_triangle(snap),
        fig_shift_dotplot(selected_df, countries),
        fig_coverage_matrix(selected_df, countries),
        kpi_children,
    )


if __name__ == "__main__":
    app.run(debug=True)
