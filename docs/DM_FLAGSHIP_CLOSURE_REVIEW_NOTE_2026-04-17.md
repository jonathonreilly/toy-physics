# DM Flagship Gate — Closure Review

**Date:** 2026-04-17
**Status:** flagship gate CLOSED on the live DM-neutrino source-oriented sheet via the observational PMNS promotion (P3) lane. The basin-uniqueness sub-blocker is closed by a retained theorem (Sylvester inertia preservation on the source branch). The closure is conditional on (i) the observational hierarchy pairing `σ_hier = (2, 1, 0)` and (ii) the SM-canonical Higgs Z_3 assignment `q_H = 0`; the θ_23 upper-octant prediction is retained-grade and falsifiable at DUNE / JUNO / Hyper-K.
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
**Runner coverage:** 14 frontier runners, **PASS = 422, FAIL = 0**.

## Scope

This note is the single-document reviewer entry point for the integrated
closure of the DM flagship gate's last-mile selector problem — the
right-sensitive 2-real selector law on the active pair `(δ, q_+)` on the
live DM-neutrino source-oriented sheet.

The story has four movements:

1. **Baseline promotion.** The retained three-generation observable algebra
   acts irreducibly on `H_hw=1`. Schur's lemma then forces the zero-source
   baseline `D = m I_3`, promoting the previously bounded scalar-baseline
   active quadratic from diagnostic to theorem-native curvature.

2. **Systematic obstruction tour.** Ten independent runners prove that no
   sole-axiom functional on the retained atlas can pin `(δ, q_+)` at the
   local-polynomial microscopic level. Each obstruction is a new retained
   theorem in its own right.

3. **Closure via observational promotion.** Direct diagonalization of the
   retained affine Hermitian `H(m, δ, q_+)` on `H_hw=1`, with the charged-
   lepton mass basis fixed via the `q_H = 0` branch of the Z_3 trichotomy,
   yields an explicit retained map
    ```
    (m, δ, q_+) ↦ (sin²θ_12, sin²θ_13, sin²θ_23, δ_CP)
    ```
   on the chamber `q_+ ≥ √(8/3) − δ`. Observational PMNS (PDG 2024 / NuFit
   5.3 NO central) pins the unique perturbative-regime chamber solution
    ```
    (m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042).
    ```

4. **Downstream unlock + falsifiable predictions.** PMNS is promoted from
   atlas-open to retained as `f(H)` on the chamber, unlocking flavor /
   cosmology / leptogenesis downstream. The closure produces two
   independent retained predictions:
    ```
    sin(δ_CP) = −0.9874,   δ_CP ≈ −81° (= 279°),   |J| = 0.0328
    s_23² ≥ 0.5410    (upper octant required for chamber closure)
    ```
   both falsifiable at DUNE / JUNO / Hyper-Kamiokande.

## Why this matters

The DM flagship gate was the sole remaining live flagship gate on the
retained publication surface. Closing this gate lifts the DM flagship into
the retained publication-grade package AND unlocks downstream observational
lanes (PMNS angles, leptogenesis transport, flavor sector) that route
through PMNS.

## Attack structure — 14 retained runners

The attack surface is structured as a clean sequence of attack-and-obstruction /
attack-and-closure runs. Each runner is self-contained with PASS/FAIL harness.

| # | Role | Runner | PASS | Result |
|---|------|--------|-----:|--------|
| 1 | baseline | `frontier_dm_neutrino_source_surface_schur_scalar_baseline_theorem.py` | 19 | Schur forces `D = m I_3` on retained irreducible `H_hw=1` |
| 2 | obstruction | `frontier_dm_neutrino_source_surface_info_geometric_selection_obstruction.py` | 26 | Quadratic Unanimity + Cubic Splitting |
| 3 | obstruction | `frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py` | 26 | Z_3 cubic variational obstruction |
| 4 | obstruction | `frontier_dm_neutrino_source_surface_z3_parity_split_theorem.py` | 22 | Z_3 parity-split: parity-definite scalars are 1-D on `(δ, q_+)` |
| 5 | obstruction | `frontier_dm_neutrino_transport_chamber_blindness_theorem.py` | 16 | Transport chain blind to chamber motion |
| 6 | obstruction | `frontier_dm_neutrino_source_surface_parity_mixing_selection_obstruction.py` | 27 | Parity-mixing candidate + selection ambiguity |
| 7 | obstruction | `frontier_dm_neutrino_observable_bank_exhaustion_theorem.py` | 36 | Retained observable bank exhausted; P1/P2/P3 stratification |
| 8 | obstruction | `frontier_dm_neutrino_source_surface_quartic_isotropy_and_u2_obstruction.py` | 18 | U(2)-invariance obstruction + quartic-isotropy identity `Tr(J⁴) = ½[Tr(J²)]²` |
| 9 | obstruction | `frontier_dm_neutrino_source_surface_microscopic_polynomial_impossibility_theorem.py` | 35 | Microscopic-polynomial impossibility on `(δ, q_+)` |
| 10 | obstruction | `frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py` | 37 | K_doublet is Hermitian ⇒ only U(2) adjoint, not bifundamental |
| 11 | tightening | `frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py` | 46 | Retained Sylvester inertia-preservation selector picks Basin 1 on the source branch (primary); scale bounds kept as consistency diagnostics |
| 12 | tightening | `frontier_pmns_theta23_upper_octant_chamber_closure_prediction.py` | 31 | θ_23 upper-octant retained prediction; threshold `s_23²_min = 0.5410` |
| 13 | tightening | `frontier_charged_lepton_ue_identity_via_z3_trichotomy.py` | 40 | `U_e = I` via Z_3-trichotomy `q_H = 0` branch |
| 14 | **CLOSURE** | **`frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py`** | **43** | **Retained PMNS-as-f(H) map + observational chamber pin** |
| | | **Total** | **422** | **422 PASS / 0 FAIL** |

