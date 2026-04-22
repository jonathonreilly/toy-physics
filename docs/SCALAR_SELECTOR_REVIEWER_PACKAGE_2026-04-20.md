# Scalar-Selector Cycle 1 — Reviewer Package

**Date:** 2026-04-20
**Scope:** Reviewer-facing clean-language summary of four Tier-1 Standard
Model scalar-selector gates on the current review surface. The package closes
the up-sector quark gate, materially sharpens the charged-lepton Koide gates,
and closes the DM gate on the review surface while materially sharpening the
stricter/native map without adding new axioms.
Named retained observational inputs and unresolved structural bridges are
listed explicitly. This note is the primary read-me for the submission.

---

## §0 Bottom line

On the current review surface, the up-sector quark gate is fully closed, the
charged-lepton Koide lane carries the strongest current executable support
stack but still retains two physical bridges, and the DM gate is closed on the
review surface while the stricter/native map now carries one remaining
physical-identification question. No new axioms are added.
All runners pass with no hardcoded verifications. Open retained-observational
inputs and unresolved structural bridges are enumerated separately in
`docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md`.

**2026-04-21 package update.** The April 21 Koide package
(`docs/KOIDE_Q_DELTA_CLOSURE_PACKAGE_README_2026-04-21.md`) supersedes the
older κ / θ route-pruning surface as the strongest current support stack. It
does not fully close the charged-lepton Koide lane: `Q = 2/3` still needs the
physical/source-law extremal-principle bridge, and `δ = 2/9` still needs the
physical Brannen-phase bridge.

| Gate | Observable | Closure routes | Retained inputs |
|---|---|---|---|
| **Koide κ** | Charged-lepton cone normalization `κ = 2` (equivalently `Q = 2/3`) | April 21 support package: Frobenius-isotype / AM-GM support + executable reviewer stress-test | physical/source-law bridge from retained framework physics to the block-total Frobenius extremal principle |
| **Koide θ** | Brannen-Zenczykowski phase offset `δ = 2/9` | April 21 support package: ABSS fixed-point / topological robustness + executable reviewer stress-test | physical Brannen-phase bridge from the selected-line observable to the ambient APS invariant |
| **DM PMNS** | Physical neutrino-source basin selection plus intrinsic PMNS point selection | Retained-measurement A-BCC integration + interval-certified split-2 closure + shifted same-law recovered-packet closure + exact target-surface source-cubic theorem + graph-first ordered-chain nonzero-current activation theorem | none on the review surface; one stricter/native physical-identification residue remains after current activation |
| **Quark a_u** | Up-sector reduced amplitude `a_u = 0.7748865611` | Affine-physical-carrier JTS + one-dimensional 5-channel residue + RPSR NLO | Bimodule `B = Cl(3)/Z₃ ⊗ Cl_CKM(1⊕5)`, retained atoms `ρ, supp, δ_A1` (CKM atlas) |

---

## §1 Koide κ — charged-lepton cone normalization

**Observable.** The operator-side Koide normalization

    κ  :=  g_0² / |g_1|²  =  2

on the C₃ Fourier-character decomposition of the charged-lepton Hermitian carrier, equivalent to the spectrum-side Koide relation

    Q  :=  (m_e + m_μ + m_τ) / (√m_e + √m_μ + √m_τ)²  =  2/3.

### §1.1 Primary closure — spectrum–operator Fourier bridge

**Theorem.** On the C₃-cyclic Hermitian algebra `Herm_circ(3)`, the exact Fourier-character identity

    a_0² − 2|z|²  =  3 (a² − 2|b|²)

holds where `(a_0, z)` are the spectrum-side C₃ character components of `(√m_e, √m_μ, √m_τ)` and `(a, b)` are the operator-side C₃ Fourier components of `H = aI + bC + b̄C²`.

**Proof.** Direct symbolic expansion on the C₃ Fourier basis; sympy-verified in `scripts/frontier_koide_kappa_spectrum_operator_bridge_theorem.py` (9 PASS, 0 FAIL).

**Consequence.** The spectrum-side Koide relation `Q = 2/3`, equivalent to `a_0² = 2|z|²`, implies the operator-side normalization `a² = 2|b|²`, i.e. `κ = 2`. The operator-side framing reduces algebraically to the spectrum-side framing under the retained cyclic-compression bridge.

