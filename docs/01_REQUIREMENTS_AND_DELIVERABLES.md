# Final Project Requirements and Deliverables

This file summarizes the project requirements that the final report/setup must satisfy.

## Final report requirements

The final report must extend the interim report. It should not be a lightly edited copy.

Required final-report components:

- Abstract.
- Introduction with motivation, users, goal, and why visualization is appropriate.
- Related work. This is optional in the interim report but required in the final report.
- Data Analysis / What: domain data specification and data abstraction.
- Task Analysis / Why: domain tasks and task abstraction.
- Final solution / How: visual encoding, idioms, interactions, alternatives, and design justification.
- Use cases / Results / Evaluation: use the application to make observations about the data and explain how the visualization enabled them.
- Implementation and reproducibility: language, libraries, app file, data files, run instructions, limitations.
- Conclusion and future work.
- References.
- Clear documentation of what changed after the interim report.

## Page budget

Target:

```text
7–8 pages maximum including figures, excluding references.
Around 4 pages of text.
Around 2–3 pages of figures.
```

This means the report must be dense and selective. Do not keep every interim paragraph.

## Source code requirements

The graders should be able to run the project.

README must include:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows alternative if needed
pip install -r requirements.txt
python app/tourism_structural_dashboard_designed.py
```

Also include:

- Python version.
- Required data files and where they should be located.
- Expected local URL.
- How to reproduce figures/screenshots if possible.
- Known limitations.
- What code was written by the team versus provided by libraries/frameworks.

## Screencast requirements

Prepare a 3–5 minute screencast. It should show how interaction helps perform tasks. It should not simply read the report aloud.

Minimum screencast content:

```text
0:00–0:20 Problem and user
0:20–0:50 Dashboard overview
0:50–1:50 Use case 1: tourism → employment pathway
1:50–2:50 Use case 2: tourism → development outcome + data reliability
2:50–3:30 Interaction design: filter, select, connect, details
3:30–4:00 Limitations and future work
```

Both group members should participate equally unless otherwise documented.

## AI usage requirement

AI use must be documented. Use `docs/ai_usage.md`.

Minimum columns:

```markdown
| Date | Tool/model | Prompt summary | Output used | Where used | Human verification |
|---|---|---|---|---|---|
```

Document Codex, GPT, Claude, and any other tools. Include code usage, report rewriting, proofreading, and critique.

## References and figures

- Use BibTeX consistently.
- Cite external text, figures, code, and data.
- Every figure/table must have a number, caption, label, and in-text reference.
- Do not write “the figure below.” Use `\autoref{...}` or “Figure X”.
- Use high-resolution, readable figures.
- Avoid full-width unreadable GUI screenshots unless annotated.

## Individual work report

If the group work was balanced, state that briefly if required by submission. If there was imbalance, prepare separate individual reports up to 300 words each.
