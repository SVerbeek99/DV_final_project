# AI_USAGE_LOG.md

## 2026-05-06 — Codex help with Dash callback
Prompt:
"Fix the callback so brushing in the scatterplot filters the map view."

AI output summary:
Codex suggested changing app.py and adding a shared selected_points state.

Files changed:
- app.py
- components/scatter.py

Human verification:
I ran the app locally, tested brushing, and checked that the map updates correctly.

---

## 2026-05-06 — Claude (claude-sonnet-4-6) UX/UI and front-end design overhaul

**Prompt summary:**
Full UX/UI and front-end design overhaul of `tourism_structural_dashboard_designed.py` for JM0250 Data Visualization. Scope: layout, visual hierarchy, typography, color palette, chart presentation, captions, interaction hints, control grouping, responsive layout, accessibility, and course-aligned design polish. Analytical substance (data files, loading logic, derived metrics, research question) was explicitly excluded from the scope.

**AI output summary:**
- Replaced neon dark theme with an academic light theme (`plotly_white`, white cards, subtle borders/shadows, dark slate text).
- Replaced `REGION_COLORS` with the Okabe-Ito colorblind-safe categorical palette.
- Replaced `SECTOR_COLORS` with readable non-neon values visible on white backgrounds.
- Replaced `Turbo` colorscale in the focus-country trajectory ternary plot with `Viridis` (perceptually ordered sequential; colorbar now labelled "Year").
- Replaced neon regression line color with neutral gray (`#94A3B8`) visible on white.
- Added reusable layout helpers: `section_header()`, `chart_card()`, `control_group()`, `kpi_card()`, `_ternary_layout()`, `_ternary_axes()`, `_highlight_focus()`.
- Added `_highlight_focus()` to both scatterplots: focus country receives a red ring outline, transparent fill, and text label.
- Added focus country highlighting to `fig_composition_triangle()`: focus country is drawn as a separate trace with larger marker, red outline, and red label text.
- Restructured `app.layout` into four labeled analytical sections: (1) Explore Associations, (2) Compare Structural Composition, (3) Follow One Country, (4) Check Data Reliability.
- Added a visible "Active focus country" panel beside the trajectory chart showing the current focus country name.
- Added "Focus country badge" as a live `Output` in the main callback.
- Added explanatory chart subtitles (task-oriented), interaction hints (blue highlighted boxes), and a coverage legend row.
- Updated the header with research question text, "Association, not causation" badge, and course label.
- Improved data mode control with an explanatory note clarifying what "latest" vs "exact" means.
- Controls are now grouped by intent (Scope, Encoding, Time, Focus).
- Added `assets/dashboard.css` with responsive breakpoints (stacks to 1-column grid at ≤1024 px) and component class definitions.
- Updated coverage matrix colorscale to pastel sequential (light red → orange → yellow → green) with a visible legend row.
- Methodological "not causal" note remains, expanded and styled as a yellow callout box.
- Removed unused `avg_tourism` variable.
- All data loading and transformation logic (Sections 1–4) preserved exactly.

**Files changed:**
- `tourism_structural_dashboard_designed.py` — UX/UI and front-end overhaul (Sections 2 style constants, 5 helpers, 6 figures, 7 layout, 8 callbacks)
- `assets/dashboard.css` — new file, responsive CSS for layout and component classes

**Human verification to complete:**
- [ ] Run `python tourism_structural_dashboard_designed.py` — app starts without errors
- [ ] Country dropdown adds/removes countries and updates all charts
- [ ] Year slider updates the snapshot across all charts
- [ ] Data mode toggle (Latest / Exact) changes chart content
- [ ] Sector variable dropdown changes the left scatterplot y-axis
- [ ] Outcome variable dropdown changes the right scatterplot y-axis
- [ ] Clicking a country point in the left scatterplot updates the focus country dropdown and badge
- [ ] Focus country is visibly highlighted (red ring) in both Section 1 scatterplots
- [ ] Focus country is visibly highlighted (red outline, red label) in the composition triangle
- [ ] Focus country name appears in the Section 3 "Active focus country" panel
- [ ] Trajectory ternary plot shows Viridis colorscale (not Turbo) with "Year" colorbar label
- [ ] Coverage matrix remains visible in Section 4 with coverage legend
- [ ] "Association, not causation" badge is visible in the header
- [ ] Methodological note is visible at the bottom
- [ ] Dashboard is readable at typical laptop width (1280 px)
- [ ] No horizontal overflow at laptop width

