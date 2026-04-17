# Derivation Atlas — Candidate List for Review

**Date:** 2026-04-17
**Scope:** sweep of `docs/`, `docs/work_history/`, and the Frozen-Out Registry
for subderivations / theorems / closed tools that are **not currently** rows in
[DERIVATION_ATLAS.md](./DERIVATION_ATLAS.md) but may qualify under the
atlas rule:

> 1. one current authority note on `main`
> 2. one runner or explicit validation path
> 3. safe claim boundary recorded
> 4. if older route variants exist, canonical one identified

Atlas status is **orthogonal** to the retained paper surface — a reusable
tool belongs here even if the headline result is frozen out.

This file is a **reviewer worksheet**, not an atlas edit. Each entry is a
proposal for the repo manager to accept, amend, or reject. Accepted entries
should be merged into `DERIVATION_ATLAS.md` with the full contract
(safe statement, import class, authority, runner).

Sweep coverage: 581 non-atlas notes in `docs/`, 19 files in
`docs/work_history/`, and the frozen-out families enumerated in
`docs/work_history/publication/FROZEN_OUT_REGISTRY.md`.

---

## Method

Each candidate was evaluated against these disqualifiers:

- dated audits / sweeps / worklogs (`*_2026-04-*`, `*_AUDIT_*`, `*_SWEEP_*`)
- route-history or superseded variants where a canonical atlas row already exists
- narrow numerical diagnostics without a reusable theorem
- per-experiment branch memos, companion-only phenomenology without a theorem
- figure plans, reproducibility notes, session/autopilot logs
- pure failure/negative-result logs unless they establish a reusable no-go

The remaining candidates are partitioned into **STRONG** (expected to land),
**MAYBE** (reviewer judgement needed), and **NOTE-LEVEL RECONCILE** (overlaps
an existing atlas row and the row should be strengthened or expanded).

Proposed atlas section letters match the current A–K layout.

---

## STRONG candidates

### A. Core framework and observable tools

- `BOUND_STATE_SELECTION_NOTE.md` — stable matter only at `d ≤ 3`; dimension-selection lemma for Coulomb-like bound states.
- `DECOHERENCE_ACTION_INDEPENDENCE_NOTE.md` — decoherence observable is action-independent on the retained surface; structural observable property.

### B. Spacetime and topology tools

- `LORENTZ_VIOLATION_DERIVED_NOTE.md` — residual cubic-harmonic Lorentz-violation pattern derived from `Z^3` anisotropy; structural complement to the "Emergent Lorentz invariance" atlas row (captures the bounded residual rather than the suppression).
- `BACKGROUND_INDEPENDENCE_NOTE.md` — effective geometry differs from input graph; structural lattice-geometry lemma reusable for any lane that interprets "physical lattice".

### D. Gravity tools

- `EQUIVALENCE_PRINCIPLE_NOTE.md` / `MATTER_INERTIAL_CLOSURE_NOTE.md` pair — weak-equivalence / inertial-mass identification theorem (current atlas has "WEP / time-dilation corollaries" but no explicit inertial-mass row).
- `GRAVITY_FULL_SELF_CONSISTENCY_NOTE.md` — full self-consistency forces Poisson operator on the entire framework (strengthening of atlas "Poisson self-consistency"; reconcile).
- `GRAVITOMAGNETIC_NOTE.md` — antisymmetric-in-velocity Shapiro correction portable across three families; structural gravitomagnetic tool.
- `WAVE_EQUATION_GRAVITY_NOTE.md` + `WAVE_EQUATION_SELF_FIELD_NOTE.md` + `WAVE_RETARDED_GRAVITY_NOTE.md` + `WAVE_RADIATION_NOTE.md` — d'Alembertian promotion of Poisson preserves Newton limit, gives retarded field ≠ instantaneous, supports radiation slope; complete the "wave-side gravity toolkit" currently absent from atlas D.
- `SELF_GRAVITY_BACKREACTION_CLOSURE_NOTE.md` — bounded no-go on exact-lattice Poisson backreaction under Born controls; reviewer-visible boundary lemma.
- `KUBO_CONTINUUM_LIMIT_NOTE.md` + `LINEAR_RESPONSE_TRUE_KUBO_NOTE.md` + `KUBO_RANGE_OF_VALIDITY_NOTE.md` — analytic first-order Kubo convergence plus validity window; linear-response tool reusable for any weak-field matching argument.
- `LENSING_ADJOINT_KERNEL_NOTE.md` — lensing as adjoint-weighted edge sum (not ray-angle); reusable kernel identity.
- `LENSING_DEFLECTION_NOTE.md` — deflection power-law exponent at fine refinement; structural distance-law fact.
- `LATTICE_COMPLEMENTARITY_NOTE.md` — field / propagator complementarity with sweet spot; reusable selection tool for ordered-lattice gravity work.
- `NONLINEAR_BORN_GRAVITY_NOTE.md` — nonlinear propagator breaks Born rule and gravity simultaneously; structural no-go tying Born to gravity.
- `SHAPIRO_UNIQUE_DISCRIMINATOR_V2_NOTE.md` — static cone-shape proxy reproduces detector-line phase lag exactly; reusable discriminator primitive.

