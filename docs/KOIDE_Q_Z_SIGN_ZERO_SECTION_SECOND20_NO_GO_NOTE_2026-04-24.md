# Koide Q Z-Sign / Zero-Section Second-20 No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_z_sign_zero_section_second20_no_go.py`  
**Status:** second twenty-route executable no-go; Q remains open

## Purpose

Attack the narrowed live path:

```text
derive a retained reason that Z -> -Z or the source-fibre zero section is
physical.
```

This second batch focuses on retained symmetry, representation, stable
Morita/K-theory, Frobenius/category, and field-theory mechanisms.  The target
remains the missing source-domain law:

```text
z = <Z> = 0
-> K_TL = 0
-> Q = 2/3.
```

## Theorem Attempt

Maybe full retained structure beyond the affine exact sequence makes the
singlet and real nontrivial `C3` sectors exchangeable or makes the zero
`Z` source section canonical.  If so, representation/category naturality could
derive the physical zero section rather than adding it.

## Twenty Attacks

1. Full `S3` permutation symmetry.
2. Dihedral normalizer of the `C3` axis.
3. `Aut(C3)` inversion.
4. Galois conjugation.
5. Character orthogonality.
6. Burnside/orbit averaging.
7. Real representation-ring dimension map.
8. Stable `K0` of the semisimple center.
9. Fixed total dimension.
10. Adams operation `psi_2`.
11. Frobenius/counit family.
12. Categorical/Hilbert dimension.
13. Monoidal unit.
14. Karoubi/idempotent completion.
15. Schur-lemma commutant.
16. Noether/Ward data without a plus/perp mixer.
17. Anomaly blindness in the `Z` direction.
18. Reflection/state positivity.
19. KMS/detailed balance on disconnected sectors.
20. Equivariant RG flow.

## Result

No retained-only closure.  The tested mechanisms either:

```text
fix P_plus and P_perp separately,
permute only the two complex nontrivial characters inside P_perp,
preserve two central source coefficients,
or make z=0 invariant without forcing the initial source to lie there.
```

The exact retained countersection remains:

```text
z = -1/3
Q = 1
K_TL = 3/8.
```

## Residual

```text
RESIDUAL_SCALAR=derive_retained_exchange_between_trivial_and_real_nontrivial_sector_or_zero_Z_section
RESIDUAL_SOURCE=representation_category_preserves_Z_label
COUNTERSECTION=z_minus_1_over_3_Q_1_K_TL_3_over_8
```

## Hostile Review

The runner does not promote a conditional support identity as closure.  The
only positive statement is conditional: Q would close if a retained theorem
made the trivial and real nontrivial sectors source-exchangeable or selected
the zero `Z` source section.  The audit finds no such retained theorem in this
batch.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_z_sign_zero_section_second20_no_go.py
python3 -m py_compile scripts/frontier_koide_q_z_sign_zero_section_second20_no_go.py
```

Expected closeout:

```text
KOIDE_Q_Z_SIGN_ZERO_SECTION_SECOND20_NO_GO=TRUE
Q_Z_SIGN_ZERO_SECTION_SECOND20_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_TRIVIAL_STANDARD_EXCHANGE_OR_ZERO_SECTION_IS_RETAINED=TRUE
```
