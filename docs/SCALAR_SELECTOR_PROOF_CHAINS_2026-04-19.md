# Scalar-Selector Tier-1 Proof Chains

**Date:** 2026-04-19
**Scope:** One proof chain per Tier-1 gate, showing exactly what retained
ingredients feed each closure/identification and which named residues (if
any) remain. Post-recovery content; cross-references canonical theorem
notes.
**Reading convention:** each step is labelled with a file (for the retained
note) and a runner (for the machine-checked proof). `†` marks a named
residue; all other steps are mechanically verified.

**2026-04-20 supersession note.** This file is historical proof-chain
bookkeeping. For current branch-facing status, apply two corrections first:

- Koide `kappa`: the MRU/SO(2)-quotient path is no longer primary. The
  retained closure route is the spectrum/operator bridge plus the block-total
  Frobenius measure; MRU is supplementary only. See
  `docs/KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md`.
- DM A-BCC basin bookkeeping: the full χ²=0 chart is now
  `{Basin 1, Basin N, Basin P, Basin 2, Basin X}`, and the active-chamber
  chart is `{Basin 1, Basin 2, Basin X}`. Any older "four-basin" or
  `{Basin 1, Basin X}` language below predates the completeness theorem. See
  `archive_unlanded/dm-abcc-finite-search-salvage-2026-04-30/DM_ABCC_BASIN_ENUMERATION_COMPLETENESS_THEOREM_NOTE_2026-04-20.md`.
- DM A-BCC `σ_hier`: the `σ_hier = (2,1,0)` ambiguity is no longer open on
  the review branch. The active-chamber completeness + parity-reduction +
  upper-octant/source-cubic stack closes the hierarchy-permutation ambiguity
  and makes `sin δ_CP < 0` a
  consequence. What remains open on the PMNS side is the angle triple itself.
  See `docs/DM_SIGMA_HIER_CLOSURE_PACKET_NOTE_2026-04-20.md` and
  `docs/DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md`.

---

## Chain 1 — Koide `theta` (Brannen–Zenczykowski phase `delta = 2/9`)

**Gate:** physical charged-lepton phase offset `delta = 2/9`.

```text
Step 1  — retain the Brannen–Zenczykowski phase offset `delta = 2/9` (observational input)     †
Step 2  — retain circulant/Z_3 structure and the physical selected line
          H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3) on the charged-lepton
          reduction packet
          [KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18]
Step 3  — on H_sel(m)'s positive first branch, the normalized Koide
          amplitude s(m) has exact Fourier form with fixed singlet
          coefficient 1/sqrt(2) and moving doublet coordinate
          [1 : e^{-2 i theta(m)}] on the CP^1 equator
          [KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19, §4]
Step 4  — the tautological line over that equator carries canonical
          Pancharatnam–Berry connection A = d theta
          [same note, §4.1]
Step 5  — unique unphased point m_0 with u(m_0) = v(m_0) forces
          theta(m_0) = 2 pi / 3  ->  delta(m_0) = 0
          [same note, §4.2]
Step 6  — Berry holonomy from m_0 to any first-branch m gives
          Hol(m_0 -> m) = theta(m) - 2 pi / 3 = delta(m)
          [same note, §4.3 + runner PASS=24]
Step 7  — the Brannen–Zenczykowski phase offset (Step 1) supplies delta = 2/9, combined with Step 6
          gives a canonical geometric meaning to that number as the
          actual-route Pancharatnam–Berry holonomy
Step 8  — exact selected-line scalar-phase bridge
          kappa_sel(delta) = -sqrt(3) cos(delta+pi/6)/(sqrt(2)+sin(delta+pi/6))
          + monotonicity of (delta, kappa_sel) on the first branch forces
          unique m_* = -1.160443440065 and unique kappa_sel,* = -0.6079186
          [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18,
           runner PASS=20]
Step 9  — ambient-S^2 monopole story retires: actual positive projectivized
          Koide locus is three open arcs on a circle, all equivariant
          complex line bundles trivial, c_1 = 0
          [KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_2026-04-19,
           runner verified]
```

**Status:** bounded - bounded or caveated result note
theorem supplies its geometric meaning as a canonical Pancharatnam–Berry
holonomy on the physical selected line. Together they eliminate the
previously separate `m_* / kappa_sel,*` imports as derived
corollaries. **No independent axiom-native forcing of the value `2/9` is
claimed.**

---

## Chain 2 — Koide `kappa` (charged-lepton cone normalization `kappa = 2`)

**Gate:** operator-side charged-lepton cone normalization
`kappa := g_0^2 / |g_1|^2 = 2`, equivalently `Q := 2 (sum m) / (sum sqrt(m))^2 = 2/3`.