### E. Electroweak and hierarchy tools

- `SPECTRAL_SYMMETRY_NOTE.md` — graph discrete symmetry controls decoherence / spectral gap; theorem + mechanism + scaling law.
- `HIGGS_MECHANISM_NOTE.md` — taste condensate as Higgs with natural electroweak breaking; structural mechanism note (Higgs frozen-out per F05, but the mechanism statement is a reusable tool).
- `HIGGS_MASS_DERIVED_NOTE.md` — 3-loop runner derivation; reusable bridge even while the headline mass is companion-only.

### F. Flavor, Yukawa, and mass-lane tools

- `YT_BOUNDARY_THEOREM.md` (F02 frozen-out) — physical crossover endpoint selection resolves boundary-consistency blocker; atlas-grade tool even though the zero-import `m_t` headline is superseded.
- `YT_EFT_BRIDGE_THEOREM.md` (F02) — backward Ward boundary transfer identity at `v` for EFT closure; reusable Ward-boundary tool.
- `YT_GAUGE_CROSSOVER_THEOREM.md` (F02) — one-shot Feshbach matching companion; reusable matching primitive.
- `YUKAWA_COLOR_PROJECTION_THEOREM.md` — `\sqrt{8/9}` color-singlet projection from `1/N_c`; atlas has an "EW color projection" row but no explicit Yukawa-color derivation row; reconcile.
- `YT_EXACT_HESSIAN_SELECTOR_UNIQUENESS_NOTE.md` — Hessian selector uniqueness within admissible Schur coarse-operator class.
- `YT_VERTEX_POWER_DERIVATION.md` (F02) — vertex-power counting lemma; reusable power-counting primitive.
- `YT_ZERO_IMPORT_AUTHORITY_NOTE.md` (F02) + `YT_ZERO_IMPORT_CHAIN_NOTE.md` — zero-import chain still defines the reusable import-class boundary even though the `m_t` headline is superseded.
- `YT_INTERACTING_BRIDGE_LOCALITY_NOTE.md` — bridge-locality property reusable for any interacting-bridge argument.
- `YT_EW_COUPLING_BRIDGE_NOTE.md` — EW gauge-coupling bridge; reusable coupling primitive.
- `PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md` — C3 character-holonomy closure on PMNS lane.
- `PMNS_THREE_FLUX_HOLONOMY_CLOSURE_NOTE.md` — three-flux holonomy closure.
- `PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md` — reduced-law sharpening of PMNS C3 character modes.

### G. DM and cosmology tools

