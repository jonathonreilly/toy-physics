# Scalar-Selector Cycle 1 — Remaining Open Imports

**Date:** 2026-04-20
**Scope:** Each still-open import on the four Tier-1 scalar-selector lanes
(Koide θ, Koide κ, DM A-BCC, Quark a_u) plus the supporting selected-line and
Berry lanes, with a specific statement of what derivation would close it from
Cl(3)/Z³ framework ingredients alone. Items listed here are
**retained-observational or structural-postulate inputs** that currently
prevent the corresponding lane from being marked retained-derivation on main.

## §0 Summary table

| # | Import | Lane | Current status | What closes it |
|---|---|---|---|---|
| I1 | Koide relation `Q = 2/3` | κ, θ | retained observational; the same-branch linking theorem now shows the natural general form is `Q = 2/d` by equal-sector norm, not `(d−1)/d` | a Cl(3)/Z³-native forcing of the cone condition `a_0² = 2|z|²` from retained representation-theory or from a retained scalar-potential minimization that lands on the cone |
| I2 / P | Brannen phase `δ = 2/9` on the physical base | θ | the new Brannen-phase reduction theorem reduces I2 to `I1` via `δ = Q/d`, but the cycle-2 linking theorem + direct no-go sharpen the live load-bearing step as one named radian-bridge postulate `P`: the structural count `2/d²` must be identified with the physical Berry holonomy in radians on the selected-line CP¹ base | either derive `P` directly by a retained Wilson/lattice identity on the physical base, or derive a physical-base theorem that makes the Brannen reduction `δ = Q/d` canonical; then closing `I1` closes `I2` automatically |
| I5 | PMNS observational pins (NuFit 3σ ranges, T2K `sin δ_CP < 0`) | A-BCC (sigma-chain) | retained observational inputs | framework-native derivation of NuFit angles (open on main as the broader charged-lepton flagship gate) and/or of the sign of `sin δ_CP` from Cl(3) CP structure |
| I10 | H_* witness ratio `w/v ≈ 4.101` | m_* (selected-line point) | retained observational; selected-line provenance is now closed, so only the scalar-phase pin remains | deriving `m_*` as a corollary of `δ = 2/9` via the exact scalar-phase bridge (already established). If I2 / `P` closes, I10 closes automatically |
| I12 | σ_hier permutation `(2,1,0)` | A-BCC (sigma-chain) | retained from `SIGMA_HIER_UNIQUENESS_THEOREM_NOTE` (given T2K input on `sin δ_CP`) | framework-native CP structure forcing `sin δ_CP < 0` at the physical chamber point |

## §0a Closed in cycle 2

- **I3 closed.** `H_sel(m) = H(m, √6/3, √6/3)` is now traced exactly to the
  retained-on-`main` parity-compatible observable-selector chain in
  `docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md`.
- **I4 closed.** The chamber bound `q_+ + δ ≥ √(8/3)` now has a one-step
  reviewer-grade inline derivation in
  `docs/DM_ABCC_CHAMBER_BOUND_DERIVATION_NOTE_2026-04-20.md`.
- **I6 closed by formal demotion.** The SO(2)-quotient is **not**
  retained-derived from the observable principle; MRU is now supplementary
  only, and the primary κ route is the spectrum/operator bridge plus the
  block-total Frobenius measure. See
  `docs/KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`.
- **I11 closed.** Basin enumeration completeness is now certified in
  `docs/DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md`.
  The corrected full χ²=0 chart is five basins
  `{Basin 1, Basin N, Basin P, Basin 2, Basin X}`; the active-chamber chart is
  `{Basin 1, Basin 2, Basin X}`.
- **I7, I8 closed by review-surface provenance cleanup.** The quark lane now
  states its retained bimodule and atom provenance inline in the reviewer
  package and headline theorem surfaces: `docs/SCALAR_SELECTOR_REVIEWER_PACKAGE_2026-04-20.md`,
  `docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`, and
  `docs/SCALAR_SELECTOR_PROOF_CHAINS_2026-04-19.md`.

## §1 Priority ordering for closure

Closing any single item in the following ordered list produces the largest
reduction in the retained-observational footprint of the scalar-selector
cycle.

### Priority 1: I1 (Koide `Q = 2/3`)

Closing `Q = 2/3` from Cl(3)/Z³ would immediately upgrade the Koide κ and θ
lanes from "retained-observational-conditional" to "retained-derivation" on
main. It is the single highest-leverage open item in the cycle.

**What is already ruled out (main):** six structural no-go theorems cover
Z₃-invariance alone, sectoral universality, color-sector correction,
anomaly-forced cross-species, SU(2) gauge exchange mixing, and
observable-principle character symmetry. None of these mechanisms forces the
cone point.

