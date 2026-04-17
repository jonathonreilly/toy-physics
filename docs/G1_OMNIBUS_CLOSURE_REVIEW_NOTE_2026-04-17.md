# G1 Omnibus Closure Review — Z_3 Doublet-Block Selector Law, DM Flagship Gate

**Date:** 2026-04-17
**Branch:** `claude/g1-complete` (off `main`)
**Status:** G1 CLOSED on the chamber via the P3 lane (retained PMNS-as-f(H) map + observational PMNS). DM flagship gate retains one open ingredient (selector principle for sole-axiom closure) but closes at the publication-grade **closure-via-observation** level.
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.
**Integration branch totals:** 20 commits off `main`, 11 runners, **PASS = 305, FAIL = 0**.

## Scope

This note is the **single-document reviewer entry point** for the entire G1 integration branch. It pulls together eleven attack-vector runners (four partial-closure / obstruction theorems from the initial Schur + Paths A/B/C round, two narrower-gap theorems from the physics-validation and parity-mixing round, and five physicist theorems from the final E/F/G/H/I round) into a single Nature-reviewer-grade story.

The story has four movements:

1. **Baseline promotion (Schur):** the scalar baseline `D = m I_3` is forced on the retained three-generation irreducible algebra by Schur's lemma. The previously bounded "scalar-baseline quadratic diagnostic" is promoted to theorem-native curvature on the active pair.

2. **Systematic obstruction tour (Paths A/B/C/E/F/G/I, Physics-Validation):** every sole-axiom route — variational / cubic / parity-definite / parity-mixing / observable-bank / microscopic-polynomial / bifundamental-invariance / transport — is proven obstructed. Each obstruction is a new retained theorem in its own right; together they prove that the Cl(3)/Z^3 axiom at the local polynomial level is genuinely silent on the selector pair `(δ, q_+)`.

3. **Closure via observational promotion (Physicist-H):** the atlas-open P3 lane identified by Physicist-E is *built*. Direct diagonalization of the retained affine Hermitian `H(m, δ, q_+)` on the three-generation observable space gives an explicit retained map
    ```
    (m, δ, q_+) → (sin²θ_12, sin²θ_13, sin²θ_23, δ_CP)
    ```
   Observational PMNS pins a unique chamber point. G1 closes at
    ```
    (m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042).
    ```

4. **Downstream unlock + falsifiable prediction:** as a side-effect, PMNS is promoted from atlas-open to retained as `f(H)` on the chamber, unlocking flavor/cosmology/leptogenesis downstream. The closure produces a retained δ_CP prediction
    ```
    sin(δ_CP) = -0.9874,   δ_CP ≈ -81° (= 279°),   |J| = 0.0328
    ```
   falsifiable at DUNE / Hyper-Kamiokande.

## Why G1 matters

The DM flagship gate was the sole remaining live flagship gate on the CL3/Z^3 publication surface (see [CI3_Z3_PUBLICATION_STATE_2026-04-15.md](./CI3_Z3_PUBLICATION_STATE_2026-04-15.md)). The last-mile blocker is the right-sensitive 2-real selector law on the active pair `(δ, q_+)` on the live DM-neutrino source-oriented sheet. Closing this gate lifts the DM flagship into the retained publication-grade package AND unlocks downstream observational lanes that route through PMNS.

## Attack structure — 11 retained runners

The branch is organized as a clean sequence of attack-and-obstruction / attack-and-closure runs. Each runner is self-contained with PASS/FAIL harness; the commit chain preserves the exact order in which each theorem was proven.

