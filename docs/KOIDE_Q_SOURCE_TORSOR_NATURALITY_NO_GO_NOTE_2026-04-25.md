# Koide Q source-torsor naturality no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_source_torsor_naturality_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem attempt

The previous source-fibre identity audit left the affine origin `e` free.  The
next stronger route was naturality: perhaps retained torsor translation or
equivariance structure canonically selects the origin `e=0`.

The audit rejects that as retained-only closure.  Full translation naturality
does not select a point:

```text
tau_c(e) = e  <=>  c = 0.
```

Identity-only retained naturality permits every `e`.  Translation-equivariant
affine maps have the form:

```text
f(rho) = rho + b,
```

with `b` free, and the only equivariant idempotent is the identity map rather
than a point selector.

## Gauge-slice obstruction

A slice

```text
rho - e = 0
```

selects `rho=e`.  Every `e` gives the same local determinant:

```text
d(rho-e)/d rho = 1.
```

So gauge fixing, local Jacobians, and torsor trivializations do not distinguish
the closing origin from a shifted origin.  They only restate that a basepoint
has been supplied.

## Exact counterbasepoint

```text
e = 0
  Q = 2/3
  K_TL = 0
  closes conditionally

e = 1
  Q = 1
  K_TL = 3/8
  full-determinant counterbasepoint
```

Both values lie in the retained semialgebraic source domain `rho > -1`, and
they have identical translation stabilizer data.

## Hostile review

This no-go does **not** use:

- PDG charged-lepton masses;
- an observational `H_*` pin;
- `K_TL=0` as a theorem input;
- `K=0`;
- `P_Q=1/2`;
- `Q=2/3` as a theorem input;
- `delta=2/9`.

It treats `e=0` and `e=1` symmetrically as source-torsor basepoints.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_source_torsor_basepoint_e_equals_zero
RESIDUAL_SOURCE = source_torsor_basepoint_trivialization_not_retained
COUNTERBASEPOINT = e_1_full_determinant_Q_1_K_TL_3_over_8
```

## Consequence

A positive Q closure cannot be "the torsor has a natural origin" unless it
derives the actual basepoint value.  Retained torsor algebra either permits no
point under full translations or permits every point under identity-only
naturality.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_source_torsor_naturality_no_go.py
python3 scripts/frontier_koide_q_current_retained_source_class_exhaustion_no_go.py
python3 scripts/frontier_koide_q_residual_scalar_unification_no_go.py
```

Expected closeout:

```text
KOIDE_Q_SOURCE_TORSOR_NATURALITY_NO_GO=TRUE
Q_SOURCE_TORSOR_NATURALITY_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_SOURCE_TORSOR_BASEPOINT_E_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_source_torsor_basepoint_e_equals_zero
RESIDUAL_SOURCE=source_torsor_basepoint_trivialization_not_retained
COUNTERBASEPOINT=e_1_full_determinant_Q_1_K_TL_3_over_8
```
