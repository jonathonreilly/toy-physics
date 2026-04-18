# DM Flagship Gate — Open-Gate Review

**Date:** 2026-04-17 (2026-04-18 P3 Sylvester update applied)
**Status:** **OPEN flagship gate.** On the live DM-neutrino source-oriented
sheet the old pointwise P3 branch-choice rule is no longer merely imposed:
the pointwise signature statement at the retained P3 pin is now carried by
the retained local theorem
[DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md](./DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md).
That sharpens the old source-branch conditional into one retained local
theorem plus one named remaining source-side input `A-BCC`. The live G1
PMNS-as-`f(H)` package is therefore now best read as a **bounded** package on
an otherwise open flagship gate: `A-BCC` and the observational hierarchy
pairing `σ_hier = (2, 1, 0)` remain open, and the current-bank quantitative DM
selector / mapping side is also still open. **The previously-listed `q_H = 0`
conditional has been discharged as GAUGE (retained)** via the Higgs `Z_3`-
charge gauge-redundancy theorem.
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
**Runner coverage:** 16 frontier runners, **PASS = 513, FAIL = 0**. This now
includes the dedicated P3 Sylvester linear-path signature theorem runner
(`PASS = 11, FAIL = 0`). The integrated table below is preserved as the
pre-2026-04-18 route record; its older row labels should be read in that
historical sense except where superseded by the status block above.

## Scope

This note is the single-document reviewer entry point for the integrated
closure of the DM flagship gate's last-mile selector problem — the
right-sensitive 2-real selector law on the active pair `(δ, q_+)` on the
live DM-neutrino source-oriented sheet.

The story has four movements:

1. **Baseline — Schur commutant-class lemma (conditional, NOT a live-sheet
   promotion).** The retained three-generation observable algebra acts
   irreducibly on `H_hw=1`. Schur's lemma then forces the conditional
   statement: *if* a `C`-linear Hermitian operator commutes with every retained
   generator, *then* it must be scalar (`D = m I_3`) and the associated
   observable-principle curvature is `Q(δ, q_+) = 6(δ^2 + q_+^2)/m^2`. This is
   a **commutant-class structural lemma**. It does NOT prove that the live
   DM-neutrino source-sheet zero-source baseline actually satisfies the
   commutation premise. Consequently the scalar baseline and `Q` are used in
   what follows as a **conditional reference** (the scalar-commutant class),
   NOT as theorem-native live-sheet curvature.

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