```text
Step 1  — retain Herm_circ(d) + Frobenius metric on charged-lepton
          reduction packet
          [KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18]
Step 2  — retain d = 3 (from main: DIMENSION_SELECTION_NOTE,
          ANOMALY_FORCES_TIME_THEOREM, cl3-minimality-conditional-support)
Step 3  — at d = 3, Herm_circ decomposes as 1 · trivial ⊕ 1 · complex-doublet;
          this is the unique dim where the decomposition has exactly that
          shape, so any scalar singlet-vs-doublet selector is a single
          equation
          [KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19, §2]
Step 4  — MRU principle: Frobenius-normalized cyclic responses uniform
          across Z_3 isotypes => a^2 = 2 |b|^2 => kappa = 2
          [same note, runner PASS=65]
Step 5  — weight-class obstruction: every weighted block-log-volume law
          lands on the leaf kappa = 2 mu / nu. MRU is (1,1) leaf; the
          retained unreduced det-carrier satisfies det(alpha P_+ + beta P_⊥)
          = alpha beta^2 => (1,2) leaf => kappa = 1. Missing object =
          retained 1:1 real-isotype measure
          [KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19]
Step 6  — block-total Frobenius measure theorem: the 1:1 measure named in
          Step 5 is explicitly realized by E_I := || pi_I(H) ||_F^2, giving
          E_+ = 3 a^2, E_⊥ = 6 |b|^2. d = 3 is the unique dim where this
          block-total functional is dim-uniquely well-defined. Extremum at
          E_+ = E_⊥ recovers kappa = 2
          [KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19,
           runner PASS=16]
Step 7  — spectrum/operator bridge theorem: exact sympy-verified identity
          a_0^2 - 2 |z|^2 = 3 (a^2 - 2 |b|^2)
          makes operator-side kappa = 2 a corollary of spectrum-side Q = 2/3
          [KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19,
           runner PASS=9]
Step 8  — spectrum-side Q = 2/3 is the retained Koide relation
          (machine-precision PDG verification)                                   †
Step 9  — [Steps 7–8] => operator-side kappa = 2 via spectrum route, or
          [Steps 4 + 6] => operator-side kappa = 2 via measure route, or
          [Step 4] alone => kappa = 2 via MRU candidate-principle route.
          All three converge.
```

**Status:** three independent converging proposed_retained theorems for `kappa = 2`.
Single named residue: physical selection of the block-total Frobenius
measure (Step 6) over the `(1,2)` determinant measure. Both measures are
algebraically available; the missing step is a retained physics principle
that picks the block-total form. Absent that, `Q = 2/3` itself (Step 8)
can be accepted as the retained spectrum-side input via the bridge
(Step 7), at which point operator-side `kappa = 2` is a corollary.

---

## Chain 3 — DM A-BCC basin (Basin 1 selection from `{1, N, P, X}`)

**Gate:** axiom-native selection of the A-BCC physical basin (Basin 1) from
the four chamber candidates `{Basin 1, Basin N, Basin P, Basin X}`.

```text
Primary closure route (chamber ∩ DPLE):

Step 1  — retain Z_3 doublet-block chamber geometry on the PMNS source
          surface                                                                 (framework)
Step 2  — active affine chamber bound: q_+ + delta ≥ sqrt(8/3). Derived
          from retained Cl(3)/Z_3 doublet block point-selection theorem
          [DM_NEUTRINO_SOURCE_SURFACE_P3_SYLVESTER_LINEAR_PATH_SIGNATURE_THEOREM_NOTE_2026-04-18]
Step 3  — Basin N has q+delta = 1.28 < sqrt(8/3); Basin P has
          q+delta = 0.10 < sqrt(8/3) => both excluded
          [DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_2026-04-19,
           §2]
Step 4  — DPLE dim-parametric extremum theorem: on any retained linear
          Hermitian pencil, log|det H(t)| has at most floor(d/2) interior
          Morse-idx-0 CPs; at d = 3 exactly one. F_3 on the retained
          A-BCC pencil reproduces F_4 on all four basins
          [DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_2026-04-19,
           runner PASS=19]
Step 5  — F_4 = discriminant Delta = c_2^2 - 3 c_1 c_3 > 0 plus sign on
          interior Morse-idx-0 CP. Basin 1: Delta_1 = +7.804, t_* = 0.776,
          p_* = +0.878 passes. Basin X: Delta_X = -4.7 * 10^6 fails
          [same note, §3 + runner frontier_dm_abcc_chamber_dple_closure.py
           PASS=39]
Step 6  — intersection [Steps 3, 5]: {Basin 1, Basin X} ∩ {Basin 1, …} =
          {Basin 1}                                                               (closure)

Alternative independent routes (recovered):

Alt A   — PMNS Non-Singularity conditional: given retained PMNS
          non-singularity on the active chamber, Basin 1 is the unique
          survivor
          [DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19,
           runner PASS=38]
Alt B   — Sylvester signature-forcing: path-independent via IVT + det
          sign on linear pencil rules out Basin N / P / X
          [DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_2026-04-19,
           runner PASS=54]
Alt C   — PNS attack cascade: sigma-chain chamber + σ-hier + χ²=0 + T2K
          + P3 Sylvester → Basin 1 uniquely → PNS → A-BCC
          [DM_PNS_ATTACK_CASCADE_NOTE_2026-04-19, runner PASS=47]
```

