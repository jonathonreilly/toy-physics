# Koide Q gauge-orbit projection label no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_gauge_orbit_projection_label_no_go.py`  
**Status:** no-go; retained gauge/Reynolds projection does not erase the
central label source

## Theorem Attempt

Treat the retained `C3/D3` generation symmetry as a gauge redundancy and project
physical sources to the gauge-invariant subalgebra.  If this projection erased:

```text
Z = P_plus - P_perp,
```

then the physical source would be forced to the scalar quotient and `K_TL=0`.

## Result

Negative under current retained structure.

The retained normalizer group:

```text
D3 = <C,F>
```

fixes the two central projectors separately:

```text
g P_plus g^-1 = P_plus
g P_perp g^-1 = P_perp.
```

Therefore:

```text
g Z g^-1 = Z.
```

The Reynolds projection of `Z` is exactly `Z`, not zero.

## Projected Source Algebra

For an arbitrary local source `X`, the retained `D3` Reynolds projection lands
in:

```text
R_D3(X) = alpha P_plus + beta P_perp.
```

Equivalently:

```text
R_D3(X) = ((alpha+beta)/2) I + ((alpha-beta)/2) Z.
```

Trace normalization removes the `I` part, but leaves the `Z` coefficient:

```text
(alpha-beta)/2.
```

No gauge projection identity forces `alpha=beta`.

## Counterstate

The source state:

```text
w = 1/3
```

is already gauge invariant and is preserved by the projection, but gives:

```text
Q = 1
K_TL = 3/8.
```

So gauge invariance admits both closing and non-closing center states.

## Residual

```text
RESIDUAL_SCALAR = gauge_invariant_Z_source_coefficient_equiv_K_TL
RESIDUAL_LABEL = Z_survives_retained_gauge_orbit_projection
RESIDUAL_PRIMITIVE =
  derive_physical_law_excluding_gauge_invariant_Z_source
```

## Hostile Review

- **Target import:** none.  The Koide value appears only as the conditional
  consequence of the midpoint source.
- **External empirical input:** none.
- **Hidden source-free law:** not promoted.
- **Missing axiom link:** exact.  Gauge projection keeps invariant data, and
  `Z` is invariant.
- **Closure claim:** rejected.  The runner prints
  `Q_GAUGE_ORBIT_PROJECTION_LABEL_CLOSES_Q=FALSE`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_gauge_orbit_projection_label_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
PASSED: 14/14
KOIDE_Q_GAUGE_ORBIT_PROJECTION_LABEL_NO_GO=TRUE
Q_GAUGE_ORBIT_PROJECTION_LABEL_CLOSES_Q=FALSE
RESIDUAL_SCALAR=gauge_invariant_Z_source_coefficient_equiv_K_TL
RESIDUAL_LABEL=Z_survives_retained_gauge_orbit_projection
RESIDUAL_PRIMITIVE=derive_physical_law_excluding_gauge_invariant_Z_source
```

## Consequence

The gauge-projection route reduces to the same final obstruction: derive a
physical law excluding the retained, gauge-invariant central label source
`Z=P_plus-P_perp`, or derive a law setting its coefficient to zero.