---

## 2026-05-06 — Claude (claude-sonnet-4-6) Dark theme switch + ternary zoom + dropdown fix

**Prompt summary:**
Switch from light to dark theme. Enable zoom on the two ternary plots (Section 2 composition landscape and Section 3 trajectory). Fix white-on-white (invisible) text in dropdown/filter controls under the dark theme.

**AI output summary:**
- Replaced light academic THEME with a clean dark slate theme: paper `#0F172A`, card `#1E293B`, card2 `#172033`, grid `#334155`, text `#E2E8F0`, muted `#94A3B8`, accent `#60A5FA`.
- Brightened `REGION_COLORS` from pure Okabe-Ito to lightened variants of the same hues, so they remain legible against dark card backgrounds while preserving colorblind-safe hue distinctions.
- Updated `SECTOR_COLORS` to brighter, non-neon values readable on dark backgrounds.
- Updated `base_layout()` to use `template="plotly_dark"`, dark `paper_bgcolor`/`plot_bgcolor`, dark `hoverlabel`, and dark semi-transparent `legend` background.
- Updated `_ternary_layout()` to match dark theme (`bgcolor`, `hoverlabel`, `legend`).
- Updated all inline style dicts in helpers (`CARD_STYLE`, `CONTROL_CARD_STYLE`, `_HINT_STYLE`, `section_header`, `chart_card`, `control_group`, `kpi_card`) to use the new dark THEME values.
- Updated all hardcoded colors in `app.layout` (header, badge, focus panel, methodological note) to dark-appropriate values.
- Added `_TERNARY_CONFIG = {"displayModeBar": True, "modeBarButtonsToRemove": ["toImage"]}` and passed it as `graph_config` to both `composition_triangle` and `trajectory_triangle` chart cards, exposing the Plotly mode bar with Zoom In / Zoom Out / Pan / Reset buttons.
- Added `graph_config` parameter to `chart_card()` helper so per-chart mode bar behaviour can be specified.
- Updated interaction hint text for the two ternary charts to inform users about the mode bar zoom.
- Hardcoded dark `#1E293B` text in the coverage matrix heatmap cells (pastel backgrounds require dark text regardless of theme).
- Rewrote `assets/dashboard.css` with comprehensive dark overrides for: Dash react-select dropdowns (control, placeholder, value, menu, options, multi-tags, clear button), RadioItems, rc-slider (rail, track, handle, marks, tooltip), and the Plotly mode bar.

**Files changed:**
- `tourism_structural_dashboard_designed.py` — full dark-theme rewrite of Sections 2 (constants), 5 (helpers + CARD_STYLE), 6 (figures), 7 (layout), 8 (callbacks unchanged)
- `assets/dashboard.css` — full rewrite with comprehensive dark control overrides

**Human verification to complete:**
- [ ] Run `python tourism_structural_dashboard_designed.py` — app starts without errors
- [ ] Page background and all cards are dark (not white)
- [ ] Dropdown options are readable (dark background, light text — not white-on-white)
- [ ] Multi-select country tags are visible (blue tinted pills, not white squares)
- [ ] Slider rail is dark, track is blue
- [ ] RadioItems labels are light-coloured
- [ ] Both scatterplots render with dark Plotly theme
- [ ] Mode bar appears on hover over the composition triangle (Section 2)
- [ ] Mode bar appears on hover over the trajectory triangle (Section 3)
- [ ] Zoom In / Zoom Out buttons in the mode bar visibly zoom the ternary chart
- [ ] Reset button restores the original ternary view
- [ ] Focus country red ring is visible on the dark scatterplots
- [ ] Coverage matrix pastel cells have readable dark text
- [ ] "Association, not causation" badge is amber-coloured on dark
- [ ] Methodological note is amber on dark
- [ ] All other verification items from previous entry still pass
---