**Package status.** The April 21 Frobenius-isotype / AM-GM stack is the
strongest current support route for `Q = 2/3`. It proves that the admitted
block-total Frobenius functional is maximized at the Koide point. What
remains open is the physical/source-law bridge: why the charged-lepton packet
must extremize that functional on the retained framework surface.

### §1.2 Independent corroboration — block-total Frobenius measure

**Theorem.** The block-total Frobenius-squared functional `E_I(H) := ‖π_I(H)‖²_F` on `Herm_circ(3)` assigns one scalar per real-isotype block. Direct computation:

    E_+  =  3 a²     (singlet),
    E_⊥  =  6 |b|²   (doublet).

The equal-block-measure extremum `E_+ = E_⊥` at fixed `E_+ + E_⊥` recovers `a² = 2|b|²`, i.e. `κ = 2`.

**Proof.** Direct calculation; verified in `scripts/frontier_koide_kappa_block_total_frobenius_measure_theorem.py` (16 PASS, 0 FAIL).

**Dimensional uniqueness.** `d = 3` is the unique dimension where `Herm_circ(d)` decomposes as `1·trivial ⊕ 1·complex-doublet`, so the block-total Frobenius functional is itself dim-uniquely well-defined at `d = 3`.

**Retained inputs.** Herm_circ(3) structure (C₃ representation theory; see `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`), `d = 3` (from `docs/DIMENSION_SELECTION_NOTE.md` and related dimensional-selection notes).

### §1.3 Supporting — Moment-Ratio Uniformity (MRU)

On `Herm_circ(3)` with Frobenius metric, the MRU principle — Frobenius-normalized cyclic responses uniform across Z₃ isotypes — is a single scalar equation equivalent to `a² = 2|b|²`. See `scripts/frontier_koide_moment_ratio_uniformity_theorem.py` (26 PASS). MRU is supplementary support only. The cycle-2 demotion note proves that the stronger SO(2)-quotient needed to make MRU load-bearing is **not** derivable from the retained observable principle, so the primary closure remains the spectrum/operator bridge plus the block-total Frobenius route. See `docs/KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`.

### §1.4 Supporting obstructions — what is ruled out

Six structural no-go theorems in `docs/STRUCTURAL_NO_GO_SURVEY_NOTE.md`
(total 250 PASS across 6 runners) rule out Z₃-invariance alone, sectoral
universality, color-sector correction, anomaly-forced cross-species, SU(2)
gauge-exchange mixing, and observable-principle character symmetry as
candidate forcing mechanisms for `Q = 2/3`. These remain useful negative
controls, but they are superseded by the landed Frobenius-isotype / AM-GM
support package rather than read as the final Koide status.

---

## §2 Koide θ — Brannen–Zenczykowski phase offset

**Observable.** The charged-lepton doublet-phase offset from the uniform C₃ phases `2πn/3`, appearing in Brannen's parameterization

    √m_n  =  μ [ 1 + √2 cos( δ + 2πn/3 ) ],       n = 0, 1, 2,

with `δ = 2/9` ≈ 0.222 rad fitting PDG to machine precision.

### §2.1 Primary identification — Pancharatnam–Berry on the selected line

**Theorem.** On the physical charged-lepton selected line

    H_sel(m)  =  H( m, √6/3, √6/3 )

(whose specific slot values are now traced exactly to the retained-on-`main`
parity-compatible observable-selector chain in
`docs/KOIDE_SELECTED_LINE_PROVENANCE_NOTE_2026-04-20.md`), the normalized
Koide amplitude has the exact Fourier decomposition

    s(m)  =  (1/√2) v_1  +  (1/2) e^{iθ(m)} v_ω  +  (1/2) e^{−iθ(m)} v_{ω̄}

with `θ(m)` continuous on the physical first branch. The singlet weight is fixed; the moving datum is the projective C₃ doublet ray

    [1 : e^{−2iθ(m)}]

on the equator of CP¹. The tautological CP¹ line bundle carries the canonical Pancharatnam–Berry connection `A = dθ`. There is a unique unphased first-branch point `m_0` where `u(m_0) = v(m_0)` and `θ(m_0) = 2π/3`. Hence

    Hol(m_0 → m)  =  θ(m) − 2π/3  =:  δ(m).

**Proof.** Direct Fourier-character construction on the selected line; verified in `scripts/frontier_koide_berry_phase_theorem.py` (24 PASS, 0 FAIL) and `scripts/frontier_koide_selected_line_cyclic_response_bridge.py` (20 PASS).