- Full Neutrino-Majorana no-go / boundary stack, currently only partly indexed:
  - `NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md`
  - `NEUTRINO_MAJORANA_FINITE_NORMAL_GRAMMAR_NO_GO_NOTE.md`
  - `NEUTRINO_MAJORANA_NO_STATIONARY_SCALE_THEOREM_NOTE.md`
  - `NEUTRINO_MAJORANA_STAIRCASE_BLINDNESS_THEOREM_NOTE.md`
  - `NEUTRINO_MAJORANA_ALGEBRAIC_BRIDGE_OBSTRUCTION_NOTE.md`
  - `NEUTRINO_MAJORANA_ENDPOINT_EXCHANGE_MIDPOINT_THEOREM_NOTE.md`
  - `NEUTRINO_MAJORANA_NAMBU_SOURCE_PRINCIPLE_NOTE.md`
  - `NEUTRINO_MAJORANA_OPERATOR_AXIOM_FIRST_NOTE.md`
  - `NEUTRINO_MAJORANA_PFAFFIAN_NO_FORCING_THEOREM_NOTE.md`
  - `NEUTRINO_MAJORANA_SOURCE_RAY_THEOREM_NOTE.md`
  - `NEUTRINO_MAJORANA_RESIDUAL_SHARING_SPLIT_THEOREM_NOTE.md`
  - `NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md`
- `docs/work_history/dm/DM_LEPTOGENESIS_FULL_AXIOM_CLOSURE_NOTE_2026-04-16.md` — DM leptogenesis denominator lane closed modulo `H_rad(T)`; extends atlas row set on the DM side and should be reconciled with "DM equilibrium conversion theorem".
- `PRIMORDIAL_SPECTRUM_NOTE.md` — `n_s = 1 - 2/N_e` graph-growth derivation; currently present as "Spectral tilt companion" but the graph-growth mechanism is reusable as its own tool row.

### H. Companion and discriminator tools

- `SHAPIRO_DELAY_NOTE.md` — canonical replay of discrete Shapiro-style phase lag (distinct from the V2 discriminator above; retained as its own reusable primitive).
- `IF_PROGRAM_CLOSING_NOTE.md` — uniform-architecture decoherence-search closure and IF-topology outcome; structural closure support.

---

## MAYBE candidates (reviewer judgement needed)

- `GENERATED_GEOMETRY_SYNTHESIS_NOTE.md` — full Newtonian package on grown geometry (100% TOWARD across 4 rows). Ambiguous: synthesis vs standalone theorem.
- `GRAVITATIONAL_ENTANGLEMENT_NOTE.md` — gravitational entanglement between wavepackets (4/4 gates); phrased as diagnostic gates — theorem status unclear.
- `GRAVITATIONAL_WAVE_PROBE_NOTE.md` — beyond-Newtonian gravity probe (3/4 tests positive); mixed results, clarify which component is reusable.
- `GLOBAL_COHERENCE_OFF_SCAFFOLD_NOTE.md` — off-scaffold closure: simple-classifier line exhausted on new generators; may qualify as reusable no-go lemma.
- `NEWTON_DERIVATION_NOTE.md` — Newtonian scaling from four principles; persistence-pattern inertia remains open.
- `NEUTRINO_MAJORANA_CURRENT_ATLAS_NONREALIZATION_NOTE.md` — current atlas bounds prevent full Majorana realization; boundary result.
- `NEUTRINO_MAJORANA_NATIVE_GAUSSIAN_NO_GO_NOTE.md` — native-Gaussian sector no-go; may be covered by broader Majorana stack above.
- `MULTIPOLE_TIDAL_RESPONSE_NOTE.md` — multipole/tidal response; probe vs theorem unclear.
- `SYNTHESIS_NOTE.md` — hardened synthesis on discrete causal DAGs; contains historical snapshots, authority unclear.
- `TENSOR_NETWORK_CONNECTION_NOTE.md` — tensor-network connection derivation; substantive claim unclear from headers.
- `THREE_FAMILY_CARD_NOTE.md` — three families match 9/9 properties to <5%; empirical vs structural theorem.
- `YT_BRIDGE_OPERATOR_CLOSURE_NOTE.md` — bridge operator closure proxy; check if closes a reusable lane.
- `YT_FLAGSHIP_BOUNDARY_NOTE.md` — flagship-boundary support note; classify vs YT_BOUNDARY_THEOREM.
- `YT_EXPLICIT_SYSTEMATIC_BUDGET_NOTE.md` — systematic-budget book-keeping; check if the budget itself is a reusable primitive.
- `LATTICE_GRAVITY_RESOLUTION_NOTE.md` — ultra-weak field on dense lattice gives attraction AND `1/b`; theorem-grade or numerical?
- `LATTICE_DISTANCE_LAW_NOTE.md` + `LATTICE_NN_DISTANCE_LAW_NOTE.md` + `WIDE_LATTICE_H2T_DISTANCE_LAW_NOTE.md` — distance-law scaling replays across families; candidate universality tool if consolidated.
- `COMPLEX_ACTION_NOTE.md` + `ACTION_POWER_3D_GRAVITY_SIGN_CLOSURE_NOTE.md` + `ACTION_UNIQUENESS_NOTE.md` — action-family selection tools; reviewer should check against the "Action" cluster in atlas section A.
- `FM_TRANSFER_NOTE.md` + `EMERGENT_PRODUCT_LAW_NOTE.md` — `F~M` transfer / `M1*M2` product law; reusable weak-field primitives if reconciled with Poisson row.
- `CONTINUUM_LIMIT_NOTE.md` — weak-field deflection converges via `h^2` measure; structural convergence tool.
- `DISTANCE_LAW_NOTE.md` / `DISTANCE_LAW_DEFINITIVE_NOTE.md` — steeper-than-Newtonian far-field law; could be a bounded support tool.
- `BEYOND_LATTICE_QCD_NOTE.md` — numerically demonstrated; theorem-level claim ambiguous.

