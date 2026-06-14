# AI Usage and Model Workflow

AI use must be documented. This project will use Codex, GPT, and Claude. Use this file to coordinate and log usage.

## Tool roles

### Codex

Use for:

- Code cleanup.
- Dashboard implementation changes.
- Color palette constants.
- Ternary axis/hover fixes.
- Small-multiple association overview.
- Figure export script.
- README/run instructions.
- LaTeX restructuring if safe.

Do not let Codex invent use-case findings.

### GPT Pro

Use for:

- Final report drafting.
- Section rewriting.
- Technical explanation refinement.
- Rubric alignment.
- Citation placement.
- Concision and grammar.

### Claude Opus

Use as hostile reviewer:

- Find weak justifications.
- Find unsupported claims.
- Find places where design is described but not justified.
- Find task/design mismatch.
- Find missing alternatives.

Do not blindly accept Claude output. Use it as critique.

## AI usage log template

Create or update `docs/ai_usage.md` with:

```markdown
# AI Usage Log

| Date | Tool/model | Prompt summary | Output used | Where used | Human verification |
|---|---|---|---|---|---|
| 2026-06-14 | Codex | Added fixed color palettes and removed scatterplot marker-size mapping | Code patch | app/dashboard file | Ran app locally, inspected scatterplots |
| 2026-06-14 | GPT Pro | Rewrote task abstraction section using one action-target pair per task | Edited text | report/main.tex | Checked against professor feedback |
| 2026-06-14 | Claude Opus | Critiqued final design section for weak justification | Reviewer comments only | report revision checklist | Accepted only comments matching rubric/professor feedback |
```

## Prompts to use

### Codex prompt: repo setup

```text
You are working in a GitHub repository for a Data Visualization final project. First inspect the repository structure. Create or update docs/ai_usage.md, docs/interim_feedback_checklist.md, and README.md. Ensure the dashboard can be run from a clean clone using requirements.txt. Do not rewrite the application. Return a summary of changed files and any assumptions.
```

### Codex prompt: scatterplot fixes

```text
Inspect the Dash/Plotly dashboard code. Find the functions that create the two association scatterplots. Remove any variable marker-size encoding unless it is essential. Use constant marker size and keep extra variables in hover tooltips. Add fixed color mapping for regions using a categorical palette. Do not change the data filtering behavior. After editing, explain exactly which functions changed.
```

### Codex prompt: ternary fixes

```text
Fix the Plotly ternary views so that agriculture, industry, and services are clearly labeled as percentages in a three-part composition summing to 100. Improve hover text to show country, year, services %, industry %, and agriculture %. Preserve current focus-country and selected-year behavior. Return a minimal patch.
```

### Codex prompt: small multiples

```text
Add a small-multiple association overview to the Dash dashboard. Each panel should plot tourism receipts as % of exports on the x-axis against one employment or development variable on the y-axis. Use the same selected countries, selected year, and data mode as the existing scatterplots. Use constant marker size and color by region. Keep existing views unchanged. Prefer a compact Plotly facet/subplot implementation. If this is risky, implement it behind a new dashboard section without modifying existing callbacks.
```

### Codex prompt: figure export

```text
Create scripts/export_figures.py or a documented manual export procedure that saves final report figures into report/figures/. Required figures: dashboard overview, association views, small-multiple overview if implemented, ternary trajectory, structural shift dotplot, data coverage matrix, and use-case screenshots. If fully automated export is hard because the figures depend on Dash state, create report/figures/README.md with exact manual screenshot steps.
```

### GPT prompt: data section rewrite

```text
Rewrite the Data and Task Abstraction section for the final Data Visualization report. Address this feedback: justify why only one tourism indicator is used; separate raw WDI data from project-derived attributes; define derived attributes and formulas; give each attribute one abstract type. Keep it concise, LaTeX-ready, and aligned with Munzner's What/Why/How framework. Return LaTeX only.
```

### GPT prompt: design section rewrite

```text
Rewrite the Final Design section for a Data Visualization final report. Address professor feedback: scatterplots need stronger justification and alternatives; marker size must be removed or justified; color palettes must be justified; choropleth rejection must acknowledge regional-pattern value; ternary plot does not encode tourism directly and should be explained as linked through focus-country selection; streamgraph/line-chart alternatives should be discussed; dotplot clutter should be explained precisely; coverage matrix integration should be explained. Keep it concise and LaTeX-ready. Return LaTeX only.
```

### Claude hostile review prompt

```text
Act as the professor grading this Data Visualization final report. Be strict. Find every place where the report describes what the dashboard does but does not justify why the design is appropriate. Check whether every visual encoding maps to data type and task. Check whether alternatives and trade-offs are discussed. Check whether use cases provide real evidence or just claims. Return a ranked list of actionable fixes only.
```

## Verification protocol

For every AI-generated code patch:

```text
[ ] App starts locally.
[ ] No callback errors.
[ ] Existing views still work.
[ ] New view, if any, responds to global controls.
[ ] Screenshots match report claims.
```

For every AI-generated report section:

```text
[ ] No invented facts.
[ ] Citations exist.
[ ] Claims match dashboard behavior.
[ ] Terminology follows Munzner-style vocabulary.
[ ] Text is shorter, not longer, unless adding required final-report content.
```