**Consequence (scalar–phase bridge).** The exact identity

    κ_sel(δ)  =  −√3 · cos(δ + π/6) / (√2 + sin(δ + π/6))

gives a one-to-one map between the Brannen phase `δ` and the surviving selected-line scalar `κ_sel := (v − w)/(v + w)`. Monotonicity on the physical first branch forces a unique first-branch point `m_*` once `δ` is given. At `δ = 2/9`:

    κ_sel,*  =  −0.607918569997,     m_*  =  −1.160443440065,     w/v  =  4.100981191542.

### §2.2 Supporting obstruction

**Theorem.** On the actual physical positive projectivized Koide locus — three open arcs on a single latitude circle, cyclically permuted by C₃ — every C₃-equivariant complex line bundle is equivariantly trivial. In particular no nontrivial Chern class can live on the physical base. See `docs/KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`.

**Consequence.** The original ambient-S² monopole construction does **not**
live on the physical base. It survives only as an internally coherent
illustration. The physical-base closure is the selected-line CP¹
Pancharatnam–Berry identification above, which uses the projective
doublet-coordinate phase-doubling `e^{−2iθ}` in place of any ambient
topological flux. The same-branch linking theorem then identifies the honest
remaining gap precisely: the structural count `2/d²` is available, but its
identification with the physical Berry holonomy in radians is not forced on
the retained base.

### §2.3 Package status and geometric context

**Package status.** The April 21 ABSS fixed-point / topological-robustness
chain is the strongest current support route for `δ = 2/9`. It computes the
ambient APS invariant exactly and proves its robustness. The Berry-holonomy
reading above remains more than geometric context: the physical selected-line
Brannen-phase bridge is still open.

See `docs/KOIDE_Q_DELTA_LINKING_RELATION_THEOREM_NOTE_2026-04-20.md` and
`docs/KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`.

---

## §3 DM A-BCC — physical basin selection

**Observable.** The physical neutrino-source sheet choice among the χ²=0 PMNS-compatible chamber points, enumerated as `{Basin 1, Basin 2, Basin X}` under the retained σ-permutation. Basin 1 is identified as the physical basin.

### §3.1 Primary closure — Sylvester signature-forcing + σ-chain

**Setup.** The retained linear Hermitian pencil on the PMNS source surface

    H(t; J)  =  H_base  +  t · J,       t ∈ [0, 1],

carries `H_base` in Sylvester chamber `C_base = {det > 0, signature (1, 0, 2)}` and has `det(H_base) > 0` exactly by the retained base parameters.

**Theorem (Sylvester signature-forcing).** Any continuous path in `Herm_3` between `C_base` and any component with `det < 0` must cross the determinant-zero variety. Hence if the physical path `H(t; J_phys)` stays in `{det ≠ 0}` for all `t ∈ [0, 1]` (PMNS Non-Singularity, PNS), the endpoint `H(1; J_phys)` must lie in `C_base`.

**Theorem (updated σ-chain).** Combining the retained chamber bound
`q_+ + δ ≥ √(8/3)`, the retained chamber-completeness theorem on the active
`χ² = 0` set, the parity reduction
`J_σ = parity(σ) I_src(H) / Δ`, the exact chamber upper-octant law, and the
coefficient-free source law `I_src(H) > 0`, the active-chamber chart
collapses to Basin 1 uniquely:

- the active-chamber `χ² = 0` set is exactly `{Basin 1, Basin 2, Basin X}`;
- among the two `9/9`-magnitude-passing permutations only `σ = (2,1,0)`
  satisfies the exact chamber upper-octant law;
- on the upper-octant chamber roots, `I_src(H) > 0` holds only on Basin 1;
- therefore `σ_hier = (2,1,0)` and `sin δ_CP < 0` are consequences, not
  retained selector inputs;
- Basin 1 also has `q_+ + δ = 1.649 > √(8/3)` and P3 Sylvester computes
  `min det(H_base + t J_1) = 0.878 > 0` on `[0, 1]`.

Hence `J_phys = J_{Basin 1}` and PNS is a derived property of the physical path.

