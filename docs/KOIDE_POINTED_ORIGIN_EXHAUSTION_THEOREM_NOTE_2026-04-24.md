# Koide pointed-origin exhaustion theorem

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_pointed_origin_exhaustion_theorem.py`
**Status:** exhaustive residual theorem; not full retained closure

## Question

Can the current retained source/boundary data, without a pointed origin law,
force the simultaneous closing representative:

```text
source origin = 0
CP1 selector descends/is absent
endpoint torsor basepoint = 0
```

## Theorem

Within the current Koide residual atlas, no.

The retained unpointed tests are invariant under three residual freedoms:

```text
Q source-response:
  source-origin translation

Brannen endpoint:
  CP1 line choice inside the rank-two real primitive

open determinant endpoint:
  endpoint torsor translation
```

Those freedoms preserve the unpointed retained data but change the open
charged-lepton readouts.  Therefore an origin-free retained theorem cannot
select the closing representative.  The exact next positive theorem is:

```text
retained_pointed_source_boundary_origin_law
```

## Proof Sketch

### Q source origin

On the normalized response slice:

```text
Y = (1+a, 1-a)
```

the Koide value occurs only at:

```text
a = 0.
```

Any finite polynomial invariant under source-origin translation is constant:

```text
P(a+r) = P(a)  =>  P is constant.
```

So unpointed source data cannot select `a = 0`.

### Brannen CP1 selector

On the real nontrivial `Z3` primitive, the only trace-one symmetric mark
commuting with the retained `120 degree` rotation is:

```text
I/2.
```

It is scalar and not a rank-one projector.  Scalar retained marks have the
same expectation value on every CP1 line.  A physical CP1 line angle therefore
remains extra boundary data unless a descent/absence theorem removes it.

### Endpoint torsor

The open endpoint coordinate:

```text
R_c(phi) = phi + c
```

is a torsor before a unit basepoint is selected.  Differences and affine
gluing are invariant under `c` translation, and finite polynomial invariants
of that translation action are constant.  Thus unpointed determinant/Pfaffian
line data cannot force `c = 0`.

## Countermodels

The runner exhibits retained-equivalent unpointed countermodels:

```text
a = 1/3
alpha = pi/4
c = 1/7
```

which preserve the unpointed tests but change the open readouts:

```text
Q != 2/3
delta != 2/9.
```

It also records a target-cancellation warning:

```text
alpha = pi/4
c = eta_APS sin(alpha)^2
```

can reproduce `delta = eta_APS` while retaining a spectator channel.  That is
value fitting/cancellation, not native closure.

## Exact Closeout

The exhaustion theorem proves:

```text
POINTED_ORIGIN_LAW_WOULD_CLOSE_DIMENSIONLESS_LANE = TRUE
POINTED_ORIGIN_LAW_IS_NECESSARY_WITHIN_RESIDUAL_ATLAS = TRUE
RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN = FALSE
```

It does **not** prove the missing positive law:

```text
KOIDE_DIMENSIONLESS_LANE_CLOSED_BY_THIS_RUNNER = FALSE
```

## Falsifiers

- A retained non-scalar boundary mark on the Brannen rank-two primitive.
- A retained proof that CP1 selected-line data are gauge/coordinate-only.
- A retained proof that neutral source translations are not physical
  charged-lepton source coordinates.
- A retained identity/unit theorem for the open determinant endpoint torsor.
- Any retained invariant that is not constant on the residual fibre and
  selects the closing representative without importing the target value.

## Verification

Run:

```bash
python3 scripts/frontier_koide_pointed_origin_exhaustion_theorem.py
python3 scripts/frontier_koide_pointed_origin_lattice_axiom_derivation.py
python3 scripts/frontier_koide_pointed_origin_lattice_axiom_nature_review.py
python3 scripts/frontier_koide_dimensionless_lane_pointed_origin_closure_packet.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_POINTED_ORIGIN_EXHAUSTION_THEOREM=TRUE
RETAINED_UNPOINTED_DATA_FORCE_POINTED_ORIGIN=FALSE
POINTED_ORIGIN_LAW_WOULD_CLOSE_DIMENSIONLESS_LANE=TRUE
POINTED_ORIGIN_LAW_IS_NECESSARY_WITHIN_RESIDUAL_ATLAS=TRUE
KOIDE_DIMENSIONLESS_LANE_CLOSED_BY_THIS_RUNNER=FALSE
RESIDUAL_PRIMITIVE=retained_pointed_source_boundary_origin_law
```
