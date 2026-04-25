# CKM First-Row Magnitudes Structural Identities Theorem

**Date:** 2026-04-24

**Status:** retained structural-identity subtheorem of the promoted CKM
atlas/axiom package. Companion to
[`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
and to
[`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md).
This note packages the leading-Wolfenstein structural form of the first-row
CKM matrix elements `|V_ud|`, `|V_us|`, `|V_ub|`, and the first-row
unitarity sum, in the same regression-tested style.

**Primary runner:** `scripts/frontier_ckm_first_row_magnitudes.py`

## Statement

On the retained CKM atlas/axiom surface, with the retained Wolfenstein
parameters

```text
lambda^2 = alpha_s(v) / 2,
A^2      = 2/3,
rho      = 1/6,
eta      = sqrt(5)/6,
rho^2 + eta^2 = 1/6,
```

the leading-Wolfenstein first-row magnitudes are

```text
(F1)  |V_us|^2 = lambda^2                                = alpha_s(v) / 2.
(F2)  |V_ub|^2 = A^2 lambda^6 (rho^2 + eta^2)
              = (2/3) (alpha_s(v)/2)^3 (1/6)
              = alpha_s(v)^3 / 72.
(F3)  |V_ud|^2 = 1 - |V_us|^2 - |V_ub|^2
              = 1 - alpha_s(v)/2 - alpha_s(v)^3 / 72.
```

The corresponding magnitudes are

```text
|V_us| = sqrt(alpha_s(v)/2),
|V_ub| = alpha_s(v)^(3/2) / (6 sqrt(2)),
|V_ud| = sqrt(1 - alpha_s(v)/2 - alpha_s(v)^3/72).
```

(F3) is enforced by exact CKM unitarity once (F1) and (F2) are accepted on
the retained atlas surface. It is not an additional dynamical input.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Parent CKM atlas/axiom surface | [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho^2 + eta^2 = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Canonical `alpha_s(v)` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| CKM unitarity | exact CKM unitarity is part of the parent atlas package |

## Derivation

The retained Wolfenstein expansion gives the standard leading-Wolfenstein
forms

```text
|V_us| = lambda,
|V_ub| = A lambda^3 sqrt(rho^2 + eta^2).
```

Squaring and substituting the retained inputs gives (F1) and (F2). Exact
CKM unitarity gives

```text
|V_ud|^2 + |V_us|^2 + |V_ub|^2 = 1,
```

so (F3) follows by subtraction. No separate `|V_ud|` derivation is needed
on the retained CKM atlas surface.

## Canonical Numerical Read

With the canonical `alpha_s(v) = 0.103303816...`:

| Quantity | Structural form | Canonical value |
| --- | --- | ---: |
| `|V_us|^2` | `alpha_s(v)/2` | `0.0516519080611` |
| `|V_us|` | `sqrt(alpha_s(v)/2)` | `0.227270561361` |
| `|V_ub|^2` | `alpha_s(v)^3 / 72` | `1.5311e-5` |
| `|V_ub|` | `alpha_s(v)^(3/2)/(6 sqrt(2))` | `3.913e-3` |
| `|V_ud|^2` | `1 - alpha_s(v)/2 - alpha_s(v)^3/72` | `0.948333` |
| `|V_ud|` | sqrt of above | `0.973824` |

Cross-check against the PDG 2024 CKMfitter readout `|V_ud| = 0.97373(31)`:
deviation `+0.01%`, well within the listed observational error band. The
`|V_us|` and `|V_ub|` values are the same as those carried by the parent
CKM atlas package; they are not new comparators.

## First-Row Unitarity Bookkeeping

The retained sum

```text
|V_ud|^2 + |V_us|^2 + |V_ub|^2 = 1
```

is exact by construction once (F3) is read off as the closed-form residual.
This is a bookkeeping identity on the retained atlas surface, not a separate
test.

A useful simplification is the leading-Wolfenstein expansion

```text
|V_ud|^2 = 1 - alpha_s(v)/2 - alpha_s(v)^3 / 72
        = 1 - lambda^2 - lambda^6 (rho^2 + eta^2)
        ~ 1 - lambda^2     to leading order in lambda^2.
```

The leading deviation from `1` is `lambda^2 = alpha_s(v)/2`, confirming the
Cabibbo intuition that the first-row deficit from `|V_ud|^2` reaches `|V_us|^2`
to leading order, with the cubic `|V_ub|^2` contribution at the
`alpha_s(v)^3/72` level.

## Combined CKM Magnitude Surface

Combined with the retained third-row note, the structural surface of all
nine CKM magnitudes is:

| Element | Structural identity | Order in `alpha_s(v)` |
| --- | --- | :---: |
| `|V_ud|^2` | `1 - alpha_s/2 - alpha_s^3/72` (this note) | leading 1 |
| `|V_us|^2` | `alpha_s/2` | linear |
| `|V_ub|^2` | `alpha_s^3 / 72` | cubic |
| `|V_cd|^2` | `alpha_s/2` (Cabibbo equivalence) | linear |
| `|V_cs|^2` | `1 - alpha_s/2 + O(alpha_s^2)` | leading 1 |
| `|V_cb|^2` | `alpha_s^2 / 6` | square |
| `|V_td|^2` | `5 alpha_s^3 / 72` | cubic |
| `|V_ts|^2` | `alpha_s^2 / 6` | square |
| `|V_tb|^2` | `1 - alpha_s^2/6 - 5 alpha_s^3/72` | leading 1 |

Every leading-Wolfenstein magnitude squared is a rational coefficient times
an integer power of `alpha_s(v)`, with row sums forced to one by exact CKM
unitarity.

## Scope

This note claims:

- the leading-Wolfenstein structural identities (F1) and (F2);
- the unitarity-residual identity (F3);
- the canonical numerical readout for `|V_ud|`, `|V_us|`, `|V_ub|` once the
  retained `alpha_s(v)` is supplied;
- consistency of the framework `|V_ud|` value with the listed PDG comparator.

This note does not claim:

- a new derivation of `alpha_s(v)`;
- closure of higher-order Wolfenstein corrections beyond the parent CKM
  atlas package;
- a quark mass-ratio identity;
- BSM CKM extensions, fourth-generation effects, or PMNS phases;
- a beta-decay nuclear-physics extraction of `|V_ud|`.

## Reproduction

```bash
python3 scripts/frontier_ckm_first_row_magnitudes.py
```

Expected result:

```text
TOTAL: PASS=21, FAIL=0
```

The runner uses the Python standard library plus the already-mainline
`scripts/canonical_plaquette_surface.py` constants.

## Cross-References

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
  - parent CKM package.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  - `rho`, `eta`, CP radius identities.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  - `lambda` and `A` identities.
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  - third-row companion.
- [`CKM_UNITARITY_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_UNITARITY_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  - unitarity-triangle right-angle companion.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  - canonical `alpha_s(v)` input.