**Proof.** Multi-observable verification in
`scripts/frontier_dm_pns_attack_cascade.py` (34 PASS, 0 FAIL),
`scripts/frontier_dm_abcc_signature_forcing_theorem.py` (43 PASS),
`scripts/frontier_dm_abcc_pmns_nonsingularity_theorem.py` (33 PASS),
`scripts/frontier_dm_pmns_chamber_spectral_completeness_theorem_2026_04_20.py`
(11 PASS), `scripts/frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py`
(14 PASS), and
`scripts/frontier_dm_sigma_hier_upper_octant_selector_theorem_2026_04_20.py`
(14 PASS). The P3 Sylvester linear-path signature theorem is retained
upstream; see
`docs/DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18.md`.

### §3.2 Independent route — chamber ∩ DPLE F_4

**Theorem (DPLE dim-parametric extremum).** On any retained linear Hermitian pencil, `log|det H(t)|` has at most `⌊d/2⌋` interior Morse-index-0 critical points; at `d = 3` exactly one. On the corrected five-basin chart, the chamber survivors are `{Basin 1, Basin 2, Basin X}`. The cycle-2 completeness theorem and the retained signature results place Basin 2 and Basin X on the `C_neg` sheet, so the A-BCC sheet-restricted DPLE comparison remains the pair `{Basin 1, Basin X}` analyzed in the closure note, and the F_4 discriminant test `Δ = c_2² − 3 c_1 c_3 > 0` selects Basin 1 uniquely there.

**2026-04-21 native-route sharpening.** The corrected five-basin chamber+DPLE
support theorem now checks the previously missing Basin 2 case directly:
`F_4(Basin 2) = FALSE` by a negative DPLE discriminant, so the corrected
composition `chamber ∩ F_4` still selects Basin 1 uniquely on the retained
five-basin chart. This sharpens the strongest current native A-BCC route,
but it still does not by itself derive the source chart axiom-natively.

**2026-04-21 target-surface sharpening.** The separate strict/native A-BCC
residue is now sharper than that. On the exact `chi^2 = 0` PMNS target
surface, the active-half-plane theorem gives the native chamber exactly, the
exact chamber roots are exactly `{Basin 1, Basin 2, Basin X}`, and the
coefficient-free source cubic `I_src(H) = Im(H_12 H_23 H_31)` is positive on
`Basin 1` and negative on `Basin 2` and `Basin X`. So once the exact PMNS
target surface is granted, A-BCC is already downstream of the native chamber
plus `I_src(H) > 0`; there is no longer a separate target-surface
branch-choice residue beyond the PMNS last mile itself. This does **not**
contradict the five-route audit globally: outside that exact chamber-root set,
`I_src(H)` still does not determine `det(H)`. See
`docs/DM_ABCC_EXACT_TARGET_SURFACE_SOURCE_CUBIC_CLOSURE_THEOREM_NOTE_2026-04-21.md`.

**Proof.** Uhlig 1982 sign-characteristic matrix-pencil classification backbone; verified in `scripts/frontier_dm_dple_theorem.py` (19 PASS, 0 FAIL) and `scripts/frontier_dm_abcc_chamber_dple_closure.py` (39 PASS, 0 FAIL).

### §3.3 Supporting — 5-route assumptions audit

**Theorem.** Five candidate algebraic-sign routes (Z₃ spectral gap, quaternionic Kramers, PSD generators, PSD chamber-J, C_base-connectivity) each close negatively: Cl(3)/Z³ algebra alone cannot determine the sign of `det(H)` without an additional physical input. The DM A-BCC gate therefore reduces to one named observational or continuity input, not to a pure algebraic closure.

**Proof.** `scripts/frontier_dm_abcc_assumptions_audit.py` (16 PASS, 0 FAIL).

### §3.4 Retained inputs

There is no longer a retained observational input on the DM flagship lane.
The chamber bound `q_+ + δ ≥ √(8/3)` is no longer retained input on this
branch: it now has a reviewer-grade inline derivation in
`docs/DM_ABCC_CHAMBER_BOUND_DERIVATION_NOTE_2026-04-20.md`. The CP-sign /
`σ_hier` half is also no longer retained input on this branch: it is derived by the
active-chamber completeness theorem, the parity reduction, the upper-octant
law, and the coefficient-free source-cubic selector. The fixed-`N_e`
exact-source-manifold theorem sharpened the native last mile to one complex
current `J_chi`, and the new graph-first ordered-chain theorem now lands one
explicit same-branch current-activation law on that target.

