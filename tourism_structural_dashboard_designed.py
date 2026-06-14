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
from plotly.subplots import make_subplots
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

# Okabe-Ito hues, brightened for dark backgrounds
REGION_COLORS = {
    "Europe": "#4BA3D4",
    "Asia": "#F0A500",
    "Middle East": "#2EC9A0",
    "Africa": "#E0714A",
    "Latin America & Caribbean": "#D98DB5",
    "North America": "#70C4EC",
    "Other": "#AAAAAA",
}

# Bright, non-neon sector colors readable on dark backgrounds
SECTOR_COLORS = {
    "Services": "#4ADE80",
    "Industry": "#FB923C",
    "Agriculture": "#67E8F9",
    "Tourism": "#C084FC",
}

# Clean dark academic theme
THEME = {
    "paper": "#0F172A",
    "card": "#1E293B",
    "card2": "#172033",
    "grid": "#334155",
    "text": "#E2E8F0",
    "muted": "#94A3B8",
    "accent": "#60A5FA",
    "accent2": "#38BDF8",
    "border": "rgba(148,163,184,0.18)",
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

SMALL_MULTIPLE_VARS = [
    "services_avg",
    "industry_avg",
    "agriculture_avg",
    "gdp_per_capita_current_usd",
    "urban_population_pct",
    "poverty_headcount_pct",
    "gini_index",
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
        font=dict(color=THEME["text"], family="Inter, Segoe UI, Arial, sans-serif", size=12),
        title=dict(
            text=title,
            font=dict(size=13, color=THEME["text"]),
            x=0.0,
            xanchor="left",
            pad=dict(l=4),
        ) if title else None,
        margin=dict(l=48, r=20, t=44 if title else 16, b=44),
        legend=dict(
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor=THEME["border"],
            borderwidth=1,
            font=dict(size=11, color=THEME["text"]),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor=THEME["card"],
            bordercolor=THEME["border"],
            font_size=12,
            font_family="Inter, Arial",
            font_color=THEME["text"],
        ),
    )
    fig.update_xaxes(
        gridcolor=THEME["grid"],
        zerolinecolor="#475569",
        zerolinewidth=1,
        tickfont=dict(size=11, color=THEME["muted"]),
        title_font=dict(size=12, color=THEME["text"]),
    )
    fig.update_yaxes(
        gridcolor=THEME["grid"],
        zerolinecolor="#475569",
        zerolinewidth=1,
        tickfont=dict(size=11, color=THEME["muted"]),
        title_font=dict(size=12, color=THEME["text"]),
    )
    return fig


def empty_figure(message: str) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=13, color=THEME["muted"]),
    )
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
            line=dict(color="#64748B", dash="dash", width=1.5),
            hoverinfo="skip",
        )
    )
    return fig


def latest_year_for_country(var: str, country: str) -> str:
    sub = df[df["Country Name"] == country][["year", var]].dropna()
    if sub.empty:
        return "n/a"
    return str(int(sub["year"].iloc[-1]))


# ── Layout component helpers ───────────────────────────────────────────────────

CARD_STYLE = {
    "background": THEME["card"],
    "border": f"1px solid {THEME['border']}",
    "borderRadius": "10px",
    "padding": "16px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.25)",
}

CONTROL_CARD_STYLE = {
    "background": THEME["card2"],
    "border": f"1px solid {THEME['border']}",
    "borderRadius": "10px",
    "padding": "16px",
}

# Hint box style (light blue text on subtle dark-blue tint)
_HINT_STYLE = {
    "fontSize": "11px",
    "color": "#93C5FD",
    "background": "rgba(96,165,250,0.10)",
    "borderLeft": "3px solid rgba(96,165,250,0.45)",
    "borderRadius": "0 4px 4px 0",
    "padding": "4px 8px",
    "marginBottom": "8px",
}


def section_header(number: str, title: str, description: str) -> html.Div:
    return html.Div(
        style={"marginBottom": "10px", "marginTop": "4px"},
        children=[
            html.Div(
                f"Section {number}",
                style={
                    "fontSize": "10px",
                    "fontWeight": 700,
                    "letterSpacing": "0.15em",
                    "textTransform": "uppercase",
                    "color": THEME["accent"],
                    "marginBottom": "1px",
                },
            ),
            html.H2(
                title,
                style={"margin": "0 0 2px", "fontSize": "15px", "fontWeight": 700, "color": THEME["text"]},
            ),
            html.P(
                description,
                style={"margin": "0", "fontSize": "12px", "color": THEME["muted"]},
            ),
        ],
    )