4. **Downstream unlock + falsifiable consequences.** PMNS is promoted from
   atlas-open to a retained `f(H)` map on the chamber, unlocking flavor /
   cosmology / leptogenesis downstream. The conditional/support chamber pin
   produces two independent falsifiable consequences:
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
| 1 | baseline (commutant-class lemma only) | `frontier_dm_neutrino_source_surface_schur_scalar_baseline_theorem.py` | 26 | Conditional commutant-class Schur lemma: `D = m I_3` _if_ `D` commutes with the retained algebra on `H_hw=1`. Part 6 live-sheet witness: `H_live` at the closure pin does NOT commute with retained generators (`‖[H_live, C_3]‖_F ≈ 3.96`; `‖[H_live, P_i]‖_F ≠ 0` for `i=1,2,3`). Live-sheet commutation premise is NOT derived here. |
| 2 | obstruction | `frontier_dm_neutrino_source_surface_info_geometric_selection_obstruction.py` | 26 | Quadratic Unanimity + Cubic Splitting |
| 3 | obstruction | `frontier_dm_neutrino_source_surface_cubic_variational_obstruction.py` | 26 | Z_3 cubic variational obstruction |
| 4 | obstruction | `frontier_dm_neutrino_source_surface_z3_parity_split_theorem.py` | 22 | Z_3 parity-split: parity-definite scalars are 1-D on `(δ, q_+)` |
| 5 | obstruction | `frontier_dm_neutrino_transport_chamber_blindness_theorem.py` | 16 | Transport chain blind to chamber motion |
| 6 | obstruction | `frontier_dm_neutrino_source_surface_parity_mixing_selection_obstruction.py` | 27 | Parity-mixing candidate + selection ambiguity |
| 7 | obstruction | `frontier_dm_neutrino_observable_bank_exhaustion_theorem.py` | 36 | Retained observable bank exhausted; P1/P2/P3 stratification |
| 8 | obstruction | `frontier_dm_neutrino_source_surface_quartic_isotropy_and_u2_obstruction.py` | 18 | U(2)-invariance obstruction + quartic-isotropy identity `Tr(J⁴) = ½[Tr(J²)]²` |
| 9 | obstruction | `frontier_dm_neutrino_source_surface_microscopic_polynomial_impossibility_theorem.py` | 35 | Microscopic-polynomial impossibility on `(δ, q_+)` |
| 10 | obstruction | `frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py` | 37 | K_doublet is Hermitian ⇒ only U(2) adjoint, not bifundamental |
| 11 | branch-choice rule (conditional admissibility) | `frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py` | 46 | Sylvester inertia preservation on the baseline-connected component picks Basin 1 _given_ the imposed branch-choice admissibility rule. The rule itself is NOT a retained theorem on this branch (Option B open item). |
| 12 | tightening | `frontier_pmns_theta23_upper_octant_chamber_closure_prediction.py` | 31 | θ_23 upper-octant conditional/support consequence; threshold `s_23²_min = 0.5410` |
| 13 | tightening | `frontier_charged_lepton_ue_identity_via_z3_trichotomy.py` | 40 | `U_e = I` via Z_3-trichotomy `q_H = 0` branch (status: GAUGE retained via row 15) |
| 14 | **CONDITIONAL / SUPPORT CLOSURE** | **`frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py`** | **43** | **Retained PMNS-as-f(H) map + observational chamber pin, conditional on the imposed branch-choice admissibility rule and `σ_hier = (2,1,0)`, upper octant** |
| 15 | Option-B q_H = 0 closure | `frontier_higgs_z3_charge_pmns_gauge_redundancy_theorem.py` | 73 | Higgs `Z_3`-charge gauge-redundancy theorem: `q_H` is gauge-redundant wrt PMNS observables; three branches give identical `Y_e Y_e†` on `L_L` axes ⇒ identical `U_e = I` ⇒ identical `|U_PMNS|`. Upgrades `q_H = 0` from CONDITIONAL to GAUGE (retained). Closes one of the three flagship conditionals. |
| | | **Total** | **502** | **502 PASS / 0 FAIL** |

All runners are `scripts/frontier_*.py` with their accompanying theorem
notes in `docs/*_NOTE_2026-04-17.md`.

## The Schur baseline — commutant-class lemma only (conditional)

→ [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)

**Commutant-class lemma (Schur).** The retained three-generation observable
algebra `⟨P_1, P_2, P_3, C_3[111]⟩` acts absolutely irreducibly on `H_hw=1`.
*If* a `C`-linear Hermitian operator `D` commutes with every retained
generator, *then* by Schur `D = m I_3` for real `m`, and the associated
scalar-commutant-class curvature reads

$$
Q(\delta, q_+) = 6(\delta^2 + q_+^2)/m^2.
$$

**Structural lemma (Z_3-circulant norm form).** On the scalar-commutant-class
reference,

$$
\det(m I + \delta T_\delta + q_+ T_q) = m^3 - 3m|w|^2 + 2\operatorname{Re}(w^3), \quad w = q_+ + i\delta.
$$

**What this is.** A retained-grade conditional structural lemma on the
commutant class. What it is **not**: a proof that the live DM-neutrino
source-sheet zero-source baseline satisfies the commutation premise. Explicit
tests in the associated runner confirm the live `H_base` (signature
`(2, 0, 1)`) does **not** commute with the retained three-generation algebra.
The Schur result therefore lives on the commutant class as a conditional
reference; it is not imported as theorem-native live-sheet curvature in the
P3 closure below.

**Gap status.** The earlier narration of "baseline promotion" has been
withdrawn pending a live-sheet derivation of the Schur commutation premise;
see Option B note in the *Still open* section.

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

### Source-branch selector (branch-choice / conditional admissibility rule, NOT retained-theorem)
→ [DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md)

The retained observable `W[J] = log|det(H_base + J)|` is well-defined on
the complement of the caustic `det(H_base + J) = 0`. Its natural domain on
the source-oriented sheet is the connected component containing `J = 0`,
equivalently the set of `J` preserving the retained signature

