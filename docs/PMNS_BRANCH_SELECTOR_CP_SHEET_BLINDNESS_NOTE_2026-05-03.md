# PMNS Branch Selector — CP-Sheet Blindness Excludes the Current Branch-B Bank

**Date:** 2026-05-03
**Type:** stretch_attempt (output type c) — negative structural open-gate note
**Cycle:** 21 of follow-on campaign 2026-05-03
**Branch:** physics-loop/pmns-branch-selector-2026-05-03
**Claim type:** open_gate (sharpens cycle 09 Obstruction 2)
**Status:** open with negative structural conclusion (not retained-grade)
**Script:** scripts/frontier_pmns_branch_selector.py

This document is a branch-local physics-loop artifact. Its `Status:`
line is not an audit-ratified retained status. Independent audit-lane
review is still required before the repo may treat any claim here as
retained-grade.

## Executive summary

Cycle 09 (PR #411) named Obstruction 2:

> "Branch selector not derived: framework has TWO partial η/η_obs
> predictions, 0.1888 (reduced surface, exact one-flavor transport)
> and 1.0 (low-action PMNS support branch); without a derivation of
> WHICH branch is physical, the framework cannot uniquely predict η."

This cycle synthesizes:

1. **cycle 18's structural decomposition** of Branch A:
   `η/η_obs|_A = (516/53009) · Y₀² · F_CP · κ_axiom = 0.18879...`,
   from
   [`ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md`](ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md).
2. **the four candidate Branch-B selectors**:
   - **min-info**: `D_KL(x||x_seed) + D_KL(y||y_seed) + (1 - cos δ)`
   - **observable-relative-action**: `Tr(H_seed^{-1} H_e) -
     log det(H_seed^{-1} H_e) - 3`
   - **transport-extremal**: `max_i η_i / η_obs`
   - **continuity-closure**: `λ_*` along seed→witness interpolation
3. **the cited CP-sheet blindness theorem**:
   [`DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md),
   which proves every Branch-B selector objective above is even
   under `δ → -δ`, while the baryogenesis source channel
   `γ = x_1 y_3 sin(δ)` is odd.

**Open-gate boundary by exclusion**: every Branch-B selector under the
current bank produces a CP-DEGENERATE pair `(δ, -δ)` with equal
selector value but opposite γ. So no Branch-B selector chooses a
unique baryogenesis witness; Branch B cannot uniquely close η/η_obs
under the current selector bank.

Within the current bank, **Branch A is the only branch with a
deterministic unique numerical output already documented by the
prior-cycle transport/decomposition surface**. This remains an
open-gate synthesis: cycle 18's decomposition and this note's
dependency chain still require independent audit-lane treatment
before any retained-grade reuse.

This does NOT close cycle 09 Obstruction 2 by constructing a
positive selector. It sharpens Obstruction 2 to a structural
exclusion: the entire current Branch-B selector bank fails the
parity test, so the only remaining route to unique η-closure is
Branch A. The numerical mismatch `0.1888 ≠ 1.0` between the two
branches is NOT explained here; that mismatch is downstream of
the already-named Y₀² and α_LM imports.

## A_min (minimal allowed premise set)

- (A1, bounded_theorem, audit-pending)
  [`ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md`](ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md)
  (cycle 18):
  `η/η_obs|_A = (516/53009) · Y₀² · F_CP · κ_axiom`. Pure-rational
  ABC closure with π⁴·ζ_3 cancellation.
- (A2, support-grade)
  [`DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md`](DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md):
  `γ = 1/2, E₁ = √(8/3), E₂ = √8/3` chart constants on N_e seed
  surface.
- (A3, exact obstruction theorem on open gate; effective status is
  pipeline-derived)
  [`DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md):
  every current Branch-B selector objective is even under
  `δ → -δ`.
- (A4, support-grade) Four candidate Branch-B selectors:
  - [`DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md)
  - [`DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md)
  - [`DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md)
  - [`DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md`](DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md)
- (A5, historical/exact transport provenance)
  [`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
  (cycle 09 parent): documents Branch A and Branch B.

## Forbidden imports (declared)

- η_obs (= 6.12 × 10⁻¹⁰) used **only as comparator**, never as
  derivation input.
- m_β not used.
- Σ m_ν not used.
- No PDG values consumed.
- No literature numerical comparators consumed.
- No fitted selectors consumed.
- No same-surface family arguments.
- y_0 = G_weak²/64 with G_weak = 0.653: named obstruction
  inherited from cycle 09 O1 / cycle 12 R2 / cycle 15 R1.
  **Not a new derivation input.** Branch A's prediction inherits
  this as cycle 18 already noted.
- α_LM mass scale: named obstruction inherited from cycle 09 O3.
  **Not a new derivation input.**
- Cycle 18's `(516/53009) · Y₀² · F_CP · κ_axiom` decomposition is
  admitted as prior-cycle output, not re-derived here.

## The two branches

### Branch A — One-flavor reduced surface

**Theorem-native frame**: the exact one-flavor radiation-branch
transport on the reduced one-flavor surface. The cycle-09 transport-
status note records:

```
ε_1 / ε_DI    = 0.9276...
κ_axiom       = 0.004829545290766509
η / η_obs|_A  = 0.188785929502...
```

Cycle 18's structural decomposition:

```
η/η_obs|_A = (s/n_γ) · C_sph · d_N · ε_1 · κ_axiom / η_obs
           = (516/53009) · Y₀² · F_CP · κ_axiom / η_obs
```

The pure-rational ABC = 516/53009 closes from `g_* = 427/4`,
`g_S = 43/11`, `C_sph = 28/79` with `π⁴·ζ_3` cancelling between
`s/n_γ` and `d_N`. Branch A is **NOT a selector output** — it is a
deterministic transport-chain numerical value on the reduced
surface.

### Branch B — PMNS-assisted off-seed source on N_e seed surface

**Theorem-native frame**: the fixed native N_e seed surface with
seed pair `(x̄, ȳ) = (0.5633, 0.3067)`, with off-seed `5`-real
sources `(ξ_1, ξ_2, η_1, η_2, δ)` selected by one of four candidate
laws. The cycle-09 transport-status note records:

```
η / η_obs|_B = 1.000  (low-action PMNS support branch)
```

Each of the four selectors produces a different specific source
yielding `η_{i_*} / η_obs = 1.0` on the favored column `i_*`:

| selector                  | objective                                      | source δ | output |
|---------------------------|------------------------------------------------|----------|--------|
| min-info                  | `D_KL(x||x_seed) + D_KL(y||y_seed) + (1-cos δ)` | ≈ 0     | 1.0    |
| observable-relative-action| `Tr(H_seed⁻¹ H_e) - log det(H_seed⁻¹ H_e) - 3`  | ≈ 0     | 1.0    |
| transport-extremal        | `max_i η_i/η_obs` (overshoots → 1.052)         | -2.23   | 1.052  |
| continuity closure        | `λ_*` along seed→extremal interpolation        | -2.04   | 1.0    |

## The CP-sheet blindness exclusion

The cited CP-sheet blindness theorem (A3) proves:

1. The min-info objective `D_KL(x||x_seed) + D_KL(y||y_seed) +
   (1 - cos δ)` is even under `δ → -δ` (because `cos(-δ) = cos δ`
   and the KL pieces don't depend on `δ`).
2. The observable-relative-action objective `Tr(H_seed⁻¹ H_e) -
   log det(H_seed⁻¹ H_e) - 3` is even under `δ → -δ` (because
   `H_e` is constructed from `(ξ, η, |sin δ|, cos δ)` invariants
   that are even, AND because the action functional is
   real-symmetric).
3. The transport-extremal objective `max_i η_i / η_obs` is even
   because the transport functional is constructed from the
   even invariants `E_1, E_2`, and `|γ|`.
4. The continuity-closure construction inherits parity from the
   transport-extremal endpoint.

**Decisive parity mismatch**: the baryogenesis source channel

```
γ_baryogenesis = x_1 y_3 sin(δ)
```

is **ODD** under `δ → -δ` (because `sin(-δ) = -sin δ`).

So for every Branch-B winner `(x, y, δ)`, the CP-conjugate
`(x, y, -δ)` is an equally-winning selector output but with
opposite-sign baryogenesis source `-γ`. Since both points are
selected with equal selector value, **no Branch-B selector chooses
a unique sign**, hence no unique baryogenesis witness, hence no
unique η.

In notation:
- For `M ∈ {min-info, obs-rel-action, transport-extremal,
  continuity-closure}`:
  - `M(x, y, δ) = M(x, y, -δ)`.
  - But `γ(x, y, δ) = -γ(x, y, -δ)`.
  - Therefore `argmin/argmax_M ⊃ {(x, y, δ_*), (x, y, -δ_*)}`.

A unique selection requires breaking the `δ → -δ` symmetry. The
current Branch-B selector bank does not contain such a CP-odd
functional.

## Open-gate boundary by exclusion

The cycle 21 resolution:

> Under the current Branch-A and Branch-B selector banks, only
> Branch A produces a deterministic unique numerical η output.
> Branch B's predictions are necessarily CP-paired (parity-
> degenerate), hence cannot uniquely close η without an additional
> CP-odd structural input that is not currently audit-ratified.

Therefore, **modulo independent audit treatment of cycle 18's
structural decomposition (A1), the cited CP-sheet blindness theorem
(A3), and this open-gate synthesis**, the framework's current-bank
deterministic branch is Branch A's
`(516/53009) · Y₀² · F_CP · κ_axiom`.

The 0.1888 ≠ 1.0 numerical mismatch between Branch A and Branch B
is downstream of:
- Branch A inheriting Y₀² (named obstruction O1),
- Branch B's "1.0" being a fitted-to-η_obs selector closure on a
  structurally different surface (one with nonzero off-seed source
  freedom).

This cycle does NOT explain that mismatch. It demonstrates that
Branch B's "1.0" is not an independent prediction in the sense
required for cycle 09 Obstruction 2 — it is the value that the
Branch-B closure problem is set up to give by construction (the
selector chooses the source ON the constraint `η_{i_*} / η_obs = 1`).

In other words, **Branch B's "1.0" is not a derivation; it is the
target of a fitting-to-η_obs procedure** with selector ambiguity
modulo the parity-degeneracy. By contrast, Branch A's 0.1888 is
a deterministic transport-chain output without selector freedom.

## Counterfactual — what would a Branch-B closure require?

For Branch B to provide a unique η-closure, the framework would need
an audit-ratified CP-odd selector functional. Examples of
what would NOT work (already considered and ruled out):

- **CP-odd polynomial in `(ξ, η, δ)`**: the `δ → -δ` symmetry
  forces any CP-odd polynomial to vanish at `δ = 0`, which is the
  selected value of all four current selectors. So adding a small
  CP-odd polynomial perturbation does not select a unique sheet
  unless it dominates over the CP-even action.
- **Fitting `δ_*` to PDG `δ_PMNS`**: forbidden import.
- **Selecting `sgn(sin δ_*) = +1` by convention**: violates the
  framework's discreteness-from-Cl(3) principle.

A genuinely framework-native CP-odd selector would need to derive
a sign convention from current Cl(3)/Z³ structure. The closest
candidate in the framework's existing language is the **right-
sensitive 2-real Z_3 doublet-block selector law** named in cycle
09's transport-status note as the open theorem object. Closing
that selector law is the genuine remaining hard residual; cycle
21 sharpens but does not close it.

## What this cycle claims

- (C1) The four candidate Branch-B selectors are all CP-sheet
  blind under δ → -δ — verified symbolically and numerically.
- (C2) The baryogenesis source `γ = x_1 y_3 sin(δ)` is
  CP-odd — verified symbolically.
- (C3) Therefore the entire current Branch-B selector bank
  cannot uniquely select a baryogenesis witness — exclusion
  argument from C1 + C2.
- (C4) The framework's only deterministic unique η output under
  the current bank is Branch A's
  `(516/53009) · Y₀² · F_CP · κ_axiom = 0.1888...`.
- (C5) The numerical mismatch 0.1888 vs 1.0 is downstream of
  Branch A's Y₀² and α_LM imports plus Branch B's selector-
  fitting structure on a different surface; cycle 21 does NOT
  resolve it.

## What this cycle does NOT claim

- Does NOT promote any selector or branch to retained.
- Does NOT close cycle 09 Obstruction 2 by constructing a
  positive selector — sharpens it to the right-sensitive 2-real
  Z_3 doublet-block selector law (the open hard residual).
- Does NOT consume η_obs as derivation input.
- Does NOT promote PMNS chart constants γ, E₁, E₂ to retained.
- Does NOT explain the numerical mismatch between branches.

## Inherited obstructions (named in prior cycles, not new)

- Cycle 09 O1 / cycle 12 R2 / cycle 15 R1: Y₀² = (G_weak²/64)²
  phenomenological import.
- Cycle 09 O3: α_LM mass scale via plaquette/CMT.
- Cycle 09 transport-status: right-sensitive 2-real Z_3
  doublet-block selector law. **This is the genuine remaining
  hard residual selected to bear the resolution of cycle 09
  Obstruction 2.**

## Validation

Primary runner: [`scripts/frontier_pmns_branch_selector.py`](./../scripts/frontier_pmns_branch_selector.py)
verifies:

1. Branch A reproduction: `(516/53009) · Y₀² · F_CP · κ_axiom`
   reproduces 0.1888... to 12 decimal digits via cycle 18's
   structural form.
2. Branch B reproduction: each of the four selectors yields its
   documented numerical output (1.0, 1.0, 1.052, 1.0).
3. CP-sheet blindness symbolic verification:
   - min-info: `D_KL(x||x_seed) + D_KL(y||y_seed) + (1-cos δ)`
     is even under `δ → -δ`.
   - obs-rel-action: `H_e(δ) = H_e(-δ)` for the chart
     parameterization, hence the action is even.
   - transport-extremal: `max_i η_i/η_obs` is even because
     transport functional is even.
   - continuity-closure: inherits parity.
4. Source-channel CP-oddness: `γ(δ) = -γ(-δ)` numerically and
   symbolically.
5. Counterfactual: a hypothetical CP-odd selector
   `O_odd = sin(δ) · (some CP-even action)` breaks the parity
   problem (verified).
6. Counterfactual: alternative chart constants γ=1, E₁=E₂=1
   would produce different transport but same parity issue.
7. Forbidden-import audit: η_obs comparator only; no PDG values;
   no fitted selectors; no literature numerical comparators.

## Cited dependencies

- (A1) [`ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md`](ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md)
  (bounded_theorem, audit-pending, cycle 18).
- (A2) [`DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md`](DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16.md)
  (support-grade).
- (A3) [`DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_SELECTOR_BANK_CP_SHEET_BLINDNESS_THEOREM_NOTE_2026-04-16.md)
  (exact obstruction theorem on open gate; effective status pipeline-derived).
- (A4a) [`DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW_NOTE_2026-04-16.md)
  (support-grade).
- (A4b) [`DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md)
  (support-grade).
- (A4c) [`DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md)
  (support-grade).
- (A4d) [`DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md`](DM_LEPTOGENESIS_PMNS_CONSTRUCTIVE_CONTINUITY_CLOSURE_THEOREM_NOTE_2026-04-17.md)
  (support-grade).
- (A5) [`DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md`](DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)
  (historical/exact transport provenance, cycle 09 parent).

## Cross-references

- `ETA_COSMOLOGY_DERIVATION_STRETCH_ATTEMPT_NOTE_2026-05-02.md`
  (cycle 09 parent named in prior-cycle materials; not present as a
  current-main source dependency).
- [`EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md`](EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md)
  (cycle 12; this cycle inherits cp1/cp2 = -√3).
- [`ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md`](ETA_188_STRUCTURAL_ORIGIN_PARTIAL_NOTE_2026-05-03.md)
  (cycle 18; this cycle uses the structural decomposition of Branch A).

## Honest claim type

This is a **stretch attempt with negative-structural exclusion**:

- Negative component: the entire current Branch-B selector bank
  (four candidate laws) is CP-sheet blind, hence cannot uniquely
  select a baryogenesis witness.
- Sharpening component: cycle 09 Obstruction 2 is reduced to the
  right-sensitive 2-real Z_3 doublet-block selector law (cycle
  09 transport-status open object).
- No new positive closure constructed. No retained-grade
  promotion. Audit ratification still required.