def chart_card(
    graph_id: str,
    title: str,
    subtitle: str,
    hint: str | None = None,
    extra_footer: html.Div | None = None,
    graph_config: dict | None = None,
) -> html.Div:
    """Wrap a dcc.Graph in a styled card with title, subtitle, and optional hint."""
    config = graph_config if graph_config is not None else {"displayModeBar": False}
    children: list = [
        html.Div(
            title,
            style={"fontSize": "13px", "fontWeight": 700, "color": THEME["text"], "marginBottom": "1px"},
        ),
        html.Div(
            subtitle,
            style={"fontSize": "11px", "color": THEME["muted"], "fontStyle": "italic", "marginBottom": "6px"},
        ),
    ]
    if hint:
        children.append(html.Div(hint, style=_HINT_STYLE))
    children.append(dcc.Graph(id=graph_id, config=config))
    if extra_footer:
        children.append(extra_footer)
    return html.Div(children=children, style=CARD_STYLE)


def control_group(label: str, hint: str | None, *controls) -> html.Div:
    children: list = [
        html.Div(
            label,
            style={"fontSize": "12px", "fontWeight": 600, "color": THEME["text"], "marginBottom": "5px"},
        )
    ]
    children.extend(controls)
    if hint:
        children.append(
            html.Small(
                hint,
                style={"fontSize": "11px", "color": THEME["muted"], "marginTop": "3px", "display": "block"},
            )
        )
    return html.Div(children=children, style={"marginBottom": "2px"})


def kpi_card(label: str, value: str, sub: str) -> html.Div:
    return html.Div(
        style={
            "background": THEME["card"],
            "border": f"1px solid {THEME['border']}",
            "borderRadius": "8px",
            "padding": "12px 14px",
            "minHeight": "76px",
        },
        children=[
            html.Div(
                label,
                style={
                    "fontSize": "10px",
                    "color": THEME["muted"],
                    "fontWeight": 700,
                    "textTransform": "uppercase",
                    "letterSpacing": "0.06em",
                    "marginBottom": "3px",
                },
            ),
            html.Div(
                value,
                style={"fontSize": "22px", "fontWeight": 800, "color": THEME["text"], "lineHeight": "1.2"},
            ),
            html.Div(sub, style={"fontSize": "11px", "color": THEME["muted"], "marginTop": "2px"}),
        ],
    )


# -----------------------------------------------------------------------------
# 6. Figures
# -----------------------------------------------------------------------------

def _ternary_axes() -> dict:
    return dict(
        gridcolor=THEME["grid"],
        linecolor=THEME["border"],
        tick0=0,
        dtick=20,
        ticksuffix="%",
        tickfont=dict(size=10, color=THEME["muted"]),
        title_font=dict(size=12, color=THEME["text"]),
    )


def _ternary_layout(fig: go.Figure) -> go.Figure:
    ax = _ternary_axes()
    fig.update_layout(
        ternary=dict(
            bgcolor=THEME["card"],
            sum=100,
            aaxis=dict(title="Services (%)", **ax),
            baxis=dict(title="Industry (%)", **ax),
            caxis=dict(title="Agriculture (%)", **ax),
        ),
        paper_bgcolor=THEME["card"],
        font=dict(color=THEME["text"], family="Inter, Segoe UI, Arial, sans-serif"),
        margin=dict(l=30, r=60, t=16, b=16),
        hoverlabel=dict(
            bgcolor=THEME["card"],
            bordercolor=THEME["border"],
            font_size=12,
            font_family="Inter, Arial",
            font_color=THEME["text"],
        ),
        legend=dict(
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor=THEME["border"],
            borderwidth=1,
            font=dict(size=11, color=THEME["text"]),
        ),
    )
    return fig


def _highlight_focus(
    fig: go.Figure,
    plot_df: pd.DataFrame,
    x: str,
    y: str,
    focus_country: str,
) -> go.Figure:
    """Overlay a red ring + label on the focus country point in a scatter."""
    fc = plot_df[plot_df["Country Name"] == focus_country]
    if fc.empty:
        return fig
    row = fc.iloc[0]
    if pd.isna(row.get(x, np.nan)) or pd.isna(row.get(y, np.nan)):
        return fig
    fig.add_trace(
        go.Scatter(
            x=[row[x]],
            y=[row[y]],
            mode="markers+text",
            name=f"Focus: {focus_country}",
            text=[focus_country],
            textposition="top center",
            textfont=dict(size=11, color="#FCA5A5"),
            marker=dict(
                size=22,
                color="rgba(239,68,68,0.12)",
                line=dict(color="#EF4444", width=2.5),
                symbol="circle",
            ),
            hovertemplate=f"<b>{focus_country}</b> (focus country)<extra></extra>",
            showlegend=True,
        )
    )
    return fig