All runners are `scripts/frontier_*.py` with their accompanying theorem
notes in `docs/*_NOTE_2026-04-17.md`.

## The Schur baseline

→ [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)

**Theorem (Canonical Scalar Baseline from Schur).** The retained
three-generation observable algebra `⟨P_1, P_2, P_3, C_3[111]⟩` acts
absolutely irreducibly on `H_hw=1`. Any `C`-linear operator commuting with
every retained generator is scalar (Schur); Hermiticity restricts to `R`.
Hence the zero-source baseline is `D = m I_3` for real `m`. The axiom-native
observable-principle curvature

$$
Q(\delta, q_+) = 6(\delta^2 + q_+^2)/m^2
$$

is theorem-native on the active pair.

**Structural lemma (Z_3-circulant norm form).** On the scalar baseline,

$$
\det(m I + \delta T_\delta + q_+ T_q) = m^3 - 3m|w|^2 + 2\operatorname{Re}(w^3), \quad w = q_+ + i\delta.
$$

**Gap narrowed.** From `(baseline-choice) AND (selector-principle)` to
`(selector-principle)` only.

## The obstruction tour

Nine independent obstruction theorems prove that no sole-axiom functional on
the retained atlas pins `(δ, q_+)` at the local-polynomial microscopic level.

### Info-geometric selection obstruction
→ [DM_NEUTRINO_SOURCE_SURFACE_INFO_GEOMETRIC_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_INFO_GEOMETRIC_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md)

Quadratic Unanimity Theorem — natural info-geometric functionals (minus-W,
KL, Fisher, Frobenius) are isotropic at quadratic order and share the
`(√6/3, √6/3)` chamber minimum. Cubic Splitting Obstruction — at cubic order
they split by O(1); no axiom-native tiebreaker.

### Cubic variational selection obstruction
→ [DM_NEUTRINO_SOURCE_SURFACE_CUBIC_VARIATIONAL_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_CUBIC_VARIATIONAL_OBSTRUCTION_NOTE_2026-04-17.md)

Five compounding obstructions: fixed-m chamber extrema are m-dependent,
joint stationary points are all at `det = 0` singularities, cubic-only
functional extrema disagree, cubic-maximizing orbit has multiple chamber-
accessible rays, `W = log|det|` is invariant under `sign(det)`.

### Z_3 parity-split theorem
→ [DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md)

`T_q` is purely Z_3-circulant, `T_δ` is purely Z_3-anti-circulant.
Consequently any Z_3-parity-definite scalar constrains at most one of
`(δ, q_+)` at fixed m — rules out the entire parity-definite functional
class.

### Transport chamber-blindness theorem
→ [DM_NEUTRINO_TRANSPORT_CHAMBER_BLINDNESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_TRANSPORT_CHAMBER_BLINDNESS_THEOREM_NOTE_2026-04-17.md)

`η/η_obs` factors through the source-package `(γ, E_1, E_2, K_00, cp_1, cp_2)`,
each invariant under chamber motion. Hence `η/η_obs` is CONSTANT on the
chamber at 0.189; the level set `{η/η_obs = 1}` is EMPTY on the chamber.

### Parity-mixing selection obstruction
→ [DM_NEUTRINO_SOURCE_SURFACE_PARITY_MIXING_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PARITY_MIXING_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md)

