# 19-Row Promotion Mapping vs T_∞ Identification

**Date:** 2026-05-10
**Lane:** lattice action / refinement / continuum-limit sub-lane
**Scope:** tabulation/audit recommendation only (does not modify the ledger or any source note)

## Context

Three companion PRs landed for the rescaled NN-lattice continuum bridge:

- **PR #957** — `T_∞` exists. Operator-Cauchy convergence with `r = 1.51`, `R^2 = 0.994`
  on a 15-dim observable basis through `h = 0.03125`.
  Source note: `docs/NN_LATTICE_RESCALED_OPERATOR_CAUCHY_CONVERGENCE_NOTE_2026-05-10.md`
  (branch `claude/science/nn-lattice-operator-cauchy-convergence`).
- **PR #945** — Fixed-strength gravity continuum is `0`. Saturation null-result with
  `q = 1.19`, `p = 0.45` on a joint `(h, s)` fit.
  Source note: `docs/NN_LATTICE_RESCALED_RG_GRAVITY_SATURATION_NOTE_2026-05-10.md`.
- **PR #968** — `T_∞` identified as the geodesic operator on the decoherence subblock.
  `σ_arm = C · h^0.526`, `R^2 = 0.9996`, Gaussian-arm prediction matches MI/d_TV
  to `5e-4`.
  Source note: `docs/NN_LATTICE_RESCALED_CONTINUUM_IDENTIFICATION_NOTE_2026-05-10.md`.

## Classification scheme

- **A. Promotable via #968 identification.** Load-bearing claim references
  MI / d_TV / 1−pur / Born continuum-stable values on the rescaled NN-lattice
  harness. The bounded fixed-h value already matches the continuum-operator
  value to `≤ 7.7e-3` (PR #957's tail bound).
- **B. Stays bounded for geodesic-saturation reason.** Load-bearing claim
  references fixed-strength gravity on the rescaled NN-lattice harness. The
  bound is now structurally identified rather than gap-filled (#945 + #968
  explain why the limit is zero).
- **C. Other.** Row references something orthogonal to the rescaled NN bridge
  (different harness, different observable, or different parameter regime).

## Summary

- **Class A — promotable via #968 identification:** 2 rows
  (`lattice_nn_continuum_note`, `lattice_nn_deterministic_rescale_note`).
- **Class B — stays bounded for geodesic-saturation reason:** 4 rows
  (`lattice_nn_mass_response_note`, `lattice_nn_rg_alpha_sweep_note`,
  `lattice_nn_rg_gravity_note`, `lattice_nn_rg_reconciliation_note`).
- **Class C — other (orthogonal to the rescaled NN bridge):** 13 rows
  (action-power, action-uniqueness, alt-connectivity ×2, gate-B,
  NN distance-law, moving-source, Newtonian-distance historical, restricted
  strong-field, sixth-family ×2, continuum-bridge survey, mirror-2D).

### Recommended next-step action per class

- **Class A.** Re-audit candidate: status promotion from `retained_bounded` to
  a continuum-identified tier should be feasible by citing #957 (operator
  Cauchy) + #968 (identification of `T_∞` on the decoherence subblock). The
  existing observable rows for MI / 1−pur / d_TV / Born are now bounded by
  the continuum operator's values to within #957's tail bound, so the
  finite-spacing tables stop being merely "Born-clean refinement trends" and
  start being finite-h slices of a known continuum operator.
- **Class B.** No promotion. Update the source note's "open question" /
  "RG question remains open" framing to cite #945 (fixed-strength continuum
  is zero by saturation) and #968 (the surviving operator is the geodesic
  one on the decoherence subblock, which is why fixed-strength gravity
  decays to zero rather than to a finite RG fixed point). The bound is
  structurally identified, so these rows can stay `retained_bounded` with a
  cleaner closure paragraph.
- **Class C.** No change driven by the three PRs. These rows live on a
  different harness (3D ordered action-power, alt connectivity families,
  exact 2D mirror, mixed-architecture Gate-B replay, etc.), a different
  observable (centroid-shift far-field probe, moving-source phase lag), or
  a different parameter regime (strong-field `O_h` shell class). They are
  unaffected by the rescaled NN-lattice operator-Cauchy / identification
  story and should be re-audited only on their own evidence chains.