def fig_tourism_vs_sector(snap: pd.DataFrame, sector_var: str, focus_country: str) -> go.Figure:
    plot_df = snap.dropna(subset=["tourism_receipts_pct_exports", sector_var]).copy()
    if plot_df.empty:
        return empty_figure("No data available for this selection.")

    fig = px.scatter(
        plot_df,
        x="tourism_receipts_pct_exports",
        y=sector_var,
        color="region",
        hover_name="Country Name",
        custom_data=["Country Name", "gdp_per_capita_current_usd"],
        labels={
            "tourism_receipts_pct_exports": VAR_LABELS["tourism_receipts_pct_exports"],
            sector_var: VAR_LABELS.get(sector_var, sector_var),
            "region": "Region",
            "gdp_per_capita_current_usd": VAR_LABELS["gdp_per_capita_current_usd"],
        },
        color_discrete_map=REGION_COLORS,
    )
    fig.update_traces(
        marker=dict(size=10, line=dict(color="rgba(255,255,255,0.35)", width=1), opacity=0.88),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Tourism receipts: %{x:.2f}%<br>"
            f"{VAR_LABELS.get(sector_var, sector_var)}: %{{y:.2f}}%<br>"
            "GDP per capita: $%{customdata[1]:,.0f}<br>"
            "<extra></extra>"
        ),
        selector=dict(mode="markers"),
    )
    fig = add_regression_line(fig, plot_df, "tourism_receipts_pct_exports", sector_var)
    fig = _highlight_focus(fig, plot_df, "tourism_receipts_pct_exports", sector_var, focus_country)
    return base_layout(fig)


def fig_tourism_vs_outcome(snap: pd.DataFrame, outcome_var: str, focus_country: str) -> go.Figure:
    plot_df = snap.dropna(subset=["tourism_receipts_pct_exports", outcome_var]).copy()
    if plot_df.empty:
        return empty_figure("No outcome data available for this selection.")

    fig = px.scatter(
        plot_df,
        x="tourism_receipts_pct_exports",
        y=outcome_var,
        color="region",
        hover_name="Country Name",
        custom_data=["Country Name", "services_avg"],
        labels={
            "tourism_receipts_pct_exports": VAR_LABELS["tourism_receipts_pct_exports"],
            outcome_var: VAR_LABELS.get(outcome_var, outcome_var),
            "services_avg": VAR_LABELS["services_avg"],
            "region": "Region",
        },
        color_discrete_map=REGION_COLORS,
    )
    fig.update_traces(
        marker=dict(size=10, line=dict(color="rgba(255,255,255,0.35)", width=1), opacity=0.88),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Tourism receipts: %{x:.2f}%<br>"
            f"{VAR_LABELS.get(outcome_var, outcome_var)}: %{{y:.2f}}<br>"
            "Services employment: %{customdata[1]:.2f}%<br>"
            "<extra></extra>"
        ),
        selector=dict(mode="markers"),
    )
    fig = add_regression_line(fig, plot_df, "tourism_receipts_pct_exports", outcome_var)
    fig = _highlight_focus(fig, plot_df, "tourism_receipts_pct_exports", outcome_var, focus_country)
    return base_layout(fig)


def fig_small_multiple_associations(snap: pd.DataFrame) -> go.Figure:
    rows = []
    for var in SMALL_MULTIPLE_VARS:
        if var not in snap.columns:
            continue
        sub = snap.dropna(subset=["tourism_receipts_pct_exports", var])
        for _, r in sub.iterrows():
            rows.append(
                {
                    "Country Name": r["Country Name"],
                    "region": r["region"],
                    "Variable": VAR_LABELS.get(var, var),
                    "Value": r[var],
                    "Tourism": r["tourism_receipts_pct_exports"],
                }
            )

    plot_df = pd.DataFrame(rows)
    if plot_df.empty:
        return empty_figure("No data available for the small-multiple overview.")

    variables = plot_df["Variable"].drop_duplicates().tolist()
    cols = 3
    rows_count = int(np.ceil(len(variables) / cols))
    fig = make_subplots(
        rows=rows_count,
        cols=cols,
        subplot_titles=variables,
        horizontal_spacing=0.07,
        vertical_spacing=0.14,
    )

    for index, variable in enumerate(variables):
        row = index // cols + 1
        col = index % cols + 1
        panel = plot_df[plot_df["Variable"] == variable]
        for region, rdf in panel.groupby("region"):
            fig.add_trace(
                go.Scatter(
                    x=rdf["Tourism"],
                    y=rdf["Value"],
                    mode="markers",
                    name=region,
                    legendgroup=region,
                    showlegend=index == 0,
                    marker=dict(
                        size=7,
                        color=REGION_COLORS.get(region, REGION_COLORS["Other"]),
                        line=dict(color="rgba(255,255,255,0.25)", width=0.8),
                        opacity=0.86,
                    ),
                    text=rdf["Country Name"],
                    customdata=np.stack([rdf["Variable"]], axis=-1),
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "%{customdata[0]}: %{y:.2f}<br>"
                        "Tourism receipts: %{x:.2f}%<extra></extra>"
                    ),
                ),
                row=row,
                col=col,
            )
        fig.update_xaxes(title_text="Tourism (%)", row=row, col=col)
        fig.update_yaxes(title_text="", row=row, col=col)

    fig = base_layout(fig)
    fig.update_layout(
        height=590,
        margin=dict(l=48, r=20, t=84, b=44),
        legend=dict(
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor=THEME["border"],
            borderwidth=1,
            font=dict(size=11, color=THEME["text"]),
            orientation="h",
            yanchor="bottom",
            y=1.12,
            xanchor="left",
            x=0,
        ),
    )
    fig.update_annotations(font=dict(size=11, color=THEME["text"]))
    return fig


