# Landing Instructions: audit-lane → main

**Branch:** `audit-lane`
**Target:** `main`
**Type:** policy + tooling addition + claim-vocabulary migration
**Reversibility:** the relabel step is mechanical and reversible via the
script's regex (run with swapped patterns), but the audit ledger snapshot
becomes the new source of truth once landed.

This document is the full landing checklist. Read it end-to-end before
merging.

---

## 1. What this branch lands

Two distinct layers:

**A. Audit-lane infrastructure** (under `docs/audit/`):

- Policy docs: `README.md`, `FRESH_LOOK_REQUIREMENTS.md`,
  `ALGEBRAIC_DECORATION_POLICY.md`, `AUDIT_AGENT_PROMPT_TEMPLATE.md`,
  `CI_INTEGRATION.md`.
- 9-stage mechanical pipeline in `scripts/`.
- Audit ledger seeded for all 1,601 claim notes, all `unaudited`.
- Topology-only criticality (91 critical / 569 high / 85 medium / 856 leaf).
- Cross-confirmation flow for critical claims; auto-invalidation on
  hash-drift, dep-state change, or criticality bump.

**B. Claim vocabulary migration** (across `docs/*.md`, NOT yet applied
on this branch):

- `**Status:** retained ...` → `**Status:** proposed_retained ...`
- `**Status:** promoted ...` → `**Status:** proposed_promoted ...`
- `flagship closed` → `proposed_retained` (flagship status is no longer
  used by the audit lane; see `ALGEBRAIC_DECORATION_POLICY.md` and the
  rationale in commit `c452b14`)

The migration must be applied as **part of the landing PR**, not before
or after, so the lint check, the ledger, and the source notes are
coherent in a single commit.

---

## 2. Pre-merge checklist

### 2.1 Verify branch state

```bash
git fetch origin main
git checkout audit-lane
git rebase origin/main          # should be a no-op or trivial
bash docs/audit/scripts/run_pipeline.sh
```

The pipeline must report `audit_lint: ... OK: no errors`. The 451
warnings about "Status line contains bare 'retained'" are expected at
this stage — they will become errors after the relabel step (next).

### 2.2 Apply the claim-vocabulary relabel

This step touches ~454 notes mechanically. Always run dry-run first.

```bash
# Preview every change.
python3 docs/audit/scripts/relabel_status_lines.py --dry-run | less

# Sanity-check: the only changes should be inside `**Status:**` /
# `Status:` lines. If you see anything outside a Status line, STOP and
# investigate before applying.

# Apply.
python3 docs/audit/scripts/relabel_status_lines.py
```

The script:

- Touches **only** the `**Status:** ...` line (or `Status: ...`).
- Leaves body text alone (the words "retained", "promoted", and
  "flagship" appear throughout normal prose and must not be rewritten).
- Is idempotent (rerunning is a no-op).

### 2.3 Re-run the pipeline in strict mode

```bash
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict   # MUST pass
```

What happens behind the scenes:

- `seed_audit_ledger.py` detects note-hash drift on every relabeled note
  and resets `audit_status` to `unaudited` (correct: the relabel is a
  meaningful change to the source surface).
- `compute_load_bearing.py` recomputes (no change expected).
- `audit_lint.py --strict` enforces that no source note's Status line
  contains bare `retained` or `promoted`. After the relabel this must
  pass with zero errors.

### 2.4 Stage and commit

```bash
git add docs/                                 # the relabeled notes
git add docs/audit/data/audit_ledger.json     # refreshed hashes
git add docs/audit/data/citation_graph.json
git add docs/audit/AUDIT_LEDGER.md
git add docs/audit/AUDIT_QUEUE.md
git status                                    # review

git commit -m "audit: relabel author-declared retained/promoted to proposed_*

Mechanical relabel of ~454 source-note Status lines from the legacy
author-declared tier vocabulary to the audit-lane's propose / ratify
vocabulary. Body text untouched.

After this commit, retained / promoted may only be granted by the audit
lane via audit_status=audited_clean; authors declare proposed_retained
or proposed_promoted as the strongest self-assigned tier."
```

### 2.5 Final verification

```bash
bash docs/audit/scripts/run_pipeline.sh
python3 docs/audit/scripts/audit_lint.py --strict   # zero errors
```

---

## 3. Merge

Open a PR from `audit-lane` to `main`. The PR description should include:

- Link to this file.
- Link to `docs/audit/README.md`.
- Snapshot of the criticality distribution from `AUDIT_LEDGER.md`.
- The "what this does NOT do" section (next).

Squash-merge or rebase-merge as your repo prefers. Preserve the four
audit-lane commits if the team wants the design evolution visible
(scaffold → propose/ratify split → load-bearing → drop-flagship).

