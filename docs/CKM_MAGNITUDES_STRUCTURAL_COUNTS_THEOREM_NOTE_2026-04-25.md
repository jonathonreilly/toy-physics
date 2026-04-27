# CKM Magnitudes Structural Counts Theorem

**Date:** 2026-04-25

**Status:** proposed_retained structural-identity subtheorem of the proposed_promoted CKM
atlas/axiom package. This note packages the five atlas-leading **off-diagonal**
CKM magnitude identities into one structural-counts surface on top of the
already-retained Wolfenstein and CP-plane identities. It does not change the
scope of the parent CKM theorem and it does not promote any cross-sector or
dimension-uniqueness claim.

**Primary runner:** `scripts/frontier_ckm_magnitudes_structural_counts.py`

## Statement

On the retained CKM atlas surface, let

```text
n_pair  = 2,
n_color = 3,
n_quark = n_pair n_color = 6,
lambda^2 = alpha_s(v) / n_pair,
A^2      = n_pair / n_color,
rho      = 1 / n_quark,
eta^2    = (n_quark - 1) / n_quark^2.
```

Then the five atlas-leading off-diagonal squared CKM magnitudes obey

```text
(M1)  |V_us|_0^2 = alpha_s(v) / n_pair                  = alpha_s(v) / 2,

(M2)  |V_cb|_0^2 = alpha_s(v)^2 / (n_pair n_color)      = alpha_s(v)^2 / 6,

(M3)  |V_ts|_0^2 = alpha_s(v)^2 / (n_pair n_color)      = alpha_s(v)^2 / 6,

(M4)  |V_ub|_0^2 = alpha_s(v)^3 / (8 n_color^2)         = alpha_s(v)^3 / 72,

(M5)  |V_td|_0^2 = (n_quark - 1) alpha_s(v)^3 / (8 n_color^2)
                 = 5 alpha_s(v)^3 / 72.
```

The cleanest compact readout is `(M4)`: the `n_pair` factor cancels exactly, so
the smallest atlas-leading CKM magnitude depends only on `alpha_s(v)` and
`n_color` on the retained CKM surface.

## Retained Inputs

| Input | Authority |
| --- | --- |
| Parent CKM atlas/axiom surface | [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md) |
| `lambda^2 = alpha_s(v)/2`, `A^2 = 2/3` | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `rho = 1/6`, `eta^2 = 5/36`, `rho^2 + eta^2 = 1/6` | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Thales relation `R_t^2 = 1 - rho` | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| Canonical `alpha_s(v)` | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |

No PDG CKM observable, quark mass ratio, Koide input, or dimension-color
constraint enters the derivation.

## Derivation

The retained Wolfenstein and CP-plane identities give

```text
lambda^2     = alpha_s(v) / n_pair,
A^2          = n_pair / n_color,
rho          = 1 / n_quark,
rho^2+eta^2  = 1 / n_quark.
```

The first three off-diagonal rows are immediate:

```text
|V_us|_0^2 = lambda^2 = alpha_s(v) / n_pair,

|V_cb|_0^2 = A^2 lambda^4
           = (n_pair / n_color) (alpha_s(v)/n_pair)^2
           = alpha_s(v)^2 / (n_pair n_color),

|V_ts|_0^2 = |V_cb|_0^2
```

at atlas-leading Wolfenstein order.

For `|V_ub|_0^2`, use the retained leading form

```text
|V_ub|_0^2 = A^2 lambda^6 (rho^2 + eta^2).
```

Then

```text
|V_ub|_0^2
  = (n_pair / n_color) (alpha_s(v)/n_pair)^3 (1 / n_quark)
  = (n_pair / n_color) (alpha_s(v)^3 / n_pair^3) (1 / (n_pair n_color))
  = alpha_s(v)^3 / (n_pair^3 n_color^2) * n_pair / n_pair
  = alpha_s(v)^3 / (8 n_color^2),
```