def fig_country_trajectory_triangle(country: str) -> go.Figure:
    cdf = df[df["Country Name"] == country].copy().sort_values("year")
    cdf = cdf.dropna(subset=["services_avg", "industry_avg", "agriculture_avg"])
    if cdf.empty:
        return empty_figure("No employment-composition data available for this country.")

    hover = []
    for _, r in cdf.iterrows():
        tourism_text = (
            "n/a"
            if pd.isna(r.get("tourism_receipts_pct_exports", np.nan))
            else f"{r['tourism_receipts_pct_exports']:.2f}% of exports"
        )
        gdp_text = (
            "n/a"
            if pd.isna(r.get("gdp_per_capita_current_usd", np.nan))
            else f"${r['gdp_per_capita_current_usd']:,.0f}"
        )
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
            line=dict(color="#475569", width=1.8),
            marker=dict(
                size=10,
                color=cdf["year"],
                # Viridis: perceptually ordered sequential — dark purple = earliest, bright yellow = latest
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(
                    title=dict(text="Year", font=dict(size=11, color=THEME["text"])),
                    thickness=12,
                    tickfont=dict(size=10, color=THEME["text"]),
                    outlinewidth=0,
                    bgcolor="rgba(0,0,0,0)",
                ),
                line=dict(color="rgba(255,255,255,0.4)", width=1),
                opacity=0.92,
            ),
            name=country,
        )
    )

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
            textfont=dict(size=10, color=THEME["text"]),
            marker=dict(
                size=[12, 15],
                color=["#60A5FA", "#FBBF24"],
                line=dict(color="rgba(255,255,255,0.6)", width=1.5),
            ),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    return _ternary_layout(fig)


