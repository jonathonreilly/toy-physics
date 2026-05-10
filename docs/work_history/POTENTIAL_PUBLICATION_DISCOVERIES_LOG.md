# Historical Potential Publication Discoveries Log

---

**This is a historical planning inventory / discovery-log note. It
does not establish any retained claim and does not assert audit-row
status for any listed item.**
For retained claims on individual discoveries, see the per-discovery
notes referenced from the `## Audit scope` block below.

---

**Date opened:** 2026-04-11
**Status:** support / historical planning inventory record only — does not propagate retained-grade
**Claim type:** meta
**Claim scope:** support / historical planning inventory record only — does not propagate retained-grade
**Audit authority:** independent audit ledger only; this source does not set an audit verdict.
**Propagates retained-grade:** no
**Proposes new claims:** no
**Purpose:** cumulative repo-wide log of results that look novel, publishable,
or methodologically important enough to preserve for future paper planning.

This is **not** a paper outline and **not** a claim that every item below is
already publication-ready. It is a running inventory of findings worth keeping
visible when paper planning starts.

## Audit scope (relabel 2026-05-10)

This file is a **historical planning inventory / discovery-log
note**. It is **not** a single retained theorem and **must not** be
audited as one. The audit ledger row for
`work_history.potential_publication_discoveries_log` classified this
source as conditional/open_gate with auditor's repair target:

> either gate this work-history inventory out of the audit ledger
> or register/verify the cited evidence notes and runners item by
> item.

The minimal-scope response in this PR is to **relabel** this document
as a historical planning inventory record rather than to register and
verify each cited evidence note and runner item-by-item here. That
verification belongs in a dedicated review-loop or per-D-item audit
pass. Until that work is done:

- This file makes **no** retained-claim assertions of its own.
- The whole-repo D01–D45 ledger, per-item discovery descriptions,
  per-item lane assignments, per-item status labels (`retained`,
  `bounded-retained`, `methodological`, `negative-result`,
  `exploratory-lead`), and "Why it matters" / "Evidence" columns
  below are **historical planning-inventory memory only**.
- The note's status labels are **historical discovery-log labels,
  not the publication-capture dispositions used in
  `PUBLICATION_MATRIX.md`**.
- The retained-status surface for any individual discovery is the
  audit ledger (`docs/audit/AUDIT_LEDGER.md`) plus the per-discovery
  notes cited in each row's Evidence column, **not** this discovery
  log.
- Retained-grade does **NOT** propagate from this discovery log to
  any individual D-item, status label, or successor paper-planning
  pass.

For any retained claim about a listed discovery, audit the
corresponding dedicated evidence note and its runner as a separate
scoped claim — not this historical planning inventory.

---

See also:

- [`repo/review_feedback/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md`](repo/review_feedback/PUBLICATION_DISCOVERY_AUDIT_2026-04-11.md) for the historical lane-by-lane critical audit of what was safe to treat as a paper candidate during the review pass.
- [`../repo/CONTROLLED_VOCABULARY.md`](../repo/CONTROLLED_VOCABULARY.md) for the repo-wide status taxonomy.

## Inclusion Rule

An item belongs here only if it is at least one of:

- a retained positive result with possible publication value
- a strong methodological contribution
- a strong negative/diagnostic result that teaches something structural
- an exploratory quantitative lead that looks strong enough to track

Every item should point to a retained note or runner.

## Status Legend

These are historical discovery-log labels, not the publication-capture
dispositions used in `PUBLICATION_MATRIX.md`.

- `retained`
- `bounded-retained`
- `methodological`
- `negative-result`
- `exploratory-lead`

## Whole-Repo Ledger

