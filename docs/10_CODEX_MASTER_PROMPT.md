# One-Shot Master Prompt for Codex

Use this prompt after placing all planning markdown files in the repository.

```text
You are helping prepare the final submission for a Data Visualization course project. Read the markdown files in docs/ or the root planning folder in this order:

1. 00_START_HERE_FOR_CODEX.md
2. 01_REQUIREMENTS_AND_DELIVERABLES.md
3. 02_INTERIM_FEEDBACK_CHECKLIST.md
4. 03_REPORT_REWRITE_SPEC.md
5. 04_CODE_CHANGE_TASKS.md
6. 05_FIGURE_SCREENSHOT_PLAN.md
7. 06_USE_CASE_EVALUATION_PLAN.md
8. 07_CITATION_RELATED_WORK_PLAN.md
9. 08_AI_USAGE_AND_MODEL_WORKFLOW.md
10. 09_FINAL_QA_SUBMISSION_CHECKLIST.md

Your job is to create an initial draft/setup, not the final human-approved submission.

Work in phases:

PHASE 1 — Inspect repository and report current structure. Do not change files yet.
PHASE 2 — Make the app reproducible: README, requirements, paths.
PHASE 3 — Implement safe code fixes: constant scatterplot marker size, fixed palettes, ternary labels/hover, coverage matrix integration check. Add small multiples only if low risk.
PHASE 4 — Create/organize report files under report/ and prepare figure paths.
PHASE 5 — Draft or restructure main.tex according to the final-report outline. Preserve useful interim content but fix professor feedback. Add TODO markers where real observations/citations need human verification.
PHASE 6 — Update docs/ai_usage.md with what you did.
PHASE 7 — Provide a concise summary of changed files, unresolved TODOs, and commands to run.

Hard rules:
- Do not invent use-case findings.
- Do not fabricate citations.
- Do not remove existing dashboard functionality without explaining why.
- Do not add unexplained visual encodings.
- Keep modifications targeted.
- If uncertain, add TODO comments instead of guessing.

Acceptance:
- App should run with README instructions.
- Report should compile as far as possible.
- All professor feedback items should be addressed, marked TODO, or marked LIMITATION.
```
```

## Expected Codex output

Ask Codex to return:

```text
1. Changed files
2. Summary of implementation changes
3. Summary of report changes
4. Unresolved TODOs requiring human decisions
5. Commands to run
6. Risks or assumptions
```

## Human review after Codex

After Codex finishes:

```text
[ ] Run app.
[ ] Inspect all changed plots.
[ ] Search repository for TODO.
[ ] Confirm no invented findings.
[ ] Confirm related-work citations are real.
[ ] Compile LaTeX.
[ ] Feed PDF back to GPT/Claude for review.
```
