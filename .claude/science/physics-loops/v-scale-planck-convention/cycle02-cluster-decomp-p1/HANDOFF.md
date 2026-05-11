# Handoff — Cycle 2: P1 Cluster-Decomposition Narrowing

**Date:** 2026-05-10
**Loop:** v-scale-planck-convention
**Branch:** physics-loop/v-scale-g1-cluster-decomp-20260510
**Status:** bounded support note opened for independent audit; parent row
unchanged

## Files touched

- New: `docs/OBSERVABLE_GENERATOR_ADDITIVITY_FROM_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-05-10.md`
- New: `scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py`
- New: this `HANDOFF.md`, `STATE.yaml`, `CLAIM_STATUS_CERTIFICATE.md`

## Runner check

```
python3 scripts/frontier_observable_generator_additivity_from_cluster_decomposition.py
```

Expected: `THEOREM PASS=12 FAIL=0`.

## Honest verdict

The cluster-decomposition attack on P1 of
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](../../../../docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
**narrows** P1 by proving the three-way equivalence

> (A1) P1 scalar-additivity
> <=>
> (A2) W = log|det(D + J)| up to constant
> <=>
> (A3) W is the cumulant generating functional with mixed kernels
> vanishing across no-cut-bond partitions

on the finite-Grassmann surface of the staggered Cl(3) Dirac hopping
operator over a finite block of `Z^3`, using only finite Grassmann
calculus + block-diagonal `D = D_A (+) D_B` from `Z^3` locality +
Cauchy continuity at `J = 0` + finite-block polynomial analyticity.

The equivalence does NOT retire P1. The "additional classification
axiom" the parent row identifies is mathematically equivalent to the
canonical cumulant-generator definition (A3) in finite Grassmann field
theory; the selection between additive-class (cumulant generator) and
non-additive functionals of `Z[J]` remains a definitional step. The
parent row's `audited_conditional` shape persists.

This is the honest stretch-attempt result: a narrowing, not a closure.

## V1-V5 (compressed)

- V1: parent verdict quoted (P1 as physical-principle classification
  axiom).
- V2: three-way equivalence (A1) <=> (A2) <=> (A3) with companion runner
  PASS=12 FAIL=0.
- V3: standard math can do most; failing the retained-promotion bar is
  correct because this is a narrowing, not a closure. PR opened as
  bounded-support note, not retained-promotion proposal.
- V4: non-trivial; the connected-truncated property + cut-bond
  counterfactual are structural, not definitional.
- V5: distinct from cycle-08 metadata enumeration and 2026-05-09
  P2/P3/P4 runner-local derivation.
