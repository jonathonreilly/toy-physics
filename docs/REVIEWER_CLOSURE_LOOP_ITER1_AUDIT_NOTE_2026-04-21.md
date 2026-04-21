# Reviewer-Closure Loop Iter 1: Audit of afternoon-4-21-proposal vs. Reviewer Items

**Date:** 2026-04-21
**Branch:** `evening-4-21`
**Status:** **Audit complete.** The afternoon-4-21-proposal's 3-retained-identity
closure **IS** one of the canonical reviewer's specific open items
(Gate 2 right-sensitive microscopic selector law), per the explicit
equivalence statement in `DERIVATION_ATLAS.md` line 335.
**Runner:** `scripts/frontier_reviewer_closure_audit_iter1.py` — 11/11 PASS.

---

## Reviewer's open items (as of `review/scalar-selector-cycle1-theorems` commit `ce980686`)

### Gate 1 — Charged-lepton Koide bridge package (downgraded from closed)

- **Bridge A** (physical Frobenius extremality): why the physical
  charged-lepton packet must extremize the block-total Frobenius
  functional. morning-4-21 I1 shows extremum ⟹ Q = 2/3; the physical
  argument for sitting at the extremum is missing.
- **Bridge B** (physical Brannen = ambient APS): why the physical
  selected-line Brannen phase equals the ambient APS invariant.
  morning-4-21 I2/P shows ambient APS η = 2/9; the physical
  identification of this with the Brannen phase is missing.
- Downstream of Bridge B: selected-line witness `m_* / w/v`.
- Separate / outside-scope: overall lepton scale `v_0`.

### Gate 2 — DM flagship gate

- **A-BCC axiomatic derivation** (currently observational via T2K).
- **Right-sensitive microscopic selector law** on
  `dW_e^H = Schur_Ee(D_-)`.
- Interval-certified exact-carrier dominance/completeness on residual
  split-2 selector branch.
- Chamber-wide / all-basin `σ_hier = (2, 1, 0)` extension.
- Current-bank quantitative DM mapping.

## Key audit finding — DERIVATION_ATLAS line 335 equivalence

The DM Derivation Atlas (`docs/publication/ci3_z3/DERIVATION_ATLAS.md`)
states, at line 335, the **PMNS microscopic selector reduction theorem**:

> once constructive exact closure exists and the DM thermal layer is
> bounded, the remaining blocker reduces exactly to a **right-sensitive
> microscopic selector law on `dW_e^H = Schur_Ee(D_-)`, equivalently
> the intrinsic `2`-real `Z_3` doublet-block point-selection law**

This equivalence is already theorem-grade on main. So the reviewer's
"right-sensitive microscopic selector law" item (Gate 2) **equals** the
"intrinsic 2-real Z_3 doublet-block point-selection law".

## What afternoon-4-21-proposal provides

afternoon-4-21-proposal gives three SELECTOR-based retained identities:

```
  Tr(H)    = SELECTOR² = Q_Koide = 2/3
  δ · q_+  = SELECTOR² = Q_Koide = 2/3
  det(H)   = 2 · SELECTOR / √3 = E2 = √8/3
```

that **uniquely** pin `(m, δ, q_+) = (2/3, 0.9330511, 0.7145018)` in
the A-BCC chamber, with zero PMNS observational inputs and all three
PMNS angles within NuFit 1σ NO. All 25 checks in the proposal runner
PASS.

### Structural match with the Atlas equivalence

- Identity 2 (`δ · q_+ = 2/3`) acts purely on the **intrinsic 2-real
  doublet-block coordinates** `(δ, q_+)` (m-spectator theorem,
  Atlas line 314).
- Identity 1 (`Tr(H) = 2/3`) fixes the spectator direction exactly at
  `m = Q_Koide`.
- Identity 3 (`det(H) = E2`) under Identity 1 becomes a polynomial
  constraint on `(δ, q_+)` — another **2-real doublet-block** statement.

Therefore the 3-identity closure **is** a point-selection law on the
intrinsic 2-real Z_3 doublet block. By the Atlas equivalence, it
**is** a right-sensitive microscopic selector law on
`dW_e^H = Schur_Ee(D_-)`.

## Closure summary

The afternoon-4-21-proposal:

- **Closes** Gate 2 / "right-sensitive microscopic selector law on
  `dW_e^H = Schur_Ee(D_-)`" item (via Atlas line 335 equivalence).
- **Closes** the equivalently-stated "intrinsic 2-real Z_3
  doublet-block point-selection law" item.

These are ONE item restated in two vocabularies. Both are closed by
the existing proposal.

## Remaining open items (8) — attack priorities for iter 2+

| # | Item | Gate | Priority | Target iter |
|---|---|---|---|---|
| 1 | Bridge A — physical Frobenius extremality | 1 | HIGH | 2 |
| 2 | Bridge B — physical Brannen = ambient APS | 1 | HIGH | 3 |
| 3 | A-BCC axiomatic derivation | 2 | MEDIUM | 4 |
| 4 | Chamber-wide σ_hier extension | 2 | MEDIUM | 5 |
| 5 | m_* / w/v downstream of Bridge B | 1 | (follows Bridge B) | 3 |
| 6 | Interval-certified carrier dominance | 2 | LOW | 6+ |
| 7 | Current-bank quantitative DM mapping | 2 | LOW | 6+ |
| 8 | v_0 overall lepton scale | 1 | LOW (outside-scope) | 6+ |

## What iter 1 saves us

By doing this audit FIRST, iter 2+ will not redo the work already
captured in afternoon-4-21-proposal. The loop can now focus on the
genuinely open items (1–4) rather than re-deriving the right-sensitive
microscopic selector law.

## Iter 2 plan (queued)

**Target**: Gate 1 Bridge A — physical Frobenius extremality.

**Concrete question**: morning-4-21 I1 proves that the AM-GM
maximum of `log(E_+ · E_⊥)` on `Herm_circ(3)` is at `κ = 2`, giving
`Q = 2/3`. The reviewer asks WHY the physical charged-lepton packet
sits at this maximum.

**Candidate attacks**:

1. Observable principle `W[J] = log|det(H_base + J)|` might imply a
   maximization principle on some retained functional restricted to
   physical subspace.
2. The retained SELECTOR principle might force the physical packet
   to be at the Ad-invariant extremum of the Frobenius-isotype split.
3. A cross-sector pull: afternoon-4-21-proposal has `Tr(H) = Q` and
   `δ·q+ = Q`. If the morning-4-21 Frobenius functional at its maximum
   equals Tr(H) or another afternoon-style identity, the extremal
   principle is forced by the afternoon closure.

Iter 2 will execute the most concrete of these (likely cross-sector)
and report honestly.
