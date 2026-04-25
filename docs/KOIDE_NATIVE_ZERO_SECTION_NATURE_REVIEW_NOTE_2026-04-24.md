# Koide native zero-section Nature review

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_native_zero_section_nature_review.py`  
**Status:** passes as the next native route; fails as completed retained/native
closure

## Review Question

Does the native zero-section route close the full dimensionless Koide lane as a
retained/native theorem?

## Verdict

Not yet.  It is the strongest native route found so far, but it still requires
two identification theorems before it is retained closure.

## What Is New

The route stops trying to select a rank-one line inside the nontrivial `Z3`
sector.  Instead it treats the physical Brannen endpoint as the whole real
nontrivial `Z3` primitive.

That matters because the real primitive has no nontrivial equivariant
idempotents:

```text
End_Z3(R^2_nontrivial) = {aI + bJ}
J^2 = -I
idempotents = 0, I.
```

So a native readout on this real primitive has:

```text
spectator = 0.
```

Then a unit-preserving determinant-line endpoint readout gives:

```text
c = 0.
```

Together with the independent APS computation:

```text
eta_APS = 2/9
```

this gives:

```text
delta_open = 2/9.
```

The Q side is the already sharpened native zero-source source-response route:

```text
z = 0 -> K_TL = 0 -> Q = 2/3.
```

## Why This Is Not Yet Closure

The retained Brannen corpus contains both:

```text
real-plane / conjugate-pair geometry
```

and:

```text
selected-line / CP1 / rank-one language.
```

The native route closes only if the second is a coordinate presentation of the
first, not an extra physical rank-one selector.

A hostile reviewer can still ask:

```text
why is the physical Brannen endpoint the whole real primitive,
not a rank-one CP1 line?
```

and:

```text
why is the open determinant endpoint readout unit-preserving/based,
not an unbased torsor coordinate?
```

Those are now the exact native closure obligations.

## Residual

```text
NEXT_NATIVE_THEOREM =
  derive_Brannen_endpoint_as_real_Z3_primitive_and_unit_determinant_readout

RESIDUAL_IDENTIFICATION_DELTA =
  rank_one_CP1_language_vs_real_primitive_endpoint

RESIDUAL_TRIVIALIZATION =
  unit_preserving_open_determinant_line_readout
```

## Falsifiers

- A retained proof that Brannen delta is intrinsically a rank-one CP1 line
  rather than the real nontrivial `Z3` primitive.
- A retained equivariant spectator projector on the real primitive.
- A physical open endpoint observable that is necessarily an unbased torsor.
- A native nonzero charged-lepton source that is not just the selector value in
  source coordinates.

## Verification

Run:

```bash
python3 scripts/frontier_koide_native_zero_section_closure_route.py
python3 scripts/frontier_koide_native_zero_section_nature_review.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_NATIVE_ZERO_SECTION_NATURE_REVIEW=PASS_AS_ROUTE
KOIDE_NATIVE_ZERO_SECTION_RETAINED_CLOSURE=FALSE
NATIVE_ROUTE_CLOSES_CONDITIONALLY=TRUE
NEXT_NATIVE_THEOREM=derive_Brannen_endpoint_as_real_Z3_primitive_and_unit_determinant_readout
```
