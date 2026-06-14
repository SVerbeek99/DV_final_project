"""Export static PNG figures for the LaTeX report.

This exporter deliberately avoids Plotly/Kaleido so it does not need a browser
backend. It reuses the dashboard's default selected countries and data
transforms, then redraws the report figures with Matplotlib.
"""

from __future__ import annotations

import math
import shutil
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "report" / "figures"
sys.path.insert(0, str(ROOT))

import tourism_structural_dashboard_designed as dashboard  # noqa: E402


YEAR = 2020
MODE = "latest"
FOCUS_COUNTRY = "Morocco"
SECTOR_VAR = "services_avg"
OUTCOME_VAR = "poverty_headcount_pct"

BG = "#1E293B"
FG = "#E2E8F0"
MUTED = "#94A3B8"
GRID = "#334155"
FOCUS = "#EF4444"
SECTOR_COLORS = {
    "Services": "#4ADE80",
    "Industry": "#FB923C",
    "Agriculture": "#67E8F9",
}
COUNTRY_CODES = {
    "Spain": "ESP",
    "Thailand": "THA",
    "Morocco": "MAR",
    "Dominican Republic": "DOM",
    "Mexico": "MEX",
    "South Africa": "ZAF",
    "Indonesia": "IDN",
    "Croatia": "HRV",
    "Colombia": "COL",
}


def selected_snapshot() -> pd.DataFrame:
    return dashboard.get_snapshot(dashboard.df, YEAR, dashboard.DEFAULT_COUNTRIES, MODE)


def selected_history() -> pd.DataFrame:
    return dashboard.df[dashboard.df["Country Name"].isin(dashboard.DEFAULT_COUNTRIES)].copy()


def setup_figure(width: float, height: float) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(width, height), dpi=180)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    style_axis(ax)
    return fig, ax


def style_axis(ax: plt.Axes) -> None:
    ax.tick_params(colors=FG, labelsize=8)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(True, color=GRID, linewidth=0.5, alpha=0.65)


def save(fig: plt.Figure, filename: str) -> None:
    target = FIGURES_DIR / filename
    fig.savefig(target, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)
    print(f"Wrote {target.relative_to(ROOT)}")


def color_for_region(region: str) -> str:
    return dashboard.REGION_COLORS.get(region, dashboard.REGION_COLORS["Other"])


def add_country_labels(ax: plt.Axes, frame: pd.DataFrame, x_col: str, y_col: str, size: int = 7) -> None:
    for _, row in frame.iterrows():
        code = COUNTRY_CODES.get(row["Country Name"], row["Country Name"][:3].upper())
        ax.annotate(
            code,
            (row[x_col], row[y_col]),
            xytext=(3, 3),
            textcoords="offset points",
            color=FG,
            fontsize=size,
        )


def add_regression(ax: plt.Axes, frame: pd.DataFrame, x_col: str, y_col: str) -> None:
    plot_df = frame[[x_col, y_col]].dropna()
    if len(plot_df) < 2:
        return
    x = plot_df[x_col].astype(float)
    y = plot_df[y_col].astype(float)
    slope, intercept = np.polyfit(x, y, 1)
    xs = np.array([x.min(), x.max()])
    ax.plot(xs, slope * xs + intercept, color="#CBD5E1", linestyle="--", linewidth=1.1, alpha=0.85)


def association_panel(ax: plt.Axes, snap: pd.DataFrame, y_col: str, title: str) -> None:
    plot_df = snap.dropna(subset=["tourism_receipts_pct_exports", y_col]).copy()
    for region, region_df in plot_df.groupby("region"):
        ax.scatter(
            region_df["tourism_receipts_pct_exports"],
            region_df[y_col],
            s=58,
            color=color_for_region(region),
            edgecolors=(1, 1, 1, 0.45),
            linewidths=0.6,
            alpha=0.9,
            label=region,
        )
    focus = plot_df[plot_df["Country Name"] == FOCUS_COUNTRY]
    if not focus.empty:
        ax.scatter(
            focus["tourism_receipts_pct_exports"],
            focus[y_col],
            s=150,
            facecolors="none",
            edgecolors=FOCUS,
            linewidths=1.8,
            label=f"Focus: {FOCUS_COUNTRY}",
        )
    add_regression(ax, plot_df, "tourism_receipts_pct_exports", y_col)
    add_country_labels(ax, plot_df, "tourism_receipts_pct_exports", y_col)
    ax.set_title(title, fontsize=10, pad=8)
    ax.set_xlabel("Tourism receipts (% of exports)")
    ax.set_ylabel(dashboard.VAR_LABELS.get(y_col, y_col))