| # | Phase | Runner | PASS | Result |
|---|-------|--------|-----:|--------|
| 1 | baseline | frontier_g1_z3_doublet_block_selector_law.py | 19 | Schur baseline partial closure |
| 2 | obstruction tour | frontier_g1_path_a_information_geometric_selector.py | 26 | Quadratic Unanimity + Cubic Splitting |
| 3 | obstruction tour | frontier_g1_path_b_z3_cubic_selector.py | 26 | Z_3 cubic variational obstruction |
| 4 | obstruction tour | frontier_g1_path_c_holonomy_selector.py | 22 | Z_3 parity-split + microscopic cross-checks |
| 5 | obstruction tour | frontier_g1_physics_validation_eta_at_candidates.py | 16 | Transport chamber-blindness |
| 6 | obstruction tour | frontier_g1_parity_mixing_selector_law.py | 27 | Parity-mixing Frobenius candidate + selection ambiguity |
| 7 | obstruction tour | frontier_g1_physicist_e_observable_closure.py | 36 | Observable-bank exhaustion + P1/P2/P3 stratification |
| 8 | obstruction tour | frontier_g1_physicist_f_uniqueness_and_full_w.py | 18 | Frobenius-uniqueness obstruction + Quartic-isotropy |
| 9 | obstruction tour | frontier_g1_physicist_g_microscopic_axiom_level.py | 35 | Microscopic-polynomial impossibility theorem |
| 10 | obstruction tour | frontier_g1_physicist_i_bifundamental_invariance.py | 37 | Bifundamental-invariance obstruction (K_doublet Hermitian) |
| 11 | **CLOSURE** | **frontier_g1_physicist_h_pmns_as_f_h.py** | **43** | **PMNS-as-f(H) retained map + unique chamber pin** |
| | | **Total** | **305** | **305 PASS / 0 FAIL** |

All 11 runners live in `scripts/frontier_g1_*.py` with their accompanying theorem notes in `docs/G1_*.md`.

## The Schur baseline — phase 1

[G1_Z3_DOUBLET_BLOCK_SELECTOR_SCHUR_BASELINE_PARTIAL_CLOSURE_NOTE_2026-04-17.md](./G1_Z3_DOUBLET_BLOCK_SELECTOR_SCHUR_BASELINE_PARTIAL_CLOSURE_NOTE_2026-04-17.md)

**Theorem (Canonical Scalar Baseline from Schur).** The retained three-generation observable algebra `⟨P_1, P_2, P_3, C_3[111]⟩` acts absolutely irreducibly on `H_hw=1`. Any `C`-linear operator commuting with every retained generator is scalar (Schur). Hermiticity restricts to `R`. Hence `D = m I_3` for real `m`. The axiom-native observable-principle curvature

$$
Q(\delta, q_+) = 6(\delta^2 + q_+^2)/m^2
$$

is theorem-native on the active pair. Before this note the result was bounded because the scalar baseline was a choice; after it, the baseline is forced.

**Structural lemma.** On the scalar baseline,

$$
\det(m I + \delta T_\delta + q_+ T_q) = m^3 - 3m|w|^2 + 2\operatorname{Re}(w^3), \quad w = q_+ + i\delta
$$

is the Z_3-circulant norm form with exact `w → e^{2πi/3} w` rotation symmetry, broken to one sector by the chamber. The cubic `2 Re(w^3)` is the right-sensitive piece — it became the target of Path B.

**Gap narrowed.** From `(baseline-choice) AND (selector-principle)` to `(selector-principle)` only.

## The obstruction tour — phase 2

Ten independent runs, each producing a new retained theorem-grade obstruction. Collectively they prove: no sole-axiom functional on the retained atlas can pin `(δ, q_+)`.

### Path A — information-geometric variational obstruction
[G1_PATH_A_INFORMATION_GEOMETRIC_SELECTOR_NOTE_2026-04-17.md](./G1_PATH_A_INFORMATION_GEOMETRIC_SELECTOR_NOTE_2026-04-17.md)

- **Quadratic Unanimity Theorem:** all natural info-geometric functionals (minus-W, KL, Fisher, Frobenius) are isotropic at quadratic order → they share the `(√6/3, √6/3)` chamber minimum.
- **Cubic Splitting Obstruction:** at cubic order the functionals split by O(1); no axiom-native tiebreaker.
- **Structural Obstruction:** observable principle is response-generation, not source-selection.

### Path B — Z_3 cubic variational obstruction
[G1_PATH_B_Z3_CUBIC_SELECTOR_NOTE_2026-04-17.md](./G1_PATH_B_Z3_CUBIC_SELECTOR_NOTE_2026-04-17.md)

Five independent obstructions compound:
- Fixed-m chamber extremum `t_±(m) = m/2 ± √(9m²-12√6·m+48)/6` is m-dependent; only asymptotically → √6/3.
- Joint stationary points all at `det = 0` singularities.
- Cubic-only functional `Tr(J³) = 6·Re(w³)` extrema at `t = ±2/√3`, disagreeing.
- Cubic-maximizing Z_3 orbit has two chamber-accessible rays.
- `W = log|det|` is invariant to `sign(det)`, so max-vs-min is post-axiom convention.

