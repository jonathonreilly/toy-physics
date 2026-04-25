# Koide Q Z-Sign / Zero-Section Next-20 No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_z_sign_zero_section_next20_no_go.py`  
**Status:** twenty-route executable no-go; Q remains open

## Purpose

Attack the current live path:

```text
derive a retained reason that the Z sign/exchange or the source-fibre zero
section is physical.
```

The target is still:

```text
z = <Z> = 0
-> K_TL = 0
-> Q = 2/3.
```

## Twenty Attacks

1. Retained label-preserving naturality.
2. `Z` sign/exchange.
3. Affine kernel shear.
4. Total-scale covariance.
5. Additivity/linearity.
6. Total-zero object/base fibre.
7. Positivity.
8. Complete-positive center state.
9. Entropy/anonymous prior.
10. Least-`Z` norm.
11. Legendre/sign self-duality.
12. Zero-probe source-response.
13. Real structure.
14. `Cl(3)` grade parity.
15. `C3` Reynolds/gauge projection.
16. Stable Morita normalization.
17. Quotient universal property.
18. Exact-sequence splitting uniqueness.
19. Deleting retained labels.
20. Coupling to delta/basepoint zero.

## Result

No retained-only closure.  The affine source sections remain:

```text
s_a(t) = (t, a t).
```

The exact retained countersection is:

```text
a = -1/3
z = -1/3
Q = 1
K_TL = 3/8.
```

The routes that close Q all add one of the same missing laws:

```text
retained_Z_sign_exchange
anonymous_label_quotient
least_Z_source_norm
physical_background_zero
fibre_constant_source_functor
```

Each is equivalent, for Q purposes, to choosing the physical source-domain
quotient or zero section.

## Residual

```text
RESIDUAL_SCALAR=derive_retained_Z_sign_exchange_or_source_fibre_zero_section
RESIDUAL_SOURCE=label_preserving_affine_sections_s_a_remain_free
COUNTERSECTION=s_a_with_a_minus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_z_sign_zero_section_next20_no_go.py
python3 -m py_compile scripts/frontier_koide_q_z_sign_zero_section_next20_no_go.py
```
