# Code Change Tasks for Codex

These are targeted implementation changes. Make the smallest correct changes. After each task, run the app and inspect the affected view.

## Task C1 — Repository and runnable app

### Goal
Make the app runnable from a clean clone.

### Steps

1. Ensure the main app file is in `app/` or update README to match actual location.
2. Ensure data files are in documented paths.
3. Ensure `requirements.txt` includes at least:
   - dash
   - plotly
   - pandas
   - numpy
   - kaleido if exporting static figures
4. Add README run instructions.

### Acceptance

From a clean clone:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app/tourism_structural_dashboard_designed.py
```

App starts without callback errors.

## Task C2 — Remove unjustified marker size

### Problem
Professor asked why marker size is included and whether it supports a task.

### Preferred fix
Make marker size constant in scatterplots unless there is a strong task justification.

### Implementation

- Locate scatterplot creation functions.
- Remove `size=...` mappings from Plotly Express or set a constant marker size for Graph Objects.
- Keep extra values in hover tooltips.

### Acceptance

- Scatterplot points are constant size.
- Report can state marker size is kept constant to avoid implying a third quantitative attribute.

## Task C3 — Fixed color palettes

### Problem
Professor repeatedly asked how color palette was chosen.

### Goal
Use fixed, consistent, colorblind-aware palettes.

### Implementation

Create constants near top of app file:

```python
REGION_COLORS = {
    # fill with actual region names from data
}

SECTOR_COLORS = {
    "Services": "#...",
    "Industry": "#...",
    "Agriculture": "#...",
}
```

Use the same mapping in all relevant views.

Rules:

- Region hue: categorical palette.
- Sector hue/shape: categorical palette.
- Structural shift magnitude: position, not color.
- Coverage percentage: sequential scale if quantitative.

### Acceptance

- Same region/sector has same color across views.
- Legends are stable under filtering.
- Report can justify hue as categorical channel.

## Task C4 — Ternary labels and hover

### Problem
Professor said ternary axis labeling is unclear and should communicate a 0–100 composition.

### Goal
Make ternary plot self-explanatory.

### Implementation

- Ternary axis titles: `Services (%)`, `Industry (%)`, `Agriculture (%)` or equivalent.
- Hover must show:
  - country
  - year
  - services share
  - industry share
  - agriculture share
- If possible, format ticks as percentages.
- Ensure the three values sum to approximately 100 for the selected data mode.

### Acceptance

A reader can understand the ternary figure without report text.

## Task C5 — Data coverage matrix integration

### Problem
Professor asked whether the data coverage matrix is integrated with other views.

### Goal
Ensure coverage matrix uses the same selected countries and relevant indicators.

### Implementation

- If existing matrix exists: verify it updates when selected countries/indicators change.
- If not integrated: integrate selected countries at minimum.
- Add title/subtitle explaining rows = indicators, columns = countries, color = coverage percentage.

### Acceptance

- Matrix appears in dashboard.
- Matrix reflects current selected country set.
- Screenshot can be exported for report.

## Task C6 — Small-multiple association overview

### Problem
Professor said only one employment/development indicator can be compared against tourism at a time, forcing users to rely on memory.

### Goal
Add a compact small-multiple overview that compares tourism dependence against several variables simultaneously.

### Preferred design

A grid of scatterplots with:

- x-axis: tourism receipts % of exports.
- y-axis: one outcome per panel.
- points: countries.
- color: region.
- selected year and data mode inherited from global controls.
- constant marker size.

Candidate panels:

```text
Services employment share
Industry employment share
Agriculture employment share
GDP per capita
Urban population share
Poverty headcount
Gini index
```

### Implementation options

- Plotly facet chart.
- Manually created subplots.
- Dash section with multiple compact graphs.

### Acceptance

- Users can compare multiple tourism-variable relationships side by side.
- Report can cite this as solving the memory issue.
- If time is too short, mark this as `LIMITATION` in feedback checklist and add future work paragraph.

## Task C7 — Figure export script

### Goal
Export reproducible screenshots/figures for final report.

### Implementation

Create `scripts/export_figures.py` if feasible.

It should save figures to:

```text
report/figures/
  fig_dashboard_overview.png
  fig_association_views.png
  fig_small_multiples.png
  fig_ternary_thailand.png
  fig_structural_shift.png
  fig_data_coverage.png
  fig_usecase_1.png
  fig_usecase_2.png
```

If automated export is too hard, document manual screenshot procedure in `report/figures/README.md`.

### Acceptance

All report figures exist in `report/figures/`, are readable, and match captions.

## Task C8 — README

### README must include

```markdown
# Tourism Structural Explorer

## What this project does
## Repository structure
## Requirements
## How to run
## Data files
## How to reproduce report figures
## Known limitations
## AI/code provenance
```

### Acceptance

A grader can run the app without asking questions.