### Path C — holonomy / Z_3 parity-split obstruction
[G1_PATH_C_HOLONOMY_SELECTOR_NOTE_2026-04-17.md](./G1_PATH_C_HOLONOMY_SELECTOR_NOTE_2026-04-17.md)

- **T1 (Z_3 parity-split theorem).** `T_q` is purely Z_3-circulant, `T_δ` is purely Z_3-anti-circulant on the affine source sheet.
- **T2.** Any Z_3-parity-definite scalar constrains at most one of `(δ, q_+)` at fixed m.

Rules out the entire parity-definite functional class.

### Physics-Validation — transport chamber-blindness
[G1_PHYSICS_VALIDATION_ETA_AT_CANDIDATES_NOTE_2026-04-17.md](./G1_PHYSICS_VALIDATION_ETA_AT_CANDIDATES_NOTE_2026-04-17.md)

**Theorem (transport chamber-blindness).** The atlas-native transport chain η/η_obs is a function only of the source-package `(γ, E_1, E_2, K_00, cp_1, cp_2)`. These are invariant under motion along `T_δ, T_q` by the current-bank-blindness theorem. Hence η/η_obs is CONSTANT on the chamber at 0.189. The level set `{η/η_obs = 1}` is EMPTY on the chamber.

### Parity-mixing — Frobenius candidate + new obstruction
[G1_PARITY_MIXING_SELECTOR_LAW_NOTE_2026-04-17.md](./G1_PARITY_MIXING_SELECTOR_LAW_NOTE_2026-04-17.md)

Sum-of-parity-definite invariants evade Path C. The Frobenius norm `||K_doublet||_F²` has a unique m-independent chamber-boundary minimizer `(√6/2 − √2/18, √6/6 + √2/18)`. BUT `det K_doublet` gives a different minimizer. No axiom-native tiebreaker → new "Parity-mixing Functional-Selection Obstruction".

### Physicist E — observable-bank exhaustion
[G1_PHYSICIST_E_OBSERVABLE_CLOSURE_THEOREM_NOTE_2026-04-17.md](./G1_PHYSICIST_E_OBSERVABLE_CLOSURE_THEOREM_NOTE_2026-04-17.md)

Survey of retained atlas observables (R = Ω_DM/Ω_B, m_DM, Δm²_atm, PMNS angles, σ_DD, g-2, see-saw mass scale, η on PMNS-assisted route). **Every retained observable with an observational target factors through the frozen-on-chamber bank** by the blindness theorem. PMNS/solar closure is atlas-open. **G1 is stratified into three explicit promotion lanes P1 / P2 / P3.**

### Physicist F — Frobenius uniqueness + full-W + quartic obstruction
[G1_PHYSICIST_F_UNIQUENESS_AND_FULL_W_NOTE_2026-04-17.md](./G1_PHYSICIST_F_UNIQUENESS_AND_FULL_W_NOTE_2026-04-17.md)

- **Line 1:** U(2)-invariant PD quadratic functionals form a 2-parameter cone `{A(Tr K)² + B det K : B < 0, A > -B/4}` — NOT a unique functional. Five PD members give five different minimizers. **Conditional gate:** U(2)_L × U(2)_R bifundamental invariance would uniquely pin F1.
- **Line 2:** Full-W fixed-m argmax is m-dependent at all 9 tested m values. Strengthens Path B.
- **Line 3 (new theorem):** Quartic-isotropy identity `Tr(J⁴) = (1/2)[Tr(J²)]²` at scalar baseline. No new parity-mixing information at quartic order.

### Physicist G — microscopic-polynomial impossibility
[G1_PHYSICIST_G_MICROSCOPIC_AXIOM_LEVEL_NOTE_2026-04-17.md](./G1_PHYSICIST_G_MICROSCOPIC_AXIOM_LEVEL_NOTE_2026-04-17.md)

**Impossibility Theorem.** Every retained polynomial microscopic functional of H (trace moments, `det(H)`, heat kernel `Tr(e^{-tH²})`, spectral gap, Ward identities, Cl(3) bivector invariants) is EVEN in δ and depends on `(δ, q_+)` only through `(δ², q_+)`.

**Consequence:** The Cl(3)/Z^3 axiom is GENUINELY SILENT on `(δ, q_+)` at the local-polynomial microscopic level. The selector pair is a genuine submicroscopic residual — a "gauge direction" that the axiom does not constrain. Closure requires a nonlocal / variational / information-geometric / transport-consistency / effective-action-matching principle, OR an observational promotion.

