# Koide Selected-Line Provenance: Derivation of `H_sel(m) = H(m, √6/3, √6/3)`

**Date:** 2026-04-20
**Status:** complete derivation from proposed_retained-on-`main` theorems; closes
scalar-selector cycle 1 open import **I3**.
**Scope:** names the exact theorem that fixes the slot values `(δ, q_+) =
(√6/3, √6/3)` in the Koide selected-line reduction cited throughout the
Brannen–Zenczykowski phase / θ-hierarchy chain.
**Primary verification runner:**
`scripts/frontier_koide_selected_line_provenance.py`

---

## 1. What was the open import

Every downstream charged-lepton Koide θ theorem on this branch — the
Brannen-Zenczykowski Berry-holonomy theorem
(`docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`), the γ-orbit selected-line
closure (`docs/KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md`),
the microscopic scalar-selector target
(`docs/KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md`), and the
frozen-bank decomposition
(`docs/KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md`) —
uses the physical charged-lepton selected line

```text
H_sel(m) = H(m, √6/3, √6/3)
```

as a retained starting point. The two non-`m` arguments carry specific numeric
values `(√6/3, √6/3)`, but those specific values were not derived inline at
point of use. Open import I3 of
`docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` requested the
precise retained theorem that fixes them.

## 2. The retained affine chart `H(m, δ, q_+)` on `main`

The chart is defined on `main` by the active-affine point-selection boundary
theorem,
`docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
(runner
`scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py`):

```text
H(m, δ, q_+) = H_base + m T_m + δ T_delta + q_+ T_q
```

with the fixed retained generators

```text
T_m     = [[1,0,0],[0,0,1],[0,1,0]]
T_delta = [[0,-1,1],[-1,1,0],[1,0,-1]]
T_q     = [[0,1,1],[1,0,1],[1,1,0]]
```

and the fixed retained source package `(γ, E_1, E_2) = (1/2, √(8/3), √8/3)`
that enters `H_base` (same generators and `H_base` are exported on `main` in
`scripts/frontier_charged_lepton_via_neutrino_hermitian.py`, lines 95–119).
This chart is atlas-retained as a consequence of the single framework axiom
`Cl(3)/Z^3` + `hw=1` triplet + the retained `Cl(3)` source-surface reductions.

## 3. The load-bearing retained theorem

The slot values `(δ_*, q_+*) = (√6/3, √6/3)` are fixed on `main` by the
retained parity-compatible observable-selector theorem,

**`docs/DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md`**

(runner
`scripts/frontier_dm_neutrino_source_surface_parity_compatible_observable_selector_theorem.py`).
Its derivation chain is:

1. **Scalar generator** — the retained observable-principle note
   `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` supplies the unique additive
   CPT-even scalar generator

   ```text
   W_D[J] = log|det(D + J)| − log|det D|.
   ```

2. **Active source family** — the active-affine point-selection boundary
   theorem reduces the live source to the exact 2-real family

   ```text
   J_act(δ, q_+) = δ T_delta + q_+ T_q.
   ```

3. **Parity-compatible diagonal baseline** — the retained theorem
   `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md`
   shows that compatibility with the `23` odd/even grading of the active pair
   forces `D = diag(A, B, B)` with `A, B > 0` (23-even baselines).

4. **Active half-plane** — the retained theorem
   `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
   gives the exact admissible chamber

   ```text
   q_+ ≥ √(8/3) − δ
   ```

   with source constraint `δ + ρ = √(8/3)`.

5. **Isotropic zero-source curvature** — for every `D = diag(A, B, B)` the
   parity-compatible selector theorem computes

   ```text
   det(D + J_act) = A B^2 − (A + 2B)(δ^2 + q_+^2) − 6 δ^2 q_+ + 2 q_+^3
   ```

   and therefore the zero-source Hessian on the active pair is isotropic:

   ```text
   −∂²W_D |_{(0,0)} = 2 (A + 2B)/(A B^2) · (δ^2 + q_+^2).
   ```

   So on every 23-symmetric positive baseline, the native positive-quadratic
   selector law is a positive scalar multiple of `δ^2 + q_+^2` (universal
   across the class).

