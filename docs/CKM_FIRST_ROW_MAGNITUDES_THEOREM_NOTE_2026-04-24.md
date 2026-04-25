# CKM First-Row Atlas-Leading Magnitudes Structural Identities

**Date:** 2026-04-24

**Status:** retained structural-identity subtheorem of the promoted CKM
atlas/axiom package. This note packages the first-row atlas-leading magnitude
identities carried by the same Wolfenstein and CP-plane surface named in
[`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
and
[`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md).
It is the first-row companion to
[`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md).

**Primary runner:** `scripts/frontier_ckm_first_row_magnitudes.py`

## Statement

On the promoted CKM atlas surface,

```text
lambda^2 = alpha_s(v)/2,
A^2      = 2/3,
rho      = 1/6,
eta^2    = 5/36,
rho^2 + eta^2 = 1/6.
```

The atlas-leading first-row Wolfenstein magnitudes obey

```text
(F1) |V_us|_0^2 = lambda^2
                 = alpha_s(v)/2,

(F2) |V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2)
                 = alpha_s(v)^3/72,

(F3) |V_ud|_0^2 = 1 - |V_us|_0^2 - |V_ub|_0^2
                 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72.
```

The subscript `0` marks the atlas-leading Wolfenstein surface. The parent CKM
atlas still carries the finite-`lambda` exact standard-matrix readout; this
note does not promote the leading monomial formulas as all-orders CKM matrix
entries.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Parent CKM atlas/axiom surface | [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho^2 + eta^2 = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Canonical `alpha_s(v)` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| First-row normalization on the atlas-leading surface | parent CKM atlas package |

No observed CKM matrix element, quark mass, or fitted flavor observable enters
these identities.

## Derivation

The retained leading Wolfenstein forms on the parent atlas surface give

```text
|V_us|_0 = lambda,
|V_ub|_0 = A lambda^3 sqrt(rho^2 + eta^2).
```

Squaring and substituting the retained inputs gives

```text
|V_us|_0^2 = alpha_s(v)/2,
```

and

```text
|V_ub|_0^2
  = (2/3) (alpha_s(v)/2)^3 (1/6)
  = alpha_s(v)^3/72.
```

The atlas-leading first-row completion is then fixed by row normalization:

```text
|V_ud|_0^2
  = 1 - |V_us|_0^2 - |V_ub|_0^2
  = 1 - alpha_s(v)/2 - alpha_s(v)^3/72.
```

No separate `|V_ud|` input is added.

## Numerical Read

At the canonical plaquette/CMT coupling,

```text
alpha_s(v) = 0.103303816122267...
```

the atlas-leading first row is

| quantity | atlas-leading expression | value |
|---|---:|---:|
| `|V_ud|_0` | `sqrt(1-alpha_s(v)/2-alpha_s(v)^3/72)` | `0.9738238` |
| `|V_us|_0` | `sqrt(alpha_s(v)/2)` | `0.2272706` |
| `|V_ub|_0` | `alpha_s(v)^(3/2)/(6 sqrt(2))` | `0.0039130` |

The exact standard-matrix readout from the parent atlas parameters gives the
finite-`lambda` guardrail

| quantity | exact standard-matrix readout | note |
|---|---:|---|
| `|V_ud|` | `0.9738242` | differs from `|V_ud|_0` only at the product `lambda^2 |V_ub|_0^2` level |
| `|V_us|` | `0.2272688` | includes the finite `c_13` factor |
| `|V_ub|` | `0.0039130` | equal to the atlas `s_13` input |

This distinction is deliberate. The retained theorem content is the compact
first-row atlas-leading identity surface, with the exact standard-matrix values
kept as the parent CKM readout and guardrail.

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
|V_us|_0^2 = alpha_s(v)/2,
|V_ub|_0^2 = alpha_s(v)^3/72,
|V_ud|_0^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3/72,
|V_cb|_0^2 = alpha_s(v)^2/6,
|V_td|_0^2 = 5 alpha_s(v)^3/72,
|V_ts|_0^2 = alpha_s(v)^2/6.
```

The second row remains controlled by the parent finite-`lambda` standard-matrix
readout and is not repackaged here as a standalone monomial theorem.

## Boundary

This note claims:

- the atlas-leading identities `(F1)` through `(F3)`;
- the exact rational coefficient `1/72` for the `V_ub` squared leading term;
- the first-row atlas-leading row completion for `|V_ud|_0^2`;
- a finite-`lambda` guardrail showing where the exact standard-matrix readout
  differs from the leading surface.

This note does **not** claim:

- a new derivation of `alpha_s(v)`;
- independence from the parent CKM atlas/axiom package;
- that the leading formulas are exact all-orders standard-matrix CKM entries;
- a beta-decay nuclear-physics extraction of `|V_ud|`;
- quark mass-ratio closure, hadronic matrix elements, or BSM flavor
  extensions.

## Reproduction

```bash
python3 scripts/frontier_ckm_first_row_magnitudes.py
```

Expected final flags:

```text
CKM_FIRST_ROW_ATLAS_IDENTITIES_RETAINED=TRUE
CKM_FIRST_ROW_EXACT_ALL_ORDERS_MONOMIAL_CLAIM=FALSE
```

## Cross-References

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