def export_association_views(snap: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.5), dpi=180)
    fig.patch.set_facecolor(BG)
    for ax in axes:
        ax.set_facecolor(BG)
        style_axis(ax)
    association_panel(axes[0], snap, SECTOR_VAR, "Tourism and services employment")
    association_panel(axes[1], snap, OUTCOME_VAR, "Tourism and poverty headcount")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False, fontsize=7, labelcolor=FG)
    fig.suptitle("Association views, selected countries, latest available by 2020", color=FG, fontsize=12)
    fig.tight_layout(rect=(0, 0.10, 1, 0.94))
    save(fig, "fig_association_views.png")


def export_small_multiples(snap: pd.DataFrame) -> None:
    variables = [v for v in dashboard.SMALL_MULTIPLE_VARS if v in snap.columns]
    fig, axes = plt.subplots(3, 3, figsize=(10.8, 6.0), dpi=180)
    fig.patch.set_facecolor(BG)
    axes_flat = axes.ravel()
    for ax in axes_flat:
        ax.set_facecolor(BG)
        style_axis(ax)
    for ax, var in zip(axes_flat, variables):
        plot_df = snap.dropna(subset=["tourism_receipts_pct_exports", var]).copy()
        for region, region_df in plot_df.groupby("region"):
            ax.scatter(
                region_df["tourism_receipts_pct_exports"],
                region_df[var],
                s=32,
                color=color_for_region(region),
                edgecolors=(1, 1, 1, 0.35),
                linewidths=0.4,
                alpha=0.9,
            )
        add_regression(ax, plot_df, "tourism_receipts_pct_exports", var)
        add_country_labels(ax, plot_df, "tourism_receipts_pct_exports", var, size=5)
        ax.set_title(dashboard.VAR_LABELS.get(var, var), fontsize=8, pad=5)
        ax.set_xlabel("Tourism (%)", fontsize=7)
        ax.set_ylabel("")
    for ax in axes_flat[len(variables):]:
        ax.axis("off")
    fig.suptitle("Small-multiple association overview", color=FG, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    save(fig, "fig_small_multiples.png")


def ternary_xy(services: pd.Series, industry: pd.Series, agriculture: pd.Series) -> tuple[pd.Series, pd.Series]:
    total = services + industry + agriculture
    x = (industry + 0.5 * services) / total
    y = (math.sqrt(3) / 2) * services / total
    return x, y


def draw_ternary_grid(ax: plt.Axes) -> None:
    h = math.sqrt(3) / 2
    triangle = np.array([[0, 0], [1, 0], [0.5, h], [0, 0]])
    ax.plot(triangle[:, 0], triangle[:, 1], color=FG, linewidth=1.0)
    for frac in np.linspace(0.2, 0.8, 4):
        ax.plot([frac * 0.5, 1 - frac * 0.5], [frac * h, frac * h], color=GRID, linewidth=0.45)
        ax.plot([frac, 0.5 + frac * 0.5], [0, h * (1 - frac)], color=GRID, linewidth=0.45)
        ax.plot([1 - frac, 0.5 * (1 - frac)], [0, h * (1 - frac)], color=GRID, linewidth=0.45)
    ax.text(0.5, h + 0.045, "Services", color=FG, ha="center", fontsize=9)
    ax.text(-0.03, -0.045, "Agriculture", color=FG, ha="left", fontsize=9)
    ax.text(1.03, -0.045, "Industry", color=FG, ha="right", fontsize=9)
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.08, h + 0.10)
    ax.set_aspect("equal")
    ax.axis("off")


def export_ternary_morocco(history: pd.DataFrame) -> None:
    fig, ax = setup_figure(5.0, 4.2)
    draw_ternary_grid(ax)
    cdf = history[history["Country Name"] == FOCUS_COUNTRY].dropna(
        subset=["services_avg", "industry_avg", "agriculture_avg"]
    ).sort_values("year")
    x, y = ternary_xy(cdf["services_avg"], cdf["industry_avg"], cdf["agriculture_avg"])
    points = ax.scatter(x, y, c=cdf["year"], cmap="viridis", s=38, edgecolors="white", linewidths=0.35)
    ax.plot(x, y, color="#CBD5E1", linewidth=1.1, alpha=0.8)
    ax.scatter([x.iloc[0]], [y.iloc[0]], s=70, color="#60A5FA", edgecolors="white", linewidths=0.5, label="Start")
    ax.scatter([x.iloc[-1]], [y.iloc[-1]], s=88, color="#FBBF24", edgecolors="white", linewidths=0.5, label="Latest")
    ax.annotate(str(int(cdf["year"].iloc[0])), (x.iloc[0], y.iloc[0]), xytext=(-16, -12), textcoords="offset points", color=FG, fontsize=8)
    ax.annotate(str(int(cdf["year"].iloc[-1])), (x.iloc[-1], y.iloc[-1]), xytext=(8, 8), textcoords="offset points", color=FG, fontsize=8)
    cbar = fig.colorbar(points, ax=ax, fraction=0.035, pad=0.02)
    cbar.ax.tick_params(colors=FG, labelsize=7)
    cbar.set_label("Year", color=FG, fontsize=8)
    ax.set_title(f"Employment-composition trajectory: {FOCUS_COUNTRY}", color=FG, fontsize=11, pad=10)
    save(fig, "fig_ternary_morocco.png")


