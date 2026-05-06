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