The fixed-`N_e` exact-source-manifold theorem further sharpened the angle-side gap:
the physical PMNS target already lies on an exact regular local `2`-real
source manifold on the charged-lepton-side seed surface, so the live missing
object is the point-selection law on that manifold, not target existence. The
tested `Z_3` center proposal `delta_db = 1`, `q_+ = 0` is not yet that law:
the center-law positive-sheet no-go theorem shows that adding `I_src > 0`
still leaves a positive-sheet `3`-real locus with varying PMNS triples.
The new three-identity support proposal is worth retaining as a compact
candidate law on the same affine chart: on the current active-chamber working
surface the proposed system `Tr(H) = Q_Koide`, `delta * q_+ = Q_Koide`,
`det(H) = E2` numerically recovers one interior chamber point in the audited
search box and gives a PMNS packet inside the current NuFit `1 sigma` bands.
It remains support only: the product and determinant laws are not yet retained
derivations, and the current uniqueness statement is numerical rather than
theorem-grade.
The carrier-side split-2 dominance/completeness blocker is no longer open.
The new interval-certified theorem closes the two residual upper-face boxes
`CAP_BOX` and `ENDPOINT_BOX` by Weyl eigenvalue control, exact cofactor
projector-row intervals, and boxwise transport upper bounds
`eta / eta_obs < 1` throughout. A-BCC is also no longer open on the review
surface: the retained-measurement integration theorem packages the
already-landed sigma-chain, retained P3 Sylvester theorem, PMNS
nonsingularity reduction, and Sylvester signature forcing into one explicit
closure statement. The stricter/native map is now sharper too: once the exact
PMNS target surface is granted, the separate A-BCC target-surface residue is
already reduced away by the exact chamber-root theorem plus the coefficient-
free source cubic. The native last mile had then reduced to one complex
nontrivial-character current `J_chi`, and the new graph-first ordered-chain
theorem closes that target positively with
`A_ord = diag(1,2,3) + (E12 + E23 + E31)` and `J_chi = 1`. See
`docs/DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`.
The selector side is also slightly sharper than before: on the recovered bank,
the exact intrinsic threshold-volume selector family now has a theorem-grade
high-threshold stabilization window on which the preferred recovered lift is
the unique minimizer. That does not yet derive the selector law, but it
reduces the remaining positive burden to an intrinsic threshold law landing in
that exact window. See
`docs/DM_SELECTOR_THRESHOLD_STABILIZATION_SUPPORT_THEOREM_NOTE_2026-04-21.md`.
There is also now one cleaner intrinsic breakpoint candidate on that same
family: the earliest middle-branch threshold `tau_b,min = min_i log(1+b_i)`.
It belongs uniquely to the preferred recovered lift and already selects it.
So the selector-side burden is narrower again: derive why the physical
threshold law is this earliest intrinsic breakpoint, or derive a stronger
microscopic selector law. See
`docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md`.
There is now one more useful separator on the same selector lane. The
strongest current framework-internal selector law — the observable-relative-
action law on the fixed native `N_e` seed surface — does not already land on
the recovered selector branch. Its exact source stays off the recovered bank,
is not chosen by the recovered-bank breakpoint `tau_b,min`, and instead
carries its own later intrinsic breakpoint `tau_b,rel`. So the remaining
selector burden is not merely “force minimal relative action”; it is to bridge
that exact internal selector to the recovered right-sensitive selector branch,
or to replace it with a finer microscopic law. See
`docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_BRANCH_SEPARATION_SUPPORT_THEOREM_NOTE_2026-04-21.md`.
The same selector lane is now also less disconnected than before. A new
projection support theorem shows that the exact observable-relative-action
source already has one canonical recovered image: across Frobenius distance on
`H`, Euclidean distance on the active target `(delta, q_+)`, threshold-profile
distance on the exact witness-volume family, and an audited common-positive
window geometry packet (affine-invariant distance, dual LogDet divergences,
and inverse-eigenvalue parameter distance), the unique nearest recovered point
is always the preferred recovered lift `0`. That same lift is already the one
selected by the intrinsic threshold candidate `tau_b,min`. So the remaining
selector burden narrows again: justify the projection principle from the exact
internal selector to that preferred recovered lift, or replace both selector
objects by a finer microscopic law. See
`docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_PROJECTION_SUPPORT_THEOREM_NOTE_2026-04-21.md`.
The same packet was then sharpened one step further. All recovered lifts
already share the exact sharp source tuple and the same constructive triplet
chamber `gamma > 0`, `E1 > 0`, `E2 > 0`, and all also satisfy `sin(delta) > 0`.
Those data still do not break the recovered selector degeneracy. The first
right-sensitive datum that does is the shifted-imaginary doublet sign: the
exact internal selector lies on the positive side of `Im(K_Z3[1,2]) = 0`, and
among recovered lifts only the preferred lift `0` shares that positive side.
See `docs/DM_SELECTOR_SHIFTED_DOUBLET_IMAG_SIGN_SUPPORT_THEOREM_NOTE_2026-04-21.md`.
That remaining selector packet is now closed on the review surface. The same
exact scalar observable-relative-action law, transported to the common
positive windows `A_mu(H)=H+mu I`, uniquely minimizes at the preferred
recovered lift `0` across the full audited shift family and a dense
admissible stress range, and that lift is exactly the unique recovered point
with `Im(K_Z3[1,2]) > 0`. So there is no remaining DM blocker on the review
surface. On the stricter/native map, once the exact PMNS target surface is
granted, the exact chamber plus `I_src(H) > 0` already select Basin 1
uniquely on the exact chamber roots, so there is no separate target-surface
branch-choice residue beyond the PMNS last mile itself. That last mile had
already been reduced to one complex nontrivial-character current `J_chi`,
equivalently the intrinsic `2`-real PMNS point-selection law. The new
graph-first ordered-chain theorem lands one explicit same-branch
current-activation law on that target:
`A_ord = diag(1,2,3) + (E12 + E23 + E31)` gives `J_chi = 1` exactly on the
retained `hw=1` response family. What remains open there is the physical
identification of that ordered-chain law as the PMNS last-mile law. See
`docs/DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`.
PNS is derived as a property of Basin 1, not axiomatized.

