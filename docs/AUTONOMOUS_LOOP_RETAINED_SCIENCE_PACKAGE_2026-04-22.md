# Autonomous-Loop Retained Science Package — 2026-04-22

**Date:** 2026-04-22
**Status:** **curated post-hostile-review subset** of the autonomous-loop session output. Contains only the 11 branches that defensibly survive Nature-grade review.
**Provenance:** selected from 20 session branches per the critical audit in `docs/AUTONOMOUS_LOOP_NATURE_GRADE_REVIEW_2026-04-22.md`.

---

## 0. What this package is

The autonomous-loop session produced 20 branches. A hostile Nature-grade review of those claims (included in this package as a transparency artifact) identified:

- 1 **critical P0 issue** (solar-gap 2% match was IO, not NO).
- 7 **inflated** claims (tautological restatements, internally-inconsistent chains, conjecture-mislabeled-as-attack).
- 10 **robust** branches that survive hostile pressure.
- 2 **index/navigation** branches.

This package contains **only the 10 robust branches plus the hostile review note itself** for reviewer transparency. All INFLATED and P0-flawed content is **excluded** and referenced here by name only.

## 1. Included science (11 docs + 13 runners, all on main-compatible branch)

### Theorem-grade identities

- `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` — clean retained algebraic identity `Ω_Λ = (H_inf/H_0)²` reducing three bounded cosmology rows to one open number.
- `KOIDE_Q_EQ_3DELTA_DOUBLET_MAGNITUDE_THEOREM_NOTE_2026-04-22.md` — retained-algebraic third-path identity `(E2/2)² = SELECTOR²/3 = Q_Koide/3` linking retained chart to Koide.

### Rigorous negative results

- `KOIDE_Q23_OH_COVARIANCE_NOGO_NOTE_2026-04-22.md` — explicit 48-element enumeration showing retained `H_base` chart's O_h joint-covariance group is only `{+I, −I}`. Falsifies one concrete sub-route of the spin-1 structural attack on Q=2/3.

### Scope-honest predictions (conditional on retained chain)

- `NEUTRINO_MASS_SUM_PREDICTION_NOTE_2026-04-22.md` — `Σm_ν ∈ [0.059, 0.102] eV` conditional on the retained neutrino chain's diagonal benchmark (with internal `Δm²_21` issue explicitly flagged).
- `NEUTRINOLESS_DOUBLE_BETA_MBB_PREDICTION_NOTE_2026-04-22.md` — `m_ββ ∈ [0, 7] meV` over Majorana phases, from the same conditional chain.
- `TRITIUM_BETA_EFFECTIVE_MASS_PREDICTION_NOTE_2026-04-22.md` — `m_β = 9.86 meV` single-valued prediction (Majorana-phase-independent) from the same conditional chain.

### Consolidation and support

- `KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md` — 3-iteration Brannen-phase candidate sharpening, final state honestly framed as "candidate closure" after reviewer P0 critiques on initial version.
- `CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md` — transport-factor identity cross-checking retained α_s(v) against PDG at threshold-local scale.
- `RETAINED_CROSS_LANE_CONSISTENCY_SUPPORT_NOTE_2026-04-22.md` — 26/26 numerical cross-check harness across eight retained lanes.
- `TENSOR_SCALAR_RATIO_CONSOLIDATION_THEOREM_NOTE_2026-04-22.md` — retained `r = d²/N_e² = 0.0025` consolidation with d=3 retained, N_e bounded.
- `LAMBDA_QCD_DERIVATION_SUPPORT_NOTE_2026-04-22.md` — 1-loop `Λ_QCD^(3,4,5)` extraction from retained α_s(M_Z) with scheme-truncation gap documented.
- `MONOPOLE_MASS_CONSOLIDATION_THEOREM_NOTE_2026-04-22.md` — compact 10-step consolidation of retained `M_mono ≈ 1.4 M_Planck` + inflation-requirement structural consequence.

### Transparency

- `AUTONOMOUS_LOOP_NATURE_GRADE_REVIEW_2026-04-22.md` — the hostile self-review identifying P0 issues. Included for full transparency so reviewers see the audit of the session's claims.

