# Scalar-Selector Cycle 1 — Remaining Open Imports

**Date:** 2026-04-20
**Scope:** Each still-open import on the four Tier-1 scalar-selector lanes
(Koide θ, Koide κ, DM A-BCC, Quark a_u) plus the supporting selected-line and
Berry lanes, with a specific statement of what derivation would close it from
Cl(3)/Z³ framework ingredients alone. Items listed here are
**retained-observational or structural-postulate inputs** that currently
prevent the corresponding lane from being marked retained-derivation on main.

**2026-04-21 canonical update.** The `morning-4-21` closure package is now
landed on `review/scalar-selector-cycle1-theorems`. On this canonical review
branch, `I1` (`Q = 2/3`) closes via the Frobenius-isotype / AM-GM route,
`I2 / P` (`δ = 2/9`) closes via the ABSS fixed-point / topological-robustness
route, and `I10` closes as the downstream selected-line corollary. The only
still-open named import on the canonical branch is now `I5`. The detailed
`I1` / `I2` / `I10` sections below are preserved as pre-closure archival
record.

## §0 Summary table

| # | Import | Lane | Current status | What closes it |
|---|---|---|---|---|
| I1 | Koide relation `Q = 2/3` | κ, θ | **closed on canonical 2026-04-21** via the Frobenius-isotype / AM-GM closure package (`docs/KOIDE_I1_I2_CLOSURE_PACKAGE_README_2026-04-21.md`) | closed |
| I2 / P | Brannen phase `δ = 2/9` on the physical base | θ | **closed on canonical 2026-04-21** via the ABSS fixed-point / topological-robustness closure package (`docs/KOIDE_I1_I2_CLOSURE_PACKAGE_README_2026-04-21.md`) | closed |
| I5 | PMNS angle triple `(sin² θ12, sin² θ13, sin² θ23)` | A-BCC (sigma-chain) | retained observational input; the new upper-octant / source-cubic selector theorems close the CP-sign / `σ_hier` half on the active chamber, and the fixed-`N_e` exact-source-manifold theorem shows the physical PMNS target already lies on a regular local `2`-real source manifold on the charged-lepton-side seed surface. The tested `Z_3` center law `delta_db = 1`, `q_+ = 0` is useful only conditionally: together with `I_src > 0` it still leaves a positive-sheet `3`-real locus and does not derive the PMNS target by itself | framework-native point-selection law stronger than the current `Z_3` center law on the exact PMNS / positive-center locus |
| I10 | H_* witness ratio `w/v ≈ 4.101` | m_* (selected-line point) | **closed on canonical 2026-04-21** as a corollary of the `I2 / P` closure package | closed |

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
- **I12 closed.** The `σ_hier = (2,1,0)` ambiguity is now closed without
  importing the T2K sign preference. The active-chamber support stack from
  `docs/DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md`,
  `docs/DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md`,
  `docs/DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md`,
  and the authoritative closeout
  `docs/DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md`
  proves that among the two `9/9`-magnitude-passing permutations only
  `(2,1,0)` satisfies the exact chamber upper-octant law, and the negative
  PMNS CP sign follows as a consequence. The branch-local proof chain is
  packaged in `docs/DM_I12_SIGMA_HIER_CLOSURE_PACKET_NOTE_2026-04-20.md`.
- **I7, I8 closed by review-surface provenance cleanup.** The quark lane now
  states its retained bimodule and atom provenance inline in the reviewer
  package and headline theorem surfaces: `docs/SCALAR_SELECTOR_REVIEWER_PACKAGE_2026-04-20.md`,
  `docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`, and
  `docs/SCALAR_SELECTOR_PROOF_CHAINS_2026-04-19.md`.

## §1 Priority ordering for closure

Closing any single item in the following ordered list produces the largest
reduction in the retained-observational footprint of the scalar-selector
cycle.

### Priority 1: Archived pre-closure record for I1 (Koide `Q = 2/3`)

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

### Priority 2: Archived pre-closure record for I2 / P (radian bridge for `δ = 2/9`)

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

