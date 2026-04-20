# Scalar-Selector Cycle 1 — Remaining Open Imports

**Date:** 2026-04-20
**Scope:** Each open import on the four Tier-1 scalar-selector lanes (Koide θ, Koide κ, DM A-BCC, Quark a_u) plus the supporting selected-line and Berry lanes, with a specific statement of what derivation would close it from Cl(3)/Z³ framework ingredients alone. Items listed here are **retained-observational or structural-postulate inputs** that currently prevent the corresponding lane from being marked retained-derivation on main.

## §0 Summary table

| # | Import | Lane | Current status | What closes it |
|---|---|---|---|---|
| I1 | Koide relation `Q = 2/3` | κ, θ | retained observational (not derived; 6 structural no-go theorems on main rule out several mechanisms) | a Cl(3)/Z³-native forcing of the cone condition `a_0² = 2|z|²` from retained representation-theory or from a retained scalar-potential minimization that lands on the cone |
| I2 | Brannen phase `δ = 2/9` | θ | retained observational (Berry identifies geometrically on the physical selected line; ambient-S² derivation blocked by bundle obstruction) | either (a) a justified natural completion of the physical 1-D locus to an ambient equivariant base carrying `c_1 = dim(doublet) = 2`, or (b) a Wilson-line / Z³-orbit quantization on the physical base that forces the holonomy value |
| I3 | Selected-line reduction `H_sel(m) = H(m, √6/3, √6/3)` | θ, m_* | **closed on this branch**: the Koide microscopic target note now names the charged-lepton two-Higgs canonical reduction and selected-line closure notes inline | none beyond landing the updated target note |
| I4 | Chamber bound `q_+ + δ ≥ √(8/3)` | A-BCC | **closed on this branch**: inline derivation added from the retained active-half-plane inverse chart | none beyond landing the updated A-BCC note |
| I5 | PMNS observational pins (NuFit 3σ ranges, T2K `sin δ_CP < 0`) | A-BCC (sigma-chain) | **further reduced on this branch, not fully closed**: `DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md` closes the CP-sign / `sigma_hier` half by the coefficient-free selector system `s23^2 > 1/2`, `I_src(H) > 0`; the new `DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md` shows that on the charged-lepton-side minimal branch the physical PMNS angle triple already lies on a regular local `2`-real source manifold inside the fixed native `N_e` seed surface, while the current exact nonlocal seed-surface selector families all miss it | framework-native `2`-real point-selection law on the exact PMNS source manifold (equivalently: the selected-branch Hermitian-data law on the charged-lepton-side branch) |
| I6 | Scalar-lane SO(2)-quotient of the real doublet | κ (MRU route only) | **closed on this branch**: `KOIDE_SCALAR_LANE_OBSERVABLE_RADIUS_THEOREM_NOTE_2026-04-20.md` derives the quotient from the observable-principle local scalar jet | none for the MRU route; the spectrum/operator bridge remains an independent route |
| I7 | Bimodule `B = Cl(3)/Z₃ ⊗ Cl_CKM(1⊕5)` | a_u | **closed on this branch**: the Quark ISSR1 headline theorem now carries a self-contained provenance paragraph for the bimodule route | none beyond landing the updated Quark note |
| I8 | Retained atoms `ρ = 1/√42`, `supp = 6/7`, `δ_A1 = 1/42` | a_u | **closed on this branch**: the Quark ISSR1 headline theorem now cites the exact CKM atlas atoms inline | none beyond landing the updated Quark note |
| I9 | `a_d = ρ` | a_u | retained from `QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE` | inline citation already present; nothing to close |
| I10 | H_* witness ratio `w/v ≈ 4.101` | m_* (selected-line point) | retained observational | deriving `m_*` as a corollary of `δ = 2/9` via the exact scalar-phase bridge (already established). If I2 closes, I10 closes automatically |
| I11 | Basin enumeration `{Basin 1, N, P, X}` exhaustiveness | A-BCC | **closed on this branch for the active chamber**: `DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md` proves the exact chamber `χ² = 0` set is `{Basin 1, Basin 2, Basin X}` | none for the active chamber; off-chamber chart bookkeeping is separate from the live A-BCC completeness target |
| I12 | σ_hier permutation `(2,1,0)` | A-BCC (sigma-chain) | **closed on this branch**: the authoritative closeout is `DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md`; it proves that among the two `9/9`-magnitude-passing permutations only `(2,1,0)` satisfies the exact chamber upper-octant law. The earlier `DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md` gives the exact chamber-root / source-cubic version of the same closure. See also `DM_I12_SIGMA_HIER_CLOSURE_PACKET_NOTE_2026-04-20.md` for the branch-local proof chain. | none beyond landing the closure packet and theorem |