---

## NOTE-LEVEL RECONCILE (already-indexed atlas row should expand)

These notes overlap an existing atlas row; the reviewer should decide whether
the atlas row description should widen to cite them, rather than adding new
rows.

- `docs/OMEGA_LAMBDA_DERIVATION_NOTE.md` — already covered by "Conditional `Ω_Λ` chain".
- `docs/DARK_ENERGY_EOS_NOTE.md` — already covered by "Dark-energy EOS chain" / "Cosmological-constant spectral-gap companion".
- `docs/work_history/ckm/CABIBBO_BOUND_NOTE.md` — "Cabibbo bounded companion".
- `docs/work_history/ckm/JARLSKOG_PHASE_BOUND_NOTE.md` — "Jarlskog phase companion".
- `docs/work_history/ckm/CKM_MASS_BASIS_NNI_NOTE.md` — "CKM mass-basis route" / "CKM Schur complement theorem".
- `docs/FROZEN_STARS_RIGOROUS_NOTE.md` — covered by "Frozen-star null-echo result".
- `docs/GRAVITON_MASS_DERIVED_NOTE.md` — "Graviton-mass companion".
- `docs/ACCESSIBLE_PREDICTION_NOTE.md` — companion-only phenomenology; cross-reference from "Frozen-star null-echo result" row.

---

## SKIP (out of scope, documented for audit)

Large groups deliberately excluded as not atlas candidates. Recorded so the
repo manager can see the sweep was not selective:

- All `CAUSAL_*` notes except `CAUSAL_PROPAGATING_FIELD_NOTE` — mostly work-history probes.
- `ASYMMETRY_PERSISTENCE_*` family (6 notes) — experimental parameterizations.
- `EVOLVING_NETWORK_PROTOTYPE_V1`–`V6` — superseded development history.
- `CENTRAL_BAND_*` family (8+) — numerical diagnostics without closures.
- `ACTION_POWER_*` family — branch-specific scaling replays.
- `ALT_CONNECTIVITY_FAMILY_*` — diagnosed-failure / boundary probes.
- `DIRECTIONAL_B_GEOMETRY_*` — geometry-dependent diagnostics.
- `CHIRAL_3PLUS1D_*` — "diagnosed not universal / not resolved".
- `DIAMOND_*` NV-sensor notes — lab-facing experiment proxies.
- `CLAUDE_BRANCH_*`, `CLAUDE_DEAD_END_*`, autopilot/session logs.
- All `*_2026-04-*` dated files (audits, sweeps, worklogs).
- `MOONSHOT_*_BRAINSTORM` / `MOONSHOT_*_PORTFOLIO` — active frontier brainstorms, not closed theorems.
- `MIRROR_*` legacy (5 files) — superseded by canonical chokepoint chain.
- `PERSISTENT_OBJECT_*` and `QUASI_PERSISTENT_RELAUNCH_*` (11 files) — detector/readout probes.
- `RETARDED_FIELD_*`, `PROPAGATOR_*`, `QNM_*`, `QUANTUM_*` moonshots — narrow causality probes.
- Family-specific `SECOND_GROWN_*`, `SIXTH_FAMILY_*`, `SEVENTH_FAMILY_*` — family-specific numerical results.
- `UNIVERSAL_GR_*` blockers (`CURVATURE_LOCALIZATION`, `INVARIANT_FRAME_OBSTRUCTION`, `POLARIZATION_FRAME_BUNDLE_BLOCKER`, `TENSOR_ACTION_BLOCKER`) — marked historical; confirm canon status before adding.
- Per-experiment seed/control runbooks: `WAVE_DIRECT_DM_H025_FAM*_SEED*_CONTROL_NOTE`, `WAVE_STATIC_*` control variants (19 files).
- Comparative diagnostics without standalone theorems: `SPECTRAL_SYMMETRY_SPECTRUM_MIRROR_COMPARE`, `SYMMETRY_HEAD_TO_HEAD`, `STRUCTURED_MIRROR_JOINT_VALIDATION`, `STAGGERED_GRAPH_PORTABILITY_STRESS`.
- All work-history `*_STATUS_REVIEW_*`, `*_REDUCTION_OPTIONS_*`, `PUBLICATION_CARD`, `LANE_STATUS_BOARD`, `STALE_AUTHORITY_AUDIT`, `REMOTE_BRANCH_AUDIT`, `RUNNING_PACKAGE_ISSUES` — planning/inventory only.
- `docs/work_history/GW_ECHO_TIMING_ROUTE_NOTE.md` — superseded by `GW_ECHO_NULL_RESULT_NOTE` (already in atlas).
- `docs/work_history/yt/YT_UNBOUNDED_PROGRAM_NOTE.md` — strategy memo.
- `docs/work_history/CABIBBO_JARLSKOG_ROUTE_NOTE_2026-04-12.md` — combined route note, work history only.
- `docs/BMV_BOUNDED_NEGATIVE_NOTE.md` — no discrete-spacetime prediction; continuum-convergence only.
- `UNPROMOTED_BRANCH_RETAINABILITY_AUDIT`, `TRIAGE_NO_PROMOTION` — work-history meta-audits.
- `LEGACY_EXPLORATORY_DRIVERS_NOTE`, `LITERATURE_POSITIONING_NOTE` — historical/positioning docs.

---

## Summary counts

- STRONG candidates proposed: **~48** (across A/B/D/E/F/G/H)
- MAYBE candidates: **~22**
- Already-indexed but widen-rows: **~8**

Expected effect on atlas if all STRONG accepted: ~48 new rows, ~14 existing
rows reconciled / expanded. Largest growth is in section G (Neutrino-Majorana
no-go stack, ~12 rows), section F (full YT/Yukawa tool set including
frozen-out F02 components, ~10 rows), and section D (wave-side gravity +
linear-response Kubo toolkit, ~10 rows).

## Reviewer workflow

For each candidate:

1. Confirm an authority note exists on `main` (or flag for canonicalization).
2. Confirm a runner or explicit validation path exists.
3. Draft the safe claim boundary in one line.
4. Assign the import class (zero-input structural / axiom-dependent support /
   bounded companion / etc.).
5. Decide: **LAND** (new atlas row), **RECONCILE** (expand existing row), or
   **REJECT** (document reason below).

Rejected rows should be recorded inline here with reason, so the sweep is
auditable and future janitor passes do not re-propose them.