def structural_shift_frame(history: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for country in dashboard.DEFAULT_COUNTRIES:
        cdf = history[history["Country Name"] == country].dropna(
            subset=["services_avg", "industry_avg", "agriculture_avg"]
        ).sort_values("year")
        if cdf.empty:
            continue
        first = cdf.iloc[0]
        last = cdf.iloc[-1]
        rows.extend(
            [
                {"Country Name": country, "Sector": "Services", "Change": last["services_avg"] - first["services_avg"]},
                {"Country Name": country, "Sector": "Industry", "Change": last["industry_avg"] - first["industry_avg"]},
                {"Country Name": country, "Sector": "Agriculture", "Change": last["agriculture_avg"] - first["agriculture_avg"]},
            ]
        )
    return pd.DataFrame(rows)


def export_structural_shift(history: pd.DataFrame) -> None:
    shift = structural_shift_frame(history)
    order = shift[shift["Sector"] == "Services"].sort_values("Change")["Country Name"].tolist()
    y_positions = {country: idx for idx, country in enumerate(order)}
    fig, ax = setup_figure(5.2, 4.4)
    for _, row in shift.iterrows():
        y = y_positions[row["Country Name"]]
        ax.plot([0, row["Change"]], [y, y], color=GRID, linewidth=0.7, zorder=1)
    markers = {"Services": "o", "Industry": "D", "Agriculture": "s"}
    for sector in ["Services", "Industry", "Agriculture"]:
        sdf = shift[shift["Sector"] == sector]
        ax.scatter(
            sdf["Change"],
            [y_positions[c] for c in sdf["Country Name"]],
            s=42,
            marker=markers[sector],
            color=SECTOR_COLORS[sector],
            edgecolors=(1, 1, 1, 0.45),
            linewidths=0.4,
            label=sector,
            zorder=3,
        )
    ax.axvline(0, color="#CBD5E1", linestyle="--", linewidth=0.9)
    ax.set_yticks(range(len(order)), order)
    ax.set_xlabel("Change in employment share (percentage points)")
    ax.set_title("Structural employment shifts, earliest to latest", fontsize=11)
    ax.legend(loc="lower right", frameon=False, labelcolor=FG, fontsize=8)
    fig.tight_layout()
    save(fig, "fig_structural_shift.png")


def coverage_frame(history: pd.DataFrame) -> pd.DataFrame:
    variables = [
        "tourism_receipts_pct_exports",
        "poverty_headcount_pct",
        "gini_index",
        "gdp_per_capita_current_usd",
        "urban_population_pct",
        "services_avg",
        "industry_avg",
        "agriculture_avg",
    ]
    rows: list[dict[str, object]] = []
    for var in variables:
        for country in dashboard.DEFAULT_COUNTRIES:
            cdf = history[history["Country Name"] == country]
            total = len(cdf)
            pct = 100 * cdf[var].notna().sum() / total if total else 0
            rows.append(
                {
                    "Indicator": dashboard.VAR_LABELS.get(var, var),
                    "Country": country,
                    "Coverage": pct,
                }
            )
    return pd.DataFrame(rows)


def export_data_coverage(history: pd.DataFrame) -> None:
    cov = coverage_frame(history)
    matrix = cov.pivot(index="Indicator", columns="Country", values="Coverage")
    fig, ax = setup_figure(10.8, 4.8)
    image = ax.imshow(matrix.values, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
    ax.set_xticks(range(len(matrix.columns)), matrix.columns, rotation=35, ha="right")
    ax.set_yticks(range(len(matrix.index)), matrix.index)
    ax.grid(False)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix.values[i, j]
            ax.text(j, i, f"{value:.0f}%", ha="center", va="center", color="#111827", fontsize=7)
    cbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    cbar.ax.tick_params(colors=FG, labelsize=7)
    cbar.set_label("Coverage", color=FG, fontsize=8)
    ax.set_title("Data coverage by selected country and indicator", fontsize=11)
    fig.tight_layout()
    save(fig, "fig_data_coverage.png")


def copy_dashboard_overview() -> None:
    source = FIGURES_DIR / "dashboard_overview.png"
    target = FIGURES_DIR / "fig_dashboard_overview.png"
    if target.exists():
        print(f"Kept existing {target.relative_to(ROOT)}")
        return
    if source.exists():
        shutil.copyfile(source, target)
        print(f"Copied {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    else:
        print("Missing dashboard overview screenshot; expected report/figures/dashboard_overview.png")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    snap = selected_snapshot()
    history = selected_history()
    copy_dashboard_overview()
    export_association_views(snap)
    export_small_multiples(snap)
    export_ternary_morocco(history)
    export_structural_shift(history)
    export_data_coverage(history)


if __name__ == "__main__":
    main()
