# Use Cases and Evaluation Plan

The final report must include use cases/results. This is not optional. These use cases should show how the dashboard helps answer non-trivial questions that are not easily solved by a single statistic.

## Rules

1. Do not invent findings.
2. Use the actual dashboard and data.
3. Each use case must connect back to tasks.
4. Each use case must explain the interaction path.
5. Each use case must explain why visualization helped.
6. Each use case must mention limitations or data reliability when relevant.

## Use case template

```latex
\subsection{Use Case X: <title>}

\textbf{Question.} <What the user wants to investigate.>

\textbf{Interaction path.} <Which controls/views were used, in order.>

\textbf{Observation.} <Concrete observation from the dashboard. Include country names, directions of change, outliers, or patterns.>

\textbf{Why visualization was needed.} <Explain why this required linked views, comparison, trajectory, or coverage inspection.>

\textbf{Limitations.} <Missing data, latest-available mode, non-causal interpretation, limited country set, etc.>
```

## Use Case 1 — Tourism dependence and employment pathway

### Goal
Show how a user can move from cross-country association to a single-country temporal pathway and then to a cross-country structural-shift comparison.

### Task mapping

```text
T1: Discover correlation between tourism dependence and employment composition.
T4: Identify trend for one country over time.
T5: Compare structural changes across countries.
```

### Suggested question

```text
Do tourism-dependent countries show a more service-oriented employment structure, and does a selected country move toward services over time?
```

### Interaction path

```text
1. Select comparison year.
2. Select services employment as employment variable.
3. Inspect tourism vs services scatterplot.
4. Click a focus country, e.g., Thailand or another visible case.
5. Inspect ternary trajectory.
6. Inspect structural-shift dotplot to compare first-to-latest changes across countries.
```

### What to record

- Which countries are high/low tourism dependence in the selected year.
- Whether high-tourism countries have higher services employment in the scatterplot.
- Whether the focus country's ternary trajectory moves toward services, industry, or agriculture.
- Whether the structural-shift dotplot confirms a services increase or agriculture decrease.

### Draft language with TODOs

```latex
In the first use case, the user investigates whether tourism dependence is associated with service-sector employment. The interaction starts in the tourism--employment scatterplot, where countries are positioned by tourism receipts on the horizontal axis and services employment on the vertical axis. After identifying TODO as an interesting case, the user selects it as the focus country. The ternary trajectory then shows that TODO. The structural-shift dotplot confirms that TODO. This workflow cannot be replaced by a single correlation coefficient because the scatterplot shows cross-country outliers, the ternary plot shows the pathway through the three-part employment composition, and the dotplot summarizes comparable first-to-latest changes across countries.
```

Fill TODOs from actual dashboard observations.

## Use Case 2 — Development indicator comparison and data reliability

### Goal
Show how the dashboard prevents overinterpretation by combining tourism-development comparison with data coverage inspection.

### Task mapping

```text
T2: Discover correlation between tourism dependence and development indicators.
T3: Compare distributions across regions.
S1: Summarize data availability before interpretation.
```

### Suggested question

```text
Does tourism dependence appear related to poverty or inequality, and is the comparison reliable enough to interpret?
```

### Interaction path

```text
1. Select poverty headcount or Gini index as development outcome.
2. Inspect tourism-development scatterplot.
3. Compare regional colors and outliers.
4. Toggle exact selected year vs latest available mode if available.
5. Inspect data coverage matrix for tourism, poverty, inequality, and employment indicators.
```

### What to record

- Whether poverty/Gini data are missing for some countries.
- Whether latest-available mode increases visible points compared with exact-year mode.
- Whether apparent patterns are driven by sparse data.
- Which countries/indicators have lower coverage.

### Draft language with TODOs

```latex
The second use case examines whether a tourism--development relationship is trustworthy when coverage differs across indicators. The user selects TODO as the development outcome and compares it against tourism dependence. The scatterplot suggests TODO, but the coverage matrix shows that TODO has lower availability for TODO countries/indicators. This changes the interpretation: the view supports hypothesis generation, but the user should not treat the visible pattern as a robust conclusion without considering missingness.
```

Fill TODOs from actual dashboard observations.

## Use Case 3 — Optional regional pattern use case

Use only if page budget allows.

### Suggested question

```text
Do regional groups cluster differently in tourism-employment or tourism-development space?
```

### Views

- Association scatterplots with region hue.
- Optional choropleth-related discussion if map not used.
- Structural shift dotplot.

### Use only if it produces a clear observation.

## Evaluation section structure

```latex
\section{Use Cases and Evaluation}

The system was evaluated through task-based use cases rather than a formal user study. Each use case starts from one of the domain tasks and records how the coordinated views support the analysis.

\subsection{Use Case 1: Tourism Dependence and Employment Pathway}
...

\subsection{Use Case 2: Development Indicators and Data Reliability}
...

\subsection{Summary of Findings}
The use cases show that the coordinated views support transitions from overview comparison to focus-country pathway inspection and reliability checking. They also reveal limitations: the analysis remains exploratory, the selected tourism indicator is only one proxy for tourism dependence, and missing WDI values can affect interpretation.
```

## Evidence quality scale

Use this internal scale when drafting:

```text
Strong observation: visible in at least two coordinated views.
Moderate observation: visible in one view and plausible, but needs caution.
Weak observation: not clearly visible; do not include.
```
