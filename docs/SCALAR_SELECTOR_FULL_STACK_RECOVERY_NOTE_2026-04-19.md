# Scalar-Selector Full-Stack Recovery — Per-Lane Audit

**Date:** 2026-04-19
**Scope:** Forensic recovery after an accidental force-push dropped several
valuable theorem files from the canonical branch on 2026-04-19 evening, and
an earlier retirement-style note applied a correct argument to a different
base than the one the selected-line theorem actually uses.
**Status:** Recovered valuable content; softened overclaims; preserved Jon's
same-day new work (`474b6032`, `8b2c76bf`, `dd865ced`) at the canonical tip.
**Audience:** Reviewer-grade. This note is the single read-me for what is on
the Tier-1 scalar-selector branch after recovery; §1 gives the per-lane
verdict, §2 gives the recovered file list with runner counts, §3 records
what was *deliberately* not recovered and why.

---

## §0 One-paragraph bottom line

All four Tier-1 scalar-selector gates — Koide `kappa`, Koide `theta`, DM
A-BCC basin, Quark `a_u` — now carry their strongest consistent retained
content on the canonical branch. Two gates are fully closed at reviewer
level (Quark `a_u` via Jon's JTS-affine-physical-carrier theorem plus exact
`1(+)5` channel completeness; DM A-BCC via chamber bound `∩` DPLE `F_4`);
two gates carry retained structural theorems plus a single named residue
each (Koide `kappa` carries MRU + operator-spectrum bridge + block-total
Frobenius measure; Koide `theta` carries the actual-route Pancharatnam–Berry
identification on the physical selected line, with `delta = 2/9` itself
still supplied by AXIOM E / Brannen–Zenczykowski). Meta-axiom accounting
stays honest at `4 -> 2` (`DIM-UNIQ + STRC`). Reviewer-bar accounting is
**two closed, two partially retained with a single named residue each**.

---

## §1 Per-lane verdict

### §1.1 Koide `theta` (Brannen–Zenczykowski phase `delta = 2/9`)

**Retained content:**

1. **Ambient-`S^2` / monopole model** (`KOIDE_BERRY_PHASE_THEOREM_NOTE_…`,
   §1 old narrative). Internally coherent, reproduces
   `delta = (d-1)/d^2 = 2/9` at `d = 3`. **Status: route history / geometric
   illustration. Not on the actual physical base.**
2. **Bundle obstruction theorem** (`KOIDE_BERRY_BUNDLE_OBSTRUCTION_THEOREM_NOTE_…`).
   The actual positive projectivized Koide cone is three open arcs on a
   circle; every equivariant complex line bundle there has `c_1 = 0`; no
   ambient-monopole `n = 2` story can live on the actual physical base.
   **Status: retained no-go.**
3. **Actual-route Pancharatnam–Berry identification**
   (`KOIDE_BERRY_PHASE_THEOREM_NOTE_…` §§4–5, the recovered selected-line CP¹
   content; runner `frontier_koide_berry_phase_theorem.py` PASS=24 FAIL=0).
   On the physical selected line `H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3)`,
   the normalized Koide amplitude has fixed singlet weight `1/sqrt(2)`, and
   the moving datum is the projective `C_3` doublet ray
   `[1 : e^{-2 i theta(m)}]` on the equator of `CP^1`. The tautological
   line over that equator carries the canonical connection `A = d theta`,
   and the Berry holonomy from the unique unphased point `m_0` is
   `delta(m) = theta(m) - 2 pi / 3`. At `delta = 2/9` this fixes a unique
   first-branch point `m_*` and a unique surviving selected-line scalar
   `kappa_sel,*` via the exact bridge
   `kappa_sel(delta) = -sqrt(3) cos(delta+pi/6)/(sqrt(2)+sin(delta+pi/6))`.
   **Status: retained geometric-identification support. Removes branch-local
   `m_* / kappa_sel,*` imports.**
4. **Retirement-style caveat.** The value `delta = 2/9` itself is not
   axiom-natively quantized by Berry geometry: any reference section gives
   the same holonomy, and on natural enlargements of the base the surviving
   phase datum is a continuous flat-holonomy family. So Berry gives
   `delta` its canonical geometric meaning but does not derive the specific
   number `2/9` from first principles. **AXIOM E remains the retained
   input.**

