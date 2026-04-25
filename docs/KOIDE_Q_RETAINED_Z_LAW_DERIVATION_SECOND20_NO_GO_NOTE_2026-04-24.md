# Koide Q Retained Z-Law Derivation Second-20 No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_retained_z_law_derivation_second20_no_go.py`  
**Status:** second twenty-route executable no-go; Q remains open

## Purpose

Continue deriving the missing retained law:

```text
derive Z parity,
derive a source quotient,
derive equal plus/perp cross-rates,
or derive a retained plus/perp mixer.
```

This pass tests candidate retained structures that could have protected
`ell=0`: lattice parity, CPT/antiunitary conjugation, Fourier duality, taste
amplification, anomaly/BRST, Schwinger-Dyson equations, loop determinants,
RG, KMS/ergodicity, boundary coupling, and cross-sector universality.

## Twenty Attempts

1. Spatial inversion / lattice parity.
2. Orientation-reversing normalizer.
3. CPT/antiunitary conjugation.
4. Fourier diagonalization.
5. Taste or matrix amplification.
6. Retained full determinant loop.
7. Reduced determinant conditional support.
8. Schwinger-Dyson stationarity.
9. RG naturalness.
10. Anomaly matching.
11. BRST exactness.
12. KMS chemical potential.
13. Ergodicity.
14. Detailed balance with unequal rates.
15. Boundary/delta coupling.
16. Cross-sector universality.
17. Superselection lifting.
18. Operational primitive-based readout.
19. Positive convex source potential with tilt.
20. Minimal new-law boundary.

## Result

No retained-only closure.  The exact obstruction is:

```text
parity/CPT/Fourier fix Z rather than sending Z -> -Z;
taste amplification preserves the retained rank ratio;
the full retained determinant generates a linear Z term;
the reduced determinant is conditional support, not yet retained;
Schwinger-Dyson and RG leave ell or z free;
KMS and detailed balance need a mixer or equal cross-rates;
boundary and cross-sector data do not set the Q source scalar.
```

The counterbackground remains:

```text
z = -1/3
Q = 1
K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR=derive_retained_Z_parity_source_quotient_equal_rates_or_mixer
RESIDUAL_SOURCE=retained_structures_fix_Z_or_leave_ell_z_allowed
COUNTERBACKGROUND=z_minus_1_over_3_Q_1_K_TL_3_over_8
```

## Hostile Review

The reduced determinant, ergodicity, primitive readout, and equal-rate branches
are not promoted as closure.  They are conditional support until derived from
retained charged-lepton structure.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_retained_z_law_derivation_second20_no_go.py
python3 -m py_compile scripts/frontier_koide_q_retained_z_law_derivation_second20_no_go.py
```

Expected closeout:

```text
KOIDE_Q_RETAINED_Z_LAW_DERIVATION_SECOND20_NO_GO=TRUE
Q_RETAINED_Z_LAW_DERIVATION_SECOND20_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_Z_PARITY_SOURCE_QUOTIENT_EQUAL_RATES_OR_MIXER_IS_RETAINED=TRUE
```