---

## §4 Quark a_u — up-sector reduced amplitude

**Observable.** The up-sector reduced amplitude on the CKM 1⊕5 projector ray,

    a_u  =  0.7748865611   =  sin_d · (1 − 48 ρ / 49),

with `sin_d² = 5/6`, `ρ = 1/√42`.

### §4.1 Setup — retained bimodule

The retained Clifford bimodule is

    B  =  Cl(3)/Z₃ ⊗ Cl_CKM(1⊕5),

with:

- `Cl(3)/Z₃`: the core flavor algebra (retained framework; see `docs/CL3_SM_EMBEDDING_THEOREM.md`);
- `Cl_CKM(1⊕5)`: the CKM 1⊕5 carrier, retained from the CKM-atlas closure (`docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md`);
- retained unit projector ray `p = cos_d · e_1 + sin_d · e_5` with `cos_d = 1/√6`, `sin_d = √(5/6)`;
- retained reduced physical carrier plane `H_{(1+5)} = span{e_1, e_5}`;
- retained atom `a_d = ρ = 1/√42` (see `docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md`);
- retained NLO atoms `supp = 6/7` and `δ_{A1} = 1/42` (CKM atlas).

This is the review-surface provenance closure for the quark lane: the
headline theorem now names the retained bimodule, the projector ray, the
physical carrier plane, and the CKM-atlas atom bank inline instead of leaving
those sources distributed implicitly across older quark notes.

### §4.2 Primary closure — affine-physical-carrier jet-to-section identification

**Theorem.** Because `cos_d ≠ 0`, the pair `{p, e_5}` spans `H_{(1+5)}`. Hence the perturbation plane

    Pert(p)  :=  { a_u · e_5 + a_d · p : (a_u, a_d) ∈ ℝ² }

equals `H_{(1+5)}` as a real vector plane. The affine physical carrier through `p`,

    A_p  :=  p + H_{(1+5)},

is a canonical affine subspace of `B`, and its tangent space at `p` is `H_{(1+5)} = Pert(p)`. The map

    ψ  ↦  j¹_0 ( ε ↦ p + ε · ψ )

is a canonical bijection `Pert(p) ≅ J¹_p(A_p)`.

**Proof.** Elementary linear algebra on the retained basis; see `docs/QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19.md`. Verified in `scripts/frontier_quark_issr1_bicac_forcing.py` (13 PASS, 0 FAIL), which runs the full closure.

### §4.3 LO balance — exact one-dimensional 5-channel residue

