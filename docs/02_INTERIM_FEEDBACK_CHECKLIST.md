# Interim Feedback Repair Checklist

This checklist is derived from the professor's PDF annotations. Treat it as the master list. Do not mark an item DONE until both code/report changes are completed and manually inspected.

## Legend

Status values:

```text
TODO      not started
DOING     in progress
DONE      fixed and checked
LIMITATION deliberately not implemented; explained in report
```

## Data and abstraction feedback

| ID | Area | Professor comment | Required fix | Acceptance criteria | Status |
|---|---|---|---|---|---|
| D1 | Tourism indicator | “It would be helpful to justify why only a single tourism indicator is used given that tourism dependence could be captured in multiple ways.” | Add a paragraph justifying international tourism receipts as % of exports. Discuss alternatives such as raw receipts or arrivals and state limitation. | Data section clearly explains why this indicator was selected and what it does not capture. | TODO |
| D2 | Data vs design | “Mixes data characteristics with design decisions. It's unclear whether the derivations (e.g., averaging male/female employment) are inherent to the dataset or choices made by you, so this could be clarified.” | Split raw WDI variables from project-derived attributes. | Separate subsection `Derived Attributes and Data Processing`; clear distinction between WDI fields and dashboard-derived fields. | TODO |
| D3 | Derived attributes | “The derived attributes are not sufficiently explained. It is unclear why they are necessary and exactly how they are computed.” | Add formulas/definitions for latest-available value, data coverage, structural shift, and gender-average if used. | Report contains precise definitions and formulas; no ambiguity about computation. | TODO |
| D4 | Abstraction types | “Some data types are ambiguously specified (e.g., quantitative or ordinal), but each attribute should have a single, clearly defined abstraction type.” | Revise data abstraction table so each attribute has one abstract type only. | No table cell says “or”; coverage is either quantitative sequential or ordinal depending on implementation. | TODO |

## Task feedback

| ID | Area | Professor comment | Required fix | Acceptance criteria | Status |
|---|---|---|---|---|---|
| T1 | Task organization | “The task structure needs to be better organized. Right now, spatial (cross-country), temporal (over time), and single-country analyses are mixed together, which makes it hard to follow. The high-level tasks should map more clearly to the mid-level tasks.” | Reorganize domain tasks by analytical perspective: cross-country association, development comparison, regional comparison, temporal pathway, structural change, reliability support. | Tasks are grouped logically and map from high-level goal to task table. | TODO |
| T2 | Reliability task | “It’s unclear why data reliability checks are treated as a mid-level analytical task alongside the others. Tasks like comparing countries or analyzing trends are core analytical goals, whereas checking for missing or substituted values is more of a supporting or validation step.” | Reframe data reliability as supporting validation task S1, not a core analytical goal. | Task table labels reliability as supporting task; design section explains it supports interpretation. | TODO |
| T3 | Action-target pairs | “Per task, there should be a single action target pair.” | Revise task abstraction table to one action + one target per task. | Each row has exactly one action and one target. | TODO |

## Visual encoding / interaction feedback

| ID | Area | Professor comment | Required fix | Acceptance criteria | Status |
|---|---|---|---|---|---|
| V1 | Variable comparison | “Only one employment or development indicator can be compared against the tourism indicator at a time. Users cannot directly compare relationships across variables and must rely on memory.” | Preferably add small-multiple association overview. If not feasible, explicitly document limitation and future work. | Either working small multiples exist, or limitation is explicitly discussed. | TODO |
| V2 | Color palette | “How was the color palette chosen?” | Use fixed colorblind-aware categorical palettes for region/sector and justify. | Palette constants in code; report explains hue for categorical attributes and fixed mapping across views. | TODO |
| V3 | Choropleth tradeoff | “The reasoning behind the rejection of a choropleth should be further reflected upon, as it could still support T3 by revealing regional patterns, even if adjacency is not central.” | Rewrite choropleth paragraph honestly: useful for broad regional geography, rejected as primary view because comparison/trajectory tasks dominate. | Design alternatives paragraph acknowledges what map would support and why it was not primary. | TODO |
| V4 | Marker size | “Should justify why include it at all? Does it support a specific task?” | Remove marker size or justify exactly. Preferred: make marker size constant and move extra values to hover. | No unexplained marker size; report says constant size avoids implying third variable importance. | TODO |
| V5 | Scatterplot justification | “The scatterplot choice generally fits the task... but justification is incomplete... alternatives not properly evaluated... overplotting not discussed... link to T1/T2 should be explicit.” | Strengthen scatterplot design section. Discuss why scatterplots, alternatives, overplotting, trend line limits, small multiples, mapping to T1/T2. | Section explicitly states scatterplots support T1/T2, why position is used, why size is limited/removed, and what alternatives/tradeoffs exist. | TODO |
| V6 | Ternary axes | “The axis labeling in the ternary plot is unclear. Since the data represents a three-part composition that should sum to 100%, the axes would normally follow a consistent 0–100 scale.” | Fix Plotly ternary labels/ticks/hover. | Ternary figure is understandable as a 100% composition; hover shows exact sector shares. | TODO |
| V7 | Tourism not encoded | “But there is no tourism encoding here so its unclear how.” | Stop claiming ternary alone supports tourism hypothesis. Explain it is linked to tourism scatterplots via focus-country selection, or encode tourism explicitly. Preferred: linked-view explanation. | Report says ternary does not directly encode tourism; it supports follow-up inspection after scatterplot selection. | TODO |
| V8 | Ternary alternatives | “What other alternatives (e.g., streamgraph) were considered?” | Add alternatives paragraph: line chart, stacked area/streamgraph, ternary tradeoff. | Design section evaluates alternatives and explains why ternary + dotplot combination was chosen. | TODO |
| V9 | Single-country trajectory | “Trajectory view only shows one country at a time... prevents direct comparison of structural changes between countries...” | Explain limitation and companion structural-shift view; optionally add multi-country trajectory if feasible. | Report explicitly says one-country trajectory prevents direct trajectory comparison and dotplot compensates for cross-country change comparison. | TODO |
| V10 | Dotplot clutter | “The reasoning is valid, but the notion of ‘clutter’ is not sufficiently explained.” | Explain grouped/stacked bar clutter: too many bars, unaligned baselines, inappropriate for signed change around zero. | Dotplot paragraph explains shared zero axis and signed changes. | TODO |
| V11 | Coverage matrix | “Missing sketch/mock-up. Is this to be integrated with the other views?” | Include screenshot/mock-up of coverage matrix and explain it uses same selected countries/indicators. If not implemented, mark as limitation. | Figure included or limitation documented; integration with selections explained. | TODO |

## Existing report polish issues to fix while rewriting

| ID | Issue | Fix | Status |
|---|---|---|---|
| P1 | Figure 1 floats into middle of “reasons.” | Move figure environment or paragraph. | TODO |
| P2 | “male, female and, total” grammar error. | Use “male, female, and total.” | TODO |
| P3 | “Fig. 1” style inconsistent. | Use `\autoref{...}` consistently. | TODO |
| P4 | Figure captions are incomplete sentences or vague. | Rewrite captions to be self-contained. | TODO |
| P5 | “year observation” wording. | Use “country--year observation.” | TODO |
| P6 | Current report has no final-report use cases. | Add use cases/results section. | TODO |
| P7 | Current report has no related work section. | Add required related work. | TODO |
| P8 | Current report has no conclusion/future work. | Add conclusion/future work. | TODO |
| P9 | Current report does not document changes from interim. | Add change-log table. | TODO |
