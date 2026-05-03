# Artifact Plan — Cycle 21

## Files to create

1. `.claude/science/physics-loops/pmns-branch-selector-2026-05-03/`
   - `STATE.yaml` (resume surface)
   - `GOAL.md` (parent obstruction + honest target)
   - `ASSUMPTIONS_AND_IMPORTS.md` (A_min + forbidden imports)
   - `ROUTE_PORTFOLIO.md` (5 routes scored, Route D selected)
   - `OPPORTUNITY_QUEUE.md` (V1-V5 gate)
   - `ARTIFACT_PLAN.md` (this file)
   - `CLAIM_STATUS_CERTIFICATE.md` (claim status)
   - `HANDOFF.md` (cycle-21 handoff)

2. `docs/PMNS_BRANCH_SELECTOR_CP_SHEET_BLINDNESS_NOTE_2026-05-03.md`
   - Branch A vs Branch B frame distinction
   - Five-route portfolio summary (Routes A-E)
   - Route D execution: CP-sheet blindness applied
   - Route E support: counterfactual comparison
   - Forbidden-import audit
   - V1-V5 PR-promotion gate

3. `scripts/frontier_pmns_branch_selector.py`
   - Reproduce Branch A's 0.1888 from cycle 18 decomposition
   - Reproduce Branch B's 1.0 from min-info, observable-relative-
     action, transport-extremal, and continuity-closure selectors
   - Symbolic parity verification for all four Branch-B selectors
     under δ → -δ
   - Counterfactual: a hypothetical CP-odd selector
   - Counterfactual: alternative chart constants
   - Forbidden-import audit
   - Aim: PASS=N/0 with N ≥ 15

## Verification

```
python3 scripts/frontier_pmns_branch_selector.py
```

Expected: PASS=N/0 with N ≥ 15.

## Commit + push + PR

- Commit science block on `physics-loop/pmns-branch-selector-2026-05-03`.
- Push branch.
- Open PR with title `[physics-loop][cycle21] PMNS branch selector — CP-sheet blindness excludes the current Branch-B bank`.
- PR body links to all loop-pack files, the new note, and runner output.