| ID | Discovery | Lane | Status | Why it matters | Evidence |
|---|---|---|---|---|---|
| D01 | Exact mirror coexistence pocket: Born-clean, gravity-positive, and nontrivial MI/decoherence on the same graph family | mirror | `bounded-retained` | One of the strongest same-graph coexistence results in the repo and a historically important architecture result | [`UNIFIED_PROGRAM_NOTE.md`](UNIFIED_PROGRAM_NOTE.md), [`MIRROR_2D_VALIDATION_NOTE.md`](MIRROR_2D_VALIDATION_NOTE.md) |
| D02 | Higher-symmetry `Z2 x Z2` extension keeps Born-clean behavior, positive gravity read, and stronger decoherence/range than exact mirror on the tested dense probe | mirror / higher symmetry | `bounded-retained` | Shows the coexistence story is not unique to one exact mirror family | [`HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md`](HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md) |
| D03 | Structured chokepoint bridge: structured/generated placement survives the canonical mirror readout on a narrow retained slice | generated symmetry bridge | `bounded-retained` | Converts an older “negative/open” generated-symmetry story into a real but narrow bridge result | [`STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md`](STRUCTURED_CHOKEPOINT_BRIDGE_NOTE.md) |
| D04 | 3D dense spent-delay ordered-lattice branch keeps a real attractive window with Born / MI / decoherence on the same family | ordered lattice | `bounded-retained` | Important historical result because it showed the older ordered-lattice lane had a real 3D positive pocket, not just 2D behavior | [`LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md`](LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md) |
| D05 | Nearest-neighbor refinement bridge: weak-field/Born structure survives refinement and deterministic rescale out to finer `h` | ordered lattice / continuum bridge | `bounded-retained` | One of the strongest older continuity/refinement bridges in the repo | [`CONTINUUM_BRIDGE_NOTE.md`](CONTINUUM_BRIDGE_NOTE.md) |
| D06 | Valley-linear action-law fork improves the tested mass-law exponent and tail behavior on a fixed retained ordered-lattice family while preserving Born and TOWARD sign | action-law | `bounded-retained` | Clean same-family action-law comparison; plausible paper-shaped result even if not universal | [`VALLEY_LINEAR_ACTION_NOTE.md`](VALLEY_LINEAR_ACTION_NOTE.md) |
| D07 | Coin mixing-period diagnosis: chromaticity, equivalence problems, and long-time gravity failures in coin-based/chiral/Dirac-walk lanes trace back to the coin mixing period | coin / chiral / Dirac-walk | `negative-result` | Strong cross-architecture negative result; likely publishable as a design/diagnostic lesson | [`CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md`](CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md) |
| D08 | Exact-force vs centroid lesson on staggered lattices: centroid can oscillate with permanent lattice artifacts while exact lattice force remains stable | staggered methodological core | `methodological` | Important measurement contribution; changed how gravity should be measured on the staggered lane | [`STAGGERED_FERMION_CARD_2026-04-10.md`](STAGGERED_FERMION_CARD_2026-04-10.md), [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md) |
| D09 | Parity-coupling correction for staggered scalar gravity: the correct scalar coupling is through the same parity factor as the mass term, not an identity shift | staggered methodological core | `methodological` | Major correction that fixed the coupling convention and materially changed the physical interpretation of the staggered lane | [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md), [`TWO_SIGN_COMPARISON_NOTE_2026-04-10.md`](TWO_SIGN_COMPARISON_NOTE_2026-04-10.md) |
| D10 | Force-based canonical staggered card: parity-coupled staggered Dirac closes the retained 17-card at 1D and 3D operating points, with full-suite baseline `29/38` in 1D and `28/38` in 3D | staggered | `retained` | Current strongest retained architecture package in the repo | [`STAGGERED_FERMION_CARD_2026-04-11.md`](STAGGERED_FERMION_CARD_2026-04-11.md) |
| D11 | Graph portability: the staggered lane survives on admissible bipartite irregular graph families instead of only on periodic cubic lattices | staggered graph portability | `retained` | Important portability result; shows the mainline architecture is not just a regular-lattice artifact | [`STAGGERED_GRAPH_PORTABILITY_NOTE.md`](STAGGERED_GRAPH_PORTABILITY_NOTE.md), [`STAGGERED_GRAPH_PORTABILITY_STRESS_NOTE.md`](STAGGERED_GRAPH_PORTABILITY_STRESS_NOTE.md) |
| D12 | Native gauge/current on irregular graph cycles via persistent-current / flux response on real graph loops | staggered graph gauge | `retained` | Strong graph-native gauge result, especially because it works on irregular cycle-bearing families rather than only on rings/torii | [`CYCLE_BATTERY_NOTE_2026-04-10.md`](CYCLE_BATTERY_NOTE_2026-04-10.md), [`STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md`](STAGGERED_GRAPH_GAUGE_CLOSURE_RESULTS_2026-04-10.md) |
| D13 | Endogenous self-gravity contraction on graphs: under parity coupling, self-gravity no longer expands the packet and instead contracts it across retained cycle-bearing families | staggered self-gravity | `retained` | First real endogenous self-field result in the current mainline; materially stronger after parity coupling fix | [`CYCLE_BATTERY_NOTE_2026-04-10.md`](CYCLE_BATTERY_NOTE_2026-04-10.md), [`SELF_GRAVITY_SCALING_NOTE_2026-04-10.md`](SELF_GRAVITY_SCALING_NOTE_2026-04-10.md) |
| D14 | Two-field wave coupling on graphs: a separate dynamical `Phi` field with wave-law evolution can remain bounded while `psi` stays exactly norm-preserving on retained families, but the clean-family rerun leaves only partial `W6` closure (`2/3`, `3/3`, `2/3`) | staggered two-field | `bounded-retained` | Still methodologically important because it moves the program from static/background fields toward genuine interacting field dynamics, but it is no longer a fully retained family-robust result | [`STAGGERED_TWO_FIELD_WAVE_NOTE.md`](STAGGERED_TWO_FIELD_WAVE_NOTE.md) |
| D15 | Retarded/hybrid family closure: one operating-point sibling closes the cycle-bearing families and carries a layered DAG-derived control at `8/9`, with the source-scale gap reduced to `G_eff ~ 0.4–0.7` | staggered two-field / retarded | `bounded-retained` | Strong interacting-field structural result, even though directional gravity off-lattice is still not frozen and the layered control is not a genuinely directed-DAG closure | [`TWO_FIELD_RETARDED_FAMILY_CLOSURE_NOTE_2026-04-10.md`](TWO_FIELD_RETARDED_FAMILY_CLOSURE_NOTE_2026-04-10.md) |
| D16 | Layered DAG-derived control: staggered transport and the structural battery survive on layered acyclic templates with forward-depth bias and exact norm/Born behavior, but only after symmetrizing the adjacency | staggered DAG-like control | `bounded-retained` | Still useful because it shows the mainline architecture is not restricted to periodic lattices, but it is no longer honest to treat this as a genuinely directed causal-DAG result | [`STAGGERED_DAG_NOTE_2026-04-10.md`](STAGGERED_DAG_NOTE_2026-04-10.md) |
| D17 | Historical off-lattice same-surface sign-selection failures: off-center and transport-style irregular probes failed clean closure and narrowed the search to the later retained core-packet surface | staggered sign audit | `negative-result` | Still a valuable blocker history because it explains why the bounded irregular sign result is interpreted narrowly rather than as universal off-lattice directional closure | [`IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md`](IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md), [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md) |
| D18 | Topology-dependent onset behavior / critical-exponent hint: fitted onset exponents vary strongly across admissible graph families | staggered critical behavior | `exploratory-lead` | Quantitative lead with possible universality-class significance, but not yet a frozen full scaling law | [`CRITICAL_EXPONENTS_TOPOLOGY_NOTE_2026-04-10.md`](CRITICAL_EXPONENTS_TOPOLOGY_NOTE_2026-04-10.md) |
| D19 | Emergent-geometry growth partial reopen: matter-coupled growth can reshape coarse geometry and reopen a narrow strong-coupling toward window | emergent geometry | `exploratory-lead` | Could become a geometry paper or a strong bounded note, but currently too seed-/coupling-sensitive to promote | [`EMERGENT_GEOMETRY_GROWTH_NOTE_2026-04-10.md`](EMERGENT_GEOMETRY_GROWTH_NOTE_2026-04-10.md) |
| D20 | Bounded chiral-walk positive package: 1+1D closes exact low-k KG, strict light cone, Born-clean barrier behavior, and strong U(1) gauge response; 2+1D retains approximate KG and strong AB modulation | coin / chiral | `bounded-retained` | The coin/chiral lane is not only a negative diagnosis. In 1+1D and 2+1D it contains a real, historically important positive package that is still worth paper planning, provided the 3+1D claims stay narrowed and achromatic gravity is not overclaimed | [`CHIRAL_WALK_SYNTHESIS_2026-04-09.md`](CHIRAL_WALK_SYNTHESIS_2026-04-09.md), [`CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md`](CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md) |
| D21 | Generated-geometry transfer package: on a retained moderate-drift grown row, Born, `d_TV`, `MI`, decoherence, and far-field gravity transfer closely from the exact grid to the grown geometry | generated geometry / Gate B | `bounded-retained` | This is the cleanest historical result showing that a grown geometry can inherit a substantial part of the exact-grid observational package without immediately destroying the interference structure | [`GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](GATE_B_GROWN_JOINT_PACKAGE_NOTE.md), [`GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](GATE_B_GROWN_DISTANCE_LAW_NOTE.md) |
| D22 | Bounded staggered branch-superposition result: on a fixed 2D staggered lattice, coherent flat-vs-screened-field branching produces a detector-resolved effect distinct from the corresponding classical mixture, while 1D controls remain null | staggered branch superposition | `bounded-retained` | This is the first bounded geometry/field-branch superposition result on the current staggered Hamiltonian rather than the older path-sum ensemble lane | [`STAGGERED_GEOMETRY_SUPERPOSITION_NOTE_2026-04-11.md`](STAGGERED_GEOMETRY_SUPERPOSITION_NOTE_2026-04-11.md) |
| D23 | Simple self-gravity bipartition entropy is not an area-law instrument: the single-particle entropy is bounded by `ln(2)` and dominated by subsystem occupancy rather than boundary size | staggered entropy audit | `negative-result` | Useful publication-grade negative result because it rules out an easy overclaim and cleanly points future holography arguments toward the stronger many-body / Dirac-sea route | [`SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md`](SELF_GRAVITY_ENTROPY_NOTE_2026-04-11.md) |
| D24 | Dirac-sea boundary-law probe: on the 2D periodic staggered lattice, entanglement entropy from the filled negative-energy sector scales more cleanly with boundary size than with region volume in both the free and self-gravitating cases, and the audited BFS-ball robustness surface gives `100/100` fits above `R^2=0.95` with explicit caveats | staggered many-body boundary law | `bounded-retained` | Strong many-body-style boundary-law result, with gravity preserving the boundary-law preference while shifting the fitted coefficient; valuable for future holography triage without overclaiming AdS/CFT | [`HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md), [`BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md`](BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md) |
| D25 | Screened ring-memory diagnosis: the original `N=61` retarded pulse signal is real on its narrow protocol, but the later `mu^2` / geometry sweep shows the size-fragility is not purely Yukawa-range driven | staggered retarded field memory | `negative-result` | Worth preserving as a sharp diagnostic result: the original protocol is still not a stable graph-family memory observable, but the follow-up sweep shows geometry scaling and boundary placement matter at least as much as screening | [`GRAVITATIONAL_MEMORY_NOTE_2026-04-11.md`](GRAVITATIONAL_MEMORY_NOTE_2026-04-11.md), [`MEMORY_DECAY_DIAGNOSIS_2026-04-11.md`](MEMORY_DECAY_DIAGNOSIS_2026-04-11.md), [`MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md`](MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md) |
| D26 | Branch-mediated entanglement on an externally imposed two-branch protocol: on a fixed 2D staggered lattice with an externally imposed geometry/source branch, the coherent branch superposition entangles two separated particles beyond the corresponding classical mixture, with `delta_S > 0` on the audited robustness surface | staggered branch-mediated entanglement | `bounded-retained` | Strong positive branch-mediated entanglement result with exact norm conservation; the robustness harness turns this from a single sweep into a stable bounded side result without promoting a full BMV / mediator-null witness | [`BMV_ENTANGLEMENT_NOTE_2026-04-11.md`](BMV_ENTANGLEMENT_NOTE_2026-04-11.md), [`BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md`](BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md) |
| D27 | Weak-coupling irregular-graph sign-sensitive regime: at `G=5,10`, attractive parity coupling produces a uniformly larger shell-force TOWARD count than repulsive parity coupling across the audited irregular graph surface, while secondary gap tallies remain eigensolver-sensitive | staggered weak-coupling sign sensitivity | `bounded-retained` | Preserves the strongest stable off-lattice sign-sensitive result without overstating full directional closure at all operating points | [`WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md`](WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md) |
| D28 | Three-body branch-mediated entanglement: on the audited fixed-adjacency two-branch staggered-lattice protocol, three separated probes develop robust **W-type** tripartite branch entanglement, with `tau_3 = 0` and `W/W-asym` classification in `25/25` configurations | staggered tripartite branch entanglement | `bounded-retained` | Clean bounded extension of the two-body branch-entanglement story after retiring the stale GHZ reading; useful for paper triage without overclaiming a multipartite BMV witness | [`BMV_THREEBODY_NOTE_2026-04-11.md`](BMV_THREEBODY_NOTE_2026-04-11.md), [`BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md`](BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md) |
| D29 | Open-boundary Wilson two-orbital mutual attraction: the two-body channel survives on larger open 3D Wilson lattices with clean `shared` vs `self_only` separation, and the default screened law is steep but screen-controlled | Wilson two-body | `bounded-retained` | First genuinely clean two-orbital mutual-attraction channel in the repo that survives removal of the periodic small-box sign flip; the follow-up `mu^2` sweep shows the exponent moves toward Newton as screening is reduced | [`WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`](WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md), [`WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md`](WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md) |
| D30 | Anderson-vs-gravity phase window plus eigenvalue-statistics negative result: gravity is most cleanly distinguishable from matched disorder in a finite perturbative window, while no chaos transition appears in the audited spacing statistics | staggered Anderson / spectral diagnostics | `bounded-retained` | Sharpens the older Anderson control into a real phase-window map and pairs it with a clear spectral negative result that supports the repo-wide “spectral, not chaotic” picture | [`EIGENVALUE_ANDERSON_PHASE_NOTE_2026-04-11.md`](EIGENVALUE_ANDERSON_PHASE_NOTE_2026-04-11.md) |
| D31 | Wilson screening-mass sweep: the open-lattice distance exponent softens from `-3.290` at `mu^2=0.22` toward `-1.857` at `mu^2=0.0`, so the steep exponent is largely screening-controlled rather than a fixed discrete law | Wilson two-body / screening control | `bounded-retained` | Key calibration result: the mutual channel is real, but the steep exponent is not stable under screening removal and approaches Newtonian scaling as screening vanishes | [`WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md`](WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md) |
| D32 | Memory `mu^2` / geometry sweep: the original ring-memory signal is protocol-sensitive, but the later fixed-geometry slice survives and grows with `N`, so the failure is not primarily a Yukawa-range artifact | staggered retarded field memory | `negative-result` | Important narrowing result: the original size-fragility is driven at least as much by geometry scaling / boundary placement as by screening, so the memory lane remains exploratory rather than a pure screening no-go | [`MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md`](MEMORY_MU2_GEOMETRY_SWEEP_NOTE_2026-04-11.md), [`MEMORY_DECAY_DIAGNOSIS_2026-04-11.md`](MEMORY_DECAY_DIAGNOSIS_2026-04-11.md) |
| D33 | Potential-weighted Ollivier curvature proxy: on the screened periodic staggered torus, `Delta_kappa ~ G*T` survives corrected wraparound weights and strongly beats random/shuffled `Phi` controls, but a fixed initial-source potential reproduces an increasing fraction of the same signal | staggered curvature proxy | `bounded-retained` | Retains a real linearized curvature-density proxy while explicitly ruling out the stronger “Einstein equation derived” overclaim | [`OLLIVIER_EINSTEIN_PROXY_NOTE_2026-04-11.md`](OLLIVIER_EINSTEIN_PROXY_NOTE_2026-04-11.md) |
| D34 | Open-cubic staggered trajectory Newton reproduction: on the primary staggered architecture, a blocked envelope observable on an open 3D cubic surface reproduces a Newton-compatible external-source distance law, and the companion blocking-sensitivity sweep shows the near-Newton exponent survives sensible parity-suppressing readouts but fails under over-coarsening | staggered open-cubic trajectory | `bounded-retained` | Important because it shows Wilson is not the only architecture with a Newton-compatible trajectory-side distance law, while keeping the claim bounded to an external-source, open-cubic, blocked-observable surface | [`STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md`](STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md), [`STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md`](STAGGERED_NEWTON_BLOCKING_SENSITIVITY_NOTE_2026-04-11.md) |
| D35 | 3D staggered self-gravity contraction / sign split: the primary staggered architecture has a clean blocked-envelope 3D self-gravity contraction observable, while the matched sign-flip control remains a clean negative for trajectory-side sign closure on the same centered surface | staggered 3D trajectory self-gravity | `bounded-retained` | Worth preserving because it adds a real 3D trajectory-level positive on the main architecture without overclaiming that sign-selective trajectory gravity is solved | [`STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md`](STAGGERED_3D_SELF_GRAVITY_SIGN_NOTE_2026-04-11.md) |
| D36 | Open-cubic staggered self-consistent two-body partner-force channel: on the primary staggered architecture, two separate orbitals sourcing one shared Poisson field produce a clean attractive partner-force law with a near-Newton distance exponent on the calibrated open-cubic surface, while the blocked trajectory channel remains noisy | staggered self-consistent two-body | `bounded-retained` | Worth preserving because it lifts the primary staggered lane from external-source-only trajectory reproduction to a genuine self-consistent two-body force positive without overclaiming trajectory or both-masses closure | [`STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md`](STAGGERED_SELF_CONSISTENT_TWO_BODY_NOTE_2026-04-11.md) |
| D37 | Unscreened Anderson companion on the corrected torus: lowering `mu2` to `0.001` preserves and numerically strengthens the gravity-vs-disorder boundary-law separation on the corrected periodic 2D surface, while changing the interpretation from a narrow perturbative window to a low-variance low-`alpha` offset | staggered Anderson / spectral diagnostics | `bounded-retained` | Worth preserving because it shows the corrected torus disorder-separation lane survives unscreening, but only as a bounded periodic-surface companion with weak sign discrimination | [`ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md`](ANDERSON_PHASE_MU2_0001_NOTE_2026-04-11.md) |
| D38 | Wilson test-mass / continuum companion: on the low-screening open-Wilson surface, the test-mass limit closes exact source-mass scaling while the same-convention continuum extrapolation drives the mutual-channel distance exponent to `-2.009 +/- 0.019` | Wilson test-mass / continuum | `bounded-retained` | Strengthens the Wilson lane materially without overclaiming full both-masses Newton closure; preserves the cleanest bounded Wilson evidence for a Newton-compatible weak-field limit | [`WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`](WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md) |
| D39 | Open-cubic staggered weak-field test-mass/source-mass companion: on the primary staggered architecture, a static-source companion closes exact source-mass scaling in the force observable and near-linear source scaling in the blocked-envelope trajectory observable across the audited side/separation surface | staggered weak-field source-mass companion | `bounded-retained` | Worth preserving because it gives the primary architecture a clean weak-field source-mass companion without overclaiming both-masses closure, self-consistent transfer, or a standalone distance law | [`STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md`](STAGGERED_TEST_MASS_COMPANION_NOTE_2026-04-11.md) |
| D40 | 3D path-sum distance continuation: a single 64^3 path-sum family gives a bounded numerical continuation of the distance-law story, with finite-size extrapolation approaching a Newton-compatible weak-field trend on this surface | path-sum distance continuation | `bounded-retained` | Worth preserving as a narrow continuation note because the trend is clean, but it remains boundary-sensitive and lacks frozen/static control, portability, and both-masses closure | [`DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md`](DISTANCE_LAW_3D_64_CLOSURE_NOTE_2026-04-11.md) |
| D41 | Newtonian mass scaling from four principles: on the retained ordered-lattice family, linear amplitude propagation, phase valley, additive one-parameter mass, and momentum conservation select `p = 1`, while the persistent-pattern inertial-mass step remains open | ordered-lattice derivation | `bounded-retained` | Worth preserving because it turns the mass-scaling story into an explicit bounded derivation candidate rather than a loose heuristic, while keeping the open persistent-pattern step visible | [`NEWTON_DERIVATION_NOTE.md`](NEWTON_DERIVATION_NOTE.md) |
| D42 | Bounded irregular core-packet same-surface sign separator: on the audited irregular bipartite families, a centered non-oscillating core packet separates attractive from repulsive parity coupling at both `mu^2 = 0.1` and `mu^2 = 0.001`, with a minimum positive-margin fraction of `93.3%` across the ball/depth observables | staggered irregular sign separator | `bounded-retained` | First bounded same-surface irregular sign closure in the repo that survives both screening levels without leaning on cubic exact-force semantics; still intentionally narrow to one packet/observable family | [`IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`](IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md) |
| D43 | Emergent cross-field product-law companion: on the audited open 3D staggered cross-field Poisson surface, the mutual force scales as `F ~ M_A^1.0146 M_B^0.9863` with `R^2 = 0.999993`, and the frozen-source control stays essentially identical | staggered cross-field product law | `bounded-retained` | Worth preserving because it is the first audited surface in the repo where the `M_A M_B`-style scaling is not explicit in the Hamiltonian and is instead recovered from field linearity; still bounded to one open 3D staggered surface and not full Newton closure | [`EMERGENT_PRODUCT_LAW_NOTE.md`](EMERGENT_PRODUCT_LAW_NOTE.md), [`EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md`](EMERGENT_PRODUCT_LAW_AUDIT_2026-04-11.md) |
| D44 | Architecture portability companion for source-mass scaling and attraction: ordered 3D cubic, staggered 3D cubic, Wilson 3D cubic, and a 2D random geometric control row all preserve `beta ~ 1` and attractive sign on the audited surface | cross-architecture source-mass portability | `bounded-retained` | Worth preserving because it shows the source-mass law and attractive sign are not tied to one lattice convention, while keeping the 2D irregular row explicitly mass-only and avoiding any architecture-independent Newton-closure overclaim | [`ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md`](ARCHITECTURE_PORTABILITY_SWEEP_NOTE.md), [`repo/review_feedback/ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md`](../../archive_unlanded/work-history-unverifiable-portability-2026-04-30/ARCHITECTURE_PORTABILITY_AUDIT_2026-04-11.md) |
| D45 | Bounded graph-first gauge closure on `CI(3)` / `Z^3`: exact native `Cl(3)` / `SU(2)`, a derived graph-first weak-axis selector on the canonical cube shifts, and structural `su(3)` closure with bounded left-handed `+1/3` / `-1` abelian matching | CI(3) / `Z^3` gauge structure | `bounded-retained` | Worth preserving because it closes the structural color algebra on a replayable graph-first surface while keeping anomaly-complete hypercharge and downstream phenomenology explicitly bounded | [`NATIVE_GAUGE_CLOSURE_NOTE.md`](NATIVE_GAUGE_CLOSURE_NOTE.md), [`GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md`](GRAPH_FIRST_SELECTOR_DERIVATION_NOTE.md), [`GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`](GRAPH_FIRST_SU3_INTEGRATION_NOTE.md) |

## What This Log Is Not Saying

- It is **not** saying every item above belongs in the same paper.
- It is **not** saying every item is equally strong.
- It is **not** replacing the retained matrix or the lane board.

Use this log when asking:

- what discoveries are worth preserving for paper planning?
- which results are methodological vs physical vs negative?
- which older lanes still contain paper-grade findings even if they are not the
  current default architecture?

## Maintenance Rule

When a new result looks paper-grade, add it here only after it has:

1. a runner,
2. a retained note or bounded note,
3. a lane assignment,
4. and a status label.