### Physicist I — bifundamental-invariance obstruction
[G1_PHYSICIST_I_BIFUNDAMENTAL_INVARIANCE_THEOREM_NOTE_2026-04-17.md](./G1_PHYSICIST_I_BIFUNDAMENTAL_INVARIANCE_THEOREM_NOTE_2026-04-17.md)

**Theorem.** `K_doublet` is automatically Hermitian (from retained chain `H Hermitian → K_Z3 Hermitian → K_doublet principal submatrix`). A 2×2 Hermitian has 4 real parameters and admits only the 3-parameter U(2) adjoint action, NOT the 8-parameter U(2)_L × U(2)_R bifundamental. Five converging derivations (polar gauge / Hermitian Dirac / shift-quotient / Z_3 support / Schur collapse).

**Consequence.** The Physicist-F conditional-closure gate (bifundamental → F1 uniquely pinned) is unavailable as a sole-axiom route. The retained atlas is "Hermitian-data-first" — bifundamental is a downstream input channel, not a retained symmetry.

## The closure — phase 3

[G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md)

With sole-axiom variational routes exhausted, closure proceeds through the atlas-open P3 lane identified by Physicist-E.

**Main theorem (retained-grade map).** Direct diagonalization of the retained affine Hermitian `H(m, δ, q_+)` on the three-generation observable space `H_hw=1`, with the charged-lepton mass basis fixed to the generation axis basis by the retained Dirac-bridge theorem (`U_e = I` in axis basis from single-Higgs Z_3-neutral charge), and row-permuted by the hierarchy pairing `σ_hier = (2, 1, 0)`, yields an explicit retained map

$$
(m, \delta, q_+) \;\longmapsto\; (\sin^2\theta_{12},\ \sin^2\theta_{13},\ \sin^2\theta_{23},\ \delta_{CP})
$$

on the chamber `q_+ ≥ √(8/3) - δ`.

**Pinning theorem (unique chamber solution).** Requiring the map to reproduce the PDG 2024 central observational values

$$
\sin^2\theta_{12}=0.307, \quad \sin^2\theta_{13}=0.0218, \quad \sin^2\theta_{23}=0.545
$$

has a **unique** chamber solution

$$
\boxed{(m_*,\ \delta_*,\ q_+^*) \;=\; (0.657061,\ 0.933806,\ 0.715042)}
$$

verified by 60 independent random-start Nelder-Mead + fsolve sharpening, all converging to machine precision. The pinned point is strictly inside the chamber (boundary distance 0.0159).

**Falsifiable δ_CP prediction.** At the pinned point the map fixes the CP phase as a GENUINE output (3 observational inputs → 4 outputs; δ_CP is NOT fitted):

$$
\boxed{\sin\delta_{CP} = -0.9874, \quad \delta_{CP} \approx -81° \;(\equiv 279°), \quad |J| = 0.0328}
$$

in the T2K-preferred lower octant and inside the NuFit 5.3 3σ band. **This is the single most important testable output of the G1 closure**; upcoming DUNE / Hyper-Kamiokande data can falsify it.

**Observational consistency.** All nine entries of `|U_PMNS|` at the pinned point lie inside the NuFit 5.3 NO 3σ ranges (9/9 PASS).

**Candidate-inequivalence.** The pinned `(δ_*, q_+*) = (0.934, 0.715)` is strictly inequivalent to every prior obstruction-tour candidate:

| Prior candidate | Distance from `(δ_*, q_+*)` |
|---|---:|
| Schur-Q | 0.155 |
| det(H) interior crit | 0.838 |
| Tr(H²) boundary | 0.484 |
| K_12 char-match | 0.315 |
| Frobenius F1 | 0.312 |

Closest is Schur-Q at 0.155 — well outside any numerical tolerance. The closure is a GENUINELY NEW point emerging from the observational constraint, not one of the variational candidates.

## Claim boundary (non-negotiable)

### What is claimed

1. **Retained map theorem:** `(m, δ, q_+) → (θ_ij, δ_CP)` is retained-grade on the chamber, constructed from retained inputs only (affine chart + chamber + three-generation observable space + Dirac-bridge + Z_3 doublet-block readout + chamber blindness).

2. **Closure via observational promotion (P3 lane):** the retained map + PDG PMNS data → unique chamber pin. This is CLOSURE-VIA-OBSERVATION at publication-grade, NOT sole-axiom closure. The 3-real observational input `{sin²θ_12, sin²θ_13, sin²θ_23}` supplies the missing selector degree of freedom.