### Runners (13)

All included in `scripts/` with matching filenames. Each runs self-contained; all pass at their documented test counts.

## 2. Excluded from this package (and why)

### P0 issues (one branch)

- **`neutrino-solar-gap-alpha-lm-squared`** (loop 17): claimed "2% match closes solar gap" but the match was between theoretical `Δm²_32` and observed `Δm²_21` — different observables under NO labeling. Properly identified, it's an IO (inverted ordering) candidate, currently disfavored at 2-3σ. Needs reframing as IO prediction before inclusion on main.
- **`neutrino-three-level-staircase-proposal`** (loop 18): inherits the IO misidentification. The structural three-level mechanism is still a reasonable hypothesis but shouldn't be promoted before the IO reframing is done.

### Inflated "Q=2/3 attack" branches (four branches)

- **`koide-q23-anomaly-structural-attack`** (loop 12): conjecture `E2² = |Tr[Y³]|/2` is arithmetic match at d=3, not structural derivation. The factor 1/2 has no retained justification. "Structural attack" language overstates progress.
- **`koide-q23-spin1-structural-route`** (loop 13): `Q = (d-1)/d = 2s/(2s+1)` at d=3 is tautological — plugging in d=3 to get 2/3 is not a derivation.
- **`koide-q23-spin1-subroute-status`** (loop 15): landscape note claiming "8 converging support routes", when hostile audit shows only ~3 are genuinely independent.
- **`koide-q23-variational-coupling-conjecture`** (loop 16): `C(σ) = σ(1−σ)` unique max at σ=1/2 is pure math (any quadratic peaks at center), not a physics closure.

### Index branches (two)

- **`autonomous-loop-index-2026-04-22`** and **`autonomous-loop-index-update-2026-04-22`**: navigation index branches. Their headline claims ("significant candidate closures", "two major findings") are overstated per the review. The catalog content itself is fine but the framing was inflated. This README replaces them.

## 3. What this package claims and does not claim

### Claims

1. **One clean algebraic identity**: `Ω_Λ = (H_inf/H_0)²` reducing three cosmology bounded rows to one open number.
2. **One rigorous negative result**: retained `H_base` chart is not O_h-covariant (7th no-go on Q=2/3).
3. **One retained-algebraic identity**: `(E2/2)² = SELECTOR²/3 = Q_Koide/3` connects retained chart to Koide structure.
4. **Three scope-honest predictions** (conditional on retained chain): `Σm_ν`, `m_ββ`, `m_β` with the retained chain's known `Δm²_21` issue explicitly flagged.
5. **Multiple consolidation/support theorems** that don't advance new physics but cross-check and navigate retained material.

### Does NOT claim

- **Closure of Koide Q = 2/3**: the physical-identification principle remains open. This package contains zero branches claiming to close it.
- **Closure of the neutrino solar gap**: excluded entirely pending IO/NO reframing.
- **New variational principles, SO(3) extensions, or anomaly-identity bridges**: these were explored but excluded as conjectural or tautological.
- **New retained-theorem-grade physics predictions**: the predictions included are conditional on bounded-lane chains.

## 4. Relation to existing main content

This package is **ADDITIVE** relative to main's existing retained structure:

- Does not modify any retained theorems.
- Adds one new clean identity (Ω_Λ = (H_inf/H_0)²) that belongs on the cosmology surface.
- Adds one new rigorous no-go (O_h covariance) that belongs in the Q=2/3 open-item register alongside the existing 6 no-gos.
- Adds retained-algebraic identities bridging known retained quantities.
- Adds scope-honest neutrino predictions explicitly flagged as conditional.

None of these require retained-theorem-surface changes elsewhere.

## 5. What reviewers should note

**This is NOT a "20 branches of novel physics" submission**. After hostile self-review, the genuine new content is modest:

- Three rigorous new results (`Ω_Λ` identity, O_h no-go, `(E2/2)² = Q/3`).
- Several consolidations and scope-honest predictions.
- One explicitly withdrawn/flagged branch pair (solar-gap IO issue) with honest public review note.