**Further same-branch sharpening (2026-04-20 evening):** the actual
selected-line local packet is now proved too small to close `P`. On the
physical selected-line `CP¹` carrier, the canonical local geometry is flat
(`A = dθ`, `F = 0`) with constant equator metric density, while the structural
scalar `ρ_δ = |Im(b_F)|² = 2/d²` is branch-constant. Two distinct interior
first-branch points therefore carry the same local invariant packet
`(F, g_FS, ρ_δ)` but different Berry holonomies `δ(m)`. So no intrinsic
**local** selected-line law built from the tautological Berry geometry plus
`ρ_δ` can select the physical point `δ = 2/d²`. Any successful closure of `P`
must therefore be nonlocal on the branch (endpoint/continuation/transport) or
must add extra Wilson/lattice phase data. See
`docs/KOIDE_SELECTED_LINE_LOCAL_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`.
On the repo's physical `3+1` reading, that means the missing content cannot
live in the `1`-dimensional selected-line base itself; it has to come from
ambient continuation/transport data or extra retained Wilson/lattice
structure.

**Further reduction (2026-04-20 late):** combining the actual Berry theorem,
the selected-line cyclic-response bridge, the selected-line local no-go, and
the retained anomaly-forced-time theorem now sharpens the live native route
further. Since `δ(m)` is already the actual Berry holonomy and `δ = 2/9`
already fixes one unique interior first-branch point `m_*`, while no local
selected-line invariant packet can distinguish that point, the residual
postulate `P` is now reduced to a **one-clock ambient `3+1`
continuation/endpoint/transport law** or to an extra retained Wilson/lattice
phase datum on that same ambient. In other words: the anomaly/time derivation
does not close `P` by itself, but it does identify the only remaining native
category where a closure law could still live. See
`docs/KOIDE_P_ONE_CLOCK_3PLUS1_TRANSPORT_REDUCTION_NOTE_2026-04-20.md`.

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

### Priority 3: I5 (PMNS angle triple)

Scope is larger than the scalar-selector cycle; this is part of the broader
charged-lepton flagship gate. Closing it requires framework-native PMNS
derivation, which is an open program on multiple branches
(lepton-mass-tower, lepton-pmns-integration, dm-leptons-review). Not scoped
to tomorrow's submission.

**New same-branch reduction (2026-04-20):** the PMNS CP-sign / hierarchy half
is no longer open. `docs/DM_SIGMA_HIER_H_INTRINSIC_NO_GO_THEOREM_NOTE_2026-04-20.md`
rules out the `H`-intrinsic and `μ↔τ`-even scalar families;
`docs/DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md` reduces the
remaining ambiguity to one parity bit; and the coefficient-free selector
system

```text
sin² θ23 > 1/2,
I_src(H) > 0
```

closes that bit on the exact active-chamber root set via
`docs/DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md`.
The cleaner authoritative closeout is
`docs/DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md`, which
uses the exact chamber upper-octant law to select `σ_hier = (2,1,0)` from the
two `9/9`-magnitude-passing permutations and then gets `sin δ_CP < 0` as a
consequence. So the only remaining PMNS observational input on this branch is
the angle triple itself, not the CP sign.

**Further same-branch reduction (2026-04-20):** the new fixed-`N_e`
exact-source-manifold theorem closes an important existence loophole. The
physical PMNS angle triple is already realized exactly on the charged-lepton-
side fixed native `N_e` seed surface, and on the verified exact patch the
PMNS-angle Jacobian has full rank `3`, so the physical target lies on a local
regular `2`-real source manifold inside that `5`-real seed surface. The
current exact nonlocal seed-surface selector families still miss that
manifold. So the remaining live `I5` object is now sharper than “derive the
PMNS angle triple somehow”: it is the missing point-selection law on that
exact `2`-real source manifold. See
`docs/DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md`.

**Tested center-law route (2026-04-20):** the proposed coefficient-free
`Z_3` doublet-block center law `delta_db(H) = 1`, `q_+(H) = 0` does not close
`I5` by itself, even after adding the already-closed sheet law `I_src(H) > 0`.
On the verified patch it leaves a local positive-sheet `3`-real center locus,
and the PMNS angle triple varies macroscopically along that locus. So the
center law is a useful conditional cut on the exact PMNS manifold, but not yet
the missing native point-selection law. See
`docs/DM_PMNS_Z3_DOUBLET_BLOCK_CENTER_POSITIVE_SHEET_NO_GO_THEOREM_NOTE_2026-04-20.md`.

### Priority 4: Archived pre-closure record for I10 (selected-line physical point)

Now the only open content behind `m_*` is the scalar-phase pin itself. If
`I2 / P` closes, `I10` closes immediately by the exact selected-line
scalar-phase bridge.

## §2 What a Nature reviewer will still see after submission

With the 2026-04-21 Koide closure package now landed on canonical, the honest
Nature-grade statement for this cycle is:

> Four Tier-1 scalar-selector gates of the Standard Model — the Koide
> charged-lepton cone normalization (κ = 2, equivalently the operator-side
> Koide relation), the Koide Brannen–Zenczykowski phase offset (δ = 2/9), the
> dark-matter A-BCC basin-sheet choice, and the up-sector quark reduced
> amplitude (a_u) — each reduce to retained Cl(3)/Z³ framework ingredients,
> with the only still-open named retained input now being the PMNS angle
> triple point-selection law on the exact charged-lepton-side seed manifold
> beyond the currently tested `Z_3`
> center law. No new
> axioms are added this cycle. The framework
> contributes (i) a retained-forced Frobenius-isotype / AM-GM closure of the
> Koide cone relation `Q = 2/3`, (ii) a retained-forced ABSS fixed-point /
> topological-robustness closure of the Brannen phase `δ = 2/9`, (iii) an exact
> Fourier-bridge algebraic reduction of operator-side κ = 2 to spectrum-side Q = 2/3,
> (iv) a Sylvester-inertia reduction of A-BCC, closed via a multi-observable
> sigma-chain that combines retained Cl(3)/Z³ theorems with the PMNS
> angle-triple pin, now sharpened by an exact fixed-`N_e` source-manifold
> theorem showing the target already lies on a regular `2`-real source
> manifold together with a center-law positive-sheet no-go showing that the
> current `delta_db = 1`, `q_+ = 0`, `I_src > 0` proposal is still
> insufficient, and (v) a linear-algebra derivation of the up-sector
> quark closure on the retained `1⊕5` bimodule and CKM-atlas atom package,
> whose provenance is now surfaced inline on the review branch. Each retained
> observational input or structural postulate still blocking native closure is
> listed in the Remaining-Open-Imports register along with the derivation that
> would close it.

The cycle-2 housekeeping imports I3, I4, I6, I11, and I12 are now closed;
with the 2026-04-21 Koide package, the remaining irreducible frontier on the
canonical review branch is `I5` alone.

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
| DM A-BCC (active-chamber completeness) | `frontier_dm_pmns_chamber_spectral_completeness_theorem_2026_04_20.py` | 11 | exact chamber `χ²=0` set = `{Basin 1, Basin 2, Basin X}` |
| DM A-BCC (`σ_hier` upper-octant selector) | `frontier_dm_sigma_hier_upper_octant_selector_theorem_2026_04_20.py` | 14 | closes `I12` without importing T2K sign |
| DM A-BCC (upper-octant / source-cubic selector) | `frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py` | 14 | fixes Basin 1 uniquely on the active chamber |
| DM A-BCC (local-family no-go) | `frontier_dm_pmns_local_selector_family_no_go_theorem_2026_04_20.py` | 15 | reduces `I5` to nonlocal point-selection / angle triple only |
| DM A-BCC (fixed-`N_e` exact-source manifold) | `frontier_dm_pmns_ne_seed_surface_exact_source_manifold_theorem_2026_04_20.py` | 12 | shows the physical PMNS target already lies on a regular local `2`-real source manifold |
| DM A-BCC (center-law positive-sheet no-go) | `frontier_dm_pmns_z3_doublet_block_center_positive_sheet_no_go_2026_04_20.py` | 14 | shows `delta_db = 1`, `q_+ = 0`, `I_src > 0` still leaves a positive-sheet `3`-real locus |
| Quark a_u (JTS-affine-physical-carrier + ISSR1) | `frontier_quark_issr1_bicac_forcing.py` | 13 | headline closure |
| Quark a_u (JTS physical-point second route) | `frontier_quark_jts_physical_point_closure_theorem.py` | 12 | independent witness |
| Quark a_u (shell-normalization corroboration) | `frontier_quark_bimodule_lo_shell_normalization_theorem.py` | 10 | Route-2 carrier |
| Quark a_u (STRC-LO derivation from channel completeness) | `frontier_strc_lo_collinearity_theorem.py` | 12 | derives STRC as theorem |
| Quark a_u (RPSR NLO) | `frontier_quark_up_amplitude_rpsr_conditional.py` | 9 | delivers full physical target `a_u = 0.7748865611` |
| g_bare two-Ward closure (supporting) | `frontier_g_bare_two_ward_closure.py` | 18 | `g_bare = 1` |

No single runner has hardcoded `check("...", True, ...)` PASSes after the
cleanup pass. Every PASS is a numeric or symbolic verification of the stated
claim.