Sum-of-parity-definite invariants evade the parity-split obstruction. The
Frobenius norm `‖K_doublet‖_F²` has a unique m-independent minimizer at
`(√6/2 − √2/18, √6/6 + √2/18)`, but `det K_doublet` gives a different
minimizer — new "functional-selection ambiguity" obstruction.

### Observable-bank exhaustion theorem
→ [DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md)

Survey of retained atlas observables (`R = Ω_DM/Ω_B`, `m_DM`, `Δm²_atm`,
PMNS angles, `σ_DD`, `g-2`, see-saw mass, `η` on PMNS-assisted route). Every
retained observable with an observational target factors through the
frozen-on-chamber bank. Selector-gate is stratified into three explicit
promotion lanes P1 / P2 / P3.

### Quartic-isotropy + U(2)-invariance obstruction
→ [DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17.md)

U(2)-invariant PD quadratic functionals form a 2-parameter cone
`{A(Tr K)² + B det K : B < 0, A > −B/4}` — five PD members give five
different minimizers. Full-W fixed-m argmax is m-dependent at all 9 tested m
values. New identity: `Tr(J⁴) = (1/2)[Tr(J²)]²` at scalar baseline — no new
parity-mixing information at quartic order.

### Microscopic-polynomial impossibility theorem
→ [DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md)

Every retained polynomial microscopic functional of `H` (trace moments,
`det(H)`, heat kernel, spectral gap, Ward identities, Cl(3) bivector
invariants) is EVEN in δ and depends on `(δ, q_+)` only through `(δ², q_+)`.
The axiom is GENUINELY SILENT on `(δ, q_+)` at the local-polynomial level.
Closure requires a nonlocal / observational ingredient — which forces the P3
lane below.

### Bifundamental-invariance obstruction theorem
→ [DM_NEUTRINO_SOURCE_SURFACE_BIFUNDAMENTAL_INVARIANCE_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_BIFUNDAMENTAL_INVARIANCE_OBSTRUCTION_THEOREM_NOTE_2026-04-17.md)

`K_doublet` is automatically Hermitian (from the retained chain `H Hermitian →
K_Z3 Hermitian → K_doublet principal submatrix`). A 2×2 Hermitian has 4 real
parameters and admits only the 3-parameter U(2) adjoint action, NOT the
8-parameter U(2)_L × U(2)_R bifundamental. The retained atlas is
"Hermitian-data-first" — bifundamental is a downstream input channel, not a
retained symmetry.

## The three tightening theorems

After the initial obstruction tour + closure was laid down, adversarial
review surfaced five issues. Three dedicated theorems close them.

### Inertia-preservation basin-uniqueness theorem (CRITICAL 1 + 2)
→ [DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md)

The retained observable `W[J] = log|det(H_base + J)|` is well-defined on
the complement of the caustic `det(H_base + J) = 0`. Its natural domain
on the source-oriented sheet is the **source branch** `B_src` — the
connected component containing `J = 0`, equivalently the set of `J`
preserving the retained signature `signature(H_base + J) = signature(H_base) = (2, 0, 1)`.
Signature is a Sylvester congruence-invariant of the retained Hermitian
form (an algebraic axiom-native quantity, not a new principle).

Checked at all in-chamber χ²=0 basins:

| Branch | `(m, δ, q_+)` | sin(δ_CP) | `signature(H)` | `det(H)` | source branch? |
|---|---|---:|---|---:|---|
| Basin 1, σ=(2,1,0) | (0.657, 0.934, 0.715) | −0.987 | **(2, 0, 1)** | **+0.959** | **YES** |
| Basin 2, σ=(2,1,0) | (28, 21, 5) | +0.554 | (1, 0, 2) | −70377 | no (signature flipped) |
| σ=(2,0,1) cluster | (21, 13, 2) | −0.419 | (1, 0, 2) | −20295 | no (signature flipped) |

The retained inertia selector simultaneously excludes the second
σ=(2,1,0) basin AND the competing σ=(2,0,1) permutation: both flip
`signature` across the caustic and therefore lie on a different branch
than the retained baseline. Basin 1 is the unique source-branch
chamber closure.

Scale diagnostics remain recorded for transparency: `‖J‖_F / ‖H_base‖_F`
is 0.94 at Basin 1 vs 20.9 and 13.9 at the competing basins; the scale
bounds independently also pick Basin 1 (consistency check), but the
retained primary selector is the Sylvester inertia invariant.

### θ_23 upper-octant chamber-closure prediction (SERIOUS 3)
→ [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md)

