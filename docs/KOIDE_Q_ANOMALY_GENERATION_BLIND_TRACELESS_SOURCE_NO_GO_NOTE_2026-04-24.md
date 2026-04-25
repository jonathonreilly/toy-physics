# Koide Q Anomaly Generation-Blind Traceless-Source No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_anomaly_generation_blind_traceless_no_go.py`  
**Status:** executable no-go for deriving `K_TL = 0` from retained anomaly
constraints alone

## Theorem Attempt

The attempted theorem was:

> the retained anomaly-forced `3+1` matter structure removes the normalized
> singlet-vs-doublet traceless source, forcing `K_TL = 0`.

The audit rejects that theorem.  The retained SM anomaly constraints are
generation blind.  They support the matter structure, but do not select the
charged-lepton source shape.

## Exact Findings

One completed SM generation has zero perturbative anomaly vector:

```text
Tr[Y] = 0,
Tr[Y^3] = 0,
Tr[SU3^2 Y] = 0,
Tr[SU2^2 Y] = 0.
```

Therefore arbitrary generation weights remain anomaly-neutral on the completed
branch.  The perturbative anomaly constraints have rank zero on generation
weights.

The retained `C3`-equivariant source operator

```text
K = K_trace I + K_TL (P_plus - P_perp)
```

is invisible to the completed anomaly polynomial because the charge trace is
already zero.

The left-handed trigger branch is not enough either: its anomaly data are
proportional to the identity in generation space.  Identity-valued anomaly data
do not supply the independent isotype operator `P_plus - P_perp`.

## Counterexample

The runner checks the explicit off-Koide source

```text
K_TL = 1/5.
```

It gives an admissible normalized carrier point with

```text
Q = 0.825677653809...
```

while remaining invisible to completed anomaly constraints.  Hence anomaly
cancellation imposes no equation setting `K_TL` to zero.

## Hostile Review

This no-go does **not** use:

- `K_TL = 0` as an input;
- `Q = 2/3` as a closure input;
- PDG masses;
- `delta = 2/9`;
- the observational `H_*` pin.

It uses symbolic anomaly traces and symbolic generation/isotype sources.

## Executable Result

```text
PASSED: 13/13

KOIDE_Q_ANOMALY_GENERATION_BLIND_TR_SOURCE_NO_GO=TRUE
Q_ANOMALY_GENERATION_BLIND_CLOSES_Q=FALSE
RESIDUAL_SCALAR=physical_generation_isotype_no_traceless_source_K_TL
```

## Consequence

The anomaly theorem remains valuable retained structure.  It does not close
the charged-lepton Koide source law.  The surviving `Q` target is still:

```text
derive K_TL = 0
```

from a charged-lepton-specific source grammar that is not generation-blind.
