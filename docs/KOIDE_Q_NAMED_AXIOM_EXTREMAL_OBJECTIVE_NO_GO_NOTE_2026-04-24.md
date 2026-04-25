# Koide Q named-axiom extremal-objective no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_named_axiom_extremal_objective_no_go.py`  
**Status:** executable no-go; not Q closure

## Theorem attempt

After semialgebraic admissibility left the hidden source charge on a connected
interval `rho > -1`, the next possible retained route was extremality:
perhaps a named least-source, entropy, D-flatness, or action principle selects
`rho=0` without adding a new selector primitive.

The audit rejects that route.  The exact calculus is correct, but it selects
the supplied center, prior, or level:

```text
J_c = (rho-c)^2
  minimum at rho=c

S(p|pi)
  maximum at p=pi

V_zeta = (rho-zeta)^2
  minimum at rho=zeta

V_tilt = rho^2 + ell rho
  minimum at rho=-ell/2.
```

The zero-centered objective `J_0=rho^2` closes only because the zero section
has already been supplied.  The equally exact objective `J_1=(rho-1)^2`
selects the full-determinant countermodel.

## Exact countermodels

```text
rho = 0
  Q = 2/3
  K_TL = 0
  selected by J_0 = rho^2

rho = 1
  Q = 1
  K_TL = 3/8
  selected by J_1 = (rho-1)^2
```

Both centers lie in the retained semialgebraic admissible region `rho > -1`.
Strict convexity proves uniqueness after an objective is supplied; it does not
derive which objective is physical.

## Coordinate issue

A least-norm rule on the source fibre is not coordinate-free unless the zero
section is already retained.  With `eta=rho-c`, the same rule

```text
minimize eta^2
```

selects `rho=c`.  Thus "least source" becomes closure only after a retained
law identifies the physical hidden-fibre origin as `rho=0`.

## Hostile review

This no-go does **not** use:

- PDG charged-lepton masses;
- an observational `H_*` pin;
- `K_TL=0` as a theorem input;
- `K=0`;
- `P_Q=1/2`;
- `Q=2/3` as a theorem input;
- `delta=2/9`.

It treats the zero-centered and full-determinant objectives symmetrically as
exact source-fibre countermodels.

## Residual

```text
RESIDUAL_SCALAR = derive_retained_extremal_objective_centered_at_rho_zero
RESIDUAL_SOURCE = extremal_objectives_select_supplied_center_or_prior
```

## Consequence

The live Q route is narrower but not closed.  A positive proof still needs a
retained charged-lepton law deriving why the physical source objective is
centered at the hidden-fibre zero section.  Extremality alone is support
calculus, not an axiom-native derivation.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_named_axiom_extremal_objective_no_go.py
python3 scripts/frontier_koide_q_current_retained_source_class_exhaustion_no_go.py
python3 scripts/frontier_koide_q_residual_scalar_unification_no_go.py
```

Expected closeout:

```text
KOIDE_Q_NAMED_AXIOM_EXTREMAL_OBJECTIVE_NO_GO=TRUE
Q_NAMED_AXIOM_EXTREMAL_OBJECTIVE_CLOSES_Q_RETAINED_ONLY=FALSE
RESIDUAL_SCALAR=derive_retained_extremal_objective_centered_at_rho_zero
RESIDUAL_SOURCE=extremal_objectives_select_supplied_center_or_prior
COUNTERMODEL_PAIR=rho_0_least_source_and_rho_1_full_determinant_objective
```
