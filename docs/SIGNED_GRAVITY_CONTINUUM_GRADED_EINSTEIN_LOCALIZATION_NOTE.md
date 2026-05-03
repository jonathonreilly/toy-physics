# Signed Gravity Continuum Graded Einstein Localization Note

**Date:** 2026-04-26
**Status:** continuum-family transport on the chosen canonical target plus
graded formal nonlinear localization theorem; not a physical signed-gravity
claim
**Script:** [`../scripts/signed_gravity_continuum_graded_einstein_localization.py`](../scripts/signed_gravity_continuum_graded_einstein_localization.py)

This note goes after the remaining tensor-sector blocker from
[`SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md`](SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_NOTE.md):

> prove actual continuum-family transport and replace the naive nonlinear
> `h -> -h` rule by a graded nonlinear Einstein localization theorem.

The result is positive in the precise formal/local sense below. It is not a
global nonlinear PDE existence theorem and it is not a physical signed-gravity
claim.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## The Object

The signed tensor source is not an ordinary tensor source with a free sign. It
is a section of:

```text
L tensor E_T,
```

where:

```text
L   = Or(Det_APS D_Y)
E_T = ordinary retained tensor-source bundle
```

On a gapped APS sector:

```text
chi_eta in Gamma(L),   chi_eta = +/-1.
```

The source is therefore:

```text
T_g = chi_eta T_plus.
```

## Continuum-Family Transport

The continuum transport uses the already-retained universal-QG stack:

- canonical barycentric-dyadic refinement net;
- exact Schur/projective coarse-graining;
- inverse-limit Gaussian cylinder closure;
- project-native PL weak/Sobolev interface;
- smooth global gravitational weak/stationary family;
- canonical textbook continuum GR closure on the chosen target;
- retained rank-two tensor source-to-channel map.

The finite audit checks that this stack is present and that the retained
ordinary tensor source carrier still passes:

```text
retained_carrier=True
dets={'O_h': '1.629e-04', 'finite_rank': '2.014e-04'}
min_svs={'O_h': '4.440e-03', 'finite_rank': '4.049e-03'}
scalar_blind=True
additive=True
```

The APS orientation line is then treated as a flat `Z2` local system over the
atlas/refinement family. The check verifies:

```text
line_cocycle=0.0e+00
tensor_cocycle=4.9e-15
scalar_tensor_comm=0.0e+00
refine_err=0.0e+00
```

Because Schur pushforward is linear in the source, the sign local system
commutes with continuum projective transport:

```text
max_K_schur_err=3.2e-16
max_J_schur_err=1.1e-16
max_signed_J_err=1.1e-16
max_stationary_proj_err=9.0e-16
```

So the signed tensor source transports over the chosen continuum/refinement
family as a local-system twist, not as a reinserted phenomenological sign.

## Graded Nonlinear Theorem

The previous nonlinear obstruction was correct against the naive rule:

```text
h -> -h.
```

Einstein-like nonlinearities have even jets:

```text
E(h) = K h + Q_2(h,h) + Q_3(h,h,h) + ...
```

Therefore:

```text
E(-h) + E(h) = 2 Q_2(h,h) + ...
```

The correct lift is not a full-field sign flip. It is a graded formal solution:

```text
H_chi(eps) = eps chi h_1 + eps^2 h_2 + eps^3 chi h_3 + eps^4 h_4 + ...
```

Equivalently:

- odd jet orders are `L`-valued and flip under `chi_eta`;
- even jet orders are ordinary tensor backreaction and do not flip.

For an analytic gauge-fixed local Einstein operator:

```text
E(H) = K H + Q_2(H,H) + Q_3(H,H,H) + ...
```

with invertible linearized operator `K` on the retained constrained slice, the
formal recursion is:

```text
h_1 = K^-1 J,
h_n = -K^-1 [coefficient of eps^n in nonlinear terms],   n >= 2.
```

This gives a unique formal graded solution order by order. The branch law is:

```text
H_-(eps) != -H_+(eps)
```

because even backreaction is shared:

```text
H_-(eps) + H_+(eps) = 2(eps^2 h_2 + eps^4 h_4 + ...).
```

This is the key correction. The signed branch is an odd/even graded Einstein
jet, not a negative copy of the ordinary metric perturbation.

## Constraint Transport

The harness keeps the source and all nonlinear images on a constrained
Ward/Bianchi-like slice by projecting the nonlinear maps into the retained
constraint kernel. It verifies:

```text
source_constraint=4.1e-16
max_jet_constraint=5.6e-16
```

So the formal graded solution does not leave the retained linear constraint
surface in the finite audit.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_continuum_graded_einstein_localization.py
```

Result:

```text
[PASS] chosen continuum-family GR stack is available for signed tensor transport
[PASS] APS orientation line is a flat local system over atlas/refinement transport
[PASS] signed tensor source commutes with continuum Schur/projective transport
[PASS] graded nonlinear Einstein localization solves the formal jets
[PASS] Ward/Bianchi-compatible constraint surface is preserved at every graded jet
[PASS] non-claim gate remains closed
FINAL_TAG: SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
```

Representative graded readout:

```text
order=6
coeff_resid=2.5e-15
odd_norm=3.375e-01
even_backreaction_norm=1.685e-02
naive_flip_err=2.049e-05
eval_resid=6.4e-17
constraint=1.7e-15
```

## Boundary Verdict

The current tensor-sector status is:

```text
SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
```

This closes the previous tensor localization blocker in a formal/local sense:

- continuum-family transport works on the chosen canonical continuum target;
- the retained tensor carrier survives;
- the APS sign is a flat local-system twist;
- nonlinear localization is graded by jet parity rather than a naive field
  sign flip.

What remains outside this note:

1. global nonlinear PDE existence and uniqueness;
2. physical preparation of both APS sectors;
3. actual APS extraction on every retained graph/lattice gravity family;
4. global many-body and continuum UV/core stability;
5. any phenomenological signed-gravity prediction.

## Remaining-Gates Follow-Up

Those outside gates are now audited in
`SIGNED_GRAVITY_REMAINING_CLOSURE_GATES_NOTE.md` (sibling artifact;
cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_remaining_closure_gates.py`](../scripts/signed_gravity_remaining_closure_gates.py).

Result:

```text
FINAL_TAG: SIGNED_GRAVITY_REMAINING_GATES_REDUCED_TO_PRECISE_CONDITIONALS
```

That pass upgrades the nonlinear side to finite Galerkin small-data
contraction, but leaves global PDE existence unclaimed. It also shows raw
graph Hodge APS boundaries are eta-neutral, opposite-sector preparation is
boundary-data/defect preparation unless a physical channel is derived, and
pair softening is fixed-`N` bounded but not thermodynamically stable.