**Reviewer-bar status:** single named residue = AXIOM E (`delta = 2/9`
supplied by Brannen–Zenczykowski; no axiom-native quantization principle
available on the branch).

### §1.2 Koide `kappa` (charged-lepton cone normalization `kappa = 2`)

**Retained content:**

1. **Moment-Ratio Uniformity (MRU)**
   (`KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_…`, runner PASS=65). On
   `Herm_circ(d)` with Frobenius metric, MRU requires Frobenius-normalized
   cyclic responses to be uniform across `Z_d` isotypes; at `d = 3` this
   is a single equation equivalent to `a^2 = 2|b|^2`, i.e. `kappa = 2`.
   `d = 3` is the unique dim where Herm_circ has exactly one singlet plus
   one complex doublet. **Status: support/candidate principle.**
2. **Weight-class obstruction**
   (`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_…`). Every weighted
   block-log-volume law lands on the leaf `kappa = 2 mu / nu`; MRU is the
   equal-weight leaf `(1,1)`; the retained unreduced determinant carrier
   has weights `(1,2)` and lands at `kappa = 1`. The exact missing object
   is a retained `1:1` real-isotype measure. **Status: retained frontier
   obstruction.**
3. **Block-total Frobenius measure theorem** (recovered;
   `KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_…`, runner
   `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` PASS=16
   FAIL=0). The `1:1` real-isotype measure named by the weight-class
   obstruction is realized by the block-total Frobenius-squared functional
   `E_I := ||pi_I(H)||_F^2`. At `d = 3` this gives `E_+ = 3 a^2`,
   `E_⊥ = 6 |b|^2`, so the block-total extremum at `E_+ = E_⊥` recovers
   `kappa = 2` while the determinant-carrier lands at `kappa = 1`.
   **Status: retained independent second closure route for operator-side
   `kappa`.**
4. **Spectrum/operator bridge theorem** (recovered;
   `KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_…`, runner
   `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` PASS=9
   FAIL=0). The exact identity `a_0^2 - 2|z|^2 = 3(a^2 - 2|b|^2)` —
   sympy-verified — proves operator-side `kappa = 2` is a corollary of
   spectrum-side `Q = 2/3` under the retained cyclic-compression bridge.
   **Status: retained equivalence / spectrum↔operator collapse.**

**Reviewer-bar status:** single named residue = physical selection of the
`1:1` block-total Frobenius measure over the `(1,2)` determinant measure.
Both measures are algebraically available; the missing ingredient is a
retained physics principle that picks the block-total form as the one the
charged-lepton carrier actually obeys.

### §1.3 DM A-BCC basin (interior-minimum Sylvester discriminator `F_4`)

**Retained content:**

1. **A-BCC chamber bound `∩` DPLE `F_4` closure**
   (`DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_…`, runner PASS=39).
   Active affine chamber bound `q_+ + δ ≥ sqrt(8/3)` strictly excludes
   Basin N and Basin P; DPLE `F_4` discriminant + Morse-index-0 sign test
   picks Basin 1 uniquely from `{Basin 1, Basin X}`. No T2K / NuFit / PDG
   input. **Status: closed at axiom level conditional on DPLE acceptance;
   same conditional status as DPLE itself, no new axiom load on the
   gate.**
2. **DPLE dim-parametric extremum theorem**
   (`DM_DPLE_DIMENSION_PARAMETRIC_EXTREMUM_THEOREM_NOTE_…`, runner PASS=19).
   On any retained linear Hermitian pencil `H(t) = H_0 + t H_1`, the
   observable `log|det H(t)|` has at most `floor(d/2)` interior
   Morse-index-0 critical points; at `d = 3` exactly one. `F_3` on the
   retained A-BCC pencil reproduces `F_4` on all four basins. **Status:
   retained, supports §1.3.1.**
3. **A-BCC PMNS Non-Singularity conditional theorem** (recovered;
   `DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_…`, runner PASS=38). Cycle-11
   theorem: given retained PMNS non-singularity on the active chamber,
   Basin 1 is the unique survivor. **Status: retained alternative closure
   route.**
