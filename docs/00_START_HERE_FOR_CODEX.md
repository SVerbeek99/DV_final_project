# START HERE — Codex Operating Instructions

## Mission
Convert the current interim-report project into a final Data Visualization project submission. The final submission must be feedback-driven, runnable, reproducible, and written as a visualization design report rather than a dashboard manual.

The project is an interactive Dash/Plotly dashboard named **Tourism Structural Explorer**. It explores how tourism dependence relates to employment-sector composition and selected development indicators across countries and years using World Development Indicators data.

## Non-negotiable constraints

1. **Do not invent empirical findings.** Use the dashboard and data to obtain observations. If a use-case observation is not confirmed by the data, mark it as TODO for human review.
2. **Do not rewrite the whole application unless necessary.** Fix targeted issues from professor feedback.
3. **Do not remove existing functionality unless explicitly instructed.** Preserve current views unless a feedback item requires a change.
4. **Do not add unexplained visual encodings.** Every encoding must map to a task or be removed.
5. **Do not fabricate citations.** Add placeholder TODOs for related-work citations if exact bibliographic data is unavailable.
6. **Keep the report concise.** Final report target: max 7–8 pages including figures, excluding references. Aim for around 4 pages of text and 2–3 pages of figures.
7. **Keep the report in the provided LaTeX template.** Avoid unnecessary LaTeX packages unless the template already supports them or the package is essential.
8. **All AI-generated output must be documented** in `docs/ai_usage.md`.

## Working order

Work in this order. Do not jump to polishing before core content exists.

1. Read this file.
2. Read `01_REQUIREMENTS_AND_DELIVERABLES.md`.
3. Read `02_INTERIM_FEEDBACK_CHECKLIST.md`.
4. Create or verify repository structure.
5. Implement targeted code fixes from `04_CODE_CHANGE_TASKS.md`.
6. Export figures following `05_FIGURE_SCREENSHOT_PLAN.md`.
7. Draft final report using `03_REPORT_REWRITE_SPEC.md`.
8. Add use cases using `06_USE_CASE_EVALUATION_PLAN.md`.
9. Add related work/citations using `07_CITATION_RELATED_WORK_PLAN.md`.
10. Update AI documentation using `08_AI_USAGE_AND_MODEL_WORKFLOW.md`.
11. Run final QA from `09_FINAL_QA_SUBMISSION_CHECKLIST.md`.

## Expected repository structure

```text
repo/
  app/
    tourism_structural_dashboard_designed.py
  data/
    raw/
    processed/
  report/
    main.tex
    references.bib
    figures/
    final_report.pdf
  docs/
    ai_usage.md
    interim_feedback_checklist.md
    report_change_log.md
  scripts/
    export_figures.py
  requirements.txt
  README.md
```

If the current repository has a different structure, adapt carefully and update README paths accordingly.

## Git workflow

Use small commits:

```bash
git checkout -b final-report
# after each coherent change
git add .
git commit -m "fix: <short description>"
```

Suggested commits:

```text
baseline after interim feedback
fix: make dashboard reproducible from README
fix: remove unjustified marker size and standardize palettes
fix: improve ternary labels and hover values
feat: add small multiple association overview
feat: export final report figures
report: restructure task abstraction and data derivations
report: add final design justifications and alternatives
report: add use cases and evaluation
report: add related work and conclusion
submission: final QA cleanup
```

## Acceptance definition

The work is acceptable only if:

- The dashboard runs from README instructions.
- The final report compiles without missing citations or references.
- Every professor feedback item is either fixed or explicitly documented as a limitation/future work.
- The report contains related work, use cases/results, implementation/reproducibility, conclusion/future work, and a clear change log after interim feedback.
- All figures are readable and referenced in the text.
- AI usage is documented.
