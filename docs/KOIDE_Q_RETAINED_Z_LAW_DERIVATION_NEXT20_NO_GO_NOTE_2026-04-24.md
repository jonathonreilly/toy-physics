# Koide Q Retained Z-Law Derivation Next-20 No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_retained_z_law_derivation_next20_no_go.py`  
**Status:** twenty-route executable no-go; Q remains open

## Purpose

Try to derive the missing retained law directly:

```text
forbid ell*z,
make Z=P_plus-P_perp non-source-visible,
or retain a genuine plus/perp mixer.
```

Any one of those would turn zero-background from a coordinate choice into a
theorem and would conditionally close the Q bridge.

## Twenty Attempts

1. Full retained `C3` centralizer.
2. Self-adjoint retained dynamics.
3. Concrete plus/perp mixer obstruction.
4. Local polynomial dynamics `f(C)`.
5. Invariant-polynomial ring on the source coordinate.
6. Character-charge selection.
7. Spurion inversion under `Z` parity.
8. Grade involution.
9. Real/CP structure.
10. Time reversal / Hermiticity.
11. Detailed-balance rates.
12. Disconnected retained Markov dynamics.
13. Radiative beta function for `ell`.
14. Technical naturalness of `ell=0`.
15. Integrating out retained singlet data.
16. Source grammar closure under central sums.
17. Convex source potential.
18. Ward identity on an invariant scalar.
19. Quotient completion.
20. Conditional positive theorem boundary.

## Result

No retained-only closure.  The exact obstruction is:

```text
Z is a retained C3-trivial source coordinate.
The C3 commutant has no plus/perp cross block.
The linear source ell*z is symmetry-allowed.
ell=0 is not protected without adding Z parity or a quotient law.
Detailed balance closes only after equal cross-rates/mixer data are supplied.
Radiative or tadpole terms can regenerate ell.
Trace normalization removes aI but keeps bZ.
```

The exact retained counterbackground remains:

```text
V(z) = ell*z + m*z^2
ell = 2/3
m = 1
z* = -1/3
Q = 1
K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR=derive_retained_law_for_ell_zero_Z_invisibility_or_plus_perp_mixer
RESIDUAL_SOURCE=C3_trivial_Z_allows_linear_ell_z_and_no_retained_mixer
COUNTERBACKGROUND=z_minus_1_over_3_from_ell_2_over_3_m_1
```

## Hostile Review

This no-go does not rename the missing law as a theorem.  The parity,
quotient, equal-rate, and mixer branches are only conditional support unless
one is derived from retained charged-lepton structure.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_retained_z_law_derivation_next20_no_go.py
python3 -m py_compile scripts/frontier_koide_q_retained_z_law_derivation_next20_no_go.py
```

Expected closeout:

```text
KOIDE_Q_RETAINED_Z_LAW_DERIVATION_NEXT20_NO_GO=TRUE
Q_RETAINED_Z_LAW_DERIVATION_NEXT20_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_ELL_ZERO_Z_QUOTIENT_OR_PLUS_PERP_MIXER_IS_RETAINED=TRUE
```
