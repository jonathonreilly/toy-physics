# Cycle 16 (Retained-Promotion) Claim Status Certificate — PMNS Chart Constants Retention Stretch Attempt

**Block:** physics-loop/pmns-chart-constants-2026-05-03
**Note:** docs/PMNS_CHART_CONSTANTS_RETENTION_STRETCH_ATTEMPT_NOTE_2026-05-03.md
**Runner:** scripts/frontier_pmns_chart_constants_retention.py
**Target row:** cycle 12 Obstruction O1 — PMNS chart constants
γ = 1/2, E₁ = √(8/3), E₂ = √(8)/3 are support-grade in the
PMNS leptogenesis context. Three sub-obstructions:
  - Sub-obstruction A: γ = 1/2
  - Sub-obstruction B: E₁ = √(8/3)
  - Sub-obstruction C: E₂ = √(8)/3 = 2√2/3

## Block type

**Stretch attempt (output type (c)) with three sub-obstruction
analyses + named obstructions for each.**

The cycle attempts a structural-origin derivation for each of the
three chart constants γ, E₁, E₂ from minimal framework primitives
plus standard math, identifying which sub-constants achieve
closing derivation, partial derivation, or remain as named
obstructions blocking absolute retention.

## Promotion Value Gate (V1–V5)

### V1: SPECIFIC verdict-identified obstruction this PR closes/sharpens

Quoted directly from cycle 12's note `EPSILON1_FROM_CP_CHAIN_STRETCH_ATTEMPT_NOTE_2026-05-03.md`:

> ### Obstruction O1: PMNS chart constants γ, E₁, E₂ are support-grade
>
> The chart constants γ = 1/2, E₁ = √(8/3), E₂ = √8/3 appear in
> `PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21` as
> "existing chart constants" but the support note explicitly says:
>
> > The support proposal is the three-equation system... These
> > two equations are the live candidate selector laws. The
> > support package keeps them explicit as proposals rather than
> > hiding them under retained language.
>
> **Specific repair target**: produce a closing derivation that
> the chart constants (γ, E₁, E₂) are forced by retained
> PMNS-sector structure.

**This PR's stretch attempt** sharpens that obstruction by:

1. Identifying the existing structural decomposition:
   - γ = c_odd · a_sel (retained_conditional via DM_NEUTRINO_CODD_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15)
   - E₁ = √(8/3) · τ_+ (retained_conditional via DM_NEUTRINO_VEVEN_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15)
   - E₂ = (√8/3) · τ_+ (same retained_conditional theorem)
2. Examining each amplitude factor (c_odd, a_sel, v_even, τ_+)
   for retention status against minimal primitives.
3. Working through three sub-obstructions:
   - **Sub-obstruction A (γ)**: a_sel = 1/2 from sharp selector
     projector P_nu = diag(1,0), centered against (P_nu + P_e)/2;
     the centering arithmetic is trivial but the choice of
     "sharp resolved branch projector" over "soft weighted
     mixture" is the load-bearing premise.
   - **Sub-obstruction B (E₁)**: traces back to the structural
     identity √(8/3) E₁ = τ_+ · √(8/3) which forces E₁ = √(8/3)
     from the spec(F₁) = ±√(3/8) eigenvalue, with the absolute
     scale of E₁ inheriting from c_odd = +1's branch convention.
     The structural origin √(8/3) is exact via Frobenius dual
     normalization.
   - **Sub-obstruction C (E₂)**: traces back to spec(F₂) = ±3/√8
     with E₂ = √(8)/3 = (3/√8)⁻¹ · (3/√8) · 1/(3/√8) · ... a
     direct algebraic consequence; E₂² = 8/9 (so √(8/3) ≈ 1.633
     and √8/3 ≈ 0.943 are different magnitudes as the prompt
     correctly notes).
