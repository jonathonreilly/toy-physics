# CKM Atlas-LO Magnitudes Structural-Counts and Conditional Dimension-Uniqueness Support Note

**Date:** 2026-04-25

**Status:** conditional cross-sector support corollary on current `main`.
This note does **not** promote `(α_3/α_em)(bare) = 2d + 3` or
`Q_l = 2/3` to retained status. Both load-bearing premises remain
**conditional/open** on `main`:

- `(α_3/α_em)(bare) = 2d + 3` is carried by a SUPPORT note on main, not a
  retained closure (cf.
  [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)).
- `Q_l = 2/3` is an open Koide support target with active investigation
  on main, not retained closure.

This note packages the algebraic content that becomes available
**if** those premises are accepted: the unified structural-counts
form for atlas-LO CKM magnitudes, and a conditional dimension-uniqueness
template that becomes a sharp falsification surface only if the
bare-α and Koide premises independently close.

```text
(M1)  |V_us|^2  =  alpha_s(v) / N_pair                  =  alpha_s/2
(M2)  |V_cb|^2  =  alpha_s(v)^2 / (N_pair × N_color)    =  alpha_s^2/6
(M3)  |V_ts|^2  =  alpha_s(v)^2 / (N_pair × N_color)    =  alpha_s^2/6
(M4)  |V_ub|^2  =  alpha_s(v)^3 / (8 N_color^2)          =  alpha_s^3/72
(M5)  |V_td|^2  =  (N_pair N_color - 1) × alpha_s(v)^3 / (8 N_color^2)
                =  5 alpha_s^3/72
```

Identities `(M1)-(M5)` express the framework's already-retained CKM
atlas magnitudes in a unified `(N_pair, N_color, α_s)` form. They are
**equivalent** to the retained third-row, second-row, and first-row
magnitude theorems and use only the retained CKM atlas inputs.
This part of the note is on solid retained ground.

What is **conditional** is the dimension-uniqueness reading:

```text
(M6)  |V_ub|^2  =  alpha_s(v)^3 / (8 (2d+3))     [conditional on (P1)]
```

`(M6)` follows only **if** the bare-α support note's `2d+3 = N_color^2`
is accepted. Under that conditional, the observed |V_ub| is
consistent with `d = 3` and **conditionally excludes** the integer
alternatives `d ≥ 11` that the algebraic constraint
`d = (N_color² - 3)/2` allows. This is a falsification template,
not a retained empirical proof of `d = 3`.

**Primary runner:**
`scripts/frontier_ckm_magnitudes_structural_counts_dimension_uniqueness.py`

## Statement (Two Layers)

### Layer 1: Retained structural-counts repackaging (no conditional inputs)

The framework's retained CKM atlas-LO magnitudes can be expressed in
unified `(N_pair, N_color, α_s)` form using only retained CKM atlas
inputs:

```text
(M1)  |V_us|^2  =  alpha_s(v) / N_pair             [retained CKM atlas]
(M2)  |V_cb|^2  =  alpha_s(v)^2 / (N_pair N_color) [retained CKM atlas]
(M3)  |V_ts|^2  =  alpha_s(v)^2 / (N_pair N_color) [retained CKM atlas]
(M4)  |V_ub|^2  =  alpha_s(v)^3 / (8 N_color^2)    [retained CKM atlas]
(M5)  |V_td|^2  =  (N_pair N_color - 1) alpha_s(v)^3 / (8 N_color^2)
                                                    [retained CKM atlas]
```

These follow from retained `λ² = α_s/2`, `A² = N_pair/N_color`, the
CP-radius `r² = ρ²+η² = 1/N_quark` from the atlas Thales surface,
and standard Wolfenstein. **No conditional input is required for
(M1)-(M5).**

The framework values `N_pair = 2`, `N_color = 3` are retained gauge
axioms (Cl(3) clock-shift for color count; Z_2 bipartite for weak
doublet). `N_quark = 6` is the retained one-generation quark count.

