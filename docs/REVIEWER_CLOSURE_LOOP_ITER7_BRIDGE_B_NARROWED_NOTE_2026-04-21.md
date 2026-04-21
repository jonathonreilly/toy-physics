# Reviewer-Closure Loop Iter 7: Bridge B Structural Derivation — Narrowed

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Narrowed at structural level, not closed at Nature-grade.**
Bridge B weak reading (observational agreement) was closed at iter 3.
Iter 7 attempted a Z_3-representation-theoretic derivation of
`arg(b) = APS η` and finds the two quantities have DIFFERENT
mathematical types (amplitude phase vs. spectral invariant). No
tautological identity from Z_3 rep theory alone; naive Berry-phase
construction gives trivial 2π (not 2/9). A bridging construction is
needed but is outside currently retained Atlas.
**Runner:** `scripts/frontier_reviewer_closure_iter7_bridge_b_structural_derivation.py`
— 5/5 PASS (all PASS are the structural claims; the verdict is honest).

---

## Reviewer-branch state

Per `origin/review/scalar-selector-cycle1-theorems` commit `333f4a67`
(latest), Bridge B remains on the Open-Gates list:

> Bridge B: why the physical selected-line Brannen phase equals
> the ambient APS invariant

So my iter 3 numerical confirmation (arg(b) = δ_B to 5 decimals) is
NOT accepted as Nature-grade closure by the canonical reviewer. A
DERIVATION is required, not observational confirmation.

## Iter 7 attack

Test whether arg(b) (Brannen phase) and APS η = 2/9 (morning-4-21
I2/P retained) are **structurally** the same Z_3 invariant, differing
only in presentation.

### Part A — Z_3 doublet rep setup

Both sides reference the Z_3 (1, 2) weight rep:
- Koide: C on C³ has eigenvalue spectrum (1, ω, ω²); doublet block
  carries weights (1, 2) mod 3.
- APS: R²/Z_3 tangent rep has weights (1, 2) mod 3 by the core
  identity.

### Part B — Koide-side structural phase

For `M = a·I + b·C + b*·C²`, the Z_3 isotype decomposition
`K = U_Z3^† M U_Z3` has `K[1,2]` and related doublet-block entries
carrying `arg(b)` as a chart-amplitude phase.

### Part C — structural non-identity

**arg(b) and APS η have different mathematical types**:
- `arg(b)` is a continuous real amplitude phase (in [−π, π]).
- APS η = 2/9 is a regularized spectral invariant (rational in [0, 1)).

No tautological identification from Z_3 rep theory. Numerical
agreement at 5-dp is a framework **prediction**, not a trivial
consequence.

### Part D — Bridge B honest status

- **Weak reading** (observational): CLOSED at iter 3 (5-dp agreement).
- **Strong reading** (framework derivation): OPEN.

Bridging would require either:
1. A specific framework convention mapping amplitude phases to
   spectral invariants via Z_3 structure.
2. An independent physical/dynamical mechanism setting
   `arg(b) = 2/9` at the charged-lepton mass matrix.

Neither exists in the currently retained Atlas.

### Part E — Berry-phase attempt fails

Naive Berry-phase of Z_3 cyclic orbit gives trivial 2π — not 2/9 rad.
More sophisticated equivariant-η constructions could work but require
framework inputs beyond current Atlas.

## Status classification of open items

All three bridges now have the same structural status:

| Item | Observational | Framework-derived |
|---|:---:|:---:|
| Bridge A (Frobenius extremality) | empirical (< 0.1%) | open |
| Bridge B (Brannen = APS) | empirical (5 dp) | open |
| N1 (δ·q_+ = SELECTOR²) | empirical (0.16%) | open |

All three are **primitive retained identities at the observational
level** — not derivable from current retained Atlas theorems.

## Iter 8 pivot (Gate 2)

Per user discipline "stay on target until closed at Nature-grade":
three distinct attempts on N1 (iters 4, 5, 6) and a structural attack
on Bridge B (iter 7) have all failed to close at Nature-grade. The
pattern is: these bridges are primitive retained identities,
un-derivable within the available toolkit.

**Pivot reasoning**: iter 8 should attack a Gate 2 item where real
progress is possible, not continue grinding on primitive-identity
bridges. Candidates:

- **Chamber-wide σ_hier extension**: concrete, tractable — multi-basin
  numerical/structural analysis. σ_hier = (2, 1, 0) is currently
  observational at the pinned point; extending chamber-wide is a
  concrete theorem target.
- **Interval-certified carrier dominance**: concrete numerical
  analysis on the residual split-2 selector branch.
- **Current-bank quantitative DM mapping**: concrete DM calculation.

Iter 8 will attack **chamber-wide σ_hier extension** as the most
tractable untried item.