At PDG 2024 central `(s_12², s_13²) = (0.307, 0.0218)`, the H-diagonalization
admits a chamber solution iff `s_23² ≥ 0.5410`. Across the full NuFit 5.3
NO 3σ rectangle on `(s_12², s_13²)`, the threshold lies in `[0.5335, 0.5476]`
— entirely in the upper octant. The retained map therefore **predicts θ_23
in the upper octant**. A >3σ lower-octant determination would unconditionally
falsify closure.

**Structural coincidence.** The Schur-Q variational candidate `(√6/3, √6/3)`
and the PMNS-pinning threshold lie on the SAME chamber-boundary line
`q_+ + δ = √(8/3)` (because `2√6/3 = √(8/3)` exactly). Two independent
retained landmarks — variational and observational — meet on the same
1-parameter chamber-boundary ridge.

### Charged-lepton `U_e = I` via Z_3 trichotomy (MEDIUM 4)
→ [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md)

Clean retained route for `U_e = I` in the axis basis:
1. Retained conjugate Z_3 triplets `q_L = (0, +1, −1)`, `q_R = (0, −1, +1)` on
   `H_hw=1`.
2. Z_3 trichotomy + single Higgs with definite `q_H` → three permutation
   supports.
3. On the `q_H = 0` branch (SM-canonical, conditional not axiom-forced),
   `Y_e = diag(y_1, y_2, y_3)`.
4. Therefore `U_e = I` in the axis basis.

This route uses ONLY retained atlas objects and does NOT depend on the
Dirac-bridge theorem's open `C^16 → 3×3` normalization step.

## The closure

→ [PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md](./PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md)

With sole-axiom variational routes exhausted (microscopic-polynomial
impossibility + bifundamental obstruction + parity-split + info-geometric
splitting), closure proceeds through the observational-promotion P3 lane.

**Main theorem (retained-grade map).** Direct diagonalization of the
retained affine Hermitian `H(m, δ, q_+)` on `H_hw=1`, with the charged-
lepton mass basis fixed to the axis basis by the Z_3 trichotomy `q_H = 0`
branch and row-permuted by the hierarchy pairing `σ = (2, 1, 0)`, yields
an explicit retained map

$$
(m, \delta, q_+) \;\longmapsto\; (\sin^2\theta_{12},\ \sin^2\theta_{13},\ \sin^2\theta_{23},\ \delta_{CP})
$$

on the chamber `q_+ ≥ √(8/3) − δ`.

**Pinning theorem (unique source-branch chamber solution).** Requiring the
map to reproduce PDG 2024 central observational values
`(sin²θ_12, sin²θ_13, sin²θ_23) = (0.307, 0.0218, 0.545)` has a unique
source-branch (inertia-preserving) chamber solution

$$
\boxed{(m_*,\ \delta_*,\ q_+^*) \;=\; (0.657061,\ 0.933806,\ 0.715042)}
$$

verified by multi-start Nelder-Mead + fsolve sharpening to machine
precision. The two competing in-chamber χ²=0 basins sit on the
`signature = (1, 0, 2)` branch with `det(H_base + J) < 0`; they are
excluded by the Sylvester inertia-preservation theorem.

**Falsifiable δ_CP consequence.** The map sends `R^3` to a 3-dim submanifold
of `R^4`; three observational inputs pin `(m, δ, q_+)`, and δ_CP is the
forced geometric consequence:

$$
\boxed{\sin\delta_{CP} = -0.9874, \quad \delta_{CP} \approx -81° \;(\equiv 279°), \quad |J| = 0.0328}
$$

in the T2K-preferred lower octant. Disagreement with future measurements at
DUNE / Hyper-Kamiokande falsifies the construction (not just the pin).

**Observational consistency.** All nine entries of `|U_PMNS|` at the pinned
point lie inside the NuFit 5.3 NO 3σ ranges (9/9 PASS).

## Claim boundary (non-negotiable)

### What is claimed

1. **Retained map theorem.** `(m, δ, q_+) → (θ_ij, δ_CP)` is retained-grade
   on the chamber, constructed from retained inputs only (affine chart +
   chamber + three-generation observable theorem + Z_3 trichotomy `q_H = 0`
   branch + Schur baseline).
2. **Closure via observational promotion (P3 lane).** Retained map + PDG
   PMNS data + perturbative-uniqueness criterion → unique chamber pin.
   Publication-grade closure, NOT sole-axiom closure. The 3-real
   observational input supplies the missing selector degree of freedom.
3. **Falsifiable predictions.** `sin δ_CP = −0.9874` (CP phase) and
   `s_23² ≥ 0.5410` (θ_23 upper octant). Both testable at DUNE / JUNO /
   Hyper-Kamiokande.
