"""Generate factual use-case observation tables from the project CSV data."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
EMPLOYMENT_CSV = ROOT / "employmentdata.csv"
TOURISM_CSV = ROOT / "tourism15indicators.csv"
DEFAULT_OUTPUT = ROOT / "docs" / "use_case_observations.md"
DEFAULT_YEAR = 2020

DEFAULT_COUNTRIES = [
    "Spain",
    "Thailand",
    "Morocco",
    "Dominican Republic",
    "Mexico",
    "South Africa",
    "Indonesia",
    "Croatia",
    "Colombia",
]

SERIES_RENAME = {
    "Employment in services, male (% of male employment) (modeled ILO estimate)": "services_male",
    "Employment in services, female (% of female employment) (modeled ILO estimate)": "services_female",
    "Employment in industry, male (% of male employment) (modeled ILO estimate)": "industry_male",
    "Employment in industry, female (% of female employment) (modeled ILO estimate)": "industry_female",
    "Employment in agriculture, male (% of male employment) (modeled ILO estimate)": "agriculture_male",
    "Employment in agriculture, female (% of female employment) (modeled ILO estimate)": "agriculture_female",
    "International tourism, receipts (% of total exports)": "tourism_receipts_pct_exports",
    "Urban population (% of total population)": "urban_population_pct",
    "GDP per capita (current US$)": "gdp_per_capita_current_usd",
    "Poverty headcount ratio at national poverty lines (% of population)": "poverty_headcount_pct",
    "Gini index": "gini_index",
}

INDICATOR_LABELS = {
    "tourism_receipts_pct_exports": "Tourism receipts (% of exports)",
    "poverty_headcount_pct": "Poverty headcount (%)",
    "gini_index": "Gini index",
    "gdp_per_capita_current_usd": "GDP per capita (current US$)",
    "urban_population_pct": "Urban population (%)",
    "employment_sectors_complete": "Employment sectors, all three (%)",
    "services_avg": "Services employment, gender-average (%)",
    "industry_avg": "Industry employment, gender-average (%)",
    "agriculture_avg": "Agriculture employment, gender-average (%)",
}

SECTOR_AVG_COLUMNS = ["services_avg", "industry_avg", "agriculture_avg"]
COVERAGE_COLUMNS = [
    "tourism_receipts_pct_exports",
    "poverty_headcount_pct",
    "gini_index",
    "gdp_per_capita_current_usd",
    "urban_population_pct",
    "employment_sectors_complete",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write factual Markdown observation tables for the dashboard use cases."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=DEFAULT_YEAR,
        help=f"Snapshot year for latest-available tables. Default: {DEFAULT_YEAR}.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Markdown output path. Default: {DEFAULT_OUTPUT.relative_to(ROOT)}.",
    )
    parser.add_argument(
        "--countries",
        nargs="+",
        default=DEFAULT_COUNTRIES,
        help="Countries to include. Default: dashboard selected country set.",
    )
    return parser.parse_args()


def year_columns(raw: pd.DataFrame) -> list[str]:
    return [c for c in raw.columns if re.match(r"^\d{4} \[YR\d{4}\]$", c)]


def year_from_column(column: str) -> int:
    return int(re.search(r"(\d{4})", column).group(1))


def read_wdi_wide(path: Path) -> tuple[pd.DataFrame, list[int]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input CSV: {path}")

    raw = pd.read_csv(path)
    raw = raw[raw["Country Code"].astype(str).str.match(r"^[A-Z]{3}$", na=False)].copy()
    raw = raw[raw["Series Name"].isin(SERIES_RENAME)].copy()

    years = year_columns(raw)
    long_df = raw.melt(
        id_vars=["Country Name", "Country Code", "Series Name", "Series Code"],
        value_vars=years,
        var_name="year_raw",
        value_name="value",
    )
    long_df["year"] = long_df["year_raw"].map(year_from_column)
    long_df["indicator"] = long_df["Series Name"].map(SERIES_RENAME)
    long_df["value"] = pd.to_numeric(long_df["value"].replace("..", np.nan), errors="coerce")
    return (
        long_df[["Country Name", "Country Code", "year", "indicator", "value"]],
        [year_from_column(c) for c in years],
    )


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in [
        "services_male",
        "services_female",
        "industry_male",
        "industry_female",
        "agriculture_male",
        "agriculture_female",
    ]:
        if col not in df.columns:
            df[col] = np.nan

    df["services_avg"] = df[["services_male", "services_female"]].mean(axis=1)
    df["industry_avg"] = df[["industry_male", "industry_female"]].mean(axis=1)
    df["agriculture_avg"] = df[["agriculture_male", "agriculture_female"]].mean(axis=1)
    df["employment_sectors_complete"] = df[SECTOR_AVG_COLUMNS].notna().all(axis=1)
    return df


def build_dataset() -> tuple[pd.DataFrame, list[int]]:
    employment_long, employment_years = read_wdi_wide(EMPLOYMENT_CSV)
    tourism_long, tourism_years = read_wdi_wide(TOURISM_CSV)
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
    all_years = sorted(set(employment_years) | set(tourism_years))
    return wide.sort_values(["Country Name", "year"]), all_years


def latest_snapshot(df: pd.DataFrame, year: int, countries: Iterable[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    variable_cols = [c for c in df.columns if c not in {"Country Name", "Country Code", "year"}]

    for country in countries:
        sub = df[(df["Country Name"] == country) & (df["year"] <= year)].sort_values("year")
        if sub.empty:
            continue
        row: dict[str, object] = {
            "Country Name": country,
            "Country Code": sub["Country Code"].dropna().iloc[-1],
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

    return pd.DataFrame(rows)


def employment_endpoints(df: pd.DataFrame, countries: Iterable[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for country in countries:
        cdf = df[df["Country Name"] == country].dropna(subset=SECTOR_AVG_COLUMNS).sort_values("year")
        if cdf.empty:
            continue
        first = cdf.iloc[0]
        latest = cdf.iloc[-1]
        row = {
            "Country Name": country,
            "first_year": int(first["year"]),
            "latest_year": int(latest["year"]),
            "first_services": first["services_avg"],
            "first_industry": first["industry_avg"],
            "first_agriculture": first["agriculture_avg"],
            "latest_services": latest["services_avg"],
            "latest_industry": latest["industry_avg"],
            "latest_agriculture": latest["agriculture_avg"],
            "services_change_pp": latest["services_avg"] - first["services_avg"],
            "industry_change_pp": latest["industry_avg"] - first["industry_avg"],
            "agriculture_change_pp": latest["agriculture_avg"] - first["agriculture_avg"],
        }
        rows.append(row)
    return pd.DataFrame(rows)


def coverage_table(df: pd.DataFrame, countries: Iterable[str], years: list[int]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    denominator = len(years)
    for indicator in COVERAGE_COLUMNS:
        row: dict[str, object] = {"Indicator": INDICATOR_LABELS[indicator]}
        values = []
        for country in countries:
            cdf = df[(df["Country Name"] == country) & (df["year"].isin(years))]
            if indicator == "employment_sectors_complete":
                count = int(cdf[indicator].fillna(False).sum()) if indicator in cdf else 0
            else:
                count = int(cdf[indicator].notna().sum()) if indicator in cdf else 0
            pct = count / denominator * 100
            values.append(pct)
            row[country] = pct
        row["Mean"] = float(np.mean(values)) if values else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def fmt_number(value: object, digits: int = 1) -> str:
    if pd.isna(value):
        return "n/a"
    return f"{float(value):,.{digits}f}"


def fmt_int(value: object) -> str:
    if pd.isna(value):
        return "n/a"
    return str(int(value))


def fmt_value_with_year(row: pd.Series, value_col: str, digits: int = 1) -> str:
    value = row.get(value_col)
    year = row.get(f"{value_col}_source_year")
    if pd.isna(value):
        return "n/a"
    return f"{fmt_number(value, digits)} ({fmt_int(year)})"


def escape_md(value: object) -> str:
    return str(value).replace("|", "\\|")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows available._"

    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(escape_md(row.get(col, "")) for col in columns) + " |")
    return "\n".join([header, separator, *body])


def snapshot_rows(snapshot: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for _, row in snapshot.iterrows():
        rows.append(
            {
                "Country": row["Country Name"],
                "Tourism receipts": fmt_value_with_year(row, "tourism_receipts_pct_exports", 1),
                "Services": fmt_value_with_year(row, "services_avg", 1),
                "Industry": fmt_value_with_year(row, "industry_avg", 1),
                "Agriculture": fmt_value_with_year(row, "agriculture_avg", 1),
                "Poverty": fmt_value_with_year(row, "poverty_headcount_pct", 1),
                "Gini": fmt_value_with_year(row, "gini_index", 1),
                "GDP per capita": fmt_value_with_year(row, "gdp_per_capita_current_usd", 0),
                "Urban population": fmt_value_with_year(row, "urban_population_pct", 1),
            }
        )
    return rows


def tourism_vs_services_rows(snapshot: pd.DataFrame) -> list[dict[str, object]]:
    paired = snapshot.dropna(subset=["tourism_receipts_pct_exports", "services_avg"]).copy()
    paired = paired.sort_values("tourism_receipts_pct_exports", ascending=False)
    rows = []
    for _, row in paired.iterrows():
        rows.append(
            {
                "Country": row["Country Name"],
                "Tourism receipts": fmt_value_with_year(row, "tourism_receipts_pct_exports", 1),
                "Services": fmt_value_with_year(row, "services_avg", 1),
                "Services minus paired mean": fmt_number(row["services_avg"] - paired["services_avg"].mean(), 1),
            }
        )
    return rows


def endpoint_rows(endpoints: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    for _, row in endpoints.sort_values("Country Name").iterrows():
        rows.append(
            {
                "Country": row["Country Name"],
                "First year": fmt_int(row["first_year"]),
                "First services": fmt_number(row["first_services"], 1),
                "First industry": fmt_number(row["first_industry"], 1),
                "First agriculture": fmt_number(row["first_agriculture"], 1),
                "Latest year": fmt_int(row["latest_year"]),
                "Latest services": fmt_number(row["latest_services"], 1),
                "Latest industry": fmt_number(row["latest_industry"], 1),
                "Latest agriculture": fmt_number(row["latest_agriculture"], 1),
            }
        )
    return rows


def shift_rows(endpoints: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    sort_cols = ["services_change_pp", "Country Name"]
    for _, row in endpoints.sort_values(sort_cols, ascending=[False, True]).iterrows():
        rows.append(
            {
                "Country": row["Country Name"],
                "Years": f"{fmt_int(row['first_year'])}-{fmt_int(row['latest_year'])}",
                "Services change": fmt_number(row["services_change_pp"], 1),
                "Industry change": fmt_number(row["industry_change_pp"], 1),
                "Agriculture change": fmt_number(row["agriculture_change_pp"], 1),
            }
        )
    return rows


def coverage_rows(coverage: pd.DataFrame, countries: list[str]) -> list[dict[str, object]]:
    rows = []
    for _, row in coverage.iterrows():
        out = {"Indicator": row["Indicator"]}
        for country in countries:
            out[country] = f"{fmt_number(row[country], 0)}%"
        out["Mean"] = f"{fmt_number(row['Mean'], 0)}%"
        rows.append(out)
    return rows


def ranked_tourism_rows(snapshot: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    ranked = snapshot.dropna(subset=["tourism_receipts_pct_exports"]).sort_values(
        "tourism_receipts_pct_exports", ascending=False
    )
    for rank, (_, row) in enumerate(ranked.iterrows(), start=1):
        rows.append(
            {
                "Rank": rank,
                "Country": row["Country Name"],
                "Tourism receipts": fmt_value_with_year(row, "tourism_receipts_pct_exports", 1),
            }
        )
    return rows


def ranked_services_rows(snapshot: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    ranked = snapshot.dropna(subset=["services_avg"]).sort_values("services_avg", ascending=False)
    for rank, (_, row) in enumerate(ranked.iterrows(), start=1):
        rows.append(
            {
                "Rank": rank,
                "Country": row["Country Name"],
                "Services": fmt_value_with_year(row, "services_avg", 1),
            }
        )
    return rows


def ranked_service_increase_rows(endpoints: pd.DataFrame) -> list[dict[str, object]]:
    rows = []
    ranked = endpoints.sort_values("services_change_pp", ascending=False)
    for rank, (_, row) in enumerate(ranked.iterrows(), start=1):
        rows.append(
            {
                "Rank": rank,
                "Country": row["Country Name"],
                "Years": f"{fmt_int(row['first_year'])}-{fmt_int(row['latest_year'])}",
                "First services": fmt_number(row["first_services"], 1),
                "Latest services": fmt_number(row["latest_services"], 1),
                "Change": fmt_number(row["services_change_pp"], 1),
            }
        )
    return rows


def ranked_sparse_poverty_gini_rows(
    coverage: pd.DataFrame, countries: list[str]
) -> list[dict[str, object]]:
    coverage_by_indicator = coverage.set_index("Indicator")
    poverty_label = INDICATOR_LABELS["poverty_headcount_pct"]
    gini_label = INDICATOR_LABELS["gini_index"]
    rows = []
    for country in countries:
        poverty = float(coverage_by_indicator.loc[poverty_label, country])
        gini = float(coverage_by_indicator.loc[gini_label, country])
        rows.append(
            {
                "Country": country,
                "Poverty coverage": poverty,
                "Gini coverage": gini,
                "Average": (poverty + gini) / 2,
            }
        )
    rows = sorted(rows, key=lambda row: (row["Average"], row["Country"]))
    return [
        {
            "Rank": rank,
            "Country": row["Country"],
            "Poverty coverage": f"{fmt_number(row['Poverty coverage'], 0)}%",
            "Gini coverage": f"{fmt_number(row['Gini coverage'], 0)}%",
            "Average": f"{fmt_number(row['Average'], 0)}%",
        }
        for rank, row in enumerate(rows, start=1)
    ]


def summary_line(label: str, row: pd.Series, value_col: str, digits: int = 1) -> str:
    return (
        f"- {label}: {row['Country Name']} at "
        f"{fmt_value_with_year(row, value_col, digits)}."
    )


def build_markdown(
    df: pd.DataFrame,
    all_years: list[int],
    countries: list[str],
    snapshot_year: int,
) -> str:
    available_countries = [c for c in countries if c in set(df["Country Name"])]
    snapshot = latest_snapshot(df, snapshot_year, available_countries)
    endpoints = employment_endpoints(df, available_countries)
    coverage = coverage_table(df, available_countries, all_years)

    paired = snapshot.dropna(subset=["tourism_receipts_pct_exports", "services_avg"]).copy()
    lines = [
        "# Use Case Observation Candidates",
        "",
        "Generated from `employmentdata.csv` and `tourism15indicators.csv`.",
        "",
        "Scope notes:",
        f"- Selected country set: {', '.join(available_countries)}.",
        f"- Snapshot year: {snapshot_year}; latest-available mode uses the most recent non-missing value at or before {snapshot_year}.",
        "- Employment-sector shares are gender-average percentages computed from the male and female WDI employment shares.",
        f"- Coverage percentages use the {len(all_years)} CSV year columns ({min(all_years)}-{max(all_years)}) as the denominator.",
        "",
        f"## 1. Latest-Available Snapshot for {snapshot_year}",
        "",
        markdown_table(
            snapshot_rows(snapshot),
            [
                "Country",
                "Tourism receipts",
                "Services",
                "Industry",
                "Agriculture",
                "Poverty",
                "Gini",
                "GDP per capita",
                "Urban population",
            ],
        ),
        "",
        "## 2. Tourism Receipts vs Services Employment",
        "",
        f"- Countries with both values in the {snapshot_year} latest-available snapshot: {len(paired)} of {len(available_countries)}.",
    ]

    if not paired.empty:
        lines.extend(
            [
                summary_line(
                    "Highest tourism receipts among paired countries",
                    paired.sort_values("tourism_receipts_pct_exports", ascending=False).iloc[0],
                    "tourism_receipts_pct_exports",
                    1,
                ),
                summary_line(
                    "Highest services employment among paired countries",
                    paired.sort_values("services_avg", ascending=False).iloc[0],
                    "services_avg",
                    1,
                ),
            ]
        )

    lines.extend(
        [
            "",
            markdown_table(
                tourism_vs_services_rows(snapshot),
                ["Country", "Tourism receipts", "Services", "Services minus paired mean"],
            ),
            "",
            "## 3. First and Latest Available Employment-Sector Shares",
            "",
            markdown_table(
                endpoint_rows(endpoints),
                [
                    "Country",
                    "First year",
                    "First services",
                    "First industry",
                    "First agriculture",
                    "Latest year",
                    "Latest services",
                    "Latest industry",
                    "Latest agriculture",
                ],
            ),
            "",
            "## 4. Structural Shifts in Employment Sectors",
            "",
        ]
    )

    if not endpoints.empty:
        lines.extend(
            [
                f"- Largest services increase: {endpoints.sort_values('services_change_pp', ascending=False).iloc[0]['Country Name']} at {fmt_number(endpoints['services_change_pp'].max(), 1)} percentage points.",
                f"- Largest industry change by absolute value: {endpoints.loc[endpoints['industry_change_pp'].abs().idxmax(), 'Country Name']} at {fmt_number(endpoints.loc[endpoints['industry_change_pp'].abs().idxmax(), 'industry_change_pp'], 1)} percentage points.",
                f"- Largest agriculture change by absolute value: {endpoints.loc[endpoints['agriculture_change_pp'].abs().idxmax(), 'Country Name']} at {fmt_number(endpoints.loc[endpoints['agriculture_change_pp'].abs().idxmax(), 'agriculture_change_pp'], 1)} percentage points.",
                "",
            ]
        )

    lines.extend(
        [
            markdown_table(
                shift_rows(endpoints),
                ["Country", "Years", "Services change", "Industry change", "Agriculture change"],
            ),
            "",
            "## 5. Data Coverage Percentages",
            "",
            markdown_table(
                coverage_rows(coverage, available_countries),
                ["Indicator", *available_countries, "Mean"],
            ),
            "",
            "## 6. Ranked Lists",
            "",
            "### Highest Tourism Dependence",
            "",
            markdown_table(
                ranked_tourism_rows(snapshot),
                ["Rank", "Country", "Tourism receipts"],
            ),
            "",
            "### Highest Service Employment",
            "",
            markdown_table(
                ranked_services_rows(snapshot),
                ["Rank", "Country", "Services"],
            ),
            "",
            "### Largest Increase in Services",
            "",
            markdown_table(
                ranked_service_increase_rows(endpoints),
                ["Rank", "Country", "Years", "First services", "Latest services", "Change"],
            ),
            "",
            "### Sparsest Poverty/Gini Coverage",
            "",
            markdown_table(
                ranked_sparse_poverty_gini_rows(coverage, available_countries),
                ["Rank", "Country", "Poverty coverage", "Gini coverage", "Average"],
            ),
            "",
        ]
    )

    return "\n".join(lines)


def resolve_output_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def main() -> None:
    args = parse_args()
    df, all_years = build_dataset()
    output = resolve_output_path(args.output)
    markdown = build_markdown(df, all_years, args.countries, args.year)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