## §1 Priority ordering for closure

Closing any single item in the following ordered list produces the largest reduction in the retained-observational footprint of the scalar-selector cycle.

### Priority 1: I1 (Koide `Q = 2/3`)

Closing `Q = 2/3` from Cl(3)/Z³ would immediately upgrade the Koide κ and θ lanes from "retained-observational-conditional" to "retained-derivation" on main. It is the single highest-leverage open item in the cycle.

**What is already ruled out (main):** six structural no-go theorems cover Z₃-invariance alone, sectoral universality, color-sector correction, anomaly-forced cross-species, SU(2) gauge exchange mixing, and observable-principle character symmetry. None of these mechanisms forces the cone point.

**What has not been ruled out:** a forcing from a retained Z³ scalar potential that lands its physical minimum on the cone. The retained Z³ scalar potential `V(m) = const + (c1+c2/2)m + (3/2)m² + (1/6)m³` has a stationary point `m_V ≈ −0.433` which is **not** the Koide cone point `m_* ≈ −1.161` (documented on main as an honest gap). A successful derivation requires adding the first-principles retained ingredient that moves the effective minimum from `m_V` to `m_*`.

**Candidate closing routes (each needs its own derivation):**

1. **H_* witness ratio from a retained lattice calculation.** The H_* witness kappa_* ≈ −0.608 currently pins `m_*` by observational fit. If a retained lattice propagator or transport integral computes kappa_* from Cl(3)/Z³ ingredients alone, the cone point is forced. This is the most likely route.
2. **Retained microscopic selector on the 4×4 (hw=1 + baryon) block.** If the full 4×4 generator (T₂ sector + baryon) from the microscopic lattice action introduces non-uniform coupling that adds a retained m-dependent term to `V_eff`, the minimum may move to `m_*`. Ruled `low-probability` on main but not formally closed.
3. **Transport gap ratio 4π/√6.** Numerically close to the observed `η/η_obs ≈ 5.29` (3.2% mismatch). If formalized into a retained lattice identity, it could pin `m_*`.
4. **One-clock semigroup / Γ-orbit positive witness route.** Already delivers cos-similarity > 1 − 10⁻⁹ with PDG √m-vector at the cone point `H_*`. Currently conditional on G1 observational chamber pins (M_STAR, DELTA_STAR, Q_PLUS_STAR). If those three pins can be derived from retained framework, `Q = 2/3` follows.

**Required retained ingredients for any of the above:** explicit lattice propagator or transport-integral definition on the retained Cl(3)/Z³ carrier; currently on main as partial-support.

### Priority 2: I2 (Brannen phase `δ = 2/9`)

Closing `δ = 2/9` would upgrade the Koide θ lane to retained-derivation. Lower leverage than I1 but more within reach because a partial derivation already exists (the cycle-10B ambient-S² Berry-holonomy calculation `γ = 2π(d−1)/d = 2πQ`, reducing to `δ = Q/d = 2/9` at `d = 3`).

**Partial derivation already on canonical:** §2 of `KOIDE_BERRY_PHASE_THEOREM_NOTE` (ambient-S² n=2 monopole model). On the C₃-equivariant completion of the scale-free Koide locus to the unit 2-sphere, the doublet bundle carries `c_1 = dim(doublet) = 2` by Borel–Weil/Pieri; the Berry holonomy of this bundle over one C₃ cyclic period equals `2πQ = 4π/3`; reduction to Brannen units per C₃ element gives `δ = Q/d = 2/9`.

**What blocks this as a closure:** the retained positive physical Koide locus is three open arcs on a single circle (not S²), so on the actual physical base the doublet bundle is equivariantly trivial, `c_1 = 0`. See `KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE`. The ambient-S² completion is therefore the load-bearing step that needs a physics justification, not just a natural-mathematics justification.

**Candidate closing routes:**

