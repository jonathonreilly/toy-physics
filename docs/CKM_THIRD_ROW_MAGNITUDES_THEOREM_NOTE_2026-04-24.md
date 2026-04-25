# CKM Third-Row Magnitudes Structural Identities

**Date:** 2026-04-24

**Status:** retained structural-identity subtheorem of the promoted CKM
atlas/axiom package. This note packages the third-row atlas-leading magnitude
identities carried by the same Wolfenstein and CP-plane surface named in
[`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
and
[`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md).

**Primary runner:** `scripts/frontier_ckm_third_row_magnitudes.py`

## Statement

On the promoted CKM atlas surface,

```text
lambda^2 = alpha_s(v)/2,
A^2      = 2/3,
rho      = 1/6,
eta^2    = 5/36.
```

The atlas-leading third-row Wolfenstein magnitudes obey

```text
(R1) |V_td|_0^2 = A^2 lambda^6 ((1-rho)^2 + eta^2)
                 = (5/72) alpha_s(v)^3,

(R2) |V_ts|_0^2 = A^2 lambda^4
                 = (1/6) alpha_s(v)^2,

(R3) |V_tb|_0^2 = 1 - |V_td|_0^2 - |V_ts|_0^2.
```

The subscript `0` marks the atlas-leading Wolfenstein surface. The parent CKM
atlas still carries the finite-`lambda` exact standard-matrix readout; this
note does not promote the monomial formulas as all-orders CKM matrix entries.

## Derivation

The only new algebra is the third-row distance factor:

```text
(1-rho)^2 + eta^2
  = (5/6)^2 + 5/36
  = 25/36 + 5/36
  = 5/6.
```

Then

```text
|V_td|_0^2
  = (2/3) (alpha_s(v)/2)^3 (5/6)
  = (5/72) alpha_s(v)^3.
```

Similarly,

```text
|V_ts|_0^2
  = (2/3) (alpha_s(v)/2)^2
  = alpha_s(v)^2 / 6.
```

Finally, third-row unitarity fixes the leading atlas row completion:

```text
|V_tb|_0^2 = 1 - alpha_s(v)^2/6 - 5 alpha_s(v)^3/72.
```

## Numerical Read

At the canonical plaquette/CMT coupling,

```text
alpha_s(v) = 0.103303816122267...
```

the atlas-leading third row is

| quantity | atlas-leading expression | value |
|---|---:|---:|
| `|V_td|_0` | `sqrt(5/72) alpha_s(v)^(3/2)` | `0.0087497` |
| `|V_ts|_0` | `alpha_s(v)/sqrt(6)` | `0.0421736` |
| `|V_tb|_0` | `sqrt(1-alpha_s(v)^2/6-5 alpha_s(v)^3/72)` | `0.999072` |

The exact standard-matrix readout from the parent atlas parameters gives the
finite-`lambda` guardrail

| quantity | exact standard-matrix readout | note |
|---|---:|---|
| `|V_td|` | `0.0087503` | very close to the atlas-leading monomial |
| `|V_ts|` | `0.0414407` | finite-`lambda` correction is visible at the percent level |
| `|V_tb|` | `0.999103` | close to the atlas-leading unitarity completion |

This distinction is deliberate. The retained theorem content is the compact
third-row atlas identity surface, with the exact standard-matrix values kept
as the parent CKM readout and guardrail.

## Relationship To The Existing CKM Package

Together with the previously named CKM subtheorems, the promoted CKM atlas now
has named structural rows for:

```text
lambda^2 = alpha_s(v)/2,
A^2 = 2/3,
rho = 1/6,
eta = sqrt(5)/6,
cos^2(delta_CKM) = 1/6,
atlas alpha_0 = 90 deg,
|V_cb|_0^2 = alpha_s(v)^2/6,
|V_ub|_0^2 = alpha_s(v)^3/72,
|V_td|_0^2 = 5 alpha_s(v)^3/72,
|V_ts|_0^2 = alpha_s(v)^2/6.
```

This completes the named leading atlas-magnitude bookkeeping without adding
quark-mass inputs or fitted CKM observables.

## Boundary

This note claims:

- the atlas-leading identities `(R1)` through `(R3)`;
- the exact rational coefficient `5/72` for the `V_td` leading term;
- the leading degeneracy `|V_ts|_0^2 = |V_cb|_0^2 = alpha_s(v)^2/6`;
- a finite-`lambda` guardrail showing where the exact standard-matrix readout
  differs from the leading monomial surface.

This note does **not** claim:

- a new derivation of `alpha_s(v)`;
- independence from the parent CKM atlas/axiom package;
- that the leading monomial formulas are exact all-orders standard-matrix CKM
  entries;
- quark masses, hadronic matrix elements, or BSM flavor extensions.

## Reproduction

```bash
python3 scripts/frontier_ckm_third_row_magnitudes.py
```

Expected final flags:

```text
CKM_THIRD_ROW_ATLAS_IDENTITIES_RETAINED=TRUE
CKM_THIRD_ROW_EXACT_ALL_ORDERS_MONOMIAL_CLAIM=FALSE
```

## Cross-References

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