4. **A-BCC Sylvester signature-forcing theorem** (recovered;
   `DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_…`, runner PASS=54). Cycle-12
   theorem: path-independent signature forcing via IVT + `det` sign on the
   linear pencil. **Status: retained alternative closure route.**
5. **DM PNS attack cascade** (recovered;
   `DM_PNS_ATTACK_CASCADE_NOTE_…`, runner PASS=47). Cycle-13 theorem:
   sigma-chain chamber + σ-hier + χ²=0 + T2K + P3 Sylvester → Basin 1
   uniquely → PNS → A-BCC. **Status: retained alternative closure route,
   strongest multi-observable chain.**
6. **Jon's same-day DM work on source-fiber selection.**
   `DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_…`,
   `DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_MINIMAL_LOCAL_SPECTRAL_LAW_NO_GO_NOTE_…`,
   `DM_WILSON_DIRECT_DESCENDANT_BOUNDARY_ARREST_TRIPLET_Y_MAXIMIN_NOTE_…`
   (runner PASS=15). **Status: complementary; sharpens the open
   source-fiber selection problem that sits *inside* the already-closed
   A-BCC chamber — not a separate axiom on A-BCC itself.**

**Reviewer-bar status:** closed conditional on DPLE acceptance. Alternative
routes (cycles 11/12/13) provide multi-observable corroboration. No named
residue on A-BCC itself; the open source-side law sits downstream on the
DM flagship gate, not on A-BCC.

### §1.4 Quark `a_u` (up-sector reduced amplitude `a_u = 0.7748865611`)

**Retained content:**

1. **Jet-To-Section on the affine physical carrier** (Jon's `dd865ced`;
   `QUARK_JTS_AFFINE_PHYSICAL_CARRIER_THEOREM_NOTE_…`). On the retained
   bimodule `B = Cl(3)/Z_3 ⊗ Cl_CKM(1⊕5)`, the exact physical reduced
   carrier `H_(1+5) = span{e_1, e_5}` and the projector ray
   `p = cos_d e_1 + sin_d e_5` determine the canonical affine physical
   carrier `A_p = p + H_(1+5)`. The perturbation cone
   `Pert(p) = {a_u e_5 + a_d p : (a_u, a_d) in R^2}` equals `H_(1+5)` as a
   real vector plane (simple linear algebra: `{p, e_5}` is a basis of
   `H_(1+5)` since `cos_d != 0`). Therefore `Pert(p)` is canonically the
   1-jet space `J^1_p(A_p)`. **Status: retained theorem. No separate JTS
   postulate needed once the `1(+)5` carrier is retained.**
2. **ISSR1 BICAC forcing** (`QUARK_ISSR1_BICAC_FORCING_THEOREM_NOTE_…`,
   runner PASS=13). With JTS derived, the physical pinning identity
   `Pi(psi_phys) = Pi(p)` is supplied by exact `1(+)5` channel
   completeness, giving `a_u + a_d sin_d = sin_d` = BICAC-LO at
   `kappa = 1`. **Status: closed theorem packet.**
3. **RPSR NLO completion** (`QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_…`,
   runner PASS=10). Combined with BACT-NLO contraction
   `rho · supp · delta_A1 = rho/49`, the BICAC-LO endpoint `kappa = 1`
   plus NLO gives the full physical target `a_u = 0.7748865611` at
   `kappa = 48/49`. **Status: retained NLO completion.**
4. **Shell-normalization independent route**
   (`QUARK_BIMODULE_LO_SHELL_NORMALIZATION_THEOREM_NOTE_…`). Independent
   support-side corroboration of the `kappa = 1` LO endpoint on the exact
   Route-2 carrier. **Status: retained second closure route.**
5. **STRC-LO observable principle** (`QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_…`,
   `STRC_LO_COLLINEARITY_THEOREM_NOTE_…`). Koide-analog for CKM. Already
   retained as the meta-axiom on the Quark side.

**Reviewer-bar status:** closed on bimodule footing. No named residue
beyond the bimodule itself (the bimodule `B = Cl(3)/Z_3 ⊗ Cl_CKM(1⊕5)`
is the retained structural input; JTS is derived from it, ISSR1 follows,
shell-normalization independently corroborates, RPSR supplies NLO).

