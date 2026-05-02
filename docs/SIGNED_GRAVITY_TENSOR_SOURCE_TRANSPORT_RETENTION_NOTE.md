# Signed Gravity Tensor-Source Transport And Retention Note

**Date:** 2026-04-26
**Status:** finite carrier retention and projective transport positive;
nonlinear closure gated; not a physical signed-gravity claim
**Script:** [`../scripts/signed_gravity_tensor_source_transport_retention.py`](../scripts/signed_gravity_tensor_source_transport_retention.py)

This note follows the oriented tensor-source lift:

```text
T_g(Y) = chi_eta(Y) T_plus.
```

The remaining question was whether `T_plus` is an ordinary retained tensor
carrier and whether the twist transports through the retained family/refinement
structure. The answer is finite-positive for the audited linear/projective
stack, with a clean nonlinear obstruction that must not be overclaimed.

The language boundary remains strict. This is not a negative-mass, shielding,
propulsion, reactionless-force, or physical signed-gravity claim.

## Carrier Retention

The retained gravity stack already has a tensor source-to-channel map in
[`TENSOR_SOURCE_MAP_ETA_NOTE.md`](TENSOR_SOURCE_MAP_ETA_NOTE.md), with runner
[`../scripts/frontier_tensor_source_map_eta.py`](../scripts/frontier_tensor_source_map_eta.py).

That map is the restricted Jacobian:

```text
eta = d(G_0i, G_ij^TF) / d(eps_vec, eps_tf).
```

The new signed transport audit reuses that retained map and checks:

- exact local `O_h` class: rank two;
- finite-rank class: rank two;
- tensor probes are scalar-Schur-action blind;
- mixed vector/tensor probes are locally additive;
- the carrier is non-scalar, not an `A1` relabel.

Representative readout:

```text
dets={'O_h': '1.629e-04', 'finite_rank': '2.014e-04'}
min_svs={'O_h': '4.440e-03', 'finite_rank': '4.049e-03'}
scalar_blind=True
additive=True
```

This proves the ordinary tensor carrier is retained on the audited restricted
classes. It does not prove full continuum GR.

## Transport Theorem

Let:

```text
L = Or(Det_APS D_Y)
E_T = ordinary retained tensor-source bundle
T_plus in E_T
chi_eta in Gamma(L), chi_eta = +/-1 on gapped components
```

Then the oriented tensor source is a section of:

```text
L tensor E_T.
```

On a gapped component, `chi_eta` is locally constant. Therefore every linear
transport map `R` and projective pushforward `P` on the ordinary tensor bundle
commutes with the twist:

```text
R(chi_eta T_plus) = chi_eta R(T_plus)
P(chi_eta T_fine) = chi_eta P(T_fine).
```

The finite harness checks this on orientation-preserving refinements and
unitary family relabelings:

```text
+1x1:eta=+1,chi=+1
+1x2:eta=+2,chi=+1
+1x3:eta=+3,chi=+1
+1x5:eta=+5,chi=+1
-1x1:eta=-1,chi=-1
-1x2:eta=-2,chi=-1
-1x3:eta=-3,chi=-1
-1x5:eta=-5,chi=-1
max_commute_resid=5.5e-16
```

## Projective Response

The normalized refinement injection preserves cylindrical tensor response:

```text
max_projected_field_resid=1.1e-15
max_pair_observable_err=1.8e-15
```

So at the finite projective level:

- the signed tensor field projects back to the same coarse response;
- the four-pair signed response bilinear is refinement-stable;
- null sectors remain zero;
- the sign is transported as a local system, not reinserted by hand.

## Linear Constraint Transport

For a linear Ward/Bianchi-like constraint:

```text
C T_plus = 0,
```

the transported fine constraint is:

```text
C_f = C P.
```

Then:

```text
C_f R(chi_eta T_plus) = chi_eta C T_plus = 0.
```

Harness readout:

```text
max_transported_constraint_resid=9.9e-16
```

This closes the finite linear/projective transport gate.

## Nonlinear Gate

The nonlinear gate is deliberately not closed.

A linear operator is odd under the branch flip:

```text
K(-h) = -K(h).
```

But an Einstein-like local expansion contains even nonlinear jets:

```text
E(h) = K h + Q(h,h) + ...
```

Then:

```text
E(-h) + E(h) = 2 Q(h,h) + ...
```

The finite audit exposes this obstruction:

```text
linear_odd_resid=0.0e+00
nonlinear_even_resid=2.797e+01
expected_even=2.797e+01
```

So the signed tensor-source lift cannot be promoted by the naive rule
`h -> -h`. A full nonlinear theorem must be a graded localization theorem for
the Einstein operator over:

```text
ordinary even jets plus L-valued odd/source jets.
```

Until that theorem exists, nonlinear signed tensor dynamics remain
conditional.

## Continuum/Graded Follow-Up

The continuum-family and graded nonlinear pass is now recorded in
[`SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md`](SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_NOTE.md)
with runner
[`../scripts/signed_gravity_continuum_graded_einstein_localization.py`](../scripts/signed_gravity_continuum_graded_einstein_localization.py).

Result:

```text
FINAL_TAG: SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
```

That pass replaces the naive nonlinear sign flip by a graded formal Einstein
jet:

```text
H_chi(eps) = eps chi h_1 + eps^2 h_2 + eps^3 chi h_3 + ...
```

Odd jets are `L`-valued and flip; even backreaction jets are ordinary and do
not. This resolves the finite even-jet obstruction at formal/local level,
while leaving global nonlinear PDE existence outside the claim.

## Harness Result

Command:

```bash
python3 scripts/signed_gravity_tensor_source_transport_retention.py
```

Result:

```text
[PASS] retained gravity stack has an ordinary rank-two tensor source carrier
[PASS] orientation-line twist commutes with finite family/refinement transport
[PASS] projective cylindrical tensor response is refinement-stable
[PASS] linear Ward/Bianchi-like constraints transport with the twist
[PASS] nonlinear gate exposes even-jet obstruction to naive sign-flip closure
[PASS] non-claim gate remains closed
FINAL_TAG: SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL
```

## Boundary Verdict

The current tensor-source status is:

```text
SIGNED_GRAVITY_TENSOR_SOURCE_TRANSPORT_RETENTION_FINITE_CONDITIONAL
```

This is stronger than the previous oriented lift: the ordinary tensor carrier
is retained on the audited restricted gravity classes, and the signed twist is
finite-projectively portable. The subsequent continuum/graded note discharges
the next local/formal version of the target:

```text
SIGNED_GRAVITY_CONTINUUM_GRADED_EINSTEIN_LOCALIZATION_FORMAL_THEOREM
```

Global nonlinear PDE existence remains outside both notes.

No physical signed-gravity claim follows from this note.