---

## 4. What this PR does NOT do

These are deliberately deferred to follow-on work:

1. **Codex wrapper.** The prompt template exists; the script that POSTs
   to Codex GPT-5.5 and pipes responses through `apply_audit.py` is
   pseudocode in `CI_INTEGRATION.md`. First audit will be done with a
   manually-constructed prompt.

2. **Audit any claim.** The ledger ships with zero audits applied. Every
   row is `unaudited`. No claim has `effective_status = retained` or
   `effective_status = promoted`. The first audits will be done by Codex
   from the top of `AUDIT_QUEUE.md`.

3. **Update publication-facing tables.** `CLAIMS_TABLE.md`,
   `PUBLICATION_MATRIX.md`, and `ARXIV_DRAFT.md` continue to render
   what the source notes declare. After the relabel they will read
   `proposed_retained` instead of `retained`. This is correct and
   honest — those tables now publicly reflect the unratified state.
   A future PR may add a renderer that pulls `effective_status` from
   the audit ledger, or insert a banner pointing readers to
   `AUDIT_LEDGER.md`.

4. **Filter `unknown` notes from the queue.** 985 of 1601 ledger rows
   have no parseable Status line (mostly README-style overview notes).
   They show as `unknown` and clutter the queue. Removing them from the
   ledger is a follow-on refinement.

5. **Install the pre-commit hook automatically.** Each developer must
   run the install command in §6.

---

## 5. Post-merge: install local + CI hooks

### 5.1 Pre-commit hook (per developer)

```bash
ln -sf ../../docs/audit/scripts/pre_commit_audit_check.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Catches: new note added without ledger seed, hash drift on an audited
claim, hard-rule violation. Fast (a few seconds).

### 5.2 CI workflow

Drop the YAML stub from `docs/audit/CI_INTEGRATION.md` into
`.github/workflows/audit.yml` and enable. The workflow runs the full
pipeline on push to `main`, on PRs, and daily; commits a refreshed
ledger and queue back to `main` on the cron schedule.

Set `AUDIT_LINT_STRICT_RAW=1` in the workflow environment so CI fails
on any future regression that re-introduces bare `retained` /
`promoted` in a Status line.

### 5.3 First audit batch

Pull the top of `docs/audit/data/audit_queue.json` and run Codex on
each entry using `AUDIT_AGENT_PROMPT_TEMPLATE.md`. Suggested first
batch (highest-leverage critical claims):

- `ckm_cp_phase_structural_identity_theorem_note_2026-04-24`
- `wolfenstein_lambda_a_structural_identities_theorem_note_2026-04-24`
- `alpha_s_derived_note`
- `observable_principle_from_axiom_note` (the hierarchy theorem)
- `ckm_atlas_axiom_closure_note`
- `three_generation_structure_note`
- `minimal_axioms_2026-04-11`
- `yt_ward_identity_derivation_theorem`
- `graph_first_su3_integration_note`
- `left_handed_charge_matching_note`

These ten roots gate the bulk of the package. Auditing them resolves
`effective_status` for hundreds of downstream claims by inheritance.

Each requires cross-confirmation by a second auditor (Codex + Claude
or Codex + human) before `audited_clean` lands.

---

## 6. Rollback

If something goes wrong post-merge:

1. **Reverting the audit-lane infrastructure** (`docs/audit/`): safe.
   Just `git revert` the merge commit; nothing else in the repo
   depends on the audit lane.
2. **Reverting the relabel** is mechanical:
   ```bash
   # Add a one-line patch to relabel_status_lines.py that swaps the
   # patterns (proposed_retained -> retained, etc.) and run.
   ```
   Or `git revert` the relabel commit. Both work.

The audit ledger JSON files are derived state. They can always be
regenerated from the source notes via `run_pipeline.sh`.

---

## 7. After landing: what changes for contributors

- **No more author-declared `retained`.** The strongest tier you can
  self-assign is `proposed_retained`. The audit lane (Codex GPT-5.5 by
  default) ratifies your proposal.
- **Hash-drift invalidation is automatic.** Edit a previously-audited
  note and the next pipeline run resets it to `unaudited`. Re-audit
  is required.
- **Critical claims need cross-confirmation.** A claim with 250+
  transitive descendants OR 15+ direct citations requires two
  independent auditors before `audited_clean`.
- **Decoration claims get boxed.** If your new derivation is purely an
  algebraic consequence of an existing claim with no new comparator
  and no new structural integer, it will audit as `audited_decoration`
  and roll up under its parent — see `ALGEBRAIC_DECORATION_POLICY.md`.

The audit lane is intentionally adversarial to claim inflation. That is
its purpose.