**What has not been ruled out:** a forcing from a retained Z³ scalar
potential that lands its physical minimum on the cone. The retained Z³ scalar
potential `V(m) = const + (c1+c2/2)m + (3/2)m² + (1/6)m³` has a stationary
point `m_V ≈ −0.433` which is **not** the Koide cone point
`m_* ≈ −1.161` (documented on main as an honest gap). A successful
derivation requires adding the first-principles retained ingredient that
moves the effective minimum from `m_V` to `m_*`.

**New same-branch reduction (2026-04-20):** the previously vague `4 x 4`
singlet/baryon route is now reduced exactly to a `C_3`-singlet Schur law
`K_eff(m) = K_sel(m) - lambda(m) J` on the trivial Fourier projector
`J = 3 P_+`. So the open object is not a generic non-uniform `4 x 4`
correction anymore; it is one scalar function `lambda(m)`. In the
fixed-coupling subclass (`lambda` constant), making the branch-local physical
selected point `m_*` stationary forces one unique positive value
`lambda_* ~= 0.5456253117`. See
`docs/KOIDE_C3_SINGLET_EXTENSION_REDUCTION_THEOREM_NOTE_2026-04-20.md`.

**Later same-branch sharpening (2026-04-20):** the fixed-coupling subclass is
now understood more sharply. Solving the stationarity equation for constant
`lambda` gives an explicit family `lambda_±(m)` on the physical first branch,
so constant singlet dressing does **not** pick out `m_*` by itself. It
reparameterizes a whole interval of first-branch stationary points
`m in [m_pos, m_disc]`, with two positive `lambda` values on the upper part of
that interval. So the remaining open object on this route is not "find some
positive constant `lambda`"; it is still the microscopic law fixing `lambda`
itself, equivalently fixing `m`. See
`docs/KOIDE_C3_CONSTANT_SINGLET_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md`.

**Further same-branch sharpening (2026-04-20):** the canonical selected-slice
`2 x 2` `Z_3` doublet block also does **not** contain a hidden intrinsic
spectral selector. Its completed spectral data are exact, but after freezing
the bank they collapse to the sign-blind coordinate
`x^2 = (m - 4 sqrt(2)/9)^2`: `Tr(K2)` is constant, while `det(K2)`,
`Tr(K2^2)`, and the eigenvalue-gap square are all affine in `x^2`. On the
physical first branch `x < 0` everywhere, so those raw spectral scalars are
strictly monotone and the natural low-complexity spectral-law classes
(single-scalar, affine, coefficient-free monomial, normalized-by-trace) only
reparameterize the branch. They do not select the physical point. See
`docs/KOIDE_SELECTED_SLICE_SPECTRAL_COMPLETION_AND_MINIMAL_LOCAL_SPECTRAL_LAW_NO_GO_NOTE_2026-04-20.md`.

**Assumption-escape closeout (2026-04-20):** two nearby alternative readings
are now also ruled out as genuine closures. First, if one drops the current
slot readout and instead imposes `Q = 2/3` on the eigenvalues of
`exp(beta H_sel(m))`, the route does not select a point: for each fixed
selected-line spectrum the eigenvalue purity is strictly increasing in `beta`,
so `Q_eig = 2/3` cuts a unique `beta_q23(m)` and yields a one-real monotone
surface `beta = beta_q23(m)`. It still needs an independent beta-law. Second,
the striking scale near-miss `u*v*w = 1` is not an independent forcing law at
all: the `u` used there is the Koide-completed small root `u_small(v,w)`, so
that condition already lives on the imposed cone `Q = 2/3` and only
reparameterizes the existing selected-line gap. It near-hits `m_*` but does
not equal it. See
`docs/KOIDE_EIGENVALUE_Q23_SURFACE_THEOREM_NOTE_2026-04-20.md` and
`docs/KOIDE_SCALE_SELECTOR_REPARAMETERIZATION_THEOREM_NOTE_2026-04-20.md`.

**Weighted character-source closeout (2026-04-20):** the natural weighted
extension of the old `Z_3` character-source cross-check is now also closed.
For arbitrary central left/right class-function weights on the canonical
sources `s_i = e_{q_L(i)} ⊗ e_{q_R(i)}`, the weighted kernel is always exactly
diagonal: `diag(mu_0 nu_0, mu_1 nu_2, mu_2 nu_1)`. So a unique top eigenvalue
can only select a basis axis, and every basis axis has `Q = 1`, not `2/3`;
while a degenerate top leaves the ray unfixed. So observable-principle source
work must derive genuine off-axis circulant Fourier content of `D^(-1)`, not
just reweight the canonical character sources. See
`docs/KOIDE_WEIGHTED_CHARACTER_SOURCE_AXIS_THEOREM_NOTE_2026-04-20.md`.

