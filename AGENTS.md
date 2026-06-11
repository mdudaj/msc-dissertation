# AGENTS.md

This repository hosts the Kisomo dissertation platform harness for
curriculum-aligned STEM animation and narration experimentation, prototype
review, and feasibility evaluation in Tanzanian primary education.

## Startup Workflow

1. Confirm the working directory with `pwd`.
2. Read this file.
3. Read `docs/PRODUCT.md`, `docs/ARCHITECTURE.md`, and `progress.md`.
4. Run `./init.sh`.
5. Pick exactly one unfinished feature from `feature_list.json`.

## Working Rules

- Work one vertical slice at a time.
- Keep harness setup subordinate to product slices.
- Do not restore curriculum workflows until the baseline auth/harness review is complete.
- Keep auth pages and authenticated app pages on separate CSS entry points.
- Use Viewflow/material conventions before adding bespoke browser-visible UI.
- Preserve generated run artifacts as append-only once domain runs exist.

## Verification

Baseline verification:

```bash
./init.sh
python3 scripts/validate_json.py
```

Browser-visible changes should also verify template rendering and responsive
layout once the dev server is running.
