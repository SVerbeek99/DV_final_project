# Tourism Structural Explorer

Interactive Dash/Plotly dashboard for JM0250 Data Visualization. The project supports exploratory analysis of how international tourism dependence relates to employment-sector composition and selected development indicators across countries and years.

The dashboard is for comparison, hypothesis generation, and data-quality awareness. It does not claim that tourism causes employment shifts or development outcomes.

## What This Project Does

- Compares tourism receipts as a share of exports with employment and development indicators.
- Shows coordinated country views: association scatterplots, small multiples, ternary employment composition, structural-shift dotplot, and data coverage matrix.
- Supports filtering by country, year, data mode, sector variable, and development outcome.
- Lets users click a country in the association view to inspect its focus-country employment pathway.

## Repository Structure

```text
app/
  tourism_structural_dashboard_designed.py   # standard app entry point
assets/
  dashboard.css                              # Dash styling
docs/
  *.md                                       # planning, checklist, and AI-use notes
report/
  main.tex                                   # final-report draft/setup
  references.bib
  figures/
    README.md                                # manual figure export procedure
tourism_structural_dashboard_designed.py     # main Dash implementation
employmentdata.csv                           # WDI employment indicators
tourism15indicators.csv                      # WDI tourism/development indicators
requirements.txt
AI_USAGE_LOG.md
```

## Requirements

- Python 3.10 or newer recommended.
- Packages listed in `requirements.txt`: Dash, Plotly, pandas, and NumPy.
- The two CSV files must remain in the repository root unless the app data-loading paths are changed.

## How To Run

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app\tourism_structural_dashboard_designed.py
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/tourism_structural_dashboard_designed.py
```

Then open `http://127.0.0.1:8050`.

The original root-level command also works:

```bash
python tourism_structural_dashboard_designed.py
```

## Data Files

The project uses World Development Indicators data exported into:

- `employmentdata.csv`
- `tourism15indicators.csv`

Key variables include international tourism receipts as a percentage of total exports, employment shares in services/industry/agriculture, GDP per capita, urban population share, poverty headcount, and Gini index. The app derives gender-average sector employment, latest-available snapshots, first-to-latest structural shifts, and data coverage percentages.

## How To Reproduce Report Figures

Automated screenshot export is not yet implemented. Use the manual procedure in `report/figures/README.md` and save figures into `report/figures/` with the filenames expected by `report/main.tex`.

## Known Limitations

- The analysis is exploratory and associational, not causal.
- Tourism dependence is represented by one WDI indicator: international tourism receipts as a percentage of total exports.
- Missing data can affect comparisons, especially for poverty and inequality indicators.
- The report draft contains TODO markers for human-verified citations, use-case observations, screenshots, and final QA.

## AI/Code Provenance

Dashboard code was developed for the course using Python libraries and AI-assisted code review/editing. AI assistance is documented in `AI_USAGE_LOG.md` and `docs/ai_usage.md`; human review is still required before submission.
