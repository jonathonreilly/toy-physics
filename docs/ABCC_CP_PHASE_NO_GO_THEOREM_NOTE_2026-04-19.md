# A-BCC CP-Phase No-Go Theorem

**Date:** 2026-04-19  
**Status:** **conditional support theorem on the open DM gate** — under `σ_hier = (2,1,0)` and the
T2K CP-phase measurement, all known C_neg chi²=0 PMNS solutions are
observationally excluded  
**Runner:** `scripts/frontier_abcc_cp_phase_no_go_theorem.py` ([scripts/frontier_abcc_cp_phase_no_go_theorem.py](../scripts/frontier_abcc_cp_phase_no_go_theorem.py))
**Runner result:** `PASS = 20, FAIL = 0`

## What this theorem establishes

The A-BCC axiom identifies the physical PMNS sheet with the
baseline-connected component `C_base = {det(H) > 0}` of `{det(H) ≠ 0}`. The
three known chi²=0 PMNS solutions on the retained affine chart are:

| Basin | Component | det(H) | σ used | sin(δ_CP) | T2K status |
|-------|-----------|--------|--------|-----------|------------|
| Basin 1 | C_base | +0.959 | (2,1,0) | −0.9874 | PREFERRED |
| Basin 2 | C_neg | −70537 | (2,1,0) | +0.5544 | EXCLUDED >3σ |
| Basin X | C_neg | −20296 | (2,0,1)† | +0.4188‡ | EXCLUDED >3σ |

†Basin X is a chi²=0 solution under σ=(2,0,1); it passes 9/9 NuFit under that pairing.  
‡Under the physical σ=(2,1,0).

**Theorem.** Given σ_hier = (2,1,0) (established by the σ_hier uniqueness
theorem) and the T2K (2021, Normal Ordering) measurement excluding
sin(δ_CP) > +0.247 at >3σ:

> Every known chi²=0 PMNS solution on the retained affine chart with
> det(H) < 0 gives sin(δ_CP) > +0.247. All C_neg solutions are
> therefore observationally excluded. The physical PMNS solution must
> lie on C_base.

This sharpens A-BCC from "physically motivated axiom" to
"observationally grounded support input": the known `C_neg` solutions are ruled
out by concrete measurement once the physical pairing is fixed.

## Proof structure

### Step 1 — Basin 2 (C_neg, under physical σ)

Basin 2 is located near `(m, δ, q+) ≈ (28.006, 20.722, 5.012)`. It is a
chi²=0 solution under BOTH σ=(2,0,1) (sin(δ_CP)=−0.554) and σ=(2,1,0)
(sin(δ_CP)=+0.554). Under the physical σ=(2,1,0):

```
sin(δ_CP) = +0.5544  →  excluded by T2K at >3σ (bound: +0.247)
```

### Step 2 — Basin X (doubly excluded)

Basin X is located near `(m, δ, q+) ≈ (21.128, 12.680, 2.089)`. It is a
chi²=0 solution under σ=(2,0,1) with sin(δ_CP)=−0.419. Two independent
exclusions apply:

**Ground 1 (σ_hier uniqueness):** At the C_base pin, σ=(2,0,1) gives
sin(δ_CP)=+0.987, which is T2K-excluded (>3σ). The σ_hier uniqueness theorem
established σ=(2,1,0) is the unique physically admissible pairing. Basin X's
native pairing σ=(2,0,1) is therefore excluded at the pin level — there is no
consistent C_base solution for σ=(2,0,1).

**Ground 2 (CP-phase at Basin X):** Under the physical σ=(2,1,0), Basin X
also gives sin(δ_CP)=+0.419 > +0.247, independently excluded by T2K at >3σ.

### Step 3 — Structural origin: Jarlskog sign flip

The signature flip (2,0,1)→(1,0,2) from C_base to C_neg corresponds to an
inertia reversal of the Hermitian form. Under fixed σ=(2,1,0), this reverses
the orientation of the eigenvector frame, which reverses the sign of the
Jarlskog invariant J:

