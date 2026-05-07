# PR Backlog — Bridge Gap New Physics Loop

**Date:** 2026-05-06
**Loop:** bridge-gap-new-physics-20260506

## PRs opened in this campaign

| # | PR | State | Notes |
|---|---|---|---|
| Block 01 | [#617](https://github.com/jonathonreilly/cl3-lattice-framework/pull/617) | OPEN | base = main; HK Brownian time t derivation |
| Block 02 | [#619](https://github.com/jonathonreilly/cl3-lattice-framework/pull/619) | OPEN | base = #617 branch; HK 1-plaq closed form exp(-2/3) |

## Cluster cap reached

The skill's stop-condition rule states:
> "**cluster cap reached**: maximum 2 PRs per parent-row family ... per
> campaign. After 2 in a single cluster, pivot to a different family or
> stop."

Two PRs opened in `bridge_gap_new_physics_*` family. Cap reached.

## Backlog: ready-to-PR commits in current branch

The following Block 03 + Block 04 deliverables are committed to the
Block 02 branch but **not opened as separate PRs** per cluster cap.
Future campaign should open them as stacked PRs:

### Block 03 — Thermodynamic stretch + named obstruction

- **Branch (intended):** `physics-loop/bridge-gap-new-physics-block03-20260506`
- **Base:** `physics-loop/bridge-gap-new-physics-block02-20260506`
- **Title:** `[physics-loop] bridge-gap-new-physics block03: HK thermodynamic factorization + named obstruction (stretch)`
- **Deliverable:** `docs/BRIDGE_GAP_HK_THERMODYNAMIC_STRETCH_NOTE_2026-05-06.md`
- **Status:** stretch_attempt + named_obstruction
- **Key finding:** Casimir-diagonal factorization `Z = Σ (Π W_λ) F_Λ`
  separates β-dependent from geometric data; thermodynamic limit
  requires cluster-decomposition estimate not in current primitives.

To open: in a future campaign on a fresh slug (or after 24h), checkout
the existing commit `f2f87f8ff` which contains both Block 03 + Block 04
notes, create a Block 03-only branch with cherry-pick, and open the PR
with body documenting the Casimir-diagonal factorization theorem and
the named obstruction.

### Block 04 — Action-form uniqueness NO-GO

- **Branch (intended):** `physics-loop/bridge-gap-new-physics-block04-20260506`
- **Base:** `physics-loop/bridge-gap-new-physics-block03-20260506`
- **Title:** `[physics-loop] bridge-gap-new-physics block04: action-form uniqueness no-go (Wilson vs HK vs Manton)`
- **Deliverable:** `docs/BRIDGE_GAP_ACTION_FORM_UNIQUENESS_NO_GO_NOTE_2026-05-06.md`
- **Status:** named-obstruction no_go
- **Key finding:** under current retained primitives, the gauge action
  functional cannot be uniquely selected from {Wilson, HK, Manton}; all
  three are jointly compatible with the framework's primitive stack +
  continuum-limit matching, giving DISTINCT finite-β ⟨P⟩(6) values.
  Range-bounds the four cluster lanes' downstream quantitative claims
  at ~5-10% (150-300× ε_witness).

To open: same as Block 03 (cherry-pick from `f2f87f8ff`), title and body
emphasizing the no-go theorem, the consequence for the four cluster
lanes' range-bounding, and the structural reason this no-go is not a
research-effort gap but a primitive-stack limitation.

## Why backlog rather than open

The cluster cap's stated rationale: "the marginal value of cycle N+1
reliably drops below the cost of audit-lane review burden once N
exceeds ~5–8 in one session." At N = 2 the rationale is conservative
but the rule is strict.

Block 03 and Block 04 are NOT corollary churn — they introduce
genuinely new content (Casimir-diagonal factorization, action-form
uniqueness no-go). Their value is preserved in the loop pack +
committed branch state; opening them in a fresh campaign maintains
audit-lane reviewability.

## Future-campaign instructions

Recommended next campaign on the bridge gap should:

1. Resume from the `physics-loop/bridge-gap-new-physics-block02-20260506`
   branch state (which contains Block 01-04 commits).
2. Open Block 03 PR (stacked on Block 02 branch).
3. Open Block 04 PR (stacked on Block 03 branch).
4. Continue with Block 05 = R4.B (Cl(3) ⊗ Cl(3) → SU(4) ⊃ SU(3) × U(1)
   tensor exploration) per `OPPORTUNITY_QUEUE.md` rank 5.
5. Or pivot to Resolution-B governance reclassification per the
   action-form no-go's consequence section.
