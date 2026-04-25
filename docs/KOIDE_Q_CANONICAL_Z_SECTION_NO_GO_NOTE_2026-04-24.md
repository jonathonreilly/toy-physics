# Koide Q Canonical Z-Section No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_canonical_z_section_no_go.py`  
**Status:** executable no-go for deriving the affine `Z` source-kernel zero
section from retained structure

## Theorem Attempt

Prove that the retained source exact sequence has a canonical zero section:

```text
0 -> span{Z} -> source_total_plus_label -> source_total -> 0.
```

If the physical charged-lepton source fibre had to choose that zero
representative, then:

```text
z = <Z> = 0
-> K_TL = 0
-> Q = 2/3.
```

## Result

No retained-only closure.  Exactness identifies the kernel and its zero
element, but it does not select the zero representative as the physical
background source.

The source sections form a one-parameter family:

```text
s_a(t) = (t, a t).
```

Every `a` is a section of the same projection.  The closing section is the
special case:

```text
a = 0.
```

The retained nonclosing countersection is:

```text
a = -1/3
z = -1/3
Q = 1
K_TL = 3/8.
```

## Candidate Canonicality Tests

- Retained label-preserving naturality supplies no equation on `a`, because
  `P_plus` and `P_perp` carry inequivalent retained labels `{0}` and `{1,2}`.
- A sign/exchange symmetry `z -> -z` would force `a=0`, but that is exactly the
  missing non-retained block exchange/source-invisibility law.
- Full affine-kernel shear invariance gives no invariant section at all; it
  cannot be used as a retained zero-section theorem.
- Positivity gives the interval `-1 <= z <= 1`, not a point.
- Anonymous entropy/midpoint and least-`Z`-norm select `z=0` conditionally, but
  each is an added source law.
- Zero-probe source-response does not set the physical `Z` background to zero.

## Residual

```text
RESIDUAL_SCALAR=derive_retained_canonical_zero_section_for_Z_source_kernel
RESIDUAL_SOURCE=label_preserving_center_allows_nonzero_Z_section
COUNTERSECTION=s_a_with_a_minus_1_over_3_Q_1_K_TL_3_over_8
```

## Verdict

The canonical-zero-section path reduces to the same missing law:

```text
derive physical Z erasure / source-domain quotient / background-zero section.
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_canonical_z_section_no_go.py
python3 -m py_compile scripts/frontier_koide_q_canonical_z_section_no_go.py
```