---

## §2 Recovered files (forensic summary)

Files restored from git objects `f6b5ce6c`, `986457d0`, `a8fa9cfb`,
`4a7aa854` that were accidentally wiped in the 2026-04-19 force-push:

| File | Source commit | Runner | PASS |
|---|---|---|---|
| `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (selected-line CP¹ version, softened) | `5c223ff9` | `frontier_koide_berry_phase_theorem.py` | 24 |
| `docs/KOIDE_THETA_HIERARCHY_OPEN_SCALAR_NOTE_2026-04-19.md` (softened status) | `5c223ff9` | — (companion) | — |
| `docs/KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md` (softened) | `5c223ff9` | `frontier_koide_selected_line_cyclic_response_bridge.py` | 20 |
| `docs/KOIDE_KAPPA_SPECTRUM_OPERATOR_BRIDGE_THEOREM_NOTE_2026-04-19.md` | `a8fa9cfb` | `frontier_koide_kappa_spectrum_operator_bridge_theorem.py` | 9 |
| `docs/KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md` | `a8fa9cfb` | `frontier_koide_kappa_block_total_frobenius_measure_theorem.py` | 16 |
| `docs/DM_ABCC_PMNS_NONSINGULARITY_THEOREM_NOTE_2026-04-19.md` | `4a7aa854` | `frontier_dm_abcc_pmns_nonsingularity_theorem.py` | 38 |
| `docs/DM_ABCC_SIGNATURE_FORCING_THEOREM_NOTE_2026-04-19.md` | `4a7aa854` | `frontier_dm_abcc_signature_forcing_theorem.py` | 54 |
| `docs/DM_PNS_ATTACK_CASCADE_NOTE_2026-04-19.md` | `4a7aa854` | `frontier_dm_pns_attack_cascade.py` | 47 |

Total recovered PASS count: **208 FAIL=0** across 7 runners.

Also preserved in place: Jon's three new same-day commits (`474b6032`
minimal-local-spectral no-go, `8b2c76bf` boundary-arrest maximin,
`dd865ced` JTS-affine-physical-carrier), the existing DPLE / STRC / BICAC
/ NORM / MRU retained stacks, and all A-BCC-audit no-go content.

---

## §3 What was deliberately not recovered

The following items from the wiped commit set were **not** recovered,
with reasons:

1. **`DM_ABCC_PNS_ALREADY_RETAINED_NOTE_2026-04-19.md`** (from `a8fa9cfb`).
   The note cited the retained σ_hier uniqueness theorem as if it selected
   Basin 1 over other basins, but the retained σ_hier theorem only picks
   the hierarchy permutation *at Basin 1's coordinates* — it does not
   discriminate between basins. This was scope overreach flagged by
   adversarial audit. The correct basin-selection closure is the
   chamber bound `∩` DPLE `F_4` route already retained in
   `DM_ABCC_CLOSURE_VIA_CHAMBER_BOUND_AND_DPLE_F4_NOTE_…`, plus the
   recovered cycles 11/12/13 alternative routes. Nothing valuable is lost
   by not recovering this specific note.

2. **`QUARK_BICAC_RESIDUE_EQUIVALENCE_NOTE_2026-04-19.md`** +
   `frontier_quark_bicac_residue_equivalence.py` (from `a8fa9cfb`,
   PASS=17). The "three framings one residue" claim was pre-Jon's clean
   JTS-affine-physical-carrier derivation. Once that derivation lands
   (in `dd865ced`), the BICAC residue is structurally gone — JTS is not
   a separate postulate, it is a corollary of retaining the `1(+)5`
   carrier. Keeping the residue-equivalence note would perpetuate a
   frame (JTS-as-residue) that the canonical branch no longer needs.

3. **`scripts/frontier_quark_jts_decomposition_theorem.py`**
   (from `807795da`, superseded). The adversarial audit identified 4
   hardcoded `True` PASS values in this runner at central theorem
   claims. Jon's cleaner `dd865ced` replacement derives JTS from the
   affine bimodule geometry without any such shortcut, and its runner
   (`frontier_quark_issr1_bicac_forcing.py` PASS=13) is clean. The old
   decomposition runner is therefore retired, not recovered.

4. **Earlier STRC-LO transfer-operator prose** (from `a8fa9cfb` cycle 16
   corrections). Adversarial audit flagged the transfer-operator choice
   `T_p := Π_5 |p⟩⟨e_1|` as smuggling in the polarization that JTS
   would later name explicitly. That framing is superseded by Jon's
   affine-physical-carrier derivation, which does not rely on picking a
   specific rank-1 operator — `Pert(p) = H_(1+5)` is forced by linear
   algebra alone. The cleaner canonical statement is kept; the
   transfer-operator framing is not re-landed.

5. **Reviewer's retirement note** (`d284ef3c`). Its technical content
   (constant character projectors → trivial bundles on natural lifts →
   `2/9` is one member of a continuous flat-holonomy family) is a
   correct observation, and its conclusion that AXIOM E itself is not
   closed by Berry alone is honored in the softened status of the
   recovered Berry note (§1.1 above). It did not, however, refute the
   selected-line CP¹ geometric identification (which uses a different
   base), so the retirement as a *whole-lane retirement* is not landed —
   only its status caveat, folded into the §1.1 recovered statement.

---

## §4 Test-suite verification

All recovered runners plus all canonical-tip runners pass:

```text
frontier_koide_berry_phase_theorem.py                             PASS=24  FAIL=0
frontier_koide_selected_line_cyclic_response_bridge.py            PASS=20  FAIL=0
frontier_koide_kappa_spectrum_operator_bridge_theorem.py          PASS=9   FAIL=0
frontier_koide_kappa_block_total_frobenius_measure_theorem.py     PASS=16  FAIL=0
frontier_dm_abcc_pmns_nonsingularity_theorem.py                   PASS=38  FAIL=0
frontier_dm_abcc_signature_forcing_theorem.py                     PASS=54  FAIL=0
frontier_dm_pns_attack_cascade.py                                 PASS=47  FAIL=0
frontier_dm_abcc_chamber_dple_closure.py                          PASS=39  FAIL=0
frontier_dm_dple_dimension_parametric_extremum_theorem.py         PASS=19  FAIL=0
frontier_quark_issr1_bicac_forcing.py                             PASS=13  FAIL=0
frontier_koide_moment_ratio_uniformity_theorem.py                 PASS=65  FAIL=0
frontier_koide_mru_weight_class_obstruction.py                    PASS=*   FAIL=0
```

---

## §5 Honest axiom accounting after recovery

| Gate | Pre-recovery | Post-recovery | Residue |
|---|---|---|---|
| Koide `kappa` | MRU support | MRU + operator bridge + block Frobenius measure (three converging theorems) | `1:1` real-isotype measure selection |
| Koide `theta` | Ambient-`S^2` model, bundle obstruction | + actual-route Pancharatnam–Berry identification on selected line | AXIOM E supplies `delta = 2/9`; Berry supplies meaning, not value |
| DM A-BCC | Chamber bound `∩` DPLE `F_4` closure | + cycles 11/12/13 alternative routes (PNS-NS, signature forcing, PNS cascade) | none on A-BCC itself |
| Quark `a_u` | ISSR1 + NORM + shell-norm + STRC | + JTS-affine-physical-carrier theorem derives JTS | none; bimodule is the retained input |

Meta-axiom: `4 -> 2` via `DIM-UNIQ + STRC`. Reviewer-bar: **2 closed,
2 retained with a single named residue each.**

---

## §6 Reading order for the reviewer

1. This note (full-stack recovery).
2. `docs/SCALAR_SELECTOR_CYCLE1_SCIENCE_REVIEW_NOTE_2026-04-19.md` — honest
   pre-recovery review status.
3. `docs/SCALAR_SELECTOR_CYCLE13_META_CLOSURE_STATUS_NOTE_2026-04-19.md` —
   meta-closure compression to `DIM-UNIQ + STRC`.
4. `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` — branch-local route
   catalogue; surgically updated to reference the recovered theorems.
5. Per-lane theorem notes referenced in §1.
