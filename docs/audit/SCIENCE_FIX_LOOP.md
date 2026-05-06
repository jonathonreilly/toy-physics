# Science-Fix Loop

**Status:** automation for closing missing-derivation rows via Codex CLI.

## What this is

`scripts/science_fix_loop.py` reads `docs/audit/MISSING_DERIVATION_PROMPTS.md`
and, for each row that hasn't been attempted yet, drives Codex GPT-5.5
(at xhigh reasoning) to attempt closing the chain and opens a PR for
human review and re-audit.

Designed to chip through the medium-difficulty backlog autonomously
while leaving the hard problems for a human. The loop only makes
candidate PRs. Those PRs still require review-loop before landing, and
the independent audit lane verifies correctness after merge.

## Mechanics

For each prompt the loop:

1. Creates a clean worktree off `origin/main` on a new branch
   (`claude/science-fix/<claim-slug>-<run-id>`)
2. Runs `codex exec -C <worktree> -s workspace-write -m gpt-5.5
   --config model_reasoning_effort=xhigh "<prompt body>"`
3. After codex returns:
   - If no edits were made (codex punted) → record `no_edits`, move on
   - If timeout → record `timeout`, move on
   - If edits were made → commit, push, `gh pr create`, record
     `pr_opened` with the PR URL
4. State is persisted to `logs/science-fix-state.json`, so the same
   row is not re-attempted unless `--retry-failed` is passed

## State file

```json
{
  "attempts": {
    "<claim_id>": {
      "attempted_at": "2026-05-06T...",
      "outcome": "pr_opened" | "no_edits" | "timeout" | "codex_failed" | "push_failed" | "pr_failed" | "error",
      "elapsed_sec": 248.3,
      "category": "renaming",
      "descendants": 435,
      "branch": "claude/science-fix/...",
      "pr_url": "https://github.com/.../pull/N"
    }
  }
}
```

The loop never auto-merges. Every successful attempt produces a PR
that must be reviewed and either landed through the normal review-loop
path or closed. After merge, the pipeline queues the changed row and the
independent audit lane picks it up in a later audit run.

## Commands

```bash
# Try the next 5 prompts (sorted by leverage within category)
python3 scripts/science_fix_loop.py --n 5

# Dry-run: show targets without invoking codex
python3 scripts/science_fix_loop.py --n 10 --dry-run

# Restrict to one category
python3 scripts/science_fix_loop.py --n 5 --category renaming
python3 scripts/science_fix_loop.py --n 5 --category failed
python3 scripts/science_fix_loop.py --n 5 --category numerical_match
python3 scripts/science_fix_loop.py --n 5 --category open_gate

# Try a specific row
python3 scripts/science_fix_loop.py --claim-id <claim_id>

# Re-attempt rows that previously timed out / errored / punted
# (skips only rows that successfully opened a PR)
python3 scripts/science_fix_loop.py --n 5 --retry-failed

# Tighter timeout for exploratory runs
python3 scripts/science_fix_loop.py --n 5 --codex-timeout-sec 600
```

## Safety properties

- **Worktree isolation.** Every attempt runs in a fresh worktree under
  `/tmp/science-fix-worktrees/`. Failures never affect main or other
  audit operations.
- **Sandbox.** `codex exec -s workspace-write` lets codex edit files
  in the worktree but does not give it broader system access.
- **No auto-merge.** Successful attempts open PRs; humans review.
- **Per-row idempotence.** State file prevents re-attempting the same
  row until `--retry-failed` is passed.
- **Per-attempt timeout.** Default 15 min; codex is killed if it
  exceeds that.

## Failure modes & what to do

| Outcome | Meaning | Action |
|---|---|---|
| `pr_opened` | Codex made edits, PR exists | Run review-loop on the PR; land or close |
| `no_edits` | Codex punted — couldn't see how to close | This row is hard; either revise the note manually or accept the verdict |
| `timeout` | Codex didn't finish in budget | Try `--retry-failed` with longer `--codex-timeout-sec`, or skip |
| `codex_failed` | Codex crashed / returncode != 0 | Read the stderr in the state file; usually transient |
| `push_failed` | Codex made edits but git push failed | Check `logs/science-fix-runs/*.jsonl` for details |
| `pr_failed` | Push succeeded but gh pr create failed | Branch is on remote; open PR manually |
| `error` | Loop-level error (worktree creation, etc.) | Check the run log under `logs/science-fix-runs/` |

## Relationship to other loops

- **`physics-loop` skill** (Codex skill in `~/.codex/skills/physics-loop`):
  the user-driven version of the same idea. The science-fix loop is
  the autonomous wrapper.
- **`audit-loop` skill** (Codex skill, `~/.codex/skills/audit-loop`):
  audits claims after they're written. The science-fix loop produces
  PRs that the audit-loop will then check.
- **`codex_audit_runner.py`**: same auditor (Codex GPT-5.5 at xhigh)
  but reads-only. Reads cached runner output and renders verdicts.
- **`compute_reaudit_candidates.py`**: when a science-fix PR merges
  and the upstream's audit changes, downstream rows show up here for
  re-audit via `codex_audit_runner.py --from-reaudit-candidates`.

The full loop:

1. `science_fix_loop.py` opens PR with new derivation
2. Human/review-loop reviews + lands or closes the PR
3. Pipeline regenerates (note hash drifts → seed_audit_ledger archives
   the prior verdict, resets to `unaudited`)
4. `codex_audit_runner.py --n 1` re-audits this specific row (via
   normal queue or `--from-reaudit-candidates` for downstream cascade)