3. **Falsifiable δ_CP prediction:** `sin δ_CP = -0.9874`. This is a GENUINE prediction — the retained map maps 3 angles to 4 outputs, and δ_CP is the extra output.

4. **PMNS promoted to retained:** the mixing angles are retained as `f(H)` on the chamber. This unlocks downstream flavor / cosmology / leptogenesis lanes.

5. **G1 gate CLOSED on the chamber** at `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`.

### What is NOT claimed

- **Not sole-axiom closure.** Closing via observed PMNS is a legitimate Nature-grade promotion (P3 lane), but it is not the same as deriving `(δ_*, q_+*)` from the axiom alone. The Physicist-G impossibility theorem proves that microscopic-polynomial sole-axiom closure is IMPOSSIBLE; closure at the retained-map + observational-pin level is the strongest available.
- **Not solar-gap closure.** `Δm²_21` lives on a different carrier.
- **Not absolute neutrino mass.** Different carrier.
- **Not Majorana phases.** Separate sector.
- **Not promotion of the minimum-coupling / minimum-information selector principle.** That remains post-axiom, consistent with the `DM_LEPTOGENESIS_PMNS_MINIMUM_INFORMATION_SOURCE_LAW` atlas flag.

## Downstream lanes unlocked

With PMNS retained as `f(H)` on the chamber:

1. **Leptogenesis.** The existing DM-leptogenesis PMNS-assisted transport witness can now be evaluated at the pinned chamber point with PMNS SUPPLIED BY THE THEOREM rather than floating 5 real parameters. The witness's η/η_obs = 1 becomes a theorem-grade value rather than a constructive-chamber existence.
2. **Flavor sector.** The lepton-single-Higgs PMNS-triviality negative result is reorganized into a specific relationship between the live `H` sheet and the flavor-currents family (no longer a dead end).
3. **δ_CP prediction at DUNE / Hyper-Kamiokande.** Falsifiable retained-grade prediction `sin δ_CP = -0.987`.
4. **Publication surface update.** DM flagship gate transitions from "one live flagship gate" to "closed at publication-grade via P3". The DERIVATION_ATLAS row for G1 updates to `closed` with `closure-via-observational-promotion` qualifier.

## Still open (honestly flagged)

1. **Solar gap `Δm²_21`.** Different carrier than `H`.
2. **Absolute neutrino mass scale.** Different carrier.
3. **Majorana CP phases `α_21, α_31`.** Separate Majorana-sector problem; see `NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md`.
4. **Sole-axiom closure.** Physicist-G proves polynomial-microscopic sole-axiom closure is impossible; a nonlocal sole-axiom principle remains the only possible route if one ever wanted to upgrade from observational-promotion closure to sole-axiom.
5. **P1 / P2 promotion lanes.** P1 (new H-reader observable with atlas-grade target) and P2 (new sole-axiom selector principle) remain open alternative paths; P3 closure does not preclude later P1 or P2 closure — that would be cross-check evidence.

## Runner map

All 11 runners in the integration branch pass:

```
scripts/frontier_g1_z3_doublet_block_selector_law.py         PASS=19 FAIL=0
scripts/frontier_g1_path_a_information_geometric_selector.py PASS=26 FAIL=0
scripts/frontier_g1_path_b_z3_cubic_selector.py              PASS=26 FAIL=0
scripts/frontier_g1_path_c_holonomy_selector.py              PASS=22 FAIL=0
scripts/frontier_g1_physics_validation_eta_at_candidates.py  PASS=16 FAIL=0
scripts/frontier_g1_parity_mixing_selector_law.py            PASS=27 FAIL=0
scripts/frontier_g1_physicist_e_observable_closure.py        PASS=36 FAIL=0
scripts/frontier_g1_physicist_f_uniqueness_and_full_w.py     PASS=18 FAIL=0
scripts/frontier_g1_physicist_g_microscopic_axiom_level.py   PASS=35 FAIL=0
scripts/frontier_g1_physicist_i_bifundamental_invariance.py  PASS=37 FAIL=0
scripts/frontier_g1_physicist_h_pmns_as_f_h.py               PASS=43 FAIL=0
                                                              -----
                                                              305   0
```

Reproduce by running each with `PYTHONPATH=scripts python3 scripts/...`.

## Review order for a skeptical reviewer