**Candidate closing routes (each needs its own derivation):**

1. **H_* witness ratio from a retained lattice calculation.** The H_* witness
   `kappa_* ≈ −0.608` currently pins `m_*` by observational fit. If a
   retained lattice propagator or transport integral computes `kappa_*` from
   Cl(3)/Z³ ingredients alone, the cone point is forced.
2. **Retained `C_3`-singlet Schur law on the `4 x 4` (`hw=1 + singlet/baryon`)
   block.** The new reduction theorem shows every equivariant `4 x 4`
   extension collapses to `K_eff(m) = K_sel(m) - lambda(m) J`. So this route
   is now exactly: derive the scalar singlet-Schur law `lambda(m)` from the
   microscopic lattice action.
3. **Missing-axis Higgs-dressed resolvent root law.** On the natural baseline
   `W_4(0) = diag(0, H_*)`, the strongest surviving transport avenue has now
   been reduced to isolated scalar roots of `Q(abs eig Sigma_lambda(0)) = 2/3`,
   with one unique small positive root
   `lambda_* = 0.015808703285395...` near chamber slack and cosine
   `0.996266...` to the PDG `sqrt(m)` direction. So this route is now exactly:
   derive the transport-side lambda-law on the missing-axis resolvent family.
   See `docs/KOIDE_HIGGS_DRESSED_RESOLVENT_ROOT_THEOREM_NOTE_2026-04-20.md`.
4. **One-clock semigroup / Γ-orbit positive witness route.** Already delivers
   cos-similarity > `1 − 10⁻⁹` with the PDG `√m` vector at the cone point
   `H_*`. Currently conditional on observational chamber pins
   `(M_STAR, DELTA_STAR, Q_PLUS_STAR)`. If those three pins can be derived
   from retained framework, `Q = 2/3` follows.

**Demoted candidate (2026-04-20):** the old transport-gap observation
`1/eta_ratio ≈ 4pi/sqrt(6)` is no longer a live selector route. Even an exact
identity there would still compare two branch-level constants and would not
introduce any selected-line `m` dependence. See
`docs/KOIDE_TRANSPORT_GAP_CONSTANT_NO_GO_NOTE_2026-04-20.md`.

**Required retained ingredients for any of the above:** explicit lattice
propagator or transport-integral definition on the retained Cl(3)/Z³ carrier;
currently on main as partial support.

### Priority 2: I2 / P (radian bridge for `δ = 2/9`)

The branch now carries two complementary results:

1. **Brannen-phase reduction theorem.**
   `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`
   shows that the candidate route `δ = Q/d` reduces I2 to I1.
2. **Cycle-2 linking theorem + direct no-go.**
   `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` and
   `docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md` sharpen the
   remaining load-bearing step as one named residual statement:

```text
Q_structural  = 2/d
δ_structural  = 2/d²
δ / Q         = 1/d
P:  2/d² is the physical Berry holonomy in radians on the selected-line CP¹ base.
```

So the open content is not the arithmetic `2/9`; it is the physical-base
identification that turns the structural ratio `2/d²` into the observed
radian phase. The direct no-go note proves that the four obvious retained
closure candidates fail: selected-line PB per element, full-orbit Bargmann
phase, bare Plancherel-weight identification, and the selected-slice midpoint
rule do not produce `2/d²` in radians on the physical base.

**Minimal additional inputs now known to suffice (any one closes `P`):**

1. **Lattice propagator radian quantum.** A retained identity of the form
   `G_{C_3}(1) = exp(i · 2/d²) G_0`.
2. **Wilson holonomy on the 4×4 `hw=1+baryon` block.** A retained non-uniform
   per-element phase `2/d²`.
3. **Z₃-orbit Wilson-line `d²`-power quantization.**
   `W_{Z_3}^{d²} = exp(2i) 1`.

See `docs/KOIDE_BRANNEN_PHASE_REDUCTION_THEOREM_NOTE_2026-04-20.md`,
`docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md`, and
`docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`.

### Priority 3: I5, I12 (PMNS observational pins and σ_hier permutation)

Scope is larger than the scalar-selector cycle; these are part of the broader
charged-lepton flagship gate. Closing them requires framework-native PMNS
derivation, which is an open program on multiple branches
(lepton-mass-tower, lepton-pmns-integration, dm-leptons-review). Not scoped
to tomorrow's submission.

### Priority 4: I10 (selected-line physical point)

Now the only open content behind `m_*` is the scalar-phase pin itself. If
`I2 / P` closes, `I10` closes immediately by the exact selected-line
scalar-phase bridge.

## §2 What a Nature reviewer will still see after submission

With the above items retained-observational, the honest Nature-grade
statement for this cycle is:

> Four Tier-1 scalar-selector gates of the Standard Model — the Koide
> charged-lepton cone normalization (κ = 2, equivalently the operator-side
> Koide relation), the Koide Brannen–Zenczykowski phase offset (δ = 2/9), the
> dark-matter A-BCC basin-sheet choice, and the up-sector quark reduced
> amplitude (a_u) — each reduce to retained Cl(3)/Z³ framework ingredients,
> with the only still-open named retained inputs now being the Koide cone
> relation Q = 2/3, the residual radian-bridge P behind the physical Brannen
> phase value δ = 2/9, and the PMNS NuFit + T2K observational pins. No new
> axioms are added this cycle. The framework
> contributes (i) a canonical Pancharatnam–Berry geometric identification of δ
> on the physical selected line together with a precise no-go for deriving its
> value from the current retained base alone, (ii) an exact Fourier-bridge
> algebraic reduction of operator-side κ = 2 to spectrum-side Q = 2/3,
> (iii) a Sylvester-inertia reduction of A-BCC, closed via a multi-observable
> sigma-chain that combines retained Cl(3)/Z³ theorems with named
> observational inputs, and (iv) a linear-algebra derivation of the up-sector
> quark closure on the retained `1⊕5` bimodule and CKM-atlas atom package,
> whose provenance is now surfaced inline on the review branch. Each retained
> observational input or structural postulate still blocking native closure is
> listed in the Remaining-Open-Imports register along with the derivation that
> would close it.

Closing any priority-1 or priority-2 item above would upgrade the
corresponding lane from retained-conditional to retained-derivation and
eliminate the named retained input. The cycle-2 housekeeping imports I3, I4,
I6, and I11 are now closed; the remaining irreducible frontier is the Koide
`Q`/radian-bridge pair and the PMNS observational pins.

## §3 Reproduction of current retained-conditional state

All runners currently pass on canonical (branch
`review/scalar-selector-cycle1-theorems`). For each of the four Tier-1 lanes
the primary closure runner and its verification counts are:

| Lane | Primary runner | PASS | Notes |
|---|---|---|---|
| Koide κ (spectrum/operator bridge) | `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` | 9 | exact sympy identity `a_0² − 2|z|² = 3(a² − 2|b|²)` |
| Koide κ (block-total Frobenius corroboration) | `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` | 16 | independent functional reaching same `κ = 2` |
| Koide θ (Berry identification on selected line) | `frontier_koide_berry_phase_theorem.py` | 24 | ambient-S² calculation § + selected-line CP¹ § + natural-selector no-go § |
| Koide θ (scalar-phase bridge) | `frontier_koide_selected_line_cyclic_response_bridge.py` | 20 | `κ_sel(δ)` exact identity |
| Koide θ (Brannen reduction route) | `frontier_koide_brannen_phase_reduction_theorem.py` | 16 | reduces `δ` to `Q/d`; physical-base load-bearing step sharpened as `P` |
| DM A-BCC (chamber ∩ DPLE) | `frontier_dm_abcc_chamber_dple_closure.py` | 39 | chamber bound + discriminant sign |
| DM A-BCC (Sylvester signature-forcing) | `frontier_dm_abcc_signature_forcing_theorem.py` | 54 | path-independent via IVT + det sign |
| DM A-BCC (PMNS Non-Singularity conditional) | `frontier_dm_abcc_pmns_nonsingularity_theorem.py` | 38 | conditional closure |
| DM A-BCC (sigma-chain attack cascade) | `frontier_dm_pns_attack_cascade.py` | 47 | multi-observable chain |
| DM A-BCC (assumptions audit) | `frontier_dm_abcc_assumptions_audit.py` | 21 | five-route structural no-go |
| Quark a_u (JTS-affine-physical-carrier + ISSR1) | `frontier_quark_issr1_bicac_forcing.py` | 13 | headline closure |
| Quark a_u (JTS physical-point second route) | `frontier_quark_jts_physical_point_closure_theorem.py` | 12 | independent witness |
| Quark a_u (shell-normalization corroboration) | `frontier_quark_bimodule_lo_shell_normalization_theorem.py` | 10 | Route-2 carrier |
| Quark a_u (STRC-LO derivation from channel completeness) | `frontier_strc_lo_collinearity_theorem.py` | 12 | derives STRC as theorem |
| Quark a_u (RPSR NLO) | `frontier_quark_up_amplitude_rpsr_conditional.py` | 9 | delivers full physical target `a_u = 0.7748865611` |
| g_bare two-Ward closure (supporting) | `frontier_g_bare_two_ward_closure.py` | 18 | `g_bare = 1` |

No single runner has hardcoded `check("...", True, ...)` PASSes after the
cleanup pass. Every PASS is a numeric or symbolic verification of the stated
claim.