def fig_composition_triangle(snap: pd.DataFrame, focus_country: str) -> go.Figure:
    plot_df = snap.dropna(subset=["services_avg", "industry_avg", "agriculture_avg"]).copy()
    if plot_df.empty:
        return empty_figure("No sector-composition data available for selected countries.")

    hover = []
    for _, r in plot_df.iterrows():
        tourism_text = (
            "n/a"
            if pd.isna(r.get("tourism_receipts_pct_exports", np.nan))
            else f"{r['tourism_receipts_pct_exports']:.2f}% ({source_year(r, 'tourism_receipts_pct_exports')})"
        )
        hover.append(
            f"<b>{r['Country Name']}</b><br>"
            f"Region: {r['region']}<br>"
            f"Services: {r['services_avg']:.1f}%<br>"
            f"Industry: {r['industry_avg']:.1f}%<br>"
            f"Agriculture: {r['agriculture_avg']:.1f}%<br>"
            f"Tourism receipts: {tourism_text}"
        )

    fig = go.Figure()

    # Draw non-focus countries grouped by region
    for region, rdf in plot_df.groupby("region"):
        non_focus = rdf[rdf["Country Name"] != focus_country]
        if non_focus.empty:
            continue
        idx = non_focus.index
        fig.add_trace(
            go.Scatterternary(
                a=non_focus["services_avg"],
                b=non_focus["industry_avg"],
                c=non_focus["agriculture_avg"],
                mode="markers+text",
                text=non_focus["Country Name"],
                textposition="top center",
                textfont=dict(size=9, color=THEME["muted"]),
                hovertext=[hover[plot_df.index.get_loc(i)] for i in idx],
                hovertemplate="%{hovertext}<extra></extra>",
                marker=dict(
                    size=11,
                    color=REGION_COLORS.get(region, REGION_COLORS["Other"]),
                    line=dict(color="rgba(255,255,255,0.3)", width=1),
                    opacity=0.88,
                ),
                name=region,
            )
        )

    # Draw focus country as a highlighted separate trace
    fc_row = plot_df[plot_df["Country Name"] == focus_country]
    if not fc_row.empty:
        r = fc_row.iloc[0]
        fc_tourism = (
            "n/a"
            if pd.isna(r.get("tourism_receipts_pct_exports", np.nan))
            else f"{r['tourism_receipts_pct_exports']:.2f}% ({source_year(r, 'tourism_receipts_pct_exports')})"
        )
        fc_hover = (
            f"<b>{focus_country}</b> (focus)<br>"
            f"Region: {r['region']}<br>"
            f"Services: {r['services_avg']:.1f}%<br>"
            f"Industry: {r['industry_avg']:.1f}%<br>"
            f"Agriculture: {r['agriculture_avg']:.1f}%<br>"
            f"Tourism receipts: {fc_tourism}"
        )
        fig.add_trace(
            go.Scatterternary(
                a=[r["services_avg"]],
                b=[r["industry_avg"]],
                c=[r["agriculture_avg"]],
                mode="markers+text",
                text=[focus_country],
                textposition="top center",
                textfont=dict(size=11, color="#FCA5A5"),
                hovertext=[fc_hover],
                hovertemplate="%{hovertext}<extra></extra>",
                marker=dict(
                    size=17,
                    color=REGION_COLORS.get(r["region"], REGION_COLORS["Other"]),
                    line=dict(color="#EF4444", width=2.5),
                    opacity=1.0,
                ),
                name=f"Focus: {focus_country}",
            )
        )

    return _ternary_layout(fig)


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
                    size=12,
                    symbol=symbols[sector],
                    color=SECTOR_COLORS[sector],
                    line=dict(color="rgba(255,255,255,0.3)", width=1),
                    opacity=0.92,
                ),
                hovertemplate=(
                    "<b>%{y}</b><br>Sector: " + sector + "<br>Change: %{x:.1f} pp<extra></extra>"
                ),
            )
        )

    for _, r in shift.iterrows():
        fig.add_shape(
            type="line",
            x0=0,
            x1=r["Change"],
            y0=r["Country Name"],
            y1=r["Country Name"],
            line=dict(color=THEME["grid"], width=1),
            layer="below",
        )

    fig.add_vline(x=0, line_width=1.2, line_dash="dash", line_color="#475569")
    fig.update_yaxes(categoryorder="array", categoryarray=service_order, title="")
    fig.update_xaxes(title="Change in employment share (percentage points)", zeroline=False)
    return base_layout(fig)


def fig_coverage_matrix(
    df_selected: pd.DataFrame,
    countries: List[str],
    sector_var: str | None = None,
    outcome_var: str | None = None,
) -> go.Figure:
    variables = [
        "tourism_receipts_pct_exports",
        sector_var,
        outcome_var,
        "services_avg",
        "industry_avg",
        "agriculture_avg",
        "gdp_per_capita_current_usd",
        "urban_population_pct",
        "poverty_headcount_pct",
        "gini_index",
    ]
    variables = [v for i, v in enumerate(variables) if v and v not in variables[:i]]
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
            rows.append({
                "Country": country,
                "Indicator": VAR_LABELS.get(var, var),
                "Coverage": pct,
                "Category": category,
                "Text": f"{pct:.0f}%",
            })
    cov = pd.DataFrame(rows)
    if cov.empty:
        return empty_figure("No coverage information available.")

    z = cov.pivot(index="Indicator", columns="Country", values="Category")
    text = cov.pivot(index="Indicator", columns="Country", values="Text")

    # Pastel sequential: red → orange → yellow → green. Text is hardcoded dark for readability on pastels.
    colorscale = [
        [0.00, "#FECACA"], [0.249, "#FECACA"],
        [0.25, "#FED7AA"], [0.499, "#FED7AA"],
        [0.50, "#FEF08A"], [0.749, "#FEF08A"],
        [0.75, "#BBF7D0"], [1.00, "#BBF7D0"],
    ]
    fig = go.Figure(
        data=go.Heatmap(
            z=z.values,
            x=z.columns,
            y=z.index,
            text=text.values,
            texttemplate="%{text}",
            textfont=dict(color="#1E293B", size=10),  # dark text on pastel cells
            colorscale=colorscale,
            zmin=0,
            zmax=3,
            showscale=False,
            hovertemplate="<b>%{x}</b><br>%{y}<br>Coverage: %{text}<extra></extra>",
        )
    )
    fig.update_xaxes(tickangle=35, tickfont=dict(size=10))
    fig.update_yaxes(tickfont=dict(size=10))
    return base_layout(fig)


# -----------------------------------------------------------------------------
# 7. Dash app and layout
# -----------------------------------------------------------------------------
app = Dash(__name__)
app.title = "Tourism & Structural Transformation"

_SPACER = html.Div(style={"height": "14px"})

