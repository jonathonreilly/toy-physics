# Cycle 22 HANDOFF — Carrier Orbit Invariance

## Cycle summary

**Loop slug:** `carrier-orbit-invariance-2026-05-03`  
**Campaign:** continuation of `retained-promotion-2026-05-02` (cycle 22)  
**Branch:** `physics-loop/carrier-orbit-invariance-2026-05-03`  
**Output type:** stretch_attempt with partial structural-insight (c)  
**Runner:** `scripts/frontier_carrier_orbit_invariance.py`  
**Runner result:** PASS=52 FAIL=0  

## What was done

Cycle 22 attacks the deepest residual blocking full retention of the
v_even theorem (and the upstream swap-reduction theorem) named by cycle
17 (PR #445):

> "the swap-reduction theorem's structural-exhaustion premise — 'no
> exact E/T-distinguishing operator on the K_R(q) carrier' — is
> established for specific operators (Theta_R^(0), Xi_R^(0) are
> bounded) but NOT exhaustively."

**Selected route:** Route B (group-theoretic / Z_2-equivariant). The
carrier K_R(q) carries an explicit Z_2 action via column swap P_ET. By
Maschke's theorem, the carrier representation V = R^4 decomposes into
isotypic components V = V^+ ⊕ V^-, each of dimension 2. The operator
space End(V) decomposes correspondingly as End(V) = End(V)^+ ⊕ End(V)^-,
each of dimension 8.

**Structural-exhaustion claim sharpened:** any retained-primitive
operator on the carrier must lie in End(V)^+ (the swap-invariant
isotypic component). The current retained primitive registry on the
carrier consists of:
- Theta_R^(0) (bounded, gamma_E - gamma_T component bounded)
- Xi_R^(0) (bounded)
- Active Hermitian basis (a, b, c, d, T_delta, T_rho) on the H-side,
  not directly on the carrier columns

Direct enumeration confirms that NO retained primitive on the audited
surface has nonzero antisymmetric component in End(V)^-.

**Residual gap (named precisely):** the closure premise — "no future
retained primitive can break this classification" — is a
meta-mathematical statement about the framework registry, not a
statement provable on the current axiomatic surface. This is the
**registry closure** obstruction that cycle 22 names precisely.

## What this closes

1. Z_2-isotypic decomposition of carrier representation: rigorous
   classification.
2. Operator space decomposition: End(V) = End(V)^+ ⊕ End(V)^-.
3. Registry enumeration on current audited surface: PASSES (no
   antisymmetric retained primitives).
4. Counterfactual antisymmetric candidates falsified.
5. Cycle 17 named residual sharpened from vague structural exhaustion
   to a single named meta-premise (registry closure).
6. Routes C, D rejected as overkill (cohomological/sheaf machinery
   adds no content beyond the rep-theoretic argument).

## What remains open

- **Registry closure** (NEW, named by cycle 22): a meta-mathematical
  premise about the framework registry. Tractable as a repo-level
  audit, NOT as a single-cycle physics derivation.
- Absolute retention of swap-reduction theorem to audited_clean.
- Absolute retention of v_even theorem (downstream).
- Cycles 16 sub-B/sub-C and cycle 17 routes A/B/C: retain
  "single-lemma-away" status; the lemma is now precisely identified.

## Audit-graph effect

If audit-lane ratifies cycle 22:

1. Swap-reduction theorem residual sharpened.
2. Cycle 17 named residual retired.
3. New named residual: registry closure (meta).
4. Cycle 16 / cycle 17 chain retains its single-lemma-away status with
   the lemma now precisely identified as registry closure.

## Forbidden imports — all clean

All cycle 22 artifacts checked:
- NO PDG values consumed
- NO literature numerical comparators
- NO fitted selectors
- NO same-surface family arguments
- NO load-bearing consumption of v_even values
- Cycle 17 routes A/B/C admitted as prior-cycle inputs only
- Standard rep theory (Maschke, Schur) declared admitted-context

## Files

- `docs/CARRIER_ORBIT_INVARIANCE_STRETCH_ATTEMPT_NOTE_2026-05-03.md` — note
- `scripts/frontier_carrier_orbit_invariance.py` — runner (PASS=52/0)
- `.claude/science/physics-loops/carrier-orbit-invariance-2026-05-03/`
  - STATE.yaml, GOAL.md, ASSUMPTIONS_AND_IMPORTS.md
  - ROUTE_PORTFOLIO.md, NO_GO_LEDGER.md, OPPORTUNITY_QUEUE.md
  - LITERATURE_BRIDGES.md, ARTIFACT_PLAN.md
  - CLAIM_STATUS_CERTIFICATE.md, REVIEW_HISTORY.md, HANDOFF.md, PR_BACKLOG.md

## Concurrency note

This cycle ran in parallel with cycles 20 and 21 of the same campaign.
The branch `physics-loop/carrier-orbit-invariance-2026-05-03` was
created fresh from origin/main; no merge conflicts with parallel
cycles' branches expected.

## Next exact action

Open review PR via `gh pr create` with the standard cycle 22 title and
body. After PR, close the cycle and continue or stop the campaign per
opportunity queue priorities.

## Honest classification

**Output type (c):** stretch attempt with partial closing-derivation.
Most likely outcome per prompt expectation. The structural exhaustion
claim is sharpened (not closed), and the named residual is a
meta-mathematical registry-closure premise — tractable for future
campaigns as an audit task, but NOT closeable as a single-cycle
physics derivation.

**Audit-lane ratification required for any retained-grade
interpretation.**
