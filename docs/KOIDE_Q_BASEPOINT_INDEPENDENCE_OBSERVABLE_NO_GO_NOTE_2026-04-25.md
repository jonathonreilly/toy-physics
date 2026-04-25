# Koide Q basepoint-independence observable no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_basepoint_independence_observable_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem attempt

After torsor naturality left the basepoint `e` free, the next reviewer-grade
route was gauge/basepoint independence: perhaps physical observables must be
independent of the arbitrary source-fibre basepoint, and that requirement
forces the closing section `e=0`.

The audit rejects that as retained-only closure.  Under simultaneous
basepoint translation

```text
(rho, e) -> (rho+c, e+c),
```

the affine invariant is:

```text
eta = rho - e.
```

On the neutral-preparation slice `rho=e`, every basepoint has `eta=0`.
Therefore a basepoint-independent observable cannot distinguish `e=0` from
`e=1`.

## Q dependence on section

The section-valued Q readout is:

```text
Q(e) = (2+e)/3
dQ/de = 1/3.
```

So Q is not basepoint-independent before a retained section is supplied.
Demanding basepoint independence either deletes the absolute source coordinate
needed to read Q, or leaves the same missing section law.

## Exact countersection

```text
e = 0
  Q = 2/3
  K_TL = 0
  closes conditionally

e = 1
  Q = 1
  K_TL = 3/8
  full-determinant countersection
```

Both sections are exact in the retained semialgebraic source domain.

## Hostile review

This no-go does **not** use:

- PDG charged-lepton masses;
- an observational `H_*` pin;
- `K_TL=0` as a theorem input;
- `K=0`;
- `P_Q=1/2`;
- `Q=2/3` as a theorem input;
- `delta=2/9`.

It treats `e=0` and `e=1` symmetrically as source-fibre sections.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_basepoint_independent_Q_readout_section_e_equals_zero
RESIDUAL_SOURCE = basepoint_invariance_erases_absolute_rho_section
COUNTERSECTION = e_1_full_determinant_Q_1_K_TL_3_over_8
```

## Consequence

A positive Q closure cannot be "make observables basepoint-independent" unless
it also derives a retained absolute section.  Basepoint-independent information
is `rho-e`; the Koide-relevant distinction is the absolute section value.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_basepoint_independence_observable_no_go.py
python3 scripts/frontier_koide_q_current_retained_source_class_exhaustion_no_go.py
python3 scripts/frontier_koide_q_residual_scalar_unification_no_go.py
```

Expected closeout:

```text
KOIDE_Q_BASEPOINT_INDEPENDENCE_OBSERVABLE_NO_GO=TRUE
Q_BASEPOINT_INDEPENDENCE_OBSERVABLE_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_BASEPOINT_SECTION_E_EQUALS_ZERO=TRUE
RESIDUAL_SCALAR=derive_retained_basepoint_independent_Q_readout_section_e_equals_zero
RESIDUAL_SOURCE=basepoint_invariance_erases_absolute_rho_section
COUNTERSECTION=e_1_full_determinant_Q_1_K_TL_3_over_8
```
