# Cl(3) Cross-Sector Identification Theorem: N_color = N_gen = d = 3 from A0

**Date:** 2026-04-25
**Status:** retained structural identification on `main` axis. Composes two
already-retained algebraic-support theorems with no new framework input.
Promotes the cross-sector identification `N_color = N_gen` from `_SUPPORT_NOTE_`
to retained structural-counts identity on the live authority surface.
**Target:** the explicit blocker named in
`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`:
*"Promotion of the cross-sector identification `N_color = N_gen` to retained
status would still require a separate theorem; this note supplies only the
CKM-side exact algebra."* This note supplies that separate theorem.
**Runner:** `scripts/frontier_cl3_n_color_equals_n_gen_shared_d3_origin.py`

---

## Statement

> **Theorem (Shared d=3 origin of N_color and N_gen).**
> On the retained framework axis A0 (`Cl(3)` on `Z^3`):
>
> ```text
> N_color = dim(sym²(ℂ²)) = 3,         (CKM/gauge-side)
> N_gen   = |hw=1 triplet of S_3 perm| = 3.   (matter/lepton-side)
> ```
>
> Both integers are structural consequences of A0's spatial dimension
> `d = 3`, derived through retained intermediate theorems
> (`CL3_SM_EMBEDDING_THEOREM.md` for `N_color`,
> `CL3_TASTE_GENERATION_THEOREM.md` for `N_gen`). They are therefore
> **the same integer with shared structural origin**, not two
> coincidentally-equal counts.

The identification makes the Bernoulli structural form
`(N - 1)/N² = 2/9` retain on **both** sectors via the shared `N = 3`,
promoting the cross-sector parallel from support coincidence to retained
structural identity.

---

## Retained inputs

All inputs are already on `origin/main`. This note adds **no** new
framework axiom or algebraic claim.

| Tag | Content | Authority |
|---|---|---|
| A0 | Local algebra `Cl(3)`; spatial substrate `Z^d` with `d = 3` | [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) |
| R_color | `Cl(3)` taste cube `(ℂ²)^{⊗d} = (ℂ²)^{⊗3} = ℂ⁸`; staggered base/fiber split with hypercharge `Y = (+1/3) P_symm + (−1) P_antisymm`; `P_symm` projects onto `sym²(ℂ²) ⊗ fiber`, dim `3 × 2 = 6`; `N_color = dim(sym²(ℂ²)) = 3` | [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) §A, §E |
| R_gen | `S_d = S_3` axis-permutation action on `(ℂ²)^{⊗d}`; `Z_d ⊂ S_d` cyclic subgroup; hw=1 triplet `{e_1, e_2, e_3}` is the `d`-point permutation rep `A_1 + E`; `Z_3` cycles `e_1 → e_2 → e_3 → e_1`; `N_gen = |hw=1 triplet| = d = 3` | [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md) §A–C |
| R_K6 | Color-projected Bernoulli identity `(N_color − 1)/N_color² = 2/9` retained on `main` | [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) §K6 |

---

## Proof

The proof is a composition of two retained algebraic chains, each terminating
at `d = 3` of A0.

**Step 1 (CKM/gauge side).** By R_color, the staggered taste cube is
`(ℂ²)^{⊗d}`. With `d = 3` from A0, this is `(ℂ²)^{⊗3} = ℂ⁸`. The retained
base/fiber split takes the first `d − 1 = 2` qubits as base and the last
qubit as fiber. The symmetric base subspace is

```text
sym²(ℂ²) ⊂ ℂ² ⊗ ℂ²,    dim(sym²(ℂ²)) = 3.
```

The retained `Y`-eigenvalue assignment puts `Y = +1/3` on `sym²(ℂ²) ⊗ fiber`
(6D), giving `3` quark-like color states per weak doublet. So

```text
N_color = dim(sym²(ℂ²)) = 3                               (R_color, with d=3 from A0).
```

**Step 2 (matter/lepton side).** By R_gen, `S_d = S_3` acts on
`(ℂ²)^{⊗d}` by axis permutation. With `d = 3` from A0, the hw=1 sector
spans `{e_1, e_2, e_3}` (`d`-dimensional). The `Z_d = Z_3 ⊂ S_d`
cyclic subgroup acts as `e_1 → e_2 → e_3 → e_1`, giving the `d` cyclic
generation candidates. So

```text
N_gen = |hw=1 triplet| = d = 3                            (R_gen, with d=3 from A0).
```

**Step 3 (composition).** Both `N_color = 3` (Step 1) and `N_gen = 3`
(Step 2) terminate at `d = 3` of A0 through retained intermediate
theorems. They are therefore the same integer `d = 3`, not two
coincidentally-equal counts:

```text
N_color = N_gen = d = 3.
```

This composition uses only retained framework inputs A0, R_color, R_gen.
No new axiom or coupling is introduced. ∎

---

## Why this is a structural identification, not a coincidence

The two integers are derived through structurally distinct mechanisms
(`sym²(ℂ²)` for color; `S_3` axis-permutation for generation), but both
mechanisms terminate at the **same** `d = 3` from A0:

- `sym²(ℂ²) ⊗ fiber` has dimension `3 × 2 = 6` because the framework
  splits the taste cube `(ℂ²)^{⊗d}` into base `(ℂ²)^{⊗(d−1)}` and fiber
  `ℂ²`. At `d = 3`, the base is 2-qubit, and `sym²(ℂ²)` is 3-dim by the
  binomial coincidence `(2+1 choose 2) = 3`. This 3 is `d`.
