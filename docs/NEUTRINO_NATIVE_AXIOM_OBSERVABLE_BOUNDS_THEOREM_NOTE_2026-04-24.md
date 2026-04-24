# Native-Axiom Neutrino Observable Bounds Theorem

**Date:** 2026-04-24
**Status:** exact positive-closure theorem package on `main`'s retained
atmospheric scale + retained normal ordering. All inputs are native-axiom
retained; no observational neutrino mass, splitting, or mixing angle is used
as a derivation input.
**Script:** `scripts/frontier_neutrino_native_axiom_observable_bounds.py`
**Lane:** absolute ν mass / Δm²_solar / Majorana (m_ββ, m_β observables)

## Scope

This note packages a set of **inequality closures** on the three directly
observable neutrino-mass quantities — Σm_ν (cosmological sum), m_β (tritium
β-decay endpoint), and m_ββ (neutrinoless double-β effective Majorana mass)
— that follow algebraically from the already-retained native-axiom inputs:

- **R1** — retained `m_3 = 5.058 × 10⁻² eV` from the atmospheric-scale
  theorem on the `k_A = 7, k_B = 8` bridge (see
  [DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md))
- **R2** — retained `Δm²_31 = 2.539 × 10⁻³ eV²` from the same theorem
- **R3** — retained **normal ordering** `m_1 < m_2 < m_3` as a structural
  consequence of the Majorana staircase (see
  [NEUTRINO_MASS_DERIVED_NOTE.md](./NEUTRINO_MASS_DERIVED_NOTE.md) §What
  Phase 4 retains)
- **R4** — PMNS unitarity `Σ_i |U_ei|² = 1` and non-negativity `m_i ≥ 0`
  (structural, no axiom input beyond SM field content)

No observed neutrino mass, splitting, or mixing angle appears in the
derivation. The solar splitting `Δm²_21`, the absolute lightest-mass `m_1`,
the PMNS angles, and the Majorana phases all remain **open** on the retained
bank; the inequalities below are the sharpest statements the retained chain
forces on each observable **without** those open quantities being closed.

## Theorem 1 — Σm_ν strict floor

**Claim.** Under R1, R3:

> `Σm_ν = m_1 + m_2 + m_3 > m_3 = 5.058 × 10⁻² eV = 50.58 meV` (strict).

**Proof.** From R3, `m_2 > m_1`. Combined with `m_1 ≥ 0` (R4), this gives
`m_2 > 0` strictly. Then

```text
Σm_ν = m_1 + m_2 + m_3 ≥ 0 + m_2 + m_3 > 0 + 0 + m_3 = m_3.
```

The inequality is strict because R3's `m_2 > m_1` forces `m_2 > 0` in
combination with `m_1 ≥ 0`, so the second `>` is strict. ∎

**Upper bound (trivial ceiling, R1 + R3).**

```text
Σm_ν < 3 m_3 = 1.517 × 10⁻¹ eV = 151.7 meV.
```

**Scope.**

- The floor Σm_ν > 50.58 meV is **PMNS-independent** and **off-diagonal-
  M_R-independent**. It rides only on R1, R3.
- It is **distinct** from the diagonal-benchmark numerical prediction
  Σm_ν ≈ 101 meV (which over-uses the failing diagonal Δm²_21) and from any
  observationally-patched value using PDG Δm²_21.

## Theorem 2 — m_β tritium-endpoint ceiling

**Claim.** Under R1, R3, R4:

> `m_β ≤ m_3 = 50.58 meV`.

**Proof.** By definition `m_β² = Σ_i |U_ei|² m_i²`. From R4, the PMNS row
`|U_ei|²` is a probability distribution over `i = 1, 2, 3`. From R3 + R1,
`m_i² ≤ m_3²` for each `i`. A convex combination is bounded by its
maximum, so

```text
m_β² = Σ_i |U_ei|² m_i² ≤ m_3² · Σ_i |U_ei|² = m_3² · 1 = m_3².
```

Taking the positive root, `m_β ≤ m_3`. ∎

