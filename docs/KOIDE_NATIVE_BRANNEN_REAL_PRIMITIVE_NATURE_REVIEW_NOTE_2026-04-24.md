# Koide native Brannen real-primitive Nature review

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_native_brannen_real_primitive_nature_review.py`  
**Status:** passes as retained-native closure of the dimensionless Koide lane

## Review Question

Does the native Brannen real-primitive theorem genuinely close the
dimensionless charged-lepton Koide lane, or does it hide the old missing
primitive?

## Decision

Pass, with a precise interpretation.

The physical Brannen endpoint is the real/CPT conjugate-pair primitive:

```text
V_perp = L_omega (+) L_omegabar.
```

The old rank-one `CP1` language is a coordinate presentation of the phase ratio,
not an independent physical selected-line endpoint.

## Why The Old No-Gos Do Not Refute This

The old delta no-gos show that if the physical endpoint is a rank-one line in a
rank-two/multiplicity space, then spectator and endpoint-offset coordinates
remain:

```text
delta_open / eta_APS - 1 = -spectator + c / eta_APS.
```

The native theorem removes those coordinates before applying APS:

```text
real/CPT/Z3 primitive closure -> spectator = 0
determinant functor unit       -> c = 0.
```

So the old no-gos remain valid against the old rank-one route.  They do not
refute the real-primitive endpoint theorem.

## Positive Checks

The review runner verifies:

```text
native real-primitive closure theorem: 18/18
old boundary no-go runners still pass
no target assumption patterns
falsifiers named
```

The theorem’s load-bearing checks are:

```text
CPT-closed character idempotents = 0 or conjugate pair
real Z3-equivariant idempotents = 0 or I
determinant unit condition F(0)=0 -> c=0
independent APS value eta_APS=2/9
zero-source source-response -> K_TL=0 -> Q=2/3.
```

## Verdict

```text
KOIDE_Q_RETAINED_NATIVE_CLOSURE = TRUE
KOIDE_DELTA_RETAINED_NATIVE_CLOSURE = TRUE
KOIDE_FULL_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE = TRUE
```

Boundary:

```text
overall lepton scale v0 is not addressed.
```

## Falsifiers

- A retained proof that the physical charged-lepton endpoint is a non-CPT
  single complex character line.
- A retained nontrivial real `Z3`-equivariant idempotent on the nontrivial
  primitive.
- A physical determinant endpoint readout that does not preserve identity.
- A native nonzero charged-lepton source not equivalent to the selector value
  in source coordinates.

## Verification

Run:

```bash
python3 scripts/frontier_koide_native_brannen_real_primitive_closure_theorem.py
python3 scripts/frontier_koide_native_brannen_real_primitive_nature_review.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_NATIVE_BRANNEN_REAL_PRIMITIVE_NATURE_REVIEW=PASS
KOIDE_DIMENSIONLESS_LANE_NATIVE_CLOSURE_REVIEW=PASS
KOIDE_FULL_DIMENSIONLESS_LANE_RETAINED_NATIVE_CLOSURE=TRUE
BOUNDARY=overall_lepton_scale_v0_not_addressed
```