$$
\operatorname{signature}(H_{\text{base}} + J) = \operatorname{signature}(H_{\text{base}}) = (2, 0, 1).
$$

Signature is a Sylvester congruence-invariant of Hermitian forms. What we
use this for is a **branch-choice admissibility rule**: if the physical PMNS
closure is required to live on the baseline-connected non-caustic component,
then exactly one of the χ²=0 chamber basins is admissible.

**Important honest label.** The statement "the physical PMNS closure must
remain on the baseline-connected non-caustic component" is NOT a retained
theorem of the current framework. The function `W[J] = log|det(H_base + J)|`
is equally well-defined on any non-caustic component, so the selector rule is
an **imposed admissibility principle**, not a retained consequence. It is
algebraically cleaner than the previous norm-bound `‖J‖ ≤ ‖H_base‖` formulation,
but it remains a branch-choice rule rather than a derived selector.

Consequence for the chamber χ²=0 basins:

| Branch | `(m, δ, q_+)` | sin(δ_CP) | `signature(H)` | `det(H)` | baseline-connected? |
|---|---|---:|---|---:|---|
| Basin 1, σ=(2,1,0) | (0.657, 0.934, 0.715) | −0.987 | **(2, 0, 1)** | **+0.959** | **YES** |
| Basin 2, σ=(2,1,0) | (28, 21, 5) | +0.554 | (1, 0, 2) | −70377 | no (signature flipped) |
| σ=(2,0,1) cluster | (21, 13, 2) | −0.419 | (1, 0, 2) | −20295 | no (signature flipped) |

*Given* the imposed branch-choice rule, the competing basins are excluded by
signature flip across the caustic and Basin 1 is the unique baseline-connected
chamber closure. *Without* the branch-choice rule the basin-uniqueness claim
is not established.

Scale diagnostics remain recorded for transparency: `‖J‖_F / ‖H_base‖_F`
is 0.94 at Basin 1 vs 20.9 and 13.9 at the competing basins; the scale
bounds independently also pick Basin 1 (consistency check).

### θ_23 upper-octant chamber-closure prediction (SERIOUS 3)
→ [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md)

At PDG 2024 central `(s_12², s_13²) = (0.307, 0.0218)`, the H-diagonalization
admits a chamber solution iff `s_23² ≥ 0.5410`. Across the full NuFit 5.3
NO 3σ rectangle on `(s_12², s_13²)`, the threshold lies in `[0.5335, 0.5476]`
— entirely in the upper octant. Given the same imposed branch-choice rule
used by the chamber pin, the retained map therefore **predicts θ_23 in the
upper octant**. A >3σ lower-octant determination would unconditionally
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
3. On the `q_H = 0` branch — now **GAUGE (retained)** via
   [`HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17`](./HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md) —
   `Y_e = diag(y_1, y_2, y_3)`. (The three `q_H` branches give identical
   `|U_PMNS|`; `q_H = 0` is the canonical gauge representative, not an
   independent physical conditional.)
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

**Pinning statement (unique baseline-connected chamber solution under the
imposed branch-choice rule).** Requiring the map to reproduce PDG 2024
central observational values `(sin²θ_12, sin²θ_13, sin²θ_23) = (0.307,
0.0218, 0.545)`, *subject to the imposed admissibility rule that the closure
lies on the baseline-connected (signature-preserving) non-caustic component*,
has a unique chamber solution

$$
\boxed{(m_*,\ \delta_*,\ q_+^*) \;=\; (0.657061,\ 0.933806,\ 0.715042)}
$$

verified by multi-start Nelder-Mead + fsolve sharpening to machine
precision. The two competing in-chamber χ²=0 basins sit on the
`signature = (1, 0, 2)` component with `det(H_base + J) < 0`; they are
excluded *if and only if* the branch-choice rule is imposed. Without that
rule the three basins are all admissible.

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

## Claim boundary (non-negotiable, Option A honest labels)

### What is claimed (conditional / support)

1. **Retained map construction.** `(m, δ, q_+) → (θ_ij, δ_CP)` is a
   retained-grade map on the chamber constructed from retained inputs
   only (affine chart + chamber + three-generation observable theorem +
   Z_3 trichotomy gauge-redundancy `q_H = 0` [retained], plus the
   scalar-commutant-class Schur reference used as a structural lemma
   only).