1. **Equivariant-completion forcing theorem.** Show that the minimal C₃-equivariant completion of the scale-free Koide locus that preserves the retained representation-theoretic data (specifically, the doublet bundle's dim-doublet Chern-class identity) is S². A theorem of the form "the minimal equivariant CW extension of `K_norm⁺/C₃` compatible with retained data is `S²`" would promote the cycle-10B calculation to retained.
2. **Wilson-line Z³-orbit quantization on the physical base.** The selected-line CP¹ Pancharatnam–Berry identification is on the physical base. Augmenting with a retained quantization condition — e.g., the Berry phase per C₃ element must satisfy a Wilson-line retention identity on the retained Cl(3)/Z³ lattice — could force `δ = 2/9`. Open territory.
3. **Derive δ as a cycle-periodic Berry phase from the retained Z³ scalar potential.** If V(m) induces a Berry-type phase on closed paths in the scalar-lane reduced configuration space, quantization of that phase by the retained Z₃ cycle could force the value.

### Priority 3: I4 (Chamber bound)

Closed on this branch. The A-BCC note now carries the explicit
active-half-plane derivation
`q_+ + delta = sqrt(8/3) + sqrt(r31^2 - 1/4) >= sqrt(8/3)`.

### Priority 4: I3, I7, I8 (provenance surfacing)

Closed on this branch. The remaining work on these three items was editorial
only; the relevant provenance now sits inline in the Koide microscopic-target
and Quark ISSR1 headline notes.

### Priority 5: I5, I12 (PMNS observational pins and σ_hier permutation)

Scope is larger than the scalar-selector cycle; these are part of the broader charged-lepton flagship gate. Closing them requires framework-native PMNS derivation, which is an open program on multiple branches (lepton-mass-tower, lepton-pmns-integration, dm-leptons-review). Not scoped to tomorrow's submission.

Update on this branch:

- `I12` is now closed. The old
  `DM_SIGMA_HIER_H_INTRINSIC_NO_GO_THEOREM_NOTE_2026-04-20.md` ruled out
  `H`-intrinsic and `μ↔τ`-even scalar families, and
  `DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md` reduced the
  gap to one parity bit. The first closeout theorem
  `DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md`
  closes that bit: the retained chamber law forces the upper octant, and the
  coefficient-free source law `I_src(H) > 0` then selects Basin 1 uniquely,
  hence `sigma_hier = (2,1,0)`. The authoritative branch-local closeout note
  is now
  `DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md`, with
  `DM_I12_SIGMA_HIER_CLOSURE_PACKET_NOTE_2026-04-20.md` added as a
  reviewer-facing proof packet.
- `I5` is reduced one step further. The CP-sign half is now closed by the same
  theorem, and the new
  `DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md`
  sharpens the angle side: on the charged-lepton-side minimal branch the
  physical PMNS angle triple already lies on a regular local `2`-real source
  manifold inside the fixed native `N_e` seed surface, but the current exact
  nonlocal seed-surface selector families do not pick it. So the remaining
  `I5` gap is no longer generic “derive the PMNS triple somehow.” It is the
  framework-native point-selection law on that exact PMNS source manifold.

### Priority 6: I6 (SO(2)-quotient)

Closed on this branch by
`KOIDE_SCALAR_LANE_OBSERVABLE_RADIUS_THEOREM_NOTE_2026-04-20.md`: the
observable-principle local scalar jet on the real `C_3` doublet is forced to
be proportional to `r_1^2 + r_2^2`, so the scalar lane really does factor
through the doublet radius.

### Priority 7: I11 (basin enumeration exhaustiveness)

Closed on this branch for the active chamber.

The old `DM_PMNS_ASYMPTOTIC_SOURCE_NO_GO_NOTE_2026-04-20.md` removed the
infinity-tail loophole. The new
`DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md` closes the
compact remainder: the exact active-chamber `chi^2 = 0` set is

```text
{Basin 1 on sigma=(2,1,0), Basin 2 on sigma=(2,1,0), Basin X on sigma=(2,0,1)}.
```

## §2 What a Nature reviewer will still see after submission

With the above items retained-observational, the honest Nature-grade statement for this cycle is:

> Four Tier-1 scalar-selector gates of the Standard Model — the Koide charged-lepton cone normalization (κ = 2, equivalently the operator-side Koide relation), the Koide Brannen–Zenczykowski phase offset (δ = 2/9), the dark-matter A-BCC basin-sheet choice, and the up-sector quark reduced amplitude (a_u) — each reduce to retained Cl(3)/Z³ framework ingredients plus named retained inputs (the Koide cone relation Q = 2/3; the Brannen phase value δ = 2/9; the PMNS angle triple `(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)`; the CKM atlas unit-ray parameter ρ = 1/√42 and its structure atoms). No new axioms are added this cycle. The framework contributes (i) a canonical Pancharatnam–Berry geometric identification of δ on the physical selected line, (ii) an exact Fourier-bridge algebraic reduction of operator-side κ = 2 to spectrum-side Q = 2/3, (iii) a Sylvester-inertia reduction of A-BCC, now sharpened by an exact compact active-chamber completeness theorem, an exact source-cubic / parity reduction of the PMNS CP sign, and a coefficient-free upper-octant / source-cubic selector law fixing `sigma_hier = (2,1,0)`, (iv) a linear-algebra derivation of the up-sector quark closure on the retained 1⊕5 bimodule. Each retained observational input is listed in the Remaining-Open-Imports register along with the derivation that would close it.

Closing any priority-1 or priority-2 item above would upgrade the corresponding lane from retained-conditional to retained-derivation and eliminate the named retained input. Closing all six priority-1–4 items would move the entire cycle from retained-conditional to retained-derivation, leaving only the PMNS angle triple as the non-derived ingredient on the DM side.

## §3 Reproduction of current retained-conditional state

All runners currently pass on canonical (branch `review/scalar-selector-cycle1-theorems`). For each of the four Tier-1 lanes the primary closure runner and its verification counts are:

| Lane | Primary runner | PASS | Notes |
|---|---|---|---|
| Koide κ (spectrum/operator bridge) | `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` | 9 | exact sympy identity `a_0² − 2|z|² = 3(a² − 2|b|²)` |
| Koide κ (block-total Frobenius corroboration) | `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` | 16 | independent functional reaching same `κ = 2` |
| Koide θ (Berry identification on selected line) | `frontier_koide_berry_phase_theorem.py` | 24 | ambient-S² calculation § + selected-line CP¹ § + natural-selector no-go § |
| Koide θ (scalar-phase bridge) | `frontier_koide_selected_line_cyclic_response_bridge.py` | 20 | `κ_sel(δ)` exact identity |
| DM A-BCC (chamber ∩ DPLE) | `frontier_dm_abcc_chamber_dple_closure.py` | 39 | chamber bound + discriminant sign |
| DM A-BCC (Sylvester signature-forcing) | `frontier_dm_abcc_signature_forcing_theorem.py` | 54 | path-independent via IVT + det sign |
| DM A-BCC (PMNS Non-Singularity conditional) | `frontier_dm_abcc_pmns_nonsingularity_theorem.py` | 38 | conditional closure |
| DM A-BCC (sigma-chain attack cascade) | `frontier_dm_pns_attack_cascade.py` | 47 | multi-observable chain |
| DM A-BCC (assumptions audit) | `frontier_dm_abcc_assumptions_audit.py` | 21 | five-route structural no-go |
| DM A-BCC (upper-octant / source-cubic selector) | `frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py` | 14 | closes `sigma_hier` and the PMNS CP-sign half on the active chamber |
| Quark a_u (JTS-affine-physical-carrier + ISSR1) | `frontier_quark_issr1_bicac_forcing.py` | 13 | headline closure |
| Quark a_u (JTS physical-point second route) | `frontier_quark_jts_physical_point_closure_theorem.py` | 12 | independent witness |
| Quark a_u (shell-normalization corroboration) | `frontier_quark_bimodule_lo_shell_normalization_theorem.py` | 10 | Route-2 carrier |
| Quark a_u (STRC-LO derivation from channel completeness) | `frontier_strc_lo_collinearity_theorem.py` | 12 | derives STRC as theorem |
| Quark a_u (RPSR NLO) | `frontier_quark_up_amplitude_rpsr_conditional.py` | 9 | delivers full physical target `a_u = 0.7748865611` |
| g_bare two-Ward closure (supporting) | `frontier_g_bare_two_ward_closure.py` | 18 | `g_bare = 1` |

No single runner has hardcoded `check("...", True, ...)` PASSes after the cycle-1 cleanup pass. Every PASS is a numeric or symbolic verification of the stated claim.