### Layer 2: Conditional dimension-uniqueness reading (load-bearing inputs)

If we additionally accept the conditional/support input

```text
(P1)  (alpha_3/alpha_em)(bare) = 2d + 3 = N_color^2
       [carried by SUPPORT note on main, not retained closure]
```

then `(M4)` rewrites as

```text
(M6)  |V_ub|^2 = alpha_s(v)^3 / (8 (2d+3))     [conditional on (P1)]
```

and the algebraic constraint `2d+3 = N_color²` (also conditional on
(P1) plus the open Koide target `Q_l = 2/3`, see the companion
support note
[`FRAMEWORK_THREE_SECTOR_DIMENSION_COLOR_QUADRATIC_IDENTITY_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_THREE_SECTOR_DIMENSION_COLOR_QUADRATIC_IDENTITY_SUPPORT_NOTE_2026-04-25.md))
restricts `d` to integer solutions `(d, N_color) ∈ {(3,3), (11,5), (23,7), …}`.

**Conditional consistency reading** (not retained empirical proof):

| `(d, N_color)` | `|V_ub|²` predicted | PDG ratio | Conditional status |
|---:|---:|---:|---|
| `(3, 3)` | `α_s³/72 = 1.531e-5` | `1.05` | consistent (framework value) |
| `(11, 5)` | `α_s³/200 = 5.51e-6` | `0.38` | excluded ~60% conditional |
| `(23, 7)` | `α_s³/392 = 2.81e-6` | `0.19` | excluded ~80% conditional |

The exclusions in this table hold **iff** premise `(P1)` is accepted
*and* the constraint to integer `(d, N_color)` solutions is taken
seriously. They do **not** constitute a retained empirical proof
that the spatial dimension is 3. PDG `|V_ub|` is consistent with
`d = 3` under these conditional readings; that is the strongest
phenomenological statement available without `(P1)` closing.

## Inputs And Status

| Input | Sector | Status | Authority on `main` |
| --- | --- | --- | --- |
| `λ² = α_s(v)/2` | CKM atlas | retained | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `A² = N_pair/N_color = 2/3` | CKM atlas | retained | [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md) |
| `ρ = 1/6`, `η² = 5/36` | CKM atlas | retained | [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md) |
| Atlas Thales `η² = ρ(1-ρ)` | CKM atlas | retained | [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md) |
| `\|V_qq\|²` retained values | CKM atlas | retained | [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md) |
| Canonical `α_s(v)` | gauge-vacuum | retained quantitative input | [`ALPHA_S_DERIVED_NOTE.md`](ALPHA_S_DERIVED_NOTE.md), `scripts/canonical_plaquette_surface.py` |
| `N_pair = 2`, `N_color = 3` | gauge structure | retained framework axioms | [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md), [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md) |
| `(α_3/α_em)(bare) = 2d+3 = 9` | color + EW | **conditional support (P1)** | [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md) |
| `Q_l = 2/3` | charged lepton | **open support target** (relevant for the companion three-sector note) | [`KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md), [`KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md`](KOIDE_Q_BACKGROUND_ZERO_Z_ERASURE_CRITERION_THEOREM_NOTE_2026-04-25.md), [`KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md`](KOIDE_Q_ONSITE_SOURCE_DOMAIN_NO_GO_SYNTHESIS_NOTE_2026-04-25.md) |

Layer 1 of this note `(M1)–(M5)` uses only the retained inputs in
the upper rows. Layer 2 (the dimension-uniqueness reading) is
conditional on the load-bearing input `(P1)` flagged below.

No PDG observable enters as a derivation input. The PDG values used
in the comparators table are post-derivation only.

## Derivation

### Layer 1 (Retained): Structural-counts forms

`|V_us|² = λ² = α_s(v)/2`. With `N_pair = 2`: `|V_us|² = α_s(v)/N_pair`.

`|V_cb|² = A² λ⁴ = (N_pair/N_color)(α_s/2)² = α_s²/(N_pair × N_color)`.

`|V_ts|² = A² λ⁴` at atlas-LO Wolfenstein (degenerate with `|V_cb|²`).

`|V_ub|² = A² λ⁶ (ρ²+η²) = A² λ⁶ × 1/N_quark`. Substituting:

```text
|V_ub|^2  =  (N_pair/N_color) × (α_s/2)^3 × 1/(N_pair × N_color)
          =  α_s^3 / (8 × N_color^2).
```

The N_pair factor cancels exactly — this is the structural reason
`|V_ub|²` depends only on `(α_s, N_color)`.

`|V_td|² = A² λ⁶ ((1-ρ)² + η²) = A² λ⁶ × (1 - ρ)` (atlas Thales)
`= (N_quark - 1) × α_s³/(8 N_color²)`.

These five identities are pure repackaging of the retained CKM
atlas magnitudes — no conditional input is required.

### Layer 2 (Conditional on P1): Dimension-uniqueness reading

If `(P1)` is accepted, then `2d + 3 = N_color²` substitutes into
`(M4)`:

```text
|V_ub|^2  =  α_s(v)^3 / (8 (2d+3)).
```

Integer solutions to `2d + 3 = N_color²` (with N_color positive
integer): `(d, N_color) ∈ {(3,3), (11,5), (23,7), …}`. Computing
`|V_ub|²` at each:

```text
d = 3:  N_color = 3,  |V_ub|² = α_s³/(8×9)   = α_s³/72   ≈ 1.531e-5
d = 11: N_color = 5,  |V_ub|² = α_s³/(8×25)  = α_s³/200  ≈ 5.51e-6
d = 23: N_color = 7,  |V_ub|² = α_s³/(8×49)  = α_s³/392  ≈ 2.81e-6
```

PDG `|V_ub|² = 1.459e-5 ± 0.16e-5`. The framework value `(d=3)` is
within `~5%` (atlas-LO precision); the alternative integer
solutions deviate by `60-80%`. **Under the conditional (P1)**,
PDG is consistent with `d = 3` and inconsistent with `d ≥ 11`.

This is a **conditional consistency reading**, not a retained
empirical determination of `d = 3`.

## Numerical Values (Layer 1 retained, Layer 2 conditional)

With canonical `α_s(v) = 0.10330381612...`:

| Quantity | Closed form | Framework | PDG | Ratio |
| --- | --- | ---: | ---: | ---: |
| `\|V_us\|²` | `α_s/N_pair` | `5.165e-2` | `5.031e-2` | `1.027` |
| `\|V_cb\|²` | `α_s²/(N_pair N_color)` | `1.779e-3` | `1.681e-3` | `1.058` |
| `\|V_ts\|²` | `α_s²/(N_pair N_color)` | `1.779e-3` | `1.657e-3` | `1.074` |
| `\|V_ub\|²` | `α_s³/(8 N_color²)` | `1.531e-5` | `1.459e-5` | `1.049` |
| `\|V_td\|²` | `(N_quark-1)α_s³/(8 N_color²)` | `7.656e-5` | `7.362e-5` | `1.040` |

PDG agreement at `4-7%` — consistent with `O(λ²) ≈ α_s/2 ≈ 5%` NLO
Wolfenstein corrections.

## What This Note Claims

**Layer 1 (retained):**
- The unified structural-counts form `(M1)-(M5)` for atlas-LO CKM
  magnitudes, equivalent to retained third/second/first-row magnitude
  theorems.
- `|V_ub|² = α_s(v)³/(8 N_color²)` with N_pair cancelling exactly.
- All atlas-LO predictions match PDG within `4-7%`, the expected
  size of NLO Wolfenstein corrections.

**Layer 2 (conditional on P1):**
- `|V_ub|² = α_s(v)³/(8 (2d+3))` follows from `(M4)` and `(P1)`.
- Under `(P1)`, integer `(d, N_color)` solutions to `2d+3 = N_color²`
  give a discrete set of allowed `|V_ub|²` values.
- PDG `|V_ub|` is conditionally consistent with `(d=3, N_color=3)`
  and inconsistent with the alternative integer solutions
  `(11,5), (23,7), ...` at `60-80%` deviation each.

## What This Note Does NOT Claim

- It does not promote `(α_3/α_em)(bare) = 2d+3` to retained closure.
  The carrier on main is a SUPPORT note.
- It does not promote `Q_l = 2/3` to retained closure (relevant for
  the companion three-sector support note where Koide enters as
  load-bearing).
- It does not establish empirically that `d = 3`. The conditional
  exclusion of `d ≥ 11` requires `(P1)` to be accepted; without that,
  the exclusion is not a retained empirical statement.
- It does not modify NLO Wolfenstein corrections; the analysis is
  atlas-LO.
- It does not promote any BSM contribution.
- It is **not part of the accepted minimal-input stack on main**.

## Falsification Use

This note is a **conditional cross-extraction template** that becomes
a sharp empirical test of the framework's `d = 3` axiom **iff**
`(P1)` `(α_3/α_em)(bare) = 2d+3` independently closes on `main`. Until
then:

- Layer 1 forms `(M1)-(M5)` are retained repackaging — usable as
  is, no conditional needed.
- Layer 2 dimension-uniqueness is a **template** that becomes a
  sharp `~3σ` (HL-LHC era) test of `d = 3` if `(P1)` closes.

Future precision on `|V_ub|`:

| Era | `σ(|V_ub|²)` | Conditional test sharpness |
| --- | ---: | --- |
| PDG 2024 | `±0.16e-5` | `~1σ` (under P1) |
| LHCb upgrade (~2027) | `~ ±0.10e-5` | `~2σ` (under P1) |
| HL-LHC | `~ ±0.07e-5` | `~3σ` (under P1) |

## Reproduction

```bash
python3 scripts/frontier_ckm_magnitudes_structural_counts_dimension_uniqueness.py
```

Expected result:

```text
TOTAL: PASS=29, FAIL=0
```

The runner verifies the algebra of `(M1)-(M5)` using only retained
inputs (Layer 1), and then verifies the conditional consistency
reading of `(M6)` and the dimension-uniqueness table assuming `(P1)`
(Layer 2). It does **not** establish retention of `(P1)`.

## Cross-References

- [`WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md`](WOLFENSTEIN_LAMBDA_A_STRUCTURAL_IDENTITIES_THEOREM_NOTE_2026-04-24.md)
  -- retained `λ² = α_s/2`, `A² = 2/3`.
- [`CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md`](CKM_CP_PHASE_STRUCTURAL_IDENTITY_THEOREM_NOTE_2026-04-24.md)
  -- retained `ρ = 1/6`, `η² = 5/36`.
- [`CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md`](CKM_ATLAS_TRIANGLE_RIGHT_ANGLE_THEOREM_NOTE_2026-04-24.md)
  -- retained Thales circle constraint.
- [`CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md`](CKM_THIRD_ROW_MAGNITUDES_THEOREM_NOTE_2026-04-24.md)
  -- retained `|V_td|² = 5α_s³/72`, `|V_ts|² = α_s²/6`.
- [`FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_BARE_ALPHA_3_ALPHA_EM_DIMENSION_FIXED_RATIO_SUPPORT_NOTE_2026-04-25.md)
  -- conditional support note carrying `(α_3/α_em)(bare) = 2d + 3` (P1).
- [`FRAMEWORK_THREE_SECTOR_DIMENSION_COLOR_QUADRATIC_IDENTITY_SUPPORT_NOTE_2026-04-25.md`](FRAMEWORK_THREE_SECTOR_DIMENSION_COLOR_QUADRATIC_IDENTITY_SUPPORT_NOTE_2026-04-25.md)
  -- companion conditional support note for `2d+3 = N_color²`.
- [`KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`](KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md)
  -- open Koide support investigation around `Q_l = 2/3`.