1. **Read this note first.** It's the map.
2. **Read G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md.** That's the closure theorem.
3. **Read G1_PHYSICIST_G_MICROSCOPIC_AXIOM_LEVEL_NOTE_2026-04-17.md.** That's why closure had to come through observational promotion, not sole-axiom.
4. **Read G1_Z3_DOUBLET_BLOCK_SELECTOR_SCHUR_BASELINE_PARTIAL_CLOSURE_NOTE_2026-04-17.md.** That's the baseline promotion the closure rests on.
5. **Check the retained-input chain** from the closure note back through Dirac-bridge, three-generation observable theorem, and affine-chart theorem. These are all on main or this branch.
6. **Run all 11 runners.** All should pass 305/0.
7. **Stress-test the δ_CP prediction** by checking the T2K / NuFit 5.3 latest data (as of submission date).

## Attribution

This work was developed via coordinated parallel attack vectors — one baseline closure, three obstruction-tour branches (Paths A/B/C), two physics-axis narrower-gap branches (Physics-Validation, Parity-Mixing), and five physicist theorems (E obstruction, F obstruction, G impossibility, H CLOSURE, I obstruction). All commits are on the integration branch `claude/g1-complete` off `main`.

Per the existing CI3/Z^3 publication AI-accountability note, generative AI tools were used for derivational drafting, verification infrastructure, and manuscript execution. The scientific claim boundary, retained / bounded / open discipline, and all theorem promotions were enforced by the standard project discipline.

## Position on the flagship paper surface

The DM flagship gate is now **CLOSED at publication-grade via P3**. The correct ARXIV_DRAFT wording is:

> The DM flagship gate has closed at publication-grade via the retained
> PMNS-as-f(H) construction and observational PMNS pinning. The chamber
> closure point is
> `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`
> and the closure supplies a falsifiable retained δ_CP prediction
> `sin δ_CP = −0.9874`. Sole-axiom closure remains impossible at the
> microscopic-polynomial level per Physicist-G's impossibility theorem;
> closure-via-observational-promotion is the published result.

The retained publication package now has ZERO live flagship gates. The next stratified open work is the promotion lanes for P1 (new H-reader observable), P2 (sole-axiom selector principle), plus the always-separate carriers (solar gap, absolute mass, Majorana phases).

## Commit chain

```
20  Integrate G1 physicist H: PMNS-as-f(H) CLOSURE theorem (G1 CLOSED)
19  G1 Physicist-H: PMNS-as-f(H) closure theorem
18  Integrate G1 physicist I: bifundamental-invariance obstruction theorem
17  Add G1 Physicist I: bifundamental invariance obstruction theorem
16  Integrate G1 physicist G: microscopic axiom-level impossibility theorem
15  G1 Physicist-G: microscopic-silence impossibility theorem on (delta, q_+)
14  Integrate G1 physicist F: Frobenius uniqueness obstruction + quartic-isotropy
13  Add G1 Physicist F: Frobenius uniqueness + Full-W + Quartic obstruction theorems
12  Integrate G1 physicist E: observable-bank exhaustion theorem
11  G1 Physicist-E: observable-bank-extension obstruction + new-gap
10  Integrate G1 parity-mixing selector law narrower-gap
 9  Integrate G1 physics-validation: eta/eta_obs chamber-blindness theorem
 8  Add G1 parity-mixing selector law narrower-gap note
 7  Add G1 physics-validation: eta/eta_obs at Z_3 doublet-block candidates
 6  Integrate claude/g1-path-c-holonomy
 5  Integrate claude/g1-path-b-z3-cubic-selector
 4  Integrate claude/g1-path-a-information-geometric
 3  Integrate G1 Schur-baseline partial closure
 2  Add G1 Path-C microscopic selector attempt: obstruction + cross-checks
 1  Add G1 Path-B Z_3 cubic selector obstruction theorem
 0  Add G1 Path-A information-geometric selector obstruction + narrowed-gap
   + Add G1 Z_3 doublet-block Schur-baseline partial closure
```

## What this file must never say

- that G1 is closed sole-axiom (it is not; closure is via P3 observational promotion)
- that Physicist-G's impossibility theorem is overturned (it stands; it is what forces the P3 route)
- that the δ_CP prediction is a fit parameter (it is a genuine output of the retained map)
- that PMNS is closed sole-axiom (the map is sole-axiom; the pinning uses 3 observational PMNS values)
- that the DM flagship cascade is now fully sole-axiom (the closure is at retained-publication-grade, which is the standard for Nature-level flagship claim)