2. **Conditional / support closure via P3 lane.** Retained map + PDG PMNS
   data + imposed branch-choice admissibility rule (baseline-connected
   non-caustic component, i.e. signature preservation) → unique chamber pin.
   This is a **conditional / support closure**, NOT a retained-grade sole-axiom
   closure and NOT a retained-grade selector closure. The imposed branch-choice
   admissibility principle is load-bearing and is not itself derived from
   retained framework structure.
3. **Falsifiable predictions (given the conditional selector).**
   `sin δ_CP = −0.9874` (CP phase) and `s_23² ≥ 0.5410` (θ_23 upper octant).
   Both testable at DUNE / JUNO / Hyper-Kamiokande.
4. **PMNS conditional support on the chamber** as `f(H)` under the listed
   conditions. The downstream flavor / cosmology / leptogenesis lanes remain
   open pending the full retained closure; the conditional support still gives
   a concrete chamber point for evaluation.

### What is NOT claimed

- **NOT flagship gate `CLOSED`.** The earlier `CLOSED` headline has been
  retracted. The honest label is `conditional / support`.
- **NOT Schur-derived live-sheet curvature.** The Schur lemma is used
  strictly as a commutant-class conditional reference; the live-sheet
  commutation premise is not derived.
- **NOT retained-theorem selector for basin uniqueness.** The source-branch
  selector is an imposed branch-choice / conditional admissibility rule.
- **Not sole-axiom closure.** The microscopic-polynomial impossibility
  theorem proves sole-axiom closure at that level is IMPOSSIBLE.
- **Not solar-gap `Δm²_21`** (different carrier than H).
- **Not absolute neutrino mass scale** (different carrier).
- **Not Majorana CP phases** (separate sector).
- **Not promotion of minimum-coupling / minimum-information to retained.**
  Those remain atlas-flagged post-axiom.
- **Conditional on `θ_23` upper octant.** Lower-octant determination at >3σ
  would falsify the closure (given its conditional selector).

## Downstream lanes unlocked

- **Leptogenesis.** The DM-leptogenesis PMNS-assisted transport witness can
  now be evaluated at the pinned chamber point with PMNS SUPPLIED BY THE
  THEOREM rather than floating 5 real parameters.
- **Flavor sector.** PMNS-triviality negative result on the two-Higgs /
  parity-mixing lane reorganizes into a specific relationship between the
  live `H` sheet and the flavor-currents family.
- **Observational predictions for DUNE / JUNO / Hyper-Kamiokande.** Two
  falsifiable conditional/support consequences on the near-term experimental
  horizon.

## Still open (honestly flagged)

1. Solar gap `Δm²_21` (different carrier).
2. Absolute neutrino mass scale (different carrier).
3. Majorana CP phases `α_21, α_31` (separate Majorana sector).
4. Sole-axiom closure of the selector principle: impossible at
   microscopic-polynomial level (proven); a nonlocal sole-axiom route
   remains hypothetically possible.
5. P1 / P2 alternative promotion lanes — identified by the observable-
   bank exhaustion theorem, complementary to the realized P3 closure.
6. **Live-sheet Schur commutation premise (Option B item 1 — OPEN).**
   Derive, on the actual source-oriented sheet, why the relevant
   zero-source baseline must commute with the retained three-generation
   algebra. Without this, the Schur result stays a commutant-class lemma
   and cannot be promoted to live-sheet curvature. Confidence: LOW —
   `H_live` has simple spectrum, so the maximal retained commutant is
   the 3-D polynomial algebra in `H_live`, which is not absolutely
   irreducible. A Schur-free route (e.g. `log|det|` expansion) is the
   more likely path; separate follow-up.
7. **Source-branch admissibility principle (Option B item 2 — OPEN).**
   Derive why the physical PMNS closure must lie on the baseline-connected
   `det ≠ 0` component rather than on another non-caustic component on
   which `W[J] = log|det(H_base + J)|` is also well-defined. Without
   this, the inertia-preserving selector stays a branch-choice rule
   rather than a retained selector. Candidate route:
   `BASIN_SIGNATURE_FROM_CONTINUITY_THEOREM_NOTE` — retained
   observable-continuity / Grassmann-additivity argument on `W[J]`.

### Closed on this landing (Option B item 3)