because `n_pair = 2`. This is the exact `n_pair` cancellation.

For `|V_td|_0^2`, use the retained leading form

```text
|V_td|_0^2 = A^2 lambda^6 ((1-rho)^2 + eta^2).
```

The retained Thales surface gives

```text
(1-rho)^2 + eta^2 = 1 - rho = (n_quark - 1) / n_quark.
```

So

```text
|V_td|_0^2
  = A^2 lambda^6 (n_quark - 1)/n_quark
  = (n_quark - 1) alpha_s(v)^3 / (8 n_color^2).
```

For the framework counts `(n_pair, n_color, n_quark) = (2, 3, 6)`, this
reduces to `5 alpha_s(v)^3 / 72`.

## Numerical Read

At the canonical plaquette/CMT coupling

```text
alpha_s(v) = 0.103303816122267...
```

the structural-counts identities give

| Quantity | Structural expression | Value |
| --- | --- | ---: |
| `|V_us|_0^2` | `alpha_s(v)/2` | `0.0516519` |
| `|V_cb|_0^2` | `alpha_s(v)^2/6` | `0.0017786` |
| `|V_ts|_0^2` | `alpha_s(v)^2/6` | `0.0017786` |
| `|V_ub|_0^2` | `alpha_s(v)^3/72` | `1.5311e-5` |
| `|V_td|_0^2` | `5 alpha_s(v)^3/72` | `7.6557e-5` |

PDG 2024 comparators:

| Quantity | Framework | PDG | Deviation |
| --- | ---: | ---: | ---: |
| `|V_us|^2` | `5.165e-2` | `5.031e-2` | `+2.7%` |
| `|V_cb|^2` | `1.779e-3` | `1.681e-3` | `+5.8%` |
| `|V_ts|^2` | `1.779e-3` | `1.657e-3` | `+7.4%` |
| `|V_ub|^2` | `1.531e-5` | `1.459e-5` | `+4.9%` |
| `|V_td|^2` | `7.656e-5` | `7.362e-5` | `+4.0%` |

These comparators are downstream checks only. The theorem content is the
structural-counts algebra on the retained CKM atlas surface.

## Why This Adds Value

The retained CKM package already had the first-, second-, and third-row
atlas-leading identities distributed across separate notes. What is new here is
the **single structural-counts packaging** of all five off-diagonal entries:

1. `|V_us|_0^2`, `|V_cb|_0^2`, `|V_ts|_0^2`, `|V_ub|_0^2`, and `|V_td|_0^2`
   are displayed on one common `(n_pair, n_color, alpha_s(v))` surface.
2. The smallest entry, `|V_ub|_0^2`, is shown in the compact form
   `alpha_s(v)^3 / (8 n_color^2)`.
3. The `n_pair` cancellation in `(M4)` is made explicit and regression-tested.

This is a CKM-side packaging theorem only. It does not upgrade any independent
dimension, color, or charged-lepton lane.

## Scope

This note claims:

- the five off-diagonal atlas-leading identities `(M1)` through `(M5)`;
- the compact `|V_ub|_0^2 = alpha_s(v)^3 / (8 n_color^2)` form;
- exact `n_pair` cancellation in `(M4)`;
- the canonical numerical readout once the retained `alpha_s(v)` is supplied.

This note does **not** claim:

- dimension uniqueness from `|V_ub|`;
- an empirical confirmation of `d = 3`;
- any reliance on `2d + 3 = n_color^2`;
- any Koide, three-sector, or cross-lane closure;
- all-orders exact CKM matrix entries beyond the parent atlas scope.

## Reproduction

```bash
python3 scripts/frontier_ckm_magnitudes_structural_counts.py
```

Expected result:

```text
TOTAL: PASS=32, FAIL=0
```

## Cross-References

- [`CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)
- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
- [`CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_FIRST_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
- [`CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md`](CKM_SECOND_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-25.md)
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
- [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md)
