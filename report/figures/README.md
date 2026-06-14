# Figure Export Procedure

Automated figure export is still a TODO. For the initial draft/setup, export screenshots manually from the running dashboard.

## Dashboard State

Use one consistent state unless a use case requires a different one:

- Year: 2020, or the final year selected for the use cases.
- Data mode: Latest available up to selected year.
- Countries: keep the default comparison set unless the use case documents a different set.
- Focus country: Thailand, unless a verified use-case observation motivates another country.
- Sector variable: Services employment, gender-average.
- Outcome variable: Poverty headcount or Gini index for the reliability use case.

## Required Files

Save readable PNG files in this directory:

```text
fig_dashboard_overview.png
fig_association_views.png
fig_small_multiples.png
fig_ternary_thailand.png
fig_structural_shift.png
fig_data_coverage.png
fig_usecase_tourism_pathway.png
fig_usecase_reliability.png
```

## Checklist

- Crop browser chrome unless it is needed for context.
- Keep axes, legends, and labels readable at report size.
- Do not use a full-dashboard screenshot when a cropped view is more legible.
- Verify every exported figure is referenced in `report/main.tex`.
- Update captions after the use-case observations are confirmed.