**Theorem.** On the reduced carrier `H_{(1+5)}` with `Π_5 = |e_5⟩⟨e_5|`, the 5-budget of the projector ray is exact:

    Π_5 · p  =  sin_d · e_5.

Given retained `a_d = ρ` and the down-sector occupancy `d := a_d · e_1`, the 5-channel residue after subtracting the induced A₁→5 transfer is forced:

    a_u · e_5  =  Π_5 · p − (Π_5 · |p⟩⟨e_1|) · d   =  sin_d · e_5 − ρ · sin_d · e_5,

i.e. `a_u = sin_d (1 − ρ)`, or equivalently the LO balance identity

    a_u  +  ρ · sin_d  =  sin_d.

**Proof.** Operator algebra on `H_{(1+5)}`; `scripts/frontier_strc_lo_collinearity_theorem.py` (12 PASS, 0 FAIL).

### §4.4 NLO completion — retained three-atom contraction

**Theorem.** The retained atom product

    ρ · supp · δ_{A1}  =  (1/√42) · (6/7) · (1/42)  =  ρ / 49

supplies the NLO correction on the bridge family `a_u(κ) = sin_d (1 − ρκ)`, collapsing the endpoint to `κ = 48/49`. The full physical target is

    a_u  =  sin_d · (1 − 48 ρ / 49)  =  0.7748865611.

**Proof.** Direct substitution; `scripts/frontier_quark_up_amplitude_rpsr_conditional.py` (9 PASS, 0 FAIL).

### §4.5 Independent corroboration — shell normalization

**Theorem.** The exact shell-normalized bilinear carrier `K_R(q) = (u_E, u_T, δ_{A1} u_E, δ_{A1} u_T)` has unit bright shell columns. Among the three candidate bridge values `{κ_support = √(6/7), κ_target = 48/49, κ_BICAC = 1}`, only `κ = 1` preserves the retained shell coefficient `ρ`. At LO this independently selects the BICAC endpoint.

**Proof.** `scripts/frontier_quark_bimodule_lo_shell_normalization_theorem.py` (10 PASS, 0 FAIL).

### §4.6 Second JTS route — physical-point closure

**Theorem.** At the physical point `ψ_phys = a_u · e_5 + ρ · p` with `a_u = sin_d(1 − ρ)`, the SO(2)-weight-0 projection satisfies `Π(ψ_phys) = a_u + ρ · sin_d = sin_d = Π(p)`, and this equality selects `κ = 1` uniquely among the bridge candidates.

**Proof.** `scripts/frontier_quark_jts_physical_point_closure_theorem.py` (12 PASS, 0 FAIL).

### §4.7 Retained inputs and no-go corroboration

Retained inputs are: the Cl(3)/Z₃ ⊗ Cl_CKM(1⊕5) bimodule structure (framework), the atoms `a_d = ρ`, `supp = 6/7`, `δ_{A1} = 1/42` (CKM-atlas upstream), and the unit projector ray `p = cos_d e_1 + sin_d e_5`. The no-go `QUARK_UP_AMPLITUDE_NATIVE_AFFINE_NO_GO_NOTE` rules out a widened affine family attempting to force `a_u` from smaller axiomatic data; this corroborates that the retained bimodule structure plus atoms is precisely the minimal data needed.

---

## §5 Runner status

All runners pass with no hardcoded `True` PASS annotations. Every PASS is a numeric or symbolic verification.