8. **Higgs `Z_3` charge `q_H = 0` conditional (Option B item 3 — CLOSED).**
   Previously listed as SM-canonical conditional; discharged by the
   Higgs `Z_3`-charge gauge-redundancy theorem
   ([`HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17`](./HIGGS_Z3_CHARGE_PMNS_GAUGE_REDUNDANCY_THEOREM_NOTE_2026-04-17.md)).
   The three `q_H ∈ {0, ±1}` branches give identical `Y_e Y_e†` on
   `L_L` axes, hence identical `U_e = I`, hence identical `|U_PMNS|`.
   `q_H` is gauge-redundant with PMNS; setting `q_H = 0` is a canonical
   choice with no physical content. Status: CONDITIONAL → GAUGE
   (retained). Residual conditionals on flagship closure: 3 → 2.

Closing items 6 AND 7 together is the Option B path back to a
retained-grade flagship-closure headline. Item 8 closed on this
landing reduces the residual conditional load from three to two.

## Review order for a skeptical reviewer

1. This note (the map).
2. [PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md](./PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md) — the closure.
3. [DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md) — what selects Basin 1.
4. [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md) — θ_23 upper-octant falsifiable prediction.
5. [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md) — why `U_e = I` in the axis basis.
6. [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md) — baseline promotion.
7. [DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md) — why closure had to go through observational promotion.

## Runner verification

All 15 runners pass on the current surface. Reproduce with:

```
PYTHONPATH=scripts python3 scripts/frontier_*_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_*_obstruction.py
PYTHONPATH=scripts python3 scripts/frontier_*_prediction.py
PYTHONPATH=scripts python3 scripts/frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py
PYTHONPATH=scripts python3 scripts/frontier_higgs_z3_charge_pmns_gauge_redundancy_theorem.py
```

Expected: total PASS = 502, FAIL = 0.

## Position on the flagship paper surface (honest Option-A labels)

The DM flagship gate is **NOT** declared CLOSED on the current branch tip.
Its honest current status is **conditional / support closure** via the
observational-promotion (P3) lane under the imposed branch-choice
admissibility rule. No ARXIV_DRAFT change is required for the flagship-row
language on this branch; the ARXIV draft on `origin/main` already lists
the DM gate as live, and that listing is consistent with the conditional /
support status on this branch. The conditional-support package is suitable
for inclusion as a support track describing the chamber pin and its
falsifiable `sin δ_CP` / upper-octant consequences, _given_ the stated
conditionality.

Suggested conditional / support wording (for future inclusion rather than
current arxiv-level promotion):

> The DM-neutrino source-oriented sheet admits a retained-grade map
> `(m, δ, q_+) → (θ_ij, δ_CP)` on the chamber. Under the imposed branch-
> choice admissibility rule that the physical closure remains on the
> baseline-connected (signature-preserving) non-caustic component, PDG 2024
> central PMNS angles pin a unique chamber point
> `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` and the map then
> forces `sin δ_CP = −0.9874` together with the falsifiable θ_23 upper-octant
> threshold `s_23² ≥ 0.5410`. This is a conditional-support closure; the
> branch-choice rule and the Schur scalar-baseline lemma are flagged as
> conditional / commutant-class ingredients rather than retained theorems.

## What this file must never say

- that the DM flagship gate is CLOSED (it is conditional / support closure
  on this branch tip).
- that the Schur result is a theorem-native promotion of live-sheet
  curvature (it is a commutant-class structural lemma only; the live-sheet
  commutation premise is not derived).
- that the source-branch selector is a retained theorem (it is an imposed
  branch-choice / conditional admissibility rule).
- that the δ_CP prediction is a fit parameter (it is a forced geometric
  consequence of the retained map, given the conditional selector).
- that PMNS is closed sole-axiom (the map is retained-grade; the pinning
  uses 3 observational PMNS values plus the conditional selector).
- that the DM flagship cascade is now fully sole-axiom.
- that a Frobenius / operator-norm scale bound is the primary basin
  selector (those are consistency diagnostics).
- that `W[J] = log|det(H_base + J)|` requires Taylor convergence at the
  Basin 1 amplitude (the log-det observable is defined on any non-caustic
  component by direct diagonalisation; the series-disk `ρ < 1` is an
  honest analytic-representation boundary, not a retained selector).
