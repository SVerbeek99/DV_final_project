# Citation and Related Work Plan

## Rules

- Do not fabricate citations.
- Do not cite only course material in related work.
- Related work must explain what is similar/different from your system.
- Use BibTeX.
- Cite data, libraries, papers, dashboards, and any external figures/code.

## Existing citations to keep

The current report already cites:

```bibtex
munzner2014
shneiderman1996
yi2007
wdi
dash
plotly
pandas
numpy
```

Keep these if still used.

## Related work targets to search and cite

Find 3–6 sources/systems. Suggested categories:

### 1. Development indicator dashboards

Search for:

```text
World Bank DataBank World Development Indicators dashboard citation
World Bank World Development Indicators API citation
Gapminder country indicator visualization citation
Our World in Data data explorer citation
```

What to discuss:

- Existing systems support country-indicator exploration.
- Many emphasize maps, time series, or individual indicators.
- Your system focuses specifically on tourism dependence + employment composition + structural shifts + data coverage.

### 2. Tourism and development dashboards / tourism data visualization

Search for:

```text
tourism dashboard international tourism receipts visualization
UN Tourism tourism data dashboard citation
World Travel Tourism Council data dashboard citation
```

What to discuss:

- Tourism dashboards often emphasize arrivals, receipts, expenditure, or geographic flows.
- Your system links tourism dependence to structural employment composition and development indicators.

### 3. Compositional visualization / ternary plots

Search for:

```text
ternary plot compositional data visualization citation
compositional data ternary diagram visualization
```

What to discuss:

- Ternary diagrams are suitable for three-part compositions.
- Limitation: less familiar, weaker for exact reading.
- Your design combines ternary trajectory with hover and structural-shift dotplot.

### 4. Coordinated multiple views / interaction

Possible sources:

- Yi et al. interaction taxonomy.
- Shneiderman information-seeking mantra.
- Munzner VAD.

Course material is acceptable for design theory, but related work should include extra systems/literature.

## Related work section draft skeleton

```latex
\section{Related Work}

Existing development-data tools such as TODO support country-level exploration of socioeconomic indicators through maps, time series, and indicator comparisons. These systems are useful for broad data access, but they generally do not focus on the specific analytical link between tourism dependence and employment-sector composition. Tourism-oriented dashboards such as TODO usually emphasize visitor arrivals, receipts, or geographic demand patterns. Our system instead uses tourism receipts as a dependence indicator and connects it to structural employment and development outcomes.

The visual design also relates to prior work on coordinated multiple views and compositional visualization. Scatterplots are widely used for discovering correlations and outliers between quantitative attributes, while ternary diagrams are appropriate when three values form a constrained composition. However, ternary plots are less familiar and less precise for exact lookup, so our dashboard combines them with hover details and a structural-shift dotplot. Coordinated interaction follows established visualization principles: users move from overview comparison to filtering, focus-country selection, and details on demand.

Compared with existing dashboards, the contribution of \emph{Tourism Structural Explorer} is not a new statistical model, but an integrated visual-analysis workflow for comparing tourism dependence, employment composition, development outcomes, temporal pathways, and data coverage within one linked interface.
```

Replace TODOs with verified citations.

## BibTeX hygiene

Use stable keys:

```text
worldbank_wdi
worldbank_databank
gapminder
gapminder2006
owid_explorer
unwto_dashboard
aitchison1982_compositional
```

Only add keys after verifying source details.

## Citation QA

Before final submission:

```text
[ ] Every \cite{} key exists in references.bib.
[ ] No citations render as [?].
[ ] References are not all course material.
[ ] All external figures/data/code are cited.
[ ] URLs compile correctly.
[ ] BibTeX names render correctly, especially Yi et al.
```
