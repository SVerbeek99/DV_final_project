# Figure and Screenshot Plan

## Figure rules

- Every figure must be referenced in the text.
- Every figure must have a meaningful caption.
- Figures must be readable at final report size.
- Avoid dumping a full dashboard screenshot unless annotated.
- Use consistent file names.
- Use high-resolution PNG or PDF if possible.
- Place figures near first reference.

## Required figures

### Figure 1 — Dashboard overview / workflow

Filename:

```text
report/figures/fig_dashboard_overview.png
```

Purpose:

Show the final dashboard layout and coordinated views.

Preferred: annotated screenshot with labels A–F:

```text
A Global controls
B Association views
C Small-multiple overview, if implemented
D Ternary composition/pathway
E Structural shift dotplot
F Data coverage matrix
```

Caption draft:

```latex
\caption{Overview of the \emph{Tourism Structural Explorer}. The dashboard combines global controls, association views, compositional trajectory views, structural-shift summaries, and data-coverage inspection to support coordinated exploratory analysis.}
```

### Figure 2 — Association views

Filename:

```text
report/figures/fig_association_views.png
```

Purpose:

Support scatterplot design justification and T1/T2.

Should show two cropped scatterplots side by side:

1. Tourism vs service employment share.
2. Tourism vs poverty/GDP/urbanization/Gini.

Caption draft:

```latex
\caption{Association views for cross-country comparison. Each point represents a country, horizontal position encodes tourism dependence, vertical position encodes the selected employment or development attribute, and hue encodes region. Marker size is kept constant so that the main quantitative comparison remains based on position.}
```

### Figure 3 — Small-multiple association overview

Filename:

```text
report/figures/fig_small_multiples.png
```

Purpose:

Directly address professor feedback that users otherwise rely on memory.

Caption draft:

```latex
\caption{Small-multiple association overview. Each panel compares tourism dependence with a different employment or development attribute using the same selected countries and year. The side-by-side layout allows users to compare relationships across variables without relying on memory.}
```

If not implemented, do not include. Instead, add as limitation/future work.

### Figure 4 — Ternary trajectory

Filename:

```text
report/figures/fig_ternary_thailand.png
```

Purpose:

Support compositional pathway analysis T4.

Caption draft:

```latex
\caption{Employment-composition trajectory for Thailand. Each point represents a country--year observation, positioned by the shares of employment in services, industry, and agriculture. The connecting line shows the direction of compositional change over time.}
```

### Figure 5 — Structural shift dotplot

Filename:

```text
report/figures/fig_structural_shift.png
```

Purpose:

Support cross-country comparison of employment changes T5.

Caption draft:

```latex
\caption{Structural employment shift by country and sector. Each mark shows the percentage-point change between the earliest and latest available observations. Values right of zero indicate an increase, and values left of zero indicate a decline.}
```

### Figure 6 — Data coverage matrix

Filename:

```text
report/figures/fig_data_coverage.png
```

Purpose:

Support reliability task S1 and professor feedback that a sketch/mock-up was missing.

Caption draft:

```latex
\caption{Data coverage matrix for the selected countries and indicators. Rows represent indicators, columns represent countries, and color encodes the percentage of years with available observations.}
```

### Figure 7/8 — Use case figures

Filename examples:

```text
report/figures/fig_usecase_tourism_pathway.png
report/figures/fig_usecase_reliability.png
```

Purpose:

Show actual observations from the dashboard.

Captions must include the observation, not only the view type.

## Screenshot style guide

Use consistent dashboard state:

```text
Selected year: 2020 or final year used in app
Data mode: latest available up to selected year
Focus country: Thailand or use-case-specific country
Selected countries: stable comparison set used in interim report
```

Avoid:

- tiny unreadable full dashboard screenshots,
- cropped images with missing axes,
- captions that say only “Scatterplots,”
- screenshots with browser UI unless relevant.

## LaTeX snippet for side-by-side figures

```latex
\begin{figure*}[t]
    \centering
    \includegraphics[width=0.95\textwidth]{fig_association_views.png}
    \caption{Association views for cross-country comparison. Each point represents a country, horizontal position encodes tourism dependence, vertical position encodes the selected employment or development attribute, and hue encodes region. Marker size is kept constant so that the main quantitative comparison remains based on position.}
    \label{fig:association-views}
\end{figure*}
```

## Final visual QA

Before submission:

```text
[ ] All figures exist in report/figures.
[ ] All figures compile in PDF.
[ ] No image placeholder boxes.
[ ] No figure splits a sentence.
[ ] Every figure is referenced before or near where it appears.
[ ] Every caption explains what the reader sees.
[ ] Axes and legends are readable.
```