The package's honest characterization: **productive infrastructure work on the retained Cl(3)/Z³ framework, with one rigorous advance (O_h no-go), clean algebraic identities, scope-honest predictions, and a candid post-session review identifying over-reach**.

## 6. File manifest

### Documents (13)

```
docs/
  AUTONOMOUS_LOOP_NATURE_GRADE_REVIEW_2026-04-22.md          [transparency]
  AUTONOMOUS_LOOP_RETAINED_SCIENCE_PACKAGE_2026-04-22.md    [this README]
  CKM_DOWN_TYPE_SCALE_CONVENTION_SUPPORT_NOTE_2026-04-22.md
  KOIDE_BRANNEN_CH_THREE_GAP_CLOSURE_NOTE_2026-04-22.md
  KOIDE_Q23_OH_COVARIANCE_NOGO_NOTE_2026-04-22.md            [rigorous new result]
  KOIDE_Q_EQ_3DELTA_DOUBLET_MAGNITUDE_THEOREM_NOTE_2026-04-22.md
  LAMBDA_QCD_DERIVATION_SUPPORT_NOTE_2026-04-22.md
  MONOPOLE_MASS_CONSOLIDATION_THEOREM_NOTE_2026-04-22.md
  NEUTRINOLESS_DOUBLE_BETA_MBB_PREDICTION_NOTE_2026-04-22.md
  NEUTRINO_MASS_SUM_PREDICTION_NOTE_2026-04-22.md
  OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md       [new retained identity]
  RETAINED_CROSS_LANE_CONSISTENCY_SUPPORT_NOTE_2026-04-22.md
  TENSOR_SCALAR_RATIO_CONSOLIDATION_THEOREM_NOTE_2026-04-22.md
  TRITIUM_BETA_EFFECTIVE_MASS_PREDICTION_NOTE_2026-04-22.md
```

### Runners (13)

```
scripts/
  frontier_ckm_down_type_scale_convention_support.py
  frontier_koide_brannen_absss_equivariant_descent.py
  frontier_koide_brannen_ch_three_gap_closure.py
  frontier_koide_q23_oh_covariance_nogo.py
  frontier_koide_q_eq_3delta_doublet_magnitude.py
  frontier_lambda_qcd_derivation_support.py
  frontier_monopole_mass_consolidation.py
  frontier_neutrino_mass_sum_prediction.py
  frontier_neutrinoless_double_beta_mbb_prediction.py
  frontier_omega_lambda_matter_bridge.py
  frontier_retained_cross_lane_consistency.py
  frontier_tensor_scalar_ratio_consolidation.py
  frontier_tritium_beta_mass_prediction.py
```

All runners independently verified passing on their respective branches. Reviewer can run any `scripts/frontier_*.py` to verify the associated note.

## 7. Further development pending

The following items from the session are deliberately **withheld** from this package:

- **Neutrino solar-gap IO reframing**: the loop 17/18 work needs IO-not-NO reframing and then can be included as a falsifiable IO prediction. Not ready for retention on main.
- **Q=2/3 structural attacks (loops 12, 13, 16)**: conjectural or tautological. Not retained until one of the candidate mechanisms is promoted to an actual derivation.
- **Three-level staircase mechanism (loop 18)**: hypothetical only; needs retained three-level adjacent-placement theorem.

These are active open questions, not retained science.

## 8. Summary for reviewer

This package contains the science from the 20-branch autonomous-loop session that **defensibly belongs on main**:

- 3 genuine new contributions (O_h no-go, Ω_Λ identity, doublet-magnitude chart link).
- 3 scope-honest predictions conditional on retained chain (Σm_ν, m_ββ, m_β).
- 5 consolidation/support notes that cross-check and strengthen retained material.
- 1 multi-iteration Brannen-phase candidate sharpening with final honest scope.
- 1 transparency review note identifying session over-reach for honesty.

**Excluded**: 1 P0 issue, 4 inflated hard-problem attacks, 2 navigation indices with inflated framing.

The result: a **smaller, honest, reviewer-ready** subset of the session's work. The excluded content remains available on its respective branches for further development, but is explicitly **not** promoted to main.