4. Counterfactual demonstrations: alternative chart constants
   would break cp1/cp2 = -√3 (cycle 12's verified ratio) or
   would conflict with the retained source-surface theorem.
5. Three named obstructions for absolute retention.

### V2: NEW derivation contained

The retained `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM_NOTE_2026-04-16`
demonstrates γ, E₁, E₂ are exact on a nonempty H-side source surface
(with explicit positive-Hermitian witness). The audited_conditional
c_odd and v_even theorems show how these values arise from sharp
projector + Frobenius dual eigenvalue spectra. But NO existing
artifact:

1. Walks through ALL THREE chart constants in a single cross-check
   runner verifying numerical agreement against multiple
   structural origin candidates (SU(2) Dynkin index, Cl(3)
   chirality projection, Koide γ-orbit, Frobenius eigenvalue,
   Casimir, swap-even projector amplitude).
2. Applies counterfactual perturbation tests to each constant
   independently (γ = 1/3, 1, 2 break sharp-projector centering;
   E₁ = √(2/3), 1, 2 break Frobenius-dual spectral match; E₂ =
   √(2/3), 1, √2 break F₂ ↔ (3/√8) Z_row spectral match).
3. Combines cycle 12's cp1/cp2 = -√3 ratio identity with each
   sub-constant counterfactual to demonstrate that ALL three
   chart constants must take their specific values to preserve
   the retained CP-channel ratio.
4. Documents the precise load-bearing premise blocking each
   sub-obstruction:
   - **Sub-A (γ)**: sharp selector projector P_nu = diag(1,0) vs
     soft mixture; load-bearing "bosonic-bilinear selector
     principle" axiom.
   - **Sub-B (E₁)**: Frobenius dual representative F₁ = (1/2)T_δ
     + (1/4)T_ρ where the coefficient 1/2, 1/4 derive from
     orthogonality on basis {A_op, b_op, c_op, d_op, T_δ, T_ρ};
     load-bearing assumption is the active Hermitian basis is
     Frobenius-orthogonal.
   - **Sub-C (E₂)**: same Frobenius dual machinery with F₂ =
     A_op + (1/4)b_op - (1/2)c_op - (1/2)d_op; load-bearing same
     orthogonality.

This is genuine new derivation content distinct from the
already-landed retained source-surface theorem. The retained
theorem proves γ, E₁, E₂ pull back to a nonempty H-side surface;
this PR works the structural ORIGIN of each constant from
upstream c_odd/v_even/swap-reduction primitives.

### V3: Audit lane couldn't already do this from existing retained primitives + standard math machinery

The audit lane in restricted one-hop context cannot synthesize:
- The three sub-obstruction analysis (A, B, C separately),
- Counterfactual perturbation across SU(2) Dynkin, Cl(3) chirality,
  Koide γ-orbit, Frobenius eigenvalue alternatives,
- Cross-constraint via cycle 12's cp1/cp2 = -√3 retained-bounded
  ratio,
- Identification of the specific load-bearing premises blocking
  each sub-constant retention,

simultaneously. Each chart constant individually is derivable
in audited_conditional form, but the cross-constraint analysis
combined with the cycle 12 ratio cross-check is multi-hop
synthesis the audit lane in one-hop scope cannot do.

### V4: Marginal content non-trivial

Yes:
- The trivial-origin candidates for γ = 1/2 (SU(2) Dynkin index,
  Cl(3) chirality projection, Casimir of fundamental rep)
  numerically match the retained value but each fails a structural
  test: γ does not transform as a Casimir invariant under the
  framework's Cl(3) automorphisms; the SU(2) Dynkin matches
  numerically by coincidence with the centered sharp-projector
  amplitude.
- E₁ = √(8/3) and E₂ = √8/3 have different magnitudes and trace
  back to different Frobenius dual representatives F₁ vs F₂; a
  single common origin candidate (e.g., both ∝ √(8/3)) is
  falsified by the runner.
- The cross-constraint with cp1/cp2 = -√3 forces specific values:
  alternative (γ, E₁, E₂) triples either preserve the ratio (if
  scaled uniformly) or break it (if scaled non-uniformly).
- The sharp-vs-soft projector choice for γ is not a textbook
  identity — it's a framework-internal selection law.

### V5: Not a one-step variant of an already-landed cycle in this campaign

| Cycle | Lane | Math |
|-------|------|------|
| 01 | matter content (anomaly) | Diophantine cubic-anomaly |
| 02 | matter content (Witten Z₂) | π_4 parity |
| 03 | observable principle | Cauchy multiplicative-additive |
| 04 | hypercharge uniqueness | Cubic in continuous Y |
| 05 | gravity (staggered) | Kogut-Susskind translation |
| 06 | Majorana null-space | synthesis 01+02+04 + null-space |
| 07 | EWSB Q = T_3 + Y/2 | EWSB derivation + Higgs ID |
| 08 | composite-Higgs | rep-theory arithmetic |
| 09 | η cosmology | numerical near-fits |
| 10 | GR atlas closure | overlap/cocycle algebra |
| 11 | unified harness 01+02+04+06+07 | integrated end-to-end |
| 12 | ε_1 from CP chain | source package → leptogenesis |
| 13 | full PL S³ atlas | 5-chart 4-simplex 10-cocycle |
| 14 | (parallel multi-day cycle) | (in progress) |
| 15 | (parallel multi-day cycle) | (in progress) |
| 16 (this) | PMNS chart-constant retention | sharp projector + Frobenius dual + spectral match across γ, E₁, E₂ |

Cycle 16 is the **first cycle to systematically attack the three
PMNS chart constants γ, E₁, E₂** as separate sub-obstructions.
Different math (sharp projector centering + Frobenius dual
isospectrality + counterfactual perturbation), different lane
(retiring cycle 12's Obstruction O1, the load-bearing PMNS
chart-constant support-grade status), and the first cycle in the
campaign to use cycle 12's cp1/cp2 = -√3 ratio as a
retained-bounded cross-constraint to falsify alternative chart
constants.

Not a one-step variant.

## Outcome classification (per prompt)

**(c) Stretch attempt with named obstructions, with partial
closing-derivation status for sub-A.**

Per-sub-constant outcome:
- **Sub-A (γ = 1/2)**: PARTIAL CLOSING DERIVATION. The
  centered sharp-projector amplitude derivation is direct
  algebra (P_nu - (1/2)(P_nu + P_e) = (1/2) S_cls), giving
  γ = c_odd · a_sel = (+1)(1/2) = 1/2. The load-bearing
  premise is "sharp resolved branch projector" vs "soft
  weighted mixture", which is itself an audited_conditional
  upstream (c_odd theorem). Falsifier: alternative weighted
  mixture would not give 1/2.
- **Sub-B (E₁ = √(8/3))**: STRETCH ATTEMPT WITH PARTIAL.
  Frobenius dual representative F₁ = (1/2)T_δ + (1/4)T_ρ has
  spec = {-√(3/8), 0, +√(3/8)}, isospectral to √(3/8) Z_row.
  Source-response on scalar baseline gives √(3/8) E₁ = τ_+,
  hence E₁ = √(8/3) τ_+ = √(8/3) (with τ_+ = 1 from sharp
  swap-even projector). Load-bearing premises: (a) Frobenius
  orthogonality of basis {A_op, b_op, c_op, d_op, T_δ, T_ρ},
  (b) τ_+ = 1 from sharp resolved swap-even projector.
- **Sub-C (E₂ = √8/3)**: STRETCH ATTEMPT WITH PARTIAL.
  Frobenius dual representative F₂ = A_op + (1/4)b_op -
  (1/2)c_op - (1/2)d_op has spec = {-3/√8, 0, +3/√8},
  isospectral to (3/√8) Z_row. Source-response gives (3/√8) E₂
  = τ_+, hence E₂ = √8/3 = 2√2/3. Same load-bearing premises
  as Sub-B.

**Not a closing derivation for Sub-B and Sub-C** because:
- Frobenius orthogonality is itself audited_conditional via
  c_odd, v_even theorems (both `audited_conditional`, not
  retained).
- τ_+ = 1 inherits from `dm_neutrino_weak_even_swap_reduction_theorem_note_2026-04-15`
  (audited_conditional).
- No fully-retained chain exists from minimal primitives to
  the specific values √(8/3), √(8)/3.

## Forbidden imports check

- η_obs (PDG / Planck observed value): NOT consumed.
- m_top: NOT consumed.
- sin²θ_W: NOT consumed.
- PDG neutrino mass values: NOT consumed.
- PMNS angle observed values: NOT consumed.
- y_0 (Yukawa scale via G_weak): NOT consumed (cycle 12's O2).
- α_LM (plaquette/CMT scale): NOT consumed (cycle 12's O3).
- cp1/cp2 = -√3 ratio: ADMITTED AS CYCLE-12 PRIOR-CYCLE INPUT.
- PMNS support-grade infrastructure: ADMITTED AS BOUNDED INPUT.
- DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM (retained):
  cited as retained framework output (not premised, derived).
- DM_NEUTRINO_CODD/VEVEN_BOSONIC_NORMALIZATION_THEOREMs
  (audited_conditional): cited as conditional upstream
  premises with role-labels.
- No fitted selectors consumed.
- No same-surface family arguments.
- Frobenius dual basis orthogonality: explicitly named as
  load-bearing premise (Obstruction B).

## Audit-graph effect

If independent audit ratifies this stretch attempt:
- Cycle 12's Obstruction O1 is sharpened from "support-grade"
  to three specific sub-obstructions with named load-bearing
  premises:
  - Sub-A: sharp resolved branch projector vs soft mixture
  - Sub-B: Frobenius dual basis orthogonality + τ_+ = 1
  - Sub-C: same as Sub-B
- The c_odd, v_even, weak-even-swap-reduction theorems become
  the targeted retention residuals for absolute closure.
- Future cycles can target ONE of: (a) promote c_odd from
  audited_conditional to retained, (b) promote v_even from
  audited_conditional to retained, (c) promote
  weak-even-swap-reduction to retained.

## Honesty disclosures

- This PR is a STRETCH ATTEMPT, not a closing derivation. None
  of the three chart constants achieves absolute closing
  derivation from retained-only primitives.
- Sub-A (γ = 1/2) achieves PARTIAL closing derivation modulo
  the c_odd theorem's audited_conditional status.
- Sub-B and Sub-C achieve PARTIAL via spectral match, but the
  Frobenius orthogonality and τ_+ = 1 premises are
  audited_conditional, not retained.
- The retained `DM_NEUTRINO_EXACT_H_SOURCE_SURFACE_THEOREM`
  proves γ, E₁, E₂ pull back to a nonempty H-side surface but
  does NOT derive their specific values from minimal primitives
  — that's the cycle 12 / cycle 16 obstruction.
- Audit-lane ratification required; no author-side tier asserted.
