# Artifact Plan — Cycle 22

## Deliverables

1. **Loop pack** at `.claude/science/physics-loops/carrier-orbit-invariance-2026-05-03/`:
   - STATE.yaml, GOAL.md, ASSUMPTIONS_AND_IMPORTS.md
   - ROUTE_PORTFOLIO.md, NO_GO_LEDGER.md, OPPORTUNITY_QUEUE.md
   - LITERATURE_BRIDGES.md, ARTIFACT_PLAN.md
   - CLAIM_STATUS_CERTIFICATE.md (with V1-V5 PROMOTION VALUE GATE)
   - REVIEW_HISTORY.md, HANDOFF.md, PR_BACKLOG.md

2. **Stretch-attempt note** at
   `docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md`:
   - A_min minimal premise set
   - Forbidden imports (no PDG, no literature, no fitted selectors)
   - Carrier representation under Z_2 swap action
   - Isotypic decomposition V = V^+ ⊕ V^-
   - Operator decomposition End(V) = End(V)^+ ⊕ End(V)^-
   - Carrier Operator Classification Theorem (partial)
   - Counterfactual hypotheticals
   - Named residual: registry closure (meta-premise)
   - Honesty disclosures

3. **Runner** at `scripts/frontier_carrier_orbit_invariance.py`:
   - Part 1: carrier swap action is involution
   - Part 2: isotypic decomposition (V^+, V^- each dim 2)
   - Part 3: operator space decomposition (End(V)^+, End(V)^- each dim 8;
     (V*)^+ , (V*)^- each dim 2)
   - Part 4: registry enumeration on retained primitives
   - Part 5: counterfactual antisymmetric candidate falsification
   - Part 6: low-degree polynomial operator enumeration (Route E)
   - Part 7: carrier trace check on retained operator basis
   - Part 8: named residual obstruction
   - Part 9: independence from v_even values
   - Part 10: V1-V5 PROMOTION VALUE GATE check
   - Target: PASS >= 15

4. **Branch + PR**:
   - Branch: `physics-loop/carrier-orbit-invariance-2026-05-03` from
     origin/main
   - Commits coherent with conventional commit format
   - PR title: `[physics-loop][carrier-orbit-invariance-2026-05-03]
     stretch attempt with partial structural-insight (output type c)`
   - PR body links HANDOFF.md, note, runner, and verification commands

## Verification

```bash
python3 scripts/frontier_carrier_orbit_invariance.py
# Expected: SUMMARY: PASS=N FAIL=0 with N >= 15
```

Actual runner result: PASS=52 FAIL=0 (exceeds target).

## What this is NOT

- NOT a closing derivation of the swap-reduction theorem to retained.
- NOT a closing derivation of v_even theorem to retained.
- NOT a Nature-grade result.

What it IS: a precise sharpening of cycle 17's named residual into a
checkable structural classification + a single named meta-premise.