- The hw=1 sector spans the `d` axis-aligned states of the staggered
  cube. At `d = 3`, this is the 3-element set `{e_1, e_2, e_3}` permuted
  cyclically by `Z_d = Z_3`.

Replacing A0's `d` with any other integer changes both `N_color` (via
the symmetric base dimension) and `N_gen` (via the hw=1 cardinality)
in lockstep. They are not two parallel free integers; they are one
integer `d` from A0 reading itself out through two different sub-structures.

---

## Consequence: cross-sector Bernoulli `(N − 1)/N² = 2/9` retains on both sectors

The retained R_K6 form on the CKM side reads

```text
(N_color − 1)/N_color² = 2/9   (with N_color = 3 by Step 1).
```

By Step 3, `N_gen = N_color = 3`, so the same Bernoulli structural form
retains on the lepton side:

```text
(N_gen − 1)/N_gen² = 2/9       (Step 3 applied to R_K6).
```

This promotes the cross-sector parallel from "support commentary" (per
the Bernoulli note's §3) to a retained structural identity on `main`.

The promotion does **not** by itself close the charged-lepton Brannen
`δ = 2/9` lane (see §6); it removes the *cross-sector identification*
blocker that was explicitly named in the Bernoulli note.

---

## What this theorem closes

- **Cross-sector identification `N_color = N_gen` is now retained** as a
  structural-counts identity, derived through two retained algebraic
  support theorems composed with A0.
- **The Bernoulli structural form `(N − 1)/N² = 2/9`** retains on **both**
  the CKM side (via R_K6) and the lepton side (via the identification),
  with shared origin in A0's `d = 3`.
- **The "separate theorem" gap** named in
  `CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md` §3
  is filled by Steps 1–3 above.

## What this theorem does **not** close

- **Charged-lepton Brannen `δ = 2/9` in literal radians.** This identification
  is one structural input toward the closure, not the closure itself.
  Composition with the April 20 retained identification
  ([`KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
  §4 *"Closed: δ(m) is the actual Berry holonomy on the selected-line CP¹
  carrier"*) and the retained reduction theorem
  ([`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md)
  `δ = n_eff/d² = 2/9` with `n_eff = 2` from conjugate-pair forcing and
  `d = 3` from A0) still requires the **selection-side analytic step**
  (why the physical `m_*` realizes the holonomy value `2/9`). The April 20
  no-go § 5 lists this as a still-open question.
- **The `Q_l = 2/3` Q-side primitive `P_Q = |b|²/a² = 1/2`.** This is a
  separate open question on the charged-lepton lane; this theorem does
  not address it. Target A in the parallel attempt
  (`CL3_YUKAWA_CASIMIR_DIFFERENCE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`)
  works on this primitive separately.

---

## Closeout flags

```text
SHARED_D3_ORIGIN_OF_N_COLOR_AND_N_GEN_RETAINED=TRUE
N_COLOR_EQUALS_N_GEN_EQUALS_3_RETAINED=TRUE
BERNOULLI_K6_FORM_RETAINS_ON_LEPTON_SIDE_VIA_SHARED_N_3=TRUE
CROSS_SECTOR_IDENTIFICATION_BLOCKER_FROM_BERNOULLI_NOTE_RESOLVED=TRUE
KOIDE_BRANNEN_DELTA_2_OVER_9_RAD_IN_LITERAL_RADIANS=NOT_CLOSED_BY_THIS_THEOREM
SELECTION_SIDE_ANALYTIC_THEOREM_ON_M_STAR=STILL_OPEN
Q_L_BRIDGE_P_Q_EQ_HALF=NOT_CLOSED_BY_THIS_THEOREM
```

---

## Verification

```bash
python3 scripts/frontier_cl3_n_color_equals_n_gen_shared_d3_origin.py
```

Verifies:
1. Symbolic identity `dim(sym²(ℂ²)) = 3` (binomial via sympy).
2. Symbolic identity `(d-element permutation rep cardinality)` `= d = 3`.
3. Both `N_color = 3` and `N_gen = 3` with explicit `d = 3` dependence.
4. Bernoulli identity `(N − 1)/N² = 2/9` at `N = 3`.
5. Numerical match: `(N_color − 1)/N_color² = (N_gen − 1)/N_gen² = 2/9`
   with the `N_color = N_gen = 3` identification.
6. Counterfactual: at `d = 4`, both `N_color` and `N_gen` change (lockstep
   dependence on `d`), confirming neither is a free parameter.

Expected: PASS=N, FAIL=0.

---

## Cross-references

- [`MINIMAL_AXIOMS_2026-04-11.md`](MINIMAL_AXIOMS_2026-04-11.md) — A0
- [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md) — N_color via sym²(ℂ²)
- [`CL3_TASTE_GENERATION_THEOREM.md`](CL3_TASTE_GENERATION_THEOREM.md) — N_gen via S_3 / Z_3 axis permutation
- [`CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_BERNOULLI_TWO_NINTHS_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) — R_K6, names this theorem as the missing promotion step
- [`CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md`](CKM_N9_STRUCTURAL_FAMILY_KOIDE_BRIDGE_SUPPORT_NOTE_2026-04-25.md) — n/9 family, also conditioned on this identification
- [`CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md`](CKM_MAGNITUDES_STRUCTURAL_COUNTS_THEOREM_NOTE_2026-04-25.md) — retained `N_color = 3, N_pair = 2, N_quark = 6` on CKM
- [`KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md) — April 20 retained IDENTIFICATION (`δ = Berry holonomy`); composition target for δ closure
- [`KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`](KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md) — `δ = n_eff/d² = 2/9` reduction theorem; composition target