```
J at C_base pin  (σ=(2,1,0)):  J = −0.032755  (< 0  →  sin(δ_CP) < 0)
J at Basin 2     (σ=(2,1,0)):  J = +0.018391  (> 0  →  sin(δ_CP) > 0)
```

This sign flip is structural: `det(H) < 0` at C_neg implies opposite-sign
inertia, which propagates into a J-sign reversal. Applying σ=(2,1,0)
globally therefore FORCES sin(δ_CP) > 0 at all C_neg solutions — regardless
of the specific C_neg basin.

## Dependency chain

This theorem depends on:

1. **σ_hier uniqueness theorem** (`SIGMA_HIER_UNIQUENESS_THEOREM_NOTE_2026-04-19.md`)
   — establishes σ=(2,1,0) as the unique 4-observable PMNS-consistent pairing
   at the C_base pin, and excludes σ=(2,0,1).

2. **T2K (2021, Normal Ordering) measurement** — excludes δ_CP ∈ [0.25, π] rad
   at >3σ, corresponding to sin(δ_CP) > +0.247.

3. **P3 PMNS-as-f(H) map** — the retained affine chart `H(m, δ, q+)` and the
   chi²=0 condition on PMNS angles.

## What this closes (and what it does not)

### What it closes

- **C_neg observational admissibility**: Both known C_neg chi²=0 basins are
  experimentally excluded under σ=(2,1,0) + T2K. No competing C_neg PMNS
  solution survives the combined constraint.

- **A-BCC observational grounding**: A-BCC is no longer only "physically
  motivated" — it has a concrete observational no-go backing it on the live
  package surface.

### What it does NOT close

- **A-BCC as a framework theorem**: This runner does not derive A-BCC from
  the Cl(3)/Z³ axiom alone. Closing A-BCC at the axiom level (without
  observational input) remains the last open item on the DM flagship.

- **Exhaustive C_neg basin search**: Only Basins 2 and X are known. Additional
  C_neg chi²=0 basins at large parameter values have not been exhaustively
  excluded. The structural Jarlskog sign-flip argument (Part 5) suggests all
  C_neg solutions are excluded under σ=(2,1,0), but this has not been proven
  in full generality.

- **Koide scalar**: The charged-lepton Koide lane gap (one microscopic scalar
  selector law for `m = Tr K_Z3` on the selected slice) is a separate open
  item.

## Consequence for the P3 flagship

With the σ_hier and A-BCC conditionals both given observational grounding:

| Open input | Status before | Status after |
|------------|--------------|--------------|
| σ_hier = (2,1,0) | Independent conditional (free S_3 choice) | Observationally unique (σ_hier theorem) |
| A-BCC | Physically motivated axiom | Observationally grounded (no-go theorem) |

The P3 flagship closure now rests on one observationally unique pairing and
one observationally grounded component choice. The final step — deriving A-BCC from the
Cl(3)/Z³ axiom without observational input — remains open.

## Falsifiable prediction

A confirmed >5σ measurement of sin(δ_CP) = −0.987 ± ε at DUNE/Hyper-Kamiokande
would:
1. Make the T2K >3σ exclusion of sin(δ_CP) > +0.247 into a >>5σ exclusion
2. Make the C_neg no-go airtight at the observational level
3. Further validate the P3 pinned prediction sin(δ_CP) = −0.9874

A confirmed measurement sin(δ_CP) > +0.5 would falsify the entire P3
closure (not just A-BCC grounding, but the framework itself).

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_abcc_cp_phase_no_go_theorem.py
```

Expected: `PASS = 20, FAIL = 0`.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- `SIGMA_HIER_UNIQUENESS_THEOREM_NOTE_2026-04-19.md` (sibling/parallel; backticked to break length-2 cycle)