**Scope.** Independent of the specific PMNS row and of m_1, m_2.
Saturates when all `|U_ei|²` mass concentrates on the `i = 3` state.

## Theorem 3 — m_ββ Majorana-phase-free ceiling

**Claim.** Under R1, R3, R4:

> `m_ββ ≤ m_3 = 50.58 meV`, uniformly in all Majorana phases.

**Proof.** By definition `m_ββ = |Σ_i U_ei² m_i|` where the `U_ei²` carry
Majorana phases. The triangle inequality and `m_i ≥ 0` give

```text
m_ββ = |Σ_i U_ei² m_i| ≤ Σ_i |U_ei|² m_i ≤ m_3 · Σ_i |U_ei|² = m_3.
```

The bound holds for every choice of Majorana phases. ∎

**Lower bound (trivial).** `m_ββ ≥ 0`, saturated when Majorana phases
achieve exact cancellation among the three terms.

## Theorem 4 — Δm²_21 structural ceiling

**Claim.** Under R1, R3:

> `0 < Δm²_21 < Δm²_31 = 2.539 × 10⁻³ eV²`.

**Proof.** R3 gives `m_1 < m_2 < m_3`, hence `m_2² - m_1² > 0` (lower
bound) and `m_2² - m_1² < m_3² - m_1² = Δm²_31` (upper bound). ∎

**Scope.** This bounds the solar splitting from above on the retained
chain **without** claiming any value for it. The observed
`Δm²_21 ≈ 7.42 × 10⁻⁵ eV²` lies well within this range; the diagonal
benchmark's over-prediction (2.1 × 10⁻³ eV²) also lies within this range.
The ceiling is therefore a weak but rigorously native-axiom constraint.

## Theorem 5 — m_1 as a retained-observable anchor (from R1, R2)

**Claim.** Under R1, R2, R3:

> `m_1² = m_3² - Δm²_31 = 0.019 × 10⁻³ eV² ⇒ m_1 = 4.35 × 10⁻³ eV = 4.35 meV`.

**Proof.** Definitional: `Δm²_31 ≡ m_3² - m_1²`. Substituting R1 and R2
yields `m_1² = (5.058 × 10⁻²)² - 2.539 × 10⁻³ = 2.558 × 10⁻³ - 2.539 × 10⁻³ =
1.9 × 10⁻⁵ eV²`, hence `m_1 = 4.35 × 10⁻³ eV`. ∎

**Caveat on robustness.** R1 and R2 are both retained on the diagonal-M_R
benchmark. Off-diagonal M_R corrections needed to repair the solar gap
perturb m_1 and Δm²_31 by quantities of order √(Δm²_21 / Δm²_31) × m_1 ~
10⁻⁴ eV — the same order as m_1 itself. This theorem therefore gives
m_1 ≈ 4 meV on the retained benchmark; its native-axiom robustness against
the (still-open) off-diagonal correction is bounded, not exact.

Theorems 1–4 above are **free of this caveat** — they use only R1 and R3
(plus definitional identities and PMNS unitarity), which are robust across
the expected off-diagonal perturbation scale.

## Consolidated summary table

| Observable | Native-axiom bound | Experimental status |
|------------|-------------------|---------------------|
| Σm_ν (lower) | **> 50.58 meV** (strict floor, Theorem 1) | DESI 2024 bound < 72 meV survives; CMB-S4 projected < 40 meV would FALSIFY |
| Σm_ν (upper) | < 151.7 meV (trivial ceiling) | Planck 2018 < 120 meV tightens upper |
| m_β (upper) | **≤ 50.58 meV** (PMNS-free, Theorem 2) | KATRIN 2022 < 800 meV; KATRIN final ~200 meV; Project 8 target ~40 meV would provide test |
| m_ββ (upper) | **≤ 50.58 meV** (phase-free, Theorem 3) | KamLAND-Zen 2022 < 28–122 meV survives; Legend-1000 ~17 meV is a test point; nEXO ~7–15 meV is a tighter test |
| Δm²_21 (upper) | < 2.539 × 10⁻³ eV² (Theorem 4) | observed 7.42 × 10⁻⁵ eV² well inside |
| Δm²_21 (lower) | > 0 (structural NO) | observed 7.42 × 10⁻⁵ eV² confirms |