6. **Unique boundary minimizer** — strictly convex minimization of
   `δ^2 + q_+^2` on the active chamber boundary `q_+ = √(8/3) − δ` gives the
   unique stationary point

   ```text
   δ_* = √(8/3) / 2 = √6/3,
   q_+* = √(8/3) − δ_* = √6/3.
   ```

   Hence, up to the universal positive scalar `λ(A, B) > 0`, every
   parity-compatible diagonal baseline produces the **same** selected point
   `(δ_*, q_+*) = (√6/3, √6/3)`, and the residual baseline ambiguity inside
   the parity-compatible class vanishes on the selector step.

7. **Selected line** — substituting these retained values back into the
   retained affine chart `H(m, δ, q_+)` gives exactly

   ```text
   H_sel(m) = H(m, √6/3, √6/3).
   ```

This is the retained provenance for the specific numeric values `(√6/3,
√6/3)` used throughout the Koide θ closure chain.

## 4. Independent cross-check via the frozen CP/slot bank

The retained intrinsic CP theorem gives `cp1 = −2√6/9`, and the selected-slice
frozen-bank decomposition note shows `q_+* = −3 cp1 / 2 = √6/3`. Therefore the
same number `q_+* = √6/3` is also encoded directly in the frozen intrinsic CP
constant of the source surface, independent of the observable-principle
minimization above. This is the retained cross-check that the selected slot
values are an intrinsic invariant of the retained source-surface reductions
and not a choice of selector principle.

## 5. Status

The derivation is **complete on retained `main` ingredients**. No additional
selector principle, no additional axiom, and no phenomenological input is
required to fix `(δ_*, q_+*) = (√6/3, √6/3)`. The residual charged-lepton gap
below the selected line remains the single real `m` coordinate (the
microscopic scalar selector target), exactly as stated in the existing
target/closure notes.

All theorems cited above are verified present on `main`:

- `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_PARITY_COMPATIBLE_DIAGONAL_BASELINE_THEOREM_NOTE_2026-04-17.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_PARITY_COMPATIBLE_OBSERVABLE_SELECTOR_THEOREM_NOTE_2026-04-17.md`
- `docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_CURVATURE_23_SYMMETRIC_BASELINE_BOUNDARY_THEOREM_NOTE_2026-04-17.md`
- `scripts/frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary.py`
- `scripts/frontier_dm_neutrino_source_surface_active_half_plane_theorem.py`
- `scripts/frontier_dm_neutrino_source_surface_parity_compatible_observable_selector_theorem.py`
- `scripts/frontier_charged_lepton_via_neutrino_hermitian.py` (exports `H(m, δ, q_+)`).

## 6. Scope note on the `main`-status of the companion charged-lepton two-Higgs reduction

Audit trace. The scalar-selector open-imports table
(`docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` row I3) and the
support package
(`docs/SCALAR_SELECTOR_REVIEWER_PACKAGE_2026-04-20.md`, `HSEL` row) name the
"retained two-Higgs canonical reduction" as the provenance citation for I3.
On direct `git ls-tree main` check, the files
`docs/CHARGED_LEPTON_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md` and
`scripts/frontier_charged_lepton_two_higgs_canonical_reduction.py` are **not
currently on `main`**; they live on this branch and on the neutrino-lane
integration branches. The two-Higgs canonical-reduction note does establish
that the charged-lepton minimal non-monomial lane carries 7 real physical
quantities, but it does **not** by itself fix the numeric values `(√6/3,
√6/3)`. The actual load-bearing provenance for those specific numbers is the
retained parity-compatible observable-selector theorem on `main` named in §3.
This note therefore upgrades the I3 citation from "cited as retained
two-Higgs reduction" (imprecise) to the exact `main` chain in §3 (precise).
The support package should be amended accordingly when I3 is closed.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_selected_line_provenance.py
```
