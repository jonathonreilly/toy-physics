# CI Integration

The audit lane has two integration surfaces: pre-commit (fast, mandatory)
and CI (full, scheduled). Both call into `scripts/`; neither performs
audits — those are done by Codex GPT-5.5 (or any independent auditor)
via `AUDIT_AGENT_PROMPT_TEMPLATE.md`.

## Pre-commit

Runs `build_citation_graph.py` + `seed_audit_ledger.py` + `audit_lint.py`
only. Fast. Catches:

- New note added without a ledger seed.
- Hash drift on an audited claim (note edited after audit landed).
- Hard-rule violation (author-declared `retained`, missing auditor on
  `audited_clean`, etc.).

Install (one-time, per local clone — git hooks are not version-controlled):

```bash
bash scripts/setup_audit_hooks.sh
```

The setup script resolves the correct hooks directory (handles main worktree
and secondary worktrees via `git rev-parse --git-path hooks`) and installs
a symlink to `docs/audit/scripts/pre_commit_audit_check.sh`. Uninstall with
`bash scripts/setup_audit_hooks.sh --uninstall`.

## CI (full pipeline)

The workflow file is provided as a TEMPLATE at
[`docs/audit/templates/audit_workflow.yml`](templates/audit_workflow.yml).
It must be installed manually by a user with `workflow` token scope (see
[`docs/audit/templates/README.md`](templates/README.md)). The bot/OAuth
account used for automated commits does not have permission to create
files under `.github/workflows/`.

After install (one-time), `.github/workflows/audit.yml` runs
`bash docs/audit/scripts/run_pipeline.sh` plus
`python3 docs/audit/scripts/render_publication_effective_status.py` on:

- every push to `main` and `audit-lane`,
- every pull request,
- a daily cron at `06:00 UTC`,
- manual `workflow_dispatch`.

On `main` pushes and scheduled runs the workflow auto-commits the regenerated
audit-data and publication-facing effective-status views back to the branch
(committed as `audit-bot`), so the publication surface can never silently
drift from the audit ledger. PR runs surface a diff warning (no auto-commit).

The full pipeline adds:

- `classify_runner_passes.py` — heuristic A/B/C/D classifier.
- `compute_load_bearing.py` — transitive descendants, criticality tier
  (topology only; the audit lane does not use author-declared flagship status).
- `invalidate_stale_audits.py` — auto-archives audits where deps changed
  or criticality bumped.
- `compute_audit_queue.py` — sorted next-up queue.
- `render_audit_ledger.py` — markdown render.

A minimal GitHub Actions workflow (drop into `.github/workflows/audit.yml`):

```yaml
name: audit-lane
on:
  push:
    branches: [main, audit-lane]
  pull_request:
  schedule:
    - cron: "0 6 * * *"   # daily 06:00 UTC

jobs:
  audit_pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Run audit pipeline
        run: bash docs/audit/scripts/run_pipeline.sh
      - name: Commit refreshed ledger if changed
        if: github.event_name == 'schedule' || github.ref == 'refs/heads/main'
        run: |
          if [[ -n "$(git status --porcelain docs/audit/data docs/audit/AUDIT_LEDGER.md docs/audit/AUDIT_QUEUE.md)" ]]; then
            git config user.name  "audit-bot"
            git config user.email "audit-bot@local"
            git add docs/audit/data docs/audit/AUDIT_LEDGER.md docs/audit/AUDIT_QUEUE.md
            git commit -m "audit: refresh ledger + queue (automated)"
            git push
          fi
      - name: Upload audit queue artifact
        uses: actions/upload-artifact@v4
        with:
          name: audit-queue
          path: docs/audit/data/audit_queue.json
```

## Codex audit invocation (recommended pattern)

The pipeline does not invoke Codex itself. Recommended pattern: a
separate workflow (manual trigger or scheduled) reads the top of
`data/audit_queue.json`, constructs the prompt from
`AUDIT_AGENT_PROMPT_TEMPLATE.md`, sends it to Codex, captures the JSON
response, and pipes it through `apply_audit.py`. Steps:

```bash
# Pseudocode for the wrapper script (not yet implemented):
top_n=10
python3 docs/audit/scripts/build_audit_prompts.py --top "${top_n}" \
    > /tmp/prompts.jsonl

while read -r prompt; do
    response=$(call_codex_api "${prompt}")
    echo "${response}" | python3 docs/audit/scripts/apply_audit.py
done < /tmp/prompts.jsonl

bash docs/audit/scripts/run_pipeline.sh
```

The Codex invocation itself depends on which transport you use; the
audit lane is transport-agnostic — anything that returns the prompt
template's JSON schema is acceptable.

## Reading the artifacts

After a pipeline run, four files are the canonical output:

| File | Purpose |
|---|---|
| `docs/audit/AUDIT_LEDGER.md` | Human-readable rendered ledger; effective_status table; per-claim audit findings. |
| `docs/audit/AUDIT_QUEUE.md` | Top-50 next-to-audit claims, sorted by criticality. |
| `docs/audit/data/audit_ledger.json` | Source of truth (machine-readable). |
| `docs/audit/data/audit_queue.json` | Full pending queue. |

Publication-facing tables (`CLAIMS_TABLE.md`, `PUBLICATION_MATRIX.md`,
`ARXIV_DRAFT.md`) should read `effective_status` from
`audit_ledger.json` (or an artifact derived from it).