4. **PMNS promoted to retained on the chamber** as `f(H)`. Unlocks
   downstream flavor / cosmology / leptogenesis lanes.
5. **DM flagship gate CLOSED** at publication-grade via P3, at
   `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`.

### What is NOT claimed

- **Not sole-axiom closure.** The microscopic-polynomial impossibility
  theorem proves sole-axiom closure at that level is IMPOSSIBLE; closure
  via retained map + observational pin is the strongest available.
- **Not solar-gap `Δm²_21`** (different carrier than H).
- **Not absolute neutrino mass scale** (different carrier).
- **Not Majorana CP phases** (separate sector).
- **Not promotion of minimum-coupling / minimum-information to retained.**
  Those remain atlas-flagged post-axiom.
- **Closure is conditional on `θ_23` upper octant.** Lower-octant
  determination at >3σ would falsify it.

## Downstream lanes unlocked

- **Leptogenesis.** The DM-leptogenesis PMNS-assisted transport witness can
  now be evaluated at the pinned chamber point with PMNS SUPPLIED BY THE
  THEOREM rather than floating 5 real parameters.
- **Flavor sector.** PMNS-triviality negative result on the two-Higgs /
  parity-mixing lane reorganizes into a specific relationship between the
  live `H` sheet and the flavor-currents family.
- **Observational predictions for DUNE / JUNO / Hyper-Kamiokande.** Two
  falsifiable retained predictions on the near-term experimental horizon.

## Still open (honestly flagged)

1. Solar gap `Δm²_21` (different carrier).
2. Absolute neutrino mass scale (different carrier).
3. Majorana CP phases `α_21, α_31` (separate Majorana sector).
4. Sole-axiom closure of the selector principle: impossible at
   microscopic-polynomial level (proven); a nonlocal sole-axiom route
   remains hypothetically possible.
5. P1 / P2 alternative promotion lanes — identified by the observable-
   bank exhaustion theorem, complementary to the realized P3 closure.

## Review order for a skeptical reviewer

1. This note (the map).
2. [PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md](./PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md) — the closure.
3. [DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md) — what selects Basin 1.
4. [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md) — θ_23 upper-octant falsifiable prediction.
5. [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md) — why `U_e = I` in the axis basis.
6. [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md) — baseline promotion.
7. [DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md) — why closure had to go through observational promotion.

## Runner verification

All 14 runners pass on the current surface. Reproduce with:

```
PYTHONPATH=scripts python3 scripts/frontier_*_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_*_obstruction.py
PYTHONPATH=scripts python3 scripts/frontier_*_prediction.py
PYTHONPATH=scripts python3 scripts/frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py
```

Expected: total PASS = 422, FAIL = 0.

## Position on the flagship paper surface

The DM flagship gate is now CLOSED at publication-grade via observational
promotion (P3). The retained publication package now has ZERO live flagship
gates. The correct ARXIV_DRAFT wording is:

> The DM flagship gate has closed at publication-grade via the retained
> PMNS-as-f(H) construction and observational PMNS pinning. The chamber
> closure point is
> `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`,
> with basin-uniqueness on the retained source branch guaranteed by the
> Sylvester inertia-preservation theorem (an algebraic congruence-invariant
> of the retained Hermitian curvature; no post-axiom principle is imported).
> The closure supplies two falsifiable retained predictions:
> `sin δ_CP = −0.9874` and `θ_23` in the upper octant with threshold
> `s_23² ≥ 0.5410`. Sole-axiom closure remains impossible at the
> microscopic-polynomial level per the impossibility theorem; closure-via-
> observational-promotion is the published result.

## What this file must never say

- that the selector gate is closed sole-axiom (it is not; closure is via
  the observational-promotion P3 lane)
- that the microscopic-polynomial impossibility theorem is overturned (it
  stands; it is what forces the P3 route)
- that the δ_CP prediction is a fit parameter (it is a forced geometric
  consequence of the retained map)
- that PMNS is closed sole-axiom (the map is sole-axiom retained-grade;
  the pinning uses 3 observational PMNS values)
- that the DM flagship cascade is now fully sole-axiom (the closure is at
  retained-publication-grade, the standard for a Nature-level flagship
  claim)
- that a Frobenius / operator-norm scale bound is the primary basin
  selector (those are consistency diagnostics; the retained primary
  selector is the Sylvester inertia-preservation theorem)
- that `W[J] = log|det(H_base + J)|` requires Taylor convergence at the
  Basin 1 amplitude (the retained log-det observable is defined on the
  source branch by direct diagonalisation; the series-disk `ρ < 1` is an
  honest analytic-representation boundary, not the retained selector)