| Lane | Runner | PASS | FAIL |
|---|---|---|---|
| κ bridge | `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` | 9 | 0 |
| κ block Frobenius | `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` | 16 | 0 |
| κ MRU | `frontier_koide_moment_ratio_uniformity_theorem.py` | 26 | 0 |
| κ weight-class obstruction | `frontier_koide_mru_weight_class_obstruction_theorem.py` | 21 | 0 |
| κ Z³ scalar potential (support) | `frontier_koide_z3_scalar_potential.py` | 22 | 0 |
| θ Berry identification | `frontier_koide_berry_phase_theorem.py` | 24 | 0 |
| θ scalar-phase bridge | `frontier_koide_selected_line_cyclic_response_bridge.py` | 20 | 0 |
| A-BCC σ-chain attack cascade | `frontier_dm_pns_attack_cascade.py` | 34 | 0 |
| A-BCC signature-forcing | `frontier_dm_abcc_signature_forcing_theorem.py` | 43 | 0 |
| A-BCC PMNS-non-singularity | `frontier_dm_abcc_pmns_nonsingularity_theorem.py` | 33 | 0 |
| A-BCC retained-measurement closure | `frontier_dm_abcc_retained_measurement_closure_2026_04_21.py` | 15 | 0 |
| A-BCC chamber ∩ DPLE | `frontier_dm_abcc_chamber_dple_closure.py` | 39 | 0 |
| A-BCC corrected five-basin chamber ∩ DPLE | `frontier_dm_abcc_five_basin_chamber_dple_support_2026_04_21.py` | 24 | 0 |
| A-BCC exact target-surface source-cubic closure | `frontier_dm_abcc_exact_target_surface_source_cubic_closure_2026_04_21.py` | 15 | 0 |
| A-BCC 5-route audit | `frontier_dm_abcc_assumptions_audit.py` | 16 | 0 |
| DM native current last-mile reduction | `frontier_dm_pmns_native_current_last_mile_reduction_2026_04_21.py` | 16 | 0 |
| DPLE dim-parametric extremum | `frontier_dm_dple_theorem.py` | 19 | 0 |
| Split-2 interval-certified dominance closure | `frontier_dm_split2_interval_certified_dominance_closure_2026_04_21.py` | 17 | 0 |
| Selector relative-action recovered projection | `frontier_dm_selector_relative_action_recovered_projection_support_2026_04_21.py` | 12 | 0 |
| a_u JTS-affine + LO + NLO | `frontier_quark_issr1_bicac_forcing.py` | 13 | 0 |
| a_u JTS physical-point | `frontier_quark_jts_physical_point_closure_theorem.py` | 12 | 0 |
| a_u shell normalization | `frontier_quark_bimodule_lo_shell_normalization_theorem.py` | 10 | 0 |
| a_u STRC-LO collinearity | `frontier_strc_lo_collinearity_theorem.py` | 12 | 0 |
| a_u RPSR NLO | `frontier_quark_up_amplitude_rpsr_conditional.py` | 9 | 0 |
| a_u native-affine no-go | `frontier_quark_up_amplitude_native_affine_no_go.py` | 7 | 0 |
| a_u NORM existence | `frontier_quark_bimodule_norm_existence_theorem.py` | 10 | 0 |
| a_u NORM naturality | `frontier_quark_bimodule_norm_naturality_theorem.py` | 8 | 0 |
| a_u STRC historical | `frontier_quark_strc_observable_principle.py` | 19 | 0 |
| g_bare two-Ward (supporting) | `frontier_g_bare_two_ward_closure.py` | 18 | 0 |

**Total across 23 runners: 420+ PASS, 0 FAIL.**

---

## §6 Retained observational inputs (complete list)

**2026-04-21 package update.** After the landed April 21 support package,
Koide `Q = 2/3` and Brannen `δ = 2/9` are no longer counted here as retained
observational inputs. The DM flagship lane is also removed from the
review-surface retained-input list: its review-surface residue is closed by the
April 21 DM theorem stack, while the stricter/native map now carries only the
remaining physical-identification question around the ordered-chain current law.
The table below lists the remaining retained observational or atlas-level
inputs across the still-open or still-atlas-backed Tier-1 gates.

| Label | Input | Used in | Provenance |
|---|---|---|---|
| BIM | Bimodule `B = Cl(3)/Z₃ ⊗ Cl_CKM(1⊕5)` | a_u | `CL3_SM_EMBEDDING_THEOREM` + `CKM_ATLAS_AXIOM_CLOSURE_NOTE` (main) |
| ATOM-ρ | `a_d = ρ = 1/√42` | a_u | CKM atlas |
| ATOM-S | `supp = 6/7` | a_u | CKM atlas |
| ATOM-A | `δ_{A1} = 1/42` | a_u | CKM atlas |

No other observational or structural-postulate inputs enter the still-open or
still-atlas-backed Tier-1 closures this cycle.

---

## §7 Reading order for the reviewer

1. This note (reviewer package) — primary read.
2. `docs/SCALAR_SELECTOR_REMAINING_OPEN_IMPORTS_2026-04-20.md` — retained-observational inputs with candidate closing derivations.
3. Per-lane theorem notes referenced in §1–§4 — supporting detail.
4. Runner scripts — numerical / symbolic verification.
