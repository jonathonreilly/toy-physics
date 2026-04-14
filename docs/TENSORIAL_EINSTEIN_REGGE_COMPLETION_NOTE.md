# Tensorial Einstein/Regge Completion Gap

**Date:** 2026-04-14  
**Branch:** `codex/review-active`  
**Status:** sharp obstruction for full nonlinear GR; restricted `3+1` lift remains real

## Goal

Starting from the restricted discrete Einstein/Regge lift already on the branch,
ask whether the current scalar bridge can be promoted to a full tensorial
completion theorem for generic nonspherical and time-dependent sectors.

The target is not to re-prove the scalar bridge. The target is to test the
missing `3+1` tensorial completion map:

> does the scalar Schur boundary action determine the full lapse-shift-spatial
> metric, or only the scalar conformal sector?

## Inputs already on the branch

The branch already has:

- exact local `O_h` shell closure
- exact same-charge bridge
- exact local static conformal lift
- exact microscopic Schur boundary action
- exact microscopic Dirichlet principle
- exact restricted discrete Einstein/Regge lift on the current bridge surface
- bounded widening to generic finite-support / fast-decay support classes

Those results are retained and not re-proved here.

## Tensorial test

The new verifier keeps the exact scalar bridge fixed and adds explicit tensorial
degrees of freedom in `3+1`:

- a shift-vector mode `beta_i`
- a traceless spatial shear mode `h_ij^TT`
- a mixed vector+tensor perturbation

The scalar trace data are left unchanged, so the exact microscopic Schur
boundary action remains unchanged by construction.

This is the right test for the missing completion principle because the current
bridge package is scalar:

- it fixes `phi`
- it fixes `psi = 1 + phi`
- it fixes `chi = 1 - phi`
- it fixes `rho` and `S` on the static conformal bridge

but it does **not** include a tensor-valued matching operator for the shift or
traceless spatial sector.

## Local equations

Write the ADM-style metric in covariant form with lapse `N`, shift `beta^i`,
and spatial metric `gamma_ij`.

The test perturbs the restricted scalar bridge by

- `beta^i = eps_vec * sin(omega t) * envelope(r) * v^i(x)`
- `h_ij   = eps_ten * cos(omega t) * envelope(r) * q_ij(x)`

with

- `v^i` a rotational shift mode
- `q_ij` a traceless quadrupole shear

The full 4D Einstein tensor is then computed numerically at shell-adjacent
probe points.

## Result

The decisive pattern is:

1. the scalar Schur boundary action is blind to the tensorial perturbations
   because the scalar trace data are unchanged
2. the vector and traceless tensor perturbations generate independent Einstein
   residuals in `G_{0i}` and the traceless part of `G_{ij}`
3. the mixed perturbation activates both tensor channels simultaneously

The verifier makes this explicit on the current branch:

- exact local `O_h` scalar bridge: `|G|_max ~ 2.78e-3`
- with a pure vector shift mode: the scalar action is unchanged, but
  `|G_{0i}|_max ~ 8.88e-5` appears on top of the scalar residual
- with a pure traceless shear mode: the scalar action is unchanged, but the
  traceless spatial residual rises to `|G_{ij}^{TF}|_max ~ 1.08e-3`
- on the finite-rank class, the same pattern persists with a larger scalar
  floor:
  - scalar bridge: `|G|_max ~ 2.93e-2`
  - tensor shear: `|G|_max ~ 2.97e-2`, with `|G_{ij}^{TF}|_max ~ 5.55e-3`

That means the current restricted lift is not a full tensorial completion
theorem.

## Sharp obstruction

The missing principle is now sharply localized:

> a tensor-valued matching/completion operator is required to extend the
> scalar bridge from the current static conformal sector to generic nonspherical
> and time-dependent `3+1` gravity.

Equivalently:

> the current Schur/Dirichlet boundary action determines only the scalar sector;
> it does not determine the full lapse-shift-spatial metric.

## What remains open

This leaves full nonlinear GR open in the following precise sense:

- the scalar/static exterior law is real
- the restricted Einstein/Regge lift is real
- the generic finite-support support widening is real
- but the tensorial completion map to the full 4D metric is still missing

So the current branch proves a strong restricted strong-field theorem, but not
full nonlinear GR in generic nonspherical/time-dependent sectors.

## Verdict

- **Restricted `3+1` lift:** closed on the current class
- **Tensorial completion to generic sectors:** open
- **Full nonlinear GR in full generality:** still blocked by the missing
  tensor-valued matching principle