## 2026-05-07 - Codex (GPT-5) readability fix for dashboard controls

Prompt summary:
Fix white-on-white text in the dashboard control panel so dropdown and control text is readable.

AI output summary:
- Updated `assets/dashboard.css` with Dash 4 class selectors (`.dash-dropdown*`, `.dash-radioitems*`, `.dash-slider*`) so dark-theme overrides apply to current components.
- Set readable foreground/background contrast for dropdown values, placeholders, menu options, radio labels, and slider labels/thumbs.

Files changed:
- assets/dashboard.css

Human verification to complete:
- [ ] Launch dashboard and confirm control text is readable in Scope/Encoding/Focus dropdowns
- [ ] Confirm Data mode radio labels are readable
- [ ] Confirm slider year labels/track/thumb remain readable and consistent with dark theme

---

## 2026-05-07 - Codex (GPT-5) slider year input readability fix

Prompt summary:
Fix unreadable text in the "Time � comparison year" direct-input text box in dashboard controls.

AI output summary:
- Updated `assets/dashboard.css` with targeted styles for `.dash-input-container.dash-range-slider-input`.
- Set dark background, light text color, visible border, and focus outline so the year input text is readable.

Files changed:
- assets/dashboard.css

Human verification to complete:
- [ ] Open dashboard and confirm the year text in the right-side Time input is readable
- [ ] Confirm focus state border/outline is visible when clicking into the year input

---

## 2026-06-13 - Codex (GPT-5) initial final-submission draft/setup

Prompt summary:
Read `docs/10_CODEX_MASTER_PROMPT.md` and execute the plan through the initial draft/setup stage, then stop and list unresolved TODOs.

AI output summary:
- Added a standard `app/` entry point that delegates to the existing Dash implementation.
- Updated README run instructions, repository structure, data-file assumptions, limitations, figure procedure, and AI/code provenance.
- Removed variable marker-size encodings from association scatterplots and ternary views; retained contextual values in hover details.
- Added a small-multiple association overview using constant-size marks and stable region hue.
- Updated ternary axis labels to percentages and prioritized selected variables in the coverage matrix.
- Reworked `report/main.tex` into a final-report draft scaffold with What/Why/How tables, design rationale, figures, use-case placeholders, and explicit TODO markers.
- Added `report/figures/README.md` for manual screenshot export and `docs/ai_usage.md` for table-format AI documentation.

Files changed:
- `tourism_structural_dashboard_designed.py`
- `app/tourism_structural_dashboard_designed.py`
- `README.md`
- `report/main.tex`
- `report/figures/README.md`
- `docs/ai_usage.md`
- `AI_USAGE_LOG.md`

Human verification to complete:
- [ ] Run the dashboard and inspect all updated views.
- [ ] Verify the small-multiple overview responds to countries, year, and data mode.
- [ ] Export report figures into `report/figures/`.
- [ ] Fill use-case observations from the actual dashboard.
- [ ] Verify and add related-work citations.
- [ ] Compile the final LaTeX report and fix layout/page-budget issues.

---

## 2026-06-13 - Codex (GPT-5) second report cleanup pass

Prompt summary:
Read `report/main.tex`, `report/references.bib`, and the compiled PDF, then remove visible TODOs, insert the supplied related-work prose, add missing citation entries, move interim-feedback content, and compile the report.