## Falsifiability

The sharpest falsification target is **Theorem 1's floor Σm_ν > 50.58 meV**:

- A confirmed cosmological bound `Σm_ν < 50 meV` falsifies the retained
  atmospheric-scale theorem or the retained normal ordering (R1 or R3).
- CMB-S4 projected sensitivity ~40 meV would put this at direct test.
- A confirmed inverted ordering falsifies R3 directly and would also
  falsify Theorem 1 (since IO allows m_3 to be the lightest, removing the
  floor mechanism).

Theorems 2, 3 are weaker test points (upper bounds, harder to falsify in
the near term), but an unambiguous `m_β > 51 meV` or `m_ββ > 51 meV`
detection at KATRIN/Legend/nEXO would falsify the retained chain.

Theorem 4 (Δm²_21 < Δm²_31) is confirmed by existing data; it provides
structural consistency rather than a live falsifiability handle.

## What this theorem does NOT claim

- Does **not** close the solar gap `Δm²_21` as a point prediction. The
  diagonal benchmark over-predicts `Δm²_21 ≈ 2.1 × 10⁻³ eV²` vs observed
  `7.42 × 10⁻⁵ eV²`; the full-matrix flavor-texture closure required to
  resolve this remains an open lane (see
  [NEUTRINO_MASS_DERIVED_NOTE.md](./NEUTRINO_MASS_DERIVED_NOTE.md) §What
  Phase 4 bounds but does not retain).
- Does **not** promote the retained Majorana lane beyond its current
  negative closure on the current-stack carrier (see
  [NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md](./NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md)).
- Does **not** give a point prediction for `m_1`, `m_2`, `m_β`, `m_ββ`,
  or `Σm_ν`. Each remains bounded, not pinned, on the retained chain.
- Does **not** rely on observational PDG/NuFit/DESI values except as
  post-derivation comparators for the falsifiability table.

## Relationship to prior feature-branch candidates

Three feature branches (not merged to `main`) attempted related
predictions:

- `neutrino-mass-sum-prediction` (0bf1405b): gave
  `Σ = 100.7 meV` (pure diagonal benchmark) and `Σ = 64.5 meV`
  (observation-patched using observed `Δm²_21` once).
  **This note supersedes that attempt** by giving a rigorously
  native-axiom inequality `Σm_ν > 50.58 meV` without any observational
  patch.
- `neutrino-solar-gap-alpha-lm-squared` (7dc55449): proposed
  `ε/B = α_LM²` matching observed `Δm²_21` to 2%. Self-flagged as
  numerical candidate; three subsidiary theorems (R1–R3 in that note's
  numbering) were required but not produced. **Not superseded by this
  note.** The solar gap remains an open lane for positive point
  prediction.
- `neutrino-three-level-staircase-proposal` (d413f696): proposed the
  structural mechanism for `ε/B = α_LM²`. Self-flagged as proposal.
  **Not superseded by this note.** The retained `1 + 2` weak-axis split
  does not admit a third level at the staircase structural level; the
  proposal is therefore structurally blocked against the current retained
  adjacent-placement theorem.

This note fills the gap left by the first branch — giving a genuine
native-axiom closure in the absolute-mass lane — while leaving the
second and third (solar gap point closure) honestly open.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_neutrino_native_axiom_observable_bounds.py
```

Expected: all checks pass with `PASS = N, FAIL = 0`.

## Cross-references

- `docs/DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE_2026-04-15.md` — R1, R2
- `docs/NEUTRINO_MASS_DERIVED_NOTE.md` — R3 + open-lane status
- `docs/NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md` — Majorana
  lane negative closure
- `docs/NEUTRINO_MAJORANA_ADJACENT_SINGLET_PLACEMENT_THEOREM_NOTE.md` —
  weak-axis 1 + 2 split (blocks three-level staircase)