## Per-row mapping

| claim_id | effective_status | claim_type | load-bearing claim (1-line) | classification | reasoning |
|---|---|---|---|---|---|
| `action_power_3d_gravity_sign_closure_note` | retained_bounded | bounded_theorem | On the 3D ordered NN family with action `S = L|f|^0.5`, the close-slit barrier gravity sign cannot flip from "away" to "toward" under field-strength weakening, denser forward connectivity, or geometric jitter (toward count `0/14`, `0/24+`, `0/8`). | C | Different harness: 3D ordered action-power barrier card with a sign-flip target on a fixed `L=12, W=6, h=1.0` family. Note explicitly says it does not address "continuum-limit rescue beyond the current ordered-family finite harness," so it is orthogonal to the rescaled NN bridge. |
| `action_uniqueness_note` | retained_bounded | bounded_theorem | On a fixed 3D ordered-lattice family (`h=0.5, W=8, L=12`, kernel `1/L^2`), the Newtonian-mass exponent `F~M` tracks the weak-field power of `f` in the action; weak-field-linear phase valleys give `F~M = 1.0`. | C | Different harness and different observable: action-universality probe on a fixed ordered family at `h=0.5`, parameterized over action choice rather than over `h`. Note explicitly says it does "not prove a universal theorem across all graph families" and is not on the rescaled NN refinement path. |
| `alt_connectivity_family_basin_note` | retained_bounded | bounded_theorem | A parity-rotated sector-transition connectivity family on the no-restore grown slice survives as a real bounded basin (`32/45` rows pass exact zero, neutral, sign, and near-linear charge-scaling controls). | C | Different connectivity family on a grown DAG slice, not the NN lattice. Observable is sign / neutral-cancellation, not the 15-dim observable basis of #957. |
| `alt_connectivity_family_failure_note` | retained_bounded | bounded_theorem | The misses in the alt-connectivity basin are pure sign-orientation failures (`13` orientation reversals; `0` zero-control or scaling leakage), not hidden control breakage. | C | Same alt-connectivity grown-DAG harness as the basin note; orthogonal to the NN refinement bridge. |
| `gate_b_connectivity_tolerance_note` | retained_bounded | bounded_theorem | Position noise on a fixed connectivity backbone is tolerated under the valley-linear law, but recomputing connectivity from geometry (templated growth, K-NN, snapped) makes the response mixed; connectivity construction, not jitter, is the Gate-B bottleneck. | C | Mixed-architecture Gate-B replay (ordered, jittered, templated, K-NN, snapped) with a mass-side detector-window observable. Not the rescaled NN bridge harness. |
| `lattice_nn_continuum_note` | retained_bounded | bounded_theorem | The raw NN lattice is Born-clean through `h = 0.25` with MI rising toward `1`, `1-pur` toward `0.5`, `d_TV` toward `1`, `k=0` exactly zero, and Born at machine precision; `h = 0.125` FAILs in the raw kernel so the continuum question is left open. | A | This is the upstream raw NN refinement that the rescaled bridge extends. The load-bearing rows are exactly the MI / 1-pur / d_TV / Born continuum-stable values now identified by #968 on the decoherence subblock. The "FAIL at h = 0.125" gate is what the rescaled deterministic schedule (and #957's operator-Cauchy run through `h = 0.03125`) closes. Quoted: "the nearest-neighbor lattice shows a Born-clean positive refinement trend through `h = 0.25`... continuum question remains open" — the operator now exists. |
| `lattice_nn_distance_law_note` | retained_bounded | bounded_theorem | On the NN refinement path, the barrier-harness centroid-shift signed delta keeps a meaningful far-field magnitude law (`|delta| ~ b^-0.93..-0.97`, `R^2 ≥ 0.96`) through `h = 0.25`; simple alpha-scaled strength laws flatten the decay rather than rescue it. | C | Distance-law observable (signed centroid shift vs `b`) is not in the 15-dim observable basis of the operator-Cauchy convergence in #957, and the runner does not check Born or `k=0`. The 2026-04-28 audit boundary explicitly flags it as conditional on a separate barrier harness. Orthogonal to the rescaled bridge identification. |
| `moving_source_cross_family_note` | retained_bounded | bounded_theorem | The bounded moving-source directional centroid-bias `delta_y vs static` and phase-lag observables survive on two portable grown families (`drift=0.20 restore=0.70`, `drift=0.05 restore=0.30`) with exact zero baselines and matched static controls. | C | Moving-source on portable grown DAG families; observable is a directional centroid bias with respect to a moving source. Not the NN-lattice refinement harness. |
| `newtonian_distance_law_confirmed` | retained_bounded | bounded_theorem | Historical headline pointer: replaced by the bounded-replay `b^(-1.17)` far-tail fit on the widened `W=12, h=0.25` valley-linear replay (z ≥ 5 window). | C | Historical import note pointing to a different replay (`VALLEY_LINEAR_WIDE_TAIL_NOTE`); not on the rescaled NN bridge. The headline itself is explicitly redirected away from the load-bearing fit. |
| `restricted_strong_field_closure_note` | retained_bounded | bounded_theorem | On the exact local `O_h` star-supported source class on a `15^3` finite box, the scalar/static-conformal sector admits an exact restricted closure: shell source `sigma_R = H_0 Pi_R^ext phi`, unique same-charge bridge `psi = 1 + phi_ext`, exact pointwise constraint lift, and minimal Schur boundary action. | C | Different harness entirely (finite-box `15^3` box with exact `O_h` star-supported source, scalar/static-conformal restricted closure). Quoted: "It does not claim a full pointwise Einstein/Regge tensor theorem." Orthogonal to the rescaled NN refinement bridge. |
| `sixth_family_sheared_fm_transfer_note` | retained_bounded | bounded_theorem | On the sixth-family parity-sheared shell connectivity rule, the rows that pass the exact gate retain near-Newtonian `F~M` weak-field linearity (mean exponent `0.999895`) across drift `0.0 .. 0.3`. | C | Sixth-family sheared-shell connectivity is a grown-DAG family, not the NN lattice. Note explicitly distinguishes itself from the original drift/restore, sector-transition, quadrant-reflection, radial-shell, and cross-quadrant load-balanced families. |
| `sixth_family_sheared_note` | retained_bounded | bounded_theorem | The sixth-family sheared-shell connectivity scout passes `12/21` rows on the exact zero / neutral / sign / weak-field charge-scaling gate, retaining a real but narrow bounded basin (mean exponent `0.999895`). | C | Same sixth-family sheared-shell harness; orthogonal to the NN refinement bridge. |
| `lattice_nn_mass_response_note` | unaudited | positive_theorem | Under the Born-safe deterministic refinement path on the raw NN lattice (rows through `h = 0.0625`), the mass response is positive but bounded/sub-linear and gravity shrinks toward zero with refinement; a narrow alpha-scaled strength law (`alpha ~ 1.5`) makes the response cleaner but does not promote `F∝M`. | B | Same rescaled NN-lattice harness as #957/#968. Quoted: "gravity still fades toward zero at the finest retained deterministic point... the response is positive but bounded/sub-linear and still refinement-sensitive." That fading is exactly the fixed-strength saturation null of #945 (`fixed-strength gravity continuum is 0`). The bound is now structurally identified. |
| `lattice_nn_rg_alpha_sweep_note` | retained_bounded | bounded_theorem | Within the `alpha ∈ {0, 0.5, 1.0, 1.5}` sweep on `strength = s0 / h^alpha` for the deterministic NN path, the strongest checked alpha is `1.5`, where gravity is "nearly h-independent" between `h = 0.5` and `h = 0.25` (ratio `0.858`); the result is fixed-point-style probe, not a renormalization theorem. | B | Same rescaled NN-lattice harness; the load-bearing claim is about whether spacing-dependent strength schedules stabilize the gravity response under refinement. Quoted: "the result is still a fixed-point style probe, not a promoted renormalization theorem." #945's joint `(h,s)` saturation null shows the limit is zero rather than a finite fixed point — the alpha-sweep ratio approach to `1` is a finite-h shadow of saturation, structurally identified. |
| `lattice_nn_rg_gravity_note` | retained_bounded | bounded_theorem | Simple spacing-dependent field-strength laws (`fixed`, `inv_h`, `inv_sqrt_h`) preserve a Born-clean refinement trend through `h = 0.25` but all three FAIL at `h = 0.125` in the raw kernel; the continuum / RG question is open. | B | Same rescaled NN harness; load-bearing claim is the gravity-response question Quoted: "do simple spacing-dependent field-strength laws preserve a finite gravity response under refinement... the continuum / renormalization question is still open." #945 closes that question structurally: the fixed-strength gravity continuum is `0` (saturation), and the rescaled deterministic schedule (cf. `lattice_nn_deterministic_rescale_note`) closes the `h = 0.125` FAIL. |
| `lattice_nn_rg_reconciliation_note` | unaudited | bounded_theorem | The canonical NN result is a Born-clean finite-resolution refinement trend through `h = 0.25` with `alpha = 1.5` as the strongest measured ratio (`0.858`); the stronger "alpha = 2.0", "RG solved", "fixed point established" branch-history claims are NOT supported by the current artifacts. | B | Same rescaled NN harness; load-bearing claim is the RG / continuum reconciliation. The "promotion criteria" the note lists ("a successful continuation at `h = 0.125` under the chosen scaling law", "a scaling law whose gravity trend stays stable across more than one refinement step") are now answered structurally — not with a finite RG fixed point but with #945's saturation null and #968's geodesic-operator identification. |
| `lattice_nn_deterministic_rescale_note` | retained_bounded | bounded_theorem | A fixed geometry-only rescale `step_scale = spacing / sqrt(3)` extends the raw NN lattice cleanly through `h = 0.0625` with `k=0 = 0`, Born at machine precision, MI → `1.0`, `1-pur_cl` → `0.5`, `d_TV` → `1.0`; gravity is positive on sub-`0.25` rows but shrinks toward zero. | A | This is the canonical rescaled NN-lattice harness that #957 and #968 build on. The load-bearing rows (MI, 1-pur, d_TV, Born) are exactly the continuum-stable observables now identified as the geodesic operator on the decoherence subblock by #968 (Gaussian-arm prediction matches MI / d_TV to `5e-4`). The bounded fixed-h values match the continuum-operator value to within #957's tail bound (`≤ 7.7e-3`). The vanishing-gravity caveat is the #945 saturation but the dominant load-bearing claim is the Born-clean rescaled refinement path itself, which is promotable. |
| `continuum_bridge_note` | audited_conditional | bounded_theorem | Across DAG families (modular, hierarchical, preferential-attachment, etc.) and lattices, gravity / Born / CL purity / 3D mass-scaling survive size growth; strict visibility gain, 4D `F~M`, asymptotic emergence, and 1/L gravity do not; lattice continuum limit (MI, decoherence, d_TV) converges. | C | Multi-architecture Gate-C survey covering random DAGs, mirror DAGs, modular families, and lattices. The "lattice continuum limit" sub-section is consistent with #957/#968 but the row's load-bearing claim is the broader survival-vs-finite-size taxonomy rather than the rescaled NN-lattice operator-Cauchy result. The note already explicitly distinguishes lattice-specific from random-DAG behavior; #957/#968 do not change the survey's load-bearing claims. |
| `mirror_2d_gravity_law_note` | unaudited | bounded_theorem | On the exact 2D mirror primary runner across `N ∈ {25,40,60,80,100}`, the gravity-side scaling fits are weak (`gravity = 6.48 N^-0.210`, `R^2 = 0.168`; mass-window `delta ~ 0.872 M^0.132`, `R^2 = 0.167`; distance-tail `delta ~ 0.342 b^0.320`, `R^2 = 0.075`), so no clean 2D mirror mass law and no clean 2D mirror distance law are supported. | C | Different harness (exact 2D mirror linear propagator, not the rescaled NN lattice). The load-bearing claim is a bounded null on the 2D mirror primary runner; #957/#968 are about the NN-lattice rescaled refinement and have no implication for the 2D mirror fit qualities. |

## Constraints honored

- This document does **not** modify any source note or `docs/audit/data/audit_ledger.json`.
- This document does **not** promote rows in the ledger; it is a recommendation
  for a downstream re-audit step.
- All 19 listed `claim_id`s are present in the ledger and were classified from
  their actual source notes.

[https://claude.ai/code/session_015mocy1jaZodDXSwpnZypjH](https://claude.ai/code/session_015mocy1jaZodDXSwpnZypjH)