# Config for ternary charts: show mode bar so zoom in/out buttons are accessible
_TERNARY_CONFIG = {"displayModeBar": True, "modeBarButtonsToRemove": ["toImage"]}

app.layout = html.Div(
    style={
        "fontFamily": "Inter, Segoe UI, Arial, sans-serif",
        "background": THEME["paper"],
        "minHeight": "100vh",
        "color": THEME["text"],
        "padding": "20px",
        "boxSizing": "border-box",
    },
    children=[

        # ── Header ──────────────────────────────────────────────────────────
        html.Div(
            style={
                "background": THEME["card"],
                "border": f"1px solid {THEME['border']}",
                "borderRadius": "10px",
                "padding": "18px 22px",
                "marginBottom": "14px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.25)",
            },
            children=[
                html.Div(
                    style={
                        "display": "flex",
                        "alignItems": "flex-start",
                        "justifyContent": "space-between",
                        "gap": "16px",
                    },
                    children=[
                        html.Div([
                            html.Div(
                                "JM0250 DATA VISUALIZATION · EXPLORATORY ANALYSIS",
                                style={
                                    "fontSize": "10px",
                                    "letterSpacing": "0.15em",
                                    "color": THEME["muted"],
                                    "fontWeight": 700,
                                    "marginBottom": "4px",
                                },
                            ),
                            html.H1(
                                "Tourism & Structural Transformation Dashboard",
                                style={
                                    "margin": "0 0 6px",
                                    "fontSize": "22px",
                                    "fontWeight": 800,
                                    "color": THEME["text"],
                                    "lineHeight": "1.2",
                                },
                            ),
                            html.P(
                                "Exploring how tourism dependence associates with employment-sector composition "
                                "and broader development outcomes across a set of countries.",
                                style={"margin": "0", "fontSize": "13px", "color": THEME["muted"], "maxWidth": "680px"},
                            ),
                        ]),
                        html.Div(
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "alignItems": "flex-end",
                                "gap": "6px",
                                "flexShrink": 0,
                            },
                            children=[
                                html.Div(
                                    "Association, not causation",
                                    style={
                                        "fontSize": "11px",
                                        "color": "#FCD34D",
                                        "background": "rgba(245,158,11,0.15)",
                                        "border": "1px solid rgba(245,158,11,0.35)",
                                        "borderRadius": "999px",
                                        "padding": "5px 12px",
                                        "fontWeight": 600,
                                        "whiteSpace": "nowrap",
                                    },
                                ),
                                html.Div(
                                    "Coordinated views · Click-to-focus · WDI data",
                                    style={"fontSize": "11px", "color": THEME["muted"]},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # ── Controls + KPIs ──────────────────────────────────────────────────
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "2fr 1fr",
                "gap": "14px",
                "marginBottom": "14px",
            },
            children=[
                # Controls panel
                html.Div(
                    style=CONTROL_CARD_STYLE,
                    children=[
                        html.Div(
                            "Dashboard controls",
                            style={"fontSize": "12px", "fontWeight": 700, "color": THEME["text"], "marginBottom": "12px"},
                        ),
                        html.Div(
                            className="controls-inner-grid",
                            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px"},
                            children=[
                                # Left column: Scope + Encodings
                                html.Div([
                                    control_group(
                                        "Scope — selected countries",
                                        None,
                                        dcc.Dropdown(
                                            id="countries",
                                            options=[{"label": c, "value": c} for c in COUNTRIES],
                                            value=DEFAULT_COUNTRIES,
                                            multi=True,
                                        ),
                                    ),
                                    _SPACER,
                                    control_group(
                                        "Encoding — sector variable (left scatter, y-axis)",
                                        None,
                                        dcc.Dropdown(
                                            id="sector_var",
                                            options=SECTOR_OPTIONS,
                                            value="services_avg",
                                            clearable=False,
                                        ),
                                    ),
                                    _SPACER,
                                    control_group(
                                        "Encoding — outcome variable (right scatter, y-axis)",
                                        None,
                                        dcc.Dropdown(
                                            id="outcome_var",
                                            options=OUTCOME_OPTIONS,
                                            value="poverty_headcount_pct",
                                            clearable=False,
                                        ),
                                    ),
                                ]),
                                # Right column: Time + Mode + Focus
                                html.Div([
                                    control_group(
                                        "Time — comparison year",
                                        None,
                                        dcc.Slider(
                                            id="year",
                                            min=min(YEARS),
                                            max=max(YEARS),
                                            step=1,
                                            value=DEFAULT_YEAR,
                                            marks={
                                                int(y): str(int(y))
                                                for y in YEARS
                                                if int(y) in [min(YEARS), 2010, 2015, 2020, max(YEARS)]
                                            },
                                            tooltip={"placement": "bottom", "always_visible": False},
                                        ),
                                    ),
                                    _SPACER,
                                    control_group(
                                        "Data mode",
                                        "'Latest' uses the most recent value up to the selected year; "
                                        "'Exact' shows data only from that specific year.",
                                        dcc.RadioItems(
                                            id="mode",
                                            options=[
                                                {"label": "Latest available up to selected year", "value": "latest"},
                                                {"label": "Exact selected year only", "value": "exact"},
                                            ],
                                            value="latest",
                                            labelStyle={"display": "block", "margin": "3px 0", "fontSize": "12px"},
                                        ),
                                    ),
                                    _SPACER,
                                    control_group(
                                        "Focus — focus country",
                                        "Or click a country point in Section 1 to set focus interactively.",
                                        dcc.Dropdown(
                                            id="focus_country",
                                            options=[{"label": c, "value": c} for c in COUNTRIES],
                                            value=DEFAULT_FOCUS_COUNTRY,
                                            clearable=False,
                                        ),
                                    ),
                                ]),
                            ],
                        ),
                    ],
                ),

                # KPI cards
                html.Div(
                    id="kpi_cards",
                    className="kpi-grid",
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gap": "10px",
                        "alignContent": "start",
                    },
                ),
            ],
        ),

        # ── Section 1: Explore Associations ──────────────────────────────────
        section_header(
            "1",
            "Explore Associations",
            "How does tourism dependence relate to sector employment and development outcomes? "
            "Click a country point to set it as the focus country.",
        ),
        html.Div(
            className="chart-grid-2",
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px", "marginBottom": "14px"},
            children=[
                chart_card(
                    "tourism_sector_scatter",
                    "Tourism dependence vs. sector employment",
                    "Task: discover association, identify outliers. "
                    "Point position = quantitative values; color = region.",
                    hint="Click a country point to set it as the focus country (highlighted with a red ring in all views).",
                ),
                chart_card(
                    "tourism_outcome_scatter",
                    "Tourism dependence vs. development outcome",
                    "Task: discover association between tourism intensity and the selected outcome. "
                    "Point position = quantitative values; color = region.",
                    hint="Focus country (set in left chart) is also highlighted here with a red ring.",
                ),
            ],
        ),

        # ── Section 2: Compare Structural Composition ─────────────────────────
        html.Div(
            style={"marginBottom": "14px"},
            children=[
                chart_card(
                    "small_multiple_associations",
                    "Small-multiple association overview",
                    "Task: compare tourism relationships across several variables without relying on memory. "
                    "Each panel uses constant-size points and region hue.",
                    hint="Panels inherit the selected countries, year, and data mode from the controls above.",
                ),
            ],
        ),
        section_header(
            "2",
            "Compare Structural Composition",
            "Where do countries sit in the employment triangle, "
            "and how much has the composition shifted over time?",
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px", "marginBottom": "14px"},
            children=[
                chart_card(
                    "composition_triangle",
                    "Employment composition landscape (snapshot)",
                    "Task: summarize and compare sector composition. "
                    "Region hue groups countries; the focus country is highlighted in red.",
                    hint="Each vertex = 100% share in that sector. "
                    "Use the mode bar (top-right) to zoom in or reset view.",
                    graph_config=_TERNARY_CONFIG,
                ),
                chart_card(
                    "structural_shift",
                    "Structural shift scoreboard",
                    "Task: compare direction and magnitude of employment change "
                    "from each country's first to latest available year.",
                    hint="Positive = sector share grew. Countries sorted by services change (ascending).",
                ),
            ],
        ),

        # ── Section 3: Follow One Country ────────────────────────────────────
        section_header(
            "3",
            "Follow One Country",
            "Trace the focus country's employment-composition pathway over all available years.",
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "2fr 1fr", "gap": "14px", "marginBottom": "14px"},
            children=[
                chart_card(
                    "trajectory_triangle",
                    "Focus-country employment trajectory",
                    "Task: explore temporal change in sector composition. "
                    "Color = year (Viridis: dark purple = earliest, bright yellow = latest). "
                    "Tourism values are available in hover.",
                    hint="Use the mode bar (top-right) to zoom in or reset view. "
                    "Switch country via the Focus control above, or click a point in Section 1.",
                    graph_config=_TERNARY_CONFIG,
                ),
                html.Div(
                    style={
                        **CARD_STYLE,
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "gap": "12px",
                    },
                    children=[
                        html.Div(
                            "Active focus country",
                            style={
                                "fontSize": "10px",
                                "fontWeight": 700,
                                "color": THEME["muted"],
                                "textTransform": "uppercase",
                                "letterSpacing": "0.1em",
                            },
                        ),
                        html.Div(
                            id="focus_country_badge",
                            style={"fontSize": "22px", "fontWeight": 800, "color": THEME["accent"]},
                            children=DEFAULT_FOCUS_COUNTRY,
                        ),
                        html.Hr(
                            style={
                                "border": "none",
                                "borderTop": f"1px solid {THEME['border']}",
                                "margin": "0",
                            }
                        ),
                        html.Div(
                            style={"fontSize": "12px", "color": THEME["muted"], "lineHeight": "1.65"},
                            children=[
                                html.Div(
                                    "The trajectory chart shows every year with complete "
                                    "employment-composition data for this country."
                                ),
                                html.Div(
                                    "Tourism receipts are shown in hover so size does not imply another quantitative ranking.",
                                    style={"marginTop": "6px"},
                                ),
                                html.Div(
                                    "Start and Latest year are labelled in the chart.",
                                    style={"marginTop": "6px"},
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),

        # ── Section 4: Check Data Reliability ────────────────────────────────
        section_header(
            "4",
            "Check Data Reliability",
            "Inspect data coverage before trusting a comparison. "
            "Gaps are explicit — not imputed in this view.",
        ),
        html.Div(
            style={"marginBottom": "14px"},
            children=[
                chart_card(
                    "coverage_matrix",
                    "Data coverage matrix",
                    "Task: inspect missingness across indicators and countries. "
                    "Cell = % of years with non-missing data.",
                    extra_footer=html.Div(
                        style={
                            "display": "flex",
                            "gap": "14px",
                            "marginTop": "8px",
                            "fontSize": "11px",
                            "color": THEME["muted"],
                            "flexWrap": "wrap",
                        },
                        children=[
                            html.Span([html.Span("■ ", style={"color": "#EF4444", "fontWeight": 700}), "0% — no data"]),
                            html.Span([html.Span("■ ", style={"color": "#F97316", "fontWeight": 700}), "< 40% — sparse"]),
                            html.Span([html.Span("■ ", style={"color": "#EAB308", "fontWeight": 700}), "40–80% — partial"]),
                            html.Span([html.Span("■ ", style={"color": "#22C55E", "fontWeight": 700}), "≥ 80% — good"]),
                        ],
                    ),
                ),
            ],
        ),

        # ── Methodological note ───────────────────────────────────────────────
        html.Div(
            style={
                "background": "rgba(217,119,6,0.12)",
                "border": "1px solid rgba(217,119,6,0.30)",
                "borderRadius": "8px",
                "padding": "12px 16px",
                "fontSize": "12px",
                "color": "#FCD34D",
                "marginBottom": "8px",
                "lineHeight": "1.6",
            },
            children=[
                html.Strong("Methodological note: ", style={"color": "#FDE68A"}),
                "This dashboard supports exploratory visual analysis only. "
                "It shows associations and structural patterns in WDI data — "
                "not causal evidence that tourism directly causes sectoral shifts, "
                "poverty reduction, or inequality changes. "
                "Interpretations should account for confounders, country context, "
                "and the data coverage shown in Section 4.",
            ],
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
    Output("small_multiple_associations", "figure"),
    Output("trajectory_triangle", "figure"),
    Output("composition_triangle", "figure"),
    Output("structural_shift", "figure"),
    Output("coverage_matrix", "figure"),
    Output("kpi_cards", "children"),
    Output("focus_country_badge", "children"),
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

    available_tourism = snap["tourism_receipts_pct_exports"].notna().sum() if "tourism_receipts_pct_exports" in snap else 0
    avg_services = snap["services_avg"].mean() if "services_avg" in snap else np.nan
    focus_latest = latest_year_for_country("tourism_receipts_pct_exports", focus_country)

    kpi_data = [
        ("Countries", f"{len(countries)}", "in active comparison set"),
        ("Tourism data", f"{available_tourism}/{len(countries)}", "countries with values"),
        ("Avg. services share", "n/a" if pd.isna(avg_services) else f"{avg_services:.1f}%", "snapshot average"),
        ("Focus tourism year", focus_latest, f"latest data for {focus_country}"),
    ]
    kpi_children = [kpi_card(label, value, sub) for label, value, sub in kpi_data]

    return (
        fig_tourism_vs_sector(snap, sector_var, focus_country),
        fig_tourism_vs_outcome(snap, outcome_var, focus_country),
        fig_small_multiple_associations(snap),
        fig_country_trajectory_triangle(focus_country),
        fig_composition_triangle(snap, focus_country),
        fig_shift_dotplot(selected_df, countries),
        fig_coverage_matrix(selected_df, countries, sector_var, outcome_var),
        kpi_children,
        focus_country,
    )


if __name__ == "__main__":
    app.run(debug=True)
