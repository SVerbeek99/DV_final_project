# Final QA and Submission Checklist

Run this checklist after code and report are complete.

## Report compile

```text
[ ] main.tex compiles without errors.
[ ] No [?] citations.
[ ] No ?? references.
[ ] references.bib is included.
[ ] Final PDF opens correctly.
[ ] Final report within page limit.
[ ] References are excluded from page count if required.
```

## Report content

```text
[ ] Abstract summarizes motivation, design, interaction, use cases, and limitation.
[ ] Introduction defines users, problem, goal, and why visualization is appropriate.
[ ] Related work section exists and uses non-course references.
[ ] Data section separates raw WDI variables from derived attributes.
[ ] Tourism indicator is justified.
[ ] Derived attributes are precisely defined.
[ ] Data abstraction table has one type per attribute.
[ ] Task analysis is organized by analytical perspective.
[ ] Data reliability is framed as supporting validation task.
[ ] Task abstraction table has exactly one action-target pair per task.
[ ] Design section maps each view to tasks.
[ ] Scatterplots discuss alternatives/trade-offs and overplotting/size limitations.
[ ] Color palette choices are justified.
[ ] Choropleth trade-off is discussed honestly.
[ ] Ternary plot section clarifies tourism is not directly encoded.
[ ] Ternary alternatives such as line chart and streamgraph are discussed.
[ ] Dotplot clutter explanation is precise.
[ ] Coverage matrix integration is explained.
[ ] Use cases/results section contains real observations from the dashboard.
[ ] Implementation/reproducibility section is practical.
[ ] Changes after interim feedback are documented.
[ ] Conclusion and future work exist.
```

## Figures

```text
[ ] Every figure file exists.
[ ] Figures are high resolution.
[ ] Figures are readable at report size.
[ ] Every figure has a caption.
[ ] Every figure has a label.
[ ] Every figure is referenced in text.
[ ] No figure interrupts a sentence.
[ ] Captions describe what the reader sees.
[ ] Ternary axis labels are understandable.
[ ] Coverage matrix screenshot/mock-up appears or limitation is documented.
```

## Code reproducibility

From a clean clone:

```text
[ ] Create virtual environment.
[ ] Install requirements.
[ ] Run app.
[ ] Dashboard loads in browser.
[ ] Data files are found.
[ ] No callback errors in terminal.
[ ] README instructions match actual commands.
[ ] Known limitations documented.
```

## Screencast

```text
[ ] 3–5 minutes long.
[ ] Shows interaction solving tasks.
[ ] Does not just read the report.
[ ] Includes voice-over or clear annotations.
[ ] Both group members participate.
[ ] Shows at least one use case.
[ ] Shows filtering/selection/linked views/details.
[ ] Mentions limitations/future work.
```

## AI and provenance

```text
[ ] docs/ai_usage.md exists.
[ ] All Codex/GPT/Claude usage documented.
[ ] AI-generated code/text manually verified.
[ ] External code/data/sources cited.
[ ] Figures from dashboard are own figures; external figures cited if any.
```

## Final submission package

```text
[ ] Final PDF.
[ ] GitHub repository link or required source-code upload.
[ ] Overleaf link if required.
[ ] Screencast/video.
[ ] README with run instructions.
[ ] Optional individual contribution reports if work division was imbalanced.
```

## Last 15-minute sanity pass

Open the final PDF and scan only for visible issues:

```text
[ ] Page 1 looks professional.
[ ] Tables are not cut off.
[ ] Figures are not blurry.
[ ] No weird LaTeX overflows.
[ ] No repeated paragraphs.
[ ] No old “interim” wording unless intentionally discussing changes.
[ ] No grammar issue in captions.
[ ] Title, authors, student IDs correct.
```
