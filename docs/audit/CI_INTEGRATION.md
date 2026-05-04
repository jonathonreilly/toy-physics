# CI Integration

The audit lane has two integration surfaces: pre-commit (fast, mandatory)
and CI (full, scheduled). Both call into `scripts/`; neither performs
audits — those are done by the current best full Codex GPT model at maximum
reasoning (or any independent auditor) via
`AUDIT_AGENT_PROMPT_TEMPLATE.md`.

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
`bash docs/audit/scripts/run_pipeline.sh` on:

- every pull request that touches `docs/**/*.md`, `docs/audit/scripts/**`,
  `scripts/**/*.py`, `scripts/**/*.sh`, or the workflow file itself,
- a nightly cron at `06:00 UTC` on `main`,
- manual `workflow_dispatch`.

The trigger set is deliberately narrow because this repo has very high
commit volume (hundreds of pushes per day). The nightly cron + the PR
pre-merge gate together still guarantee that `main` never drifts more
than 24 hours from the audit ledger, and never merges drift through a PR.

On `schedule` and `workflow_dispatch` runs the workflow auto-commits the
regenerated audit-data and publication-facing effective-status views back
to `main` (as `audit-bot`, with `[skip ci]` to prevent feedback loops).
PR runs fail if the pipeline produces a diff (no auto-commit; PRs from forks
would not have write permission anyway, and PR authors should commit the
regenerated files themselves before requesting review).

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

## Codex audit invocation

The audit pipeline does not invoke Codex itself; that is the auditor's
loop. The implemented driver is
[`scripts/codex_audit_runner.py`](../../scripts/codex_audit_runner.py),
which uses Codex CLI in non-interactive mode (charged to the local
ChatGPT subscription, no per-call API billing).

```bash
# Audit the top 5 ready-with-clean-deps rows from the queue; auto-propagate
# downstream pipeline effects after each verdict applies:
python3 scripts/codex_audit_runner.py --n 5

# Restrict to one criticality tier:
python3 scripts/codex_audit_runner.py --n 10 --criticality critical

# Skip running each row's primary runner (faster, but the auditor sees an
# empty stdout block and may return chain_closes=false where it would
# otherwise verify):
python3 scripts/codex_audit_runner.py --n 20 --no-runner

# Apply many verdicts in a batch without per-verdict propagation, then
# refresh the pipeline once at the end:
python3 scripts/codex_audit_runner.py --n 50 --no-propagate
bash docs/audit/scripts/run_pipeline.sh

# Dry-run: render prompts but do not call codex or apply_audit:
python3 scripts/codex_audit_runner.py --n 5 --dry-run
```

The runner enforces the audit lane's rules:

- **Fresh-look metadata.** Every verdict it applies records the exact
  selected `auditor_family`, for example `codex-gpt-5.6`; independence is set
  per row: first-pass Claude/human-authored rows are `cross_family`, while
  same-family second passes are `fresh_context`.
- **Auto-updating model policy.** The runner selects the first full GPT model
  with `xhigh` reasoning from Codex's local model cache, so a newer frontier
  GPT is adopted automatically after Codex refreshes its cache. A stale
  `CODEX_AUDIT_MODEL` value is reported and ignored when the cache exposes a
  newer best model. If `CODEX_AUDIT_MODEL` names a newer GPT than the local
  cache knows about, the runner uses it and records that exact family.
  `CODEX_AUDIT_FORCE_MODEL` is the explicit break-glass override.
- **Restricted inputs.** Each `codex exec` runs in an isolated empty
  workdir under `/tmp/codex-audit-isolated/<run-id>/` with
  `--skip-git-repo-check`, so Codex sees ONLY the prompt content (the
  source note, its one-hop cited authorities, and the row's primary
  runner stdout) and not the broader repo.
- **Schema-validated.** Verdicts are JSON-parsed against the prompt
  template's required fields (`verdict`, `claim_type`, `claim_scope`,
  `load_bearing_step_class`, etc.) before being passed to
  `apply_audit.py`. Malformed responses are logged and skipped.
- **Auditable trail.** Every run writes a JSONL log to
  `logs/codex-audit-runs/run-<utc>-<run-id>.jsonl` with per-row phase
  (`applied`, `codex_failed`, `extract_failed`, `json_parse_failed`,
  `validate_failed`, `apply_failed`).

`apply_audit.py`'s built-in propagation slice runs after each successful
write, so the pipeline stays consistent without a separate refresh step
unless `--no-propagate` is used.

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