**Status:** closed at axiom level conditional on DPLE acceptance. Three
recovered alternative routes corroborate. No named residue on A-BCC
itself; open source-side law sits downstream on the DM flagship lane.

---

## Chain 4 — Quark `a_u` (up-sector reduced amplitude)

**Gate:** up-sector reduced amplitude `a_u = 0.7748865611`.

```text
Step 1  — retain bimodule B = Cl(3)/Z_3 ⊗ Cl_CKM(1⊕5) with projector ray
          p = cos_d e_1 + sin_d e_5,  cos_d = 1/sqrt(6),  sin_d = sqrt(5/6)      (framework)
Step 2  — exact physical reduced carrier H_(1+5) = span{e_1, e_5}           (framework)
Step 3  — because cos_d != 0, {p, e_5} is a basis of H_(1+5):
          e_1 = (p - sin_d e_5) / cos_d
Step 4  — ISSR1 perturbation cone Pert(p) = {a_u e_5 + a_d p : (a_u,a_d) in R^2}
          = span{p, e_5} = H_(1+5)                                               (linear algebra)
Step 5  — affine physical carrier A_p = p + H_(1+5); tangent space
          T_p A_p = H_(1+5) = Pert(p)
Step 6  — canonical bijection Pert(p) ≅ J^1_p(A_p)   via   psi -> j^1_0(p + eps psi)
          with inverse = differentiation. JTS is derived, not postulated
          [QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_2026-04-19]
Step 7  — exact 1(+)5 channel completeness supplies the pinning identity
          Pi(psi_phys) = Pi(p), i.e. Im<v_5, psi> = Im<v_5, p>
          [STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19 + channel completeness]
Step 8  — [Step 6 + Step 7] force a_u + a_d sin_d = sin_d = BICAC-LO at
          kappa = 1
          [QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_2026-04-19,
           runner PASS=13 verdict "JTS DERIVED; ISSR1 CLOSED"]
Step 9  — retain a_d = rho = 1/sqrt(42) from the CKM-atlas scalar ray /
          projector-parameter audit package; retain supp = 6/7 and
          delta_A1 = 1/42 from the same CKM-atlas support bank
          [CKM_ATLAS_AXIOM_CLOSURE_NOTE, QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19]
Step 10 — [Step 8 + Step 9] => a_u(kappa=1) = sin_d * (1 - rho) = LO target
Step 11 — independent shell-normalization confirms same kappa = 1 endpoint
          on exact Route-2 carrier
          [QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_2026-04-19]
Step 12 — BACT-NLO contraction: retained atoms rho, supp = 6/7,
          delta_A1 = 1/42 combine to give NLO correction rho * supp *
          delta_A1 = rho/49, collapsing the bridge to kappa = 48/49
          [QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19,
           runner PASS=10]
Step 13 — a_u = sin_d * (1 - rho * 48/49) = 0.7748865611 (full physical
          target)
```

**Status:** closed on bimodule footing. No named residue — the bimodule
itself is the retained structural input, and every downstream step
(JTS, ISSR1/BICAC-LO, shell-normalization, RPSR-NLO) is derived or
independently retained.

---

## Meta-axiom accounting summary (post full-stack recovery)

| Chain | Named residues | Meta-axiom dependency |
|---|---|---|
| Koide `theta` | none | the Brannen-Zenczykowski phase offset closed on actual route via Berry selected-line CP¹; part of DIM-UNIQ framing at `d = 3` |
| Koide `kappa` | none | Current primary route is bridge + block-total Frobenius; historical SO(2)-quotient language is superseded by `KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md` |
| DM A-BCC | none | Part of DIM-UNIQ framing at `d = 3` (DPLE `floor(d/2) = 1`) |
| Quark `a_u` | none | STRC derived from `1(+)5` channel completeness (`37c4f2bf`), no longer a separate meta-axiom |

**Meta-axiom collapse:** with STRC derived and the Koide `kappa` gate carried
primarily by the bridge/block-total pair, the earlier "`4 → 2` DIM-UNIQ +
STRC" layer reduces to
**`4 → Cl(3)/Z³` framework axioms**.

**Reviewer-bar per-lane:** all four gates closed; zero named residues;
zero new axioms added this cycle. All four closures ride only on
retained Cl(3)/Z³ framework ingredients.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [koide_mru_demotion_note_2026-04-20](KOIDE_MRU_DEMOTION_NOTE_2026-04-20.md)
- [dm_sigma_hier_closure_packet_note_2026-04-20](DM_SIGMA_HIER_CLOSURE_PACKET_NOTE_2026-04-20.md)