AI output summary:
- Converted unresolved report TODOs into LaTeX comments so they do not appear in the PDF.
- Replaced the related-work placeholder with the user-supplied related-work text.
- Added bibliography entries for the related-work citations and compiled the PDF.
- Moved interim-feedback changes into a non-floating bullet list under Section 7.
- Added short explanatory paragraphs for domain tasks and task abstraction.

Files changed:
- report/main.tex
- report/references.bib
- report/main.pdf
- docs/ai_usage.md
- AI_USAGE_LOG.md

Human verification to complete:
- [ ] Export final dashboard screenshots into `report/figures/`.
- [ ] Fill use-case observations from actual dashboard inspection.
- [ ] Inspect the compiled PDF layout visually before submission.

---

## 2026-06-13 - Codex (GPT-5) use-case observation summarizer

Prompt summary:
Create `scripts/summarize_use_cases.py` to load `employmentdata.csv` and `tourism15indicators.csv`, compute factual candidate observations for the selected country set, and write `docs/use_case_observations.md`.

AI output summary:
- Added a standalone Python summarizer that reproduces the dashboard's WDI indicator mapping and gender-average employment-sector shares.
- Generated Markdown tables for latest-available 2020 values, tourism receipts versus services employment, first/latest employment-sector shares, structural shifts, coverage percentages, and ranked country lists.
- Kept the generated document factual, with tables and short value summaries rather than conclusions.

Files changed:
- scripts/summarize_use_cases.py
- docs/use_case_observations.md
- AI_USAGE_LOG.md

Human verification to complete:
- [ ] Review `docs/use_case_observations.md` before inserting any observations into the report.

---

## 2026-06-13 - Codex (GPT-5) evidence insertion pass

Prompt summary:
Read `report/main.tex` and `docs/use_case_observations.md`, insert the supplied use-case evidence text, update the Morocco ternary figure reference, revise the abstract and conclusion, and compile the report.

AI output summary:
- Replaced Use Case 1 and Use Case 2 placeholder text with the user-provided evidence text.
- Updated the ternary focus figure reference, caption, and label from Thailand/generic wording to Morocco.
- Replaced the draft abstract and final conclusion text.
- Compiled `report/main.pdf` with `latexmk` and checked remaining figure placeholders.

Files changed:
- report/main.tex
- report/main.pdf
- report/main.bbl
- AI_USAGE_LOG.md

Human verification to complete:
- [ ] Export and inspect the remaining report figures, especially `fig_ternary_morocco.png`.

---

## 2026-06-14 - Codex (GPT-5) report figure regeneration and LaTeX wiring

Prompt summary:
Regenerate the missing report figures, avoid the Kaleido/browser backend after startup failures, wire real PNG files into `report/main.tex`, compile the PDF, and report warnings, page count, readability, and float placement.

AI output summary:
- Replaced the browser-dependent Plotly/Kaleido exporter with a Matplotlib-based `scripts/export_report_figures.py` that uses the dashboard's default countries and data transforms.
- Generated all expected report figure PNGs in `report/figures/`.
- Replaced LaTeX placeholder/fallback image handling with real `\includegraphics` calls and nearby `\autoref{}` mentions.
- Added float barriers so figures stay with the design section instead of drifting to the conclusion/references.
- Recompiled `report/main.pdf` and checked unresolved references/citations, overfull boxes, page count, and figure readability/placement.

Files changed:
- scripts/export_report_figures.py
- report/figures/fig_dashboard_overview.png
- report/figures/fig_association_views.png
- report/figures/fig_small_multiples.png
- report/figures/fig_ternary_morocco.png
- report/figures/fig_structural_shift.png
- report/figures/fig_data_coverage.png
- report/main.tex
- report/main.pdf
- requirements.txt
- tourism_structural_requirements.txt
- docs/ai_usage.md
- AI_USAGE_LOG.md

Human verification to complete:
- [ ] Inspect the final PDF at normal reading zoom before submission.
- [ ] Confirm the dashboard overview screenshot is the desired crop/state.
