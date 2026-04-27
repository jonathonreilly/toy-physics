# CKM Second-Row Magnitudes Structural Identities Theorem

**Date:** 2026-04-25

**Status:** proposed_retained structural-identity subtheorem of the proposed_promoted CKM
atlas/axiom package. Companion to the mainline
[`CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md),
[`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
and parent CKM package. This note closes the second row of the
leading-Wolfenstein structural CKM-magnitude surface.

**Primary runner:** `scripts/frontier_ckm_second_row_magnitudes.py`

## Statement

On the retained CKM atlas/axiom surface, with the retained Wolfenstein
parameters

```text
lambda^2 = alpha_s(v) / 2,
A^2      = 2/3,
```

the leading-Wolfenstein second-row magnitudes are

```text
(M1)  |V_cd|^2 = lambda^2                                = alpha_s(v) / 2,
(M2)  |V_cb|^2 = A^2 lambda^4                             = alpha_s(v)^2 / 6,
(M3)  |V_cs|^2 = 1 - |V_cd|^2 - |V_cb|^2
              = 1 - alpha_s(v)/2 - alpha_s(v)^2 / 6.
```

(M3) is enforced by exact CKM unitarity once (M1) and (M2) are accepted on
the retained atlas surface.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Parent CKM atlas/axiom surface | [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| Canonical `alpha_s(v)` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| Exact CKM unitarity | parent CKM atlas package |

## Derivation

The retained Wolfenstein expansion gives the leading-Wolfenstein forms

```text
V_cd = -lambda + O(lambda^5),
V_cb =  A lambda^2 + O(lambda^8),
V_cs = 1 - lambda^2/2 + O(lambda^4).
```

Squaring and substituting `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3`:

```text
|V_cd|^2 = lambda^2          = alpha_s(v) / 2,
|V_cb|^2 = A^2 lambda^4      = (2/3) (alpha_s(v)/2)^2 = alpha_s(v)^2 / 6.
```

Exact second-row unitarity gives

```text
|V_cd|^2 + |V_cs|^2 + |V_cb|^2 = 1,
```

and (M3) follows by subtraction.

## Cabibbo and Third-Row Equivalences

Together with the retained first-row and third-row companions:

```text
|V_cd|^2 = |V_us|^2     = alpha_s(v) / 2     (Cabibbo equivalence at leading order),
|V_cb|^2 = |V_ts|^2     = alpha_s(v)^2 / 6   (third-row leading equivalence).
```

These are leading-Wolfenstein equivalences only. Higher-order corrections
distinguish `|V_cd|` from `|V_us|` at `O(lambda^4)` and `|V_cb|` from
`|V_ts|` at `O(lambda^4)`, but those corrections lie outside the retained
leading-Wolfenstein scope.

## Canonical Numerical Read

With the canonical `alpha_s(v) = 0.103303816...`:

| Quantity | Structural form | Canonical value |
| --- | --- | ---: |
| `|V_cd|^2` | `alpha_s(v)/2` | `0.0516519` |
| `|V_cd|` | `sqrt(alpha_s(v)/2)` | `0.2272706` |
| `|V_cb|^2` | `alpha_s(v)^2/6` | `0.001778` |
| `|V_cb|` | `alpha_s(v)/sqrt(6)` | `0.0421736` |
| `|V_cs|^2` | `1 - alpha_s(v)/2 - alpha_s(v)^2/6` | `0.946570` |
| `|V_cs|` | sqrt of above | `0.972918` |

Cross-check against PDG 2024:

| Quantity | Framework | PDG 2024 | Deviation |
| --- | ---: | ---: | ---: |
| `|V_cd|` | `0.22727` | `0.22500 +/- 0.00400` | `+1.0%` |
| `|V_cs|` | `0.97292` | `0.99700 +/- 0.01100` | `-2.4%` |
| `|V_cb|` | `0.04217` | `0.04100 +/- 0.00140` | `+2.9%` |

The `|V_cs|` line is a post-derivation direct-extraction comparator, not an
input. The retained theorem is the atlas-leading row-unitarity identity; it
does not claim a hadronic semileptonic extraction or use the direct `|V_cs|`
number to tune the row.

## Combined CKM Magnitude Surface

Combined with the retained Wolfenstein, CP-phase, first-row, third-row, and
parent CKM atlas package, every leading-Wolfenstein squared magnitude on the
retained atlas surface is now packaged:

| Element | Structural identity | Order in `alpha_s(v)` |
| --- | --- | :---: |
| `|V_ud|^2` | `1 - alpha_s/2 - alpha_s^3/72` | leading 1 |
| `|V_us|^2` | `alpha_s/2` | linear |
| `|V_ub|^2` | `alpha_s^3 / 72` | cubic |
| `|V_cd|^2` | `alpha_s/2` (M1, this note) | linear |
| `|V_cs|^2` | `1 - alpha_s/2 - alpha_s^2/6` (M3, this note) | leading 1 |
| `|V_cb|^2` | `alpha_s^2 / 6` (M2, this note) | square |
| `|V_td|^2` | `5 alpha_s^3 / 72` | cubic |
| `|V_ts|^2` | `alpha_s^2 / 6` | square |
| `|V_tb|^2` | `1 - alpha_s^2/6 - 5 alpha_s^3/72` | leading 1 |

Each listed atlas-leading squared magnitude is a rational coefficient times an
integer power of `alpha_s(v)`. Each packaged row sum is forced to one by exact
CKM unitarity.

## Scope

This note claims:

- the leading-Wolfenstein structural identities (M1) and (M2);
- the unitarity-residual identity (M3);
- the Cabibbo and third-row equivalences `|V_cd|^2 = |V_us|^2` and
  `|V_cb|^2 = |V_ts|^2` at leading Wolfenstein order;
- the canonical numerical readout once the retained `alpha_s(v)` is supplied;
- consistency of the framework second-row values with the listed PDG
  comparators at the few-percent leading-Wolfenstein-truncation level.

This note does not claim:

- a new derivation of `alpha_s(v)`;
- closure of higher-order Wolfenstein corrections beyond the parent CKM
  atlas package;
- a quark mass-ratio identity;
- BSM CKM extensions, fourth-generation effects, or PMNS phases;
- a hadronic-physics extraction of `|V_cs|` or `|V_cd|`.

## Reproduction

```bash
python3 scripts/frontier_ckm_second_row_magnitudes.py
```

Expected result:

```text
TOTAL: PASS=25, FAIL=0
```

The runner uses the Python standard library plus the already-mainline
`scripts/canonical_plaquette_surface.py` constants.

## Cross-References

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
  - parent CKM package.
- [`CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  - first-row companion.
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  - third-row companion.
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  - `lambda` and `A` identities.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  - `rho`, `eta`, CP-phase identities.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  - atlas `alpha_0 = 90` triangle companion.
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
  - canonical `alpha_s(v)` input.
