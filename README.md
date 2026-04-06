# Discrete Event-Network Toy Model

This repository is an attempt to build a toy physics model while stripping away as much human observational bias as possible from the starting assumptions.

The motivating question is:

> If we do **not** start by assuming smooth space, continuous time, point particles, or measurement as primitive, how much physics-like structure can still be recovered from a much smaller event-and-relation ontology?

## Why This Project Exists

Most physical theories are written in a language that is already heavily shaped by human perception:

- we naturally think in terms of objects moving in space
- we picture time as a universal flowing background
- we often treat geometry as given before anything happens inside it
- we describe measurement using concepts that already assume observers, apparatus, and stable classical records

This project started by trying to remove some of that built-in bias.

So instead of beginning with particles in a pre-existing spacetime, the toy begins with a much thinner picture:

- discrete events
- local influence links between events
- persistence
- compatibility
- durable records

From there, the question is whether anything recognizably physics-like can emerge:

- effective geometry
- causal order
- inertial continuation
- gravity-like path bending
- measurement-like suppression of alternatives

## Core Axioms

These are the conceptual axioms the toy is built around.

1. **Reality is an evolving network of events and influence relations.**  
   The primitive layer is not particles in a container. It is a changing relational graph of events and allowed local influences.

2. **Stable objects are persistent self-maintaining patterns in that network.**  
   What looks object-like at larger scales is modeled as a pattern that keeps reproducing its own local structure over time.

3. **Space is inferred, not assumed.**  
   Spatial structure is reconstructed from influence neighborhoods and signal-delay structure rather than taken as fundamental.

4. **Duration is local update count, not universal background time.**  
   Time is treated as something measured along histories and persistent patterns, not as a globally imposed external clock.

5. **The arrow of time is tied to durable record formation.**  
   Time-asymmetry is connected to the growth of persistent, non-erasable records rather than inserted as a separate metaphysical primitive.

6. **Free systems follow the locally simplest admissible continuation.**  
   In the absence of strong disturbances, the system prefers locally coherent continuations rather than arbitrary jumps.

7. **Inertia is undisturbed natural continuation.**  
   What looks like inertial motion is the toy version of persistence of local continuation when nothing distorts the surrounding continuation structure.

8. **Gravity is natural continuation in a distorted continuation structure.**  
   Gravity-like behavior is modeled not as a force added by hand, but as path selection through a locally altered delay/load landscape.

9. **Measurement is durable record formation that separates alternatives.**  
   Alternatives may coexist or combine when no durable record separates them; once a durable record forms, those alternatives are no longer treated the same way.

10. **Observed large-scale structure should be explained by persistent local mechanisms wherever possible.**  
    If a geometry-like or measurement-like effect appears, the preferred explanation is that it emerged from local network structure rather than being imposed from outside.

## What The Toy Actually Is

The implemented model uses:

- events as nodes
- directed local influence links
- delay-like and compatibility-like quantities on those links
- persistent patterns that act as local sources of structure
- admissible histories through the resulting network
- path-selection rules defined on the continuation landscape
- durable-record sectors in interference-style toy setups

In this formulation, geometry-like behavior is associated with the continuation structure induced by persistence and delay, rather than with a fixed background geometry.

## Analysis Program

The analysis layer measures:

- geometry and profile observables
- boundary roughness and cavity structure
- degree and neighborhood structure
- local bridge/support topology
- overlap, suppressor, and transfer behavior

These observables are used to compare mechanisms across benchmark scenarios, generated families, perturbation ensembles, and frozen-frontier subsets.

The current analysis path has been hardened against:

- benchmark/reporting mismatches
- stale helper logic
- duplicated selectors
- duplicated rule evaluators
- transfer scripts using slightly different input slices
- feature helpers that were silently double-counting

The current mechanism claims are based on that corrected analysis layer.

## Current Results

The model presently supports the following claims.

### 0. Architecture snapshot (2026-04-04)

If you only want the current high-level state, read this section first.

- **Flagship program:** exact mirror / exact 2D mirror / `Z2 x Z2`. This is
  the retained same-graph coexistence story: Born-clean at machine precision,
  positive gravity on bounded windows, and nontrivial MI / decoherence on the
  same graphs. Mirror remains the main architecture to lead with. See
  [UNIFIED_PROGRAM_NOTE.md](/Users/jonreilly/Projects/Physics/docs/UNIFIED_PROGRAM_NOTE.md)
  and
  [MIRROR_VS_LATTICE_PROGRAM_NOTE.md](/Users/jonreilly/Projects/Physics/docs/MIRROR_VS_LATTICE_PROGRAM_NOTE.md).
- **Ordered lattice:** retained secondary branch. The standard-strength branch
  is a same-family two-harness bridge, the weak-field reopening gives a narrow
  one-card pocket, the 3D dense spent-delay branch now adds a bounded
  same-family attractive window that is hierarchy-clean on the retained tested
  `z = 2..6` slice, and the no-barrier branch retains the cleanest current
  distance-law magnitude. The corrected `h = 1.0` vs `h = 0.5` refinement
  reconciliation is now explicitly negative: the older positive-refinement
  narrative does not survive physical re-mapping. A separate y-tapered 3D
  refinement branch was tested and did not recover hierarchy-clean attraction
  under `h = 1.0` or `h = 0.5`, so it stays a bounded negative topology
  branch. A genuinely wider dense `h = 0.125` replay is now also a bounded
  negative on the retained tested row: the first `phys_w = 4`, `phys_l = 6`,
  full-window width rescue stays Born-clean, keeps clean `k = 0`, and lands
  at `alpha = 0.499`, essentially identical to the fixed-family `~0.5` limit,
  so simple box widening does not reopen the weak-field mass-law bridge. The
  ordered-lattice family is real, but it does not displace the mirror
  flagship.
- **Nearest-neighbor refinement:** strongest current continuum-side bridge.
  Raw NN is Born-clean through `h = 0.25`, deterministic rescale extends a
  bounded path to `h = 0.0625`, and the canonical notes keep continuum / RG
  claims narrow. This is a refinement bridge, not a finished theorem.
- **Generated-symmetry bridge:** reopened in a bounded way. The new
  structured chokepoint bridge shows that structured placement can survive the
  canonical mirror readout while staying Born-clean and gravity-positive on a
  narrow retained slice. That is a real bridge result, but not yet a
  replacement flagship.
- **Complex-action carryover:** bounded grown-row companion. The exact-lattice
  complex-action harness now has one retained generated-geometry companion on
  the moderate-drift Gate B row: exact `gamma = 0` reduction holds, the grown
  Born proxy stays machine-clean (`|I3|/P = 1.456e-15`), weak-field `F~M`
  stays at `1.000` on the checked sweep, and the `TOWARD -> AWAY` crossover
  survives. This is a row-level transfer result, not a geometry-generic or
  continuum claim.
- **Action-power branch:** exploratory axiom fork. It has a same-harness 2D
  comparison, a retained 3D close-slit barrier Born / MI / decoherence card,
  and a retained 3D no-barrier distance / mass-response companion. The current
  ordered 3D barrier family still fails to recover attraction toward mass, so
  this remains a bounded complementary branch rather than a replacement for
  the spent-delay lane.
- **Valley-linear action fork:** bounded action-law fork on the ordered-lattice
  `1/L^2` family. A same-family comparison against spent-delay is now
  artifact-backed on `main`: on the retained `h = 0.25` family it improves the
  tested mass-law exponent and distance-tail slope while preserving Born and
  the TOWARD sign, but the gravity magnitude is much smaller on the tested
  `z=3` slice and convergence remains open. The theory-side read for this lane
  is also sharper now: bounded equivalence, momentum, and composite-source
  harnesses support a conditional `p = 1` selection story on the fixed 3D
  family, but persistent-pattern inertial mass remains open, so this is still
  a characterization result rather than a closed first-principles derivation.
- **Dimension-dependent kernel branch:** exploratory propagator fork on the
  ordered-lattice family. The imported `1/L^(d-1)` results are scientifically
  interesting and now live on `main`, including a frozen `h = 0.25`
  eight-property 3D card, but they are still bounded: persistence evidence is
  stronger than before, while transfer-norm selection and long-range asymptotic
  wording are still under reconciliation. This is frontier work, not yet part
  of the canonical top-line claim surface.
- **Main open problem:** generated symmetry and stronger continuum closure.
  The project now has a cleaner map, and one retained moderate-drift
  generated-geometry row now survives one refinement step (`h = 0.5 -> 0.25`)
  on the ordered-lattice far-field family, but broader Gate B closure and
  stronger continuum / RG closure remain open.

If you are picking up the repo fresh, start with
[START_HERE.md](/Users/jonreilly/Projects/Physics/docs/START_HERE.md).

If you want the deliberately adversarial external-reception read rather than
the internal science map, also read
[ADVERSARIAL_INTEREST_MAP.md](/Users/jonreilly/Projects/Physics/docs/ADVERSARIAL_INTEREST_MAP.md).

If you land on older exploratory drivers, use
[LEGACY_EXPLORATORY_DRIVERS_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LEGACY_EXPLORATORY_DRIVERS_NOTE.md)
as the off-ramp before treating any of them as canonical harnesses.

Unless a later section explicitly says it is a canonical retained note, treat
the architecture snapshot above plus [START_HERE.md](/Users/jonreilly/Projects/Physics/docs/START_HERE.md)
and [UNIFIED_PROGRAM_NOTE.md](/Users/jonreilly/Projects/Physics/docs/UNIFIED_PROGRAM_NOTE.md)
as the current project state. Much of the material below is historical working
context, not the promoted claim surface.

The most relevant notes for that current architecture state are:

- [ADVERSARIAL_INTEREST_MAP.md](/Users/jonreilly/Projects/Physics/docs/ADVERSARIAL_INTEREST_MAP.md)
- [UNIFIED_PROGRAM_NOTE.md](/Users/jonreilly/Projects/Physics/docs/UNIFIED_PROGRAM_NOTE.md)
- [GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md](/Users/jonreilly/Projects/Physics/docs/GRAVITY_OBSERVABLE_HIERARCHY_NOTE.md)
- [REPRODUCTION_AUDIT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/REPRODUCTION_AUDIT_NOTE.md)
- [VALLEY_LINEAR_REPRO_NOTE.md](/Users/jonreilly/Projects/Physics/docs/VALLEY_LINEAR_REPRO_NOTE.md)
- [EVOLVING_NETWORK_PROTOTYPE_NOTE.md](/Users/jonreilly/Projects/Physics/docs/EVOLVING_NETWORK_PROTOTYPE_NOTE.md)
- [LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_DENSE_SPENT_DELAY_NOTE.md)
- [LATTICE_3D_DENSE_REFINEMENT_RECONCILIATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LATTICE_3D_DENSE_REFINEMENT_RECONCILIATION_NOTE.md)
- [LATTICE_DISTANCE_LAW_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LATTICE_DISTANCE_LAW_NOTE.md)
- [LATTICE_FAMILY_VALIDATION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LATTICE_FAMILY_VALIDATION_NOTE.md)
- [SYNTHESIS_NOTE.md](/Users/jonreilly/Projects/Physics/docs/SYNTHESIS_NOTE.md)
- [SESSION_SUMMARY_2026-04-01_TOPOLOGY.md](/Users/jonreilly/Projects/Physics/docs/SESSION_SUMMARY_2026-04-01_TOPOLOGY.md)
- [DECOHERENCE_FAILURE_ANALYSIS.md](/Users/jonreilly/Projects/Physics/docs/DECOHERENCE_FAILURE_ANALYSIS.md)
- [IF_PROGRAM_CLOSING_NOTE.md](/Users/jonreilly/Projects/Physics/docs/IF_PROGRAM_CLOSING_NOTE.md)
- [CLAIM_AUDIT_NOTE_2026-04-01.md](/Users/jonreilly/Projects/Physics/docs/CLAIM_AUDIT_NOTE_2026-04-01.md)
- [ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md](/Users/jonreilly/Projects/Physics/docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md)
- [MIRROR_CHOKEPOINT_NOTE.md](/Users/jonreilly/Projects/Physics/docs/MIRROR_CHOKEPOINT_NOTE.md)
- [MIRROR_GRAVITY_PROBE_NOTE.md](/Users/jonreilly/Projects/Physics/docs/MIRROR_GRAVITY_PROBE_NOTE.md)
- [ASSUMPTION_DERIVATION_LEDGER.md](/Users/jonreilly/Projects/Physics/docs/ASSUMPTION_DERIVATION_LEDGER.md)
- [REVIEW_HARDENING_BACKLOG.md](/Users/jonreilly/Projects/Physics/docs/REVIEW_HARDENING_BACKLOG.md)

### 1. Effective delay structure

Persistent patterns can generate a local delay field in the toy. Histories evaluated against that field do not behave as if they were propagating on an undistorted fixed background. On the tested boost transformations, the retained update `sqrt(dt^2-dx^2)` is the exact invariant scalar, while coordinate delay, Euclidean edge length, and spent delay all drift. So the toy now has a proper-time-like kinematic scalar even though its gravity dynamics remain nonlinear. When local connectivity is enriched from `8` to `24` to `48` directions, the signal-speed anisotropy at radius `20` falls `8.2374% -> 2.7397% -> 1.3072%`, consistent with roughly `1/n_directions`, so the kinematic sector now has a clean richer-connectivity continuum trend even though the gravity asymptotic law is still unsettled.

### 2. Gravity-like continuation

Path selection through the derived delay field still produces inward-bending, gravity-like continuation on the benchmark suite. Small quantitative sweeps show a two-node onset and directional asymmetry. Oscillating persistent sources still bend trajectories robustly, and two-source tests still show the gravity sector is not linear: `field(A+B)` differs from `field(A)+field(B)`, and the combined optimal action differs from the sum of the single-source actions by about `48..52%` on the tested geometry. But the gravity story is now sharper than that older benchmark-only picture. The original `1/delay^p` propagator suppresses amplitude in high-field regions and therefore builds in a wrong-sign anti-gravity bias on irregular generated DAGs. Replacing that amplitude factor with geometry-only attenuation `1/L^p` isolates a corrected propagator in which gravity is purely phase-driven: on the fixed-grid regression, `k=0` gives exactly zero shift, the three-slit Sorkin test still passes at `|I_3|/P = 6.48e-16`, and the best two-slit visibility remains `V = 0.9951`. On generated causal DAGs, the current best retained regime is the `k`-averaged corrected propagator: attraction appears on `11/12` tested seeds while interference survives on `12/12`. A perturbative derivation now also shows the weak-coupling shift scales as `k^2`, and the local mechanism is a phase valley: spent-delay action decreases in the mass region, so paths through that region accumulate less phase and the beam concentrates there. The bounded saturation line is sharper now too. Replacing node phase with cumulative near-mass action deficit first improved the best retained proxy for the plateau-like momentum kick: at the same near-mass skirt probe (`x = 34`, split `y >= b`), raw action-deficit gap reached `R^2 = 0.4213`, beating the earlier raw phase-gap fit (`R^2 = 0.3459`). A tighter packet-local spread term now sharpens the normalized law further: keeping the same probe and numerator fixed, packet-local action `Q` rises to `R^2 = 0.4478` with `MAE = 0.3413`, beating both raw action gap and the older pooled-spread action `Q` (`R^2 = 0.3983`). Small guardrail windows around the packet peak keep the same read (`R^2 = 0.4482` for half-window `1`, `0.4477` for half-window `3`), so this is not just one lucky width choice. The retained saturation read is therefore narrower but stronger: the toy law gains its first bounded support when the denominator tracks packet-local near-mass action spread rather than a pooled valley-wide spread, while the downstream detector probes still do not close. The growth story also tightened: on incrementally grown generated graphs, interference turns on sharply at `6` layers while gravity appears between `3` and `8` layers depending on seed, with both present reliably from `8` layers onward. The main gravity caveat is now more specific. The lattice-side force surrogate can fit well on the rectangular benchmark (`R^2 ≈ 0.91` for the best tested observable family), but that detailed force law does not transfer to generated DAGs (`R^2 ≈ 0.20`), so the universal retained claim is the corrected sign, the phase-only `k=0` limit, and the `k^2` response law, not one topology-independent scalar force law. Likewise, the earlier 2D lensing interpretation has been retracted: attraction is real, but the current scattering observable does not yet define a clean outgoing deflection angle.

### 3. Fixed-DAG interference

In coherent mode, off-center visibility is geometry-dependent and the sampled even-width onset boundary closes exactly as
`width_crit = min(slit_sep + 2|y|, 2*slit_sep + 2)`, so the earlier `y=1` “critical ratio” is only one edge of a broader two-regime detector-side law. On a fixed DAG, the tested three-slit configurations satisfy the Sorkin inclusion-exclusion identity to machine precision, so the interference law itself remains pairwise/Born-like. That claim now survives the corrected propagator too: on the current fixed-DAG regression with geometry-only attenuation `1/L^p`, the three-slit Sorkin test still gives `|I_3|/P = 6.48e-16` and the best two-slit visibility remains `V = 0.9951`. The same coherent interference pattern also survives tested geometric embedding perturbations while exact record suppression still holds. Under both symmetric and asymmetric delay-field distortions that leave the DAG fixed, the tested visibility curves remain unchanged to numerical precision; field-only record effects do not produce decoherence in that setup. A separate norm-preservation test also shows that `p=2` is the unique tested norm preserved by the sampled unitary transforms, so the Born rule is not just empirically observed here; it follows from linear reversible amplitude propagation in the tested family. The same interference and gravity mechanisms also survive tested graph growth from `35` to `1395` nodes. Going one step further, a randomly generated causal DAG with no pre-built grid still produces interference, with `V(y=0)` ranging from `0.078046` to `0.988188` across the tested seeds while the no-barrier control stays exactly zero. With the corrected propagator, interference also emerges during graph growth on the generated-DAG lane itself: on the current growing-graph sweep, mean visibility stays zero through `5` layers, then jumps to `0.982` at `6` layers and remains essentially saturated thereafter. The current generated-DAG visibility spread is now compressed best as a two-branch detector-side packet-completion regime rather than as raw graph size or one universal scalar. On the default 64-seed slice, `center_path_balance` is the best local predictor and beats raw edge count / density. On a nearby denser-radius holdout, the winner shifts to `center_balanced_log_paths`. On the combined rows, a simple balanced-load floor `center_balanced_log_paths <= 17.671` gives the cleanest retained map: below that floor visibility is more balance-led, above it balanced center slit-load carries the signal. That split also outperforms any single family scalar on the combined sample and is not just the scenario label, because both branches contain crossover rows from the other slice. The crossover rows then show what actually pushes a row across the floor: not extra retimed slit load, but how jointly that detector-side load is shared across the two center slit packets. Abstractly, `center_balanced_log_paths` is the generated-DAG analogue of packet completion / closure-load, while `center_path_balance` and `center_balance_share` are the generated-DAG analogues of the older bridge/anchor-balance language. Retiming and slit-share still matter, but as detector-side bottleneck modifiers rather than the primary branch selector. A final residual-pair check did not justify a new global clause: the remaining opposite-endpoint exceptions can be pair-separated by ad hoc cuts, but those cuts do not generalize across the full crossover set, so the retained bridge language stops here. The shared crosswalk is now explicit: in both the geometry ladder and the generated-DAG bridge, completion/load sets the regime floor, balance selects the near-floor branch, and bottleneck/placement terms modulate the readout without becoming the main retained split.

### 4. Topology-changing record effects

The large open/closed-slit Sorkin signal comes from DAG reconfiguration rather than higher-order interference: in the tested geometries, removing a single barrier slit node rewires `38..300` causal edges and delays `30..104` downstream shared nodes, almost entirely on the post-barrier side. Across the four tested three-slit geometries, the best compact predictor of that spike is cumulative detector-boundary retiming across the three one-slit closures; it tracks `max |I_3| / max |P_ABC|` more cleanly than raw post-barrier edge-count changes. A first topology-changing record operator that adds post-barrier shortcut structure then produces non-trivial visibility reshaping instead of the trivial `V_0(1-p)` law: the effect can either enhance or suppress visibility depending on detector position because the retimed DAG prunes edges and rebalances the slit amplitudes.

The corrected-propagator decoherence story is now sharper and more constrained. Fixed-DAG field distortions still leave the tested visibility curves unchanged, and the strongest clean suppression on irregular generated DAGs still comes from injected phase noise. Small-graph finite-environment tags can produce some endogenous decoherence: the repaired node-label downstream geometry reaches `D = 4/12` with `ALL = 1/12`, and related directional-recording slices also show nonzero suppression. But the latest growing-DAG scaling sweeps narrow the retained conclusion. The relevant observable is detector-conditioned purity, not full-state purity, and the size trend survives even after partially controlling for simple environment dilution. With a fixed one-layer post-barrier environment region, node-label detector-state purity rises from `0.7060` at `8` layers to `0.8858` at `25`; when the environment depth scales roughly as `n_layers/6`, it still rises from `0.7060` to `0.7944`. A genuinely fixed-bin cumulative-phase register then stays near pure across the same size sweep (`0.9896 .. 0.9827`), and the discretized evolving-phase register either stays fully coherent or also wrong-scales (`0.8067 -> 0.8509` at the strongest tested coupling). So the non-unitary frontier is no longer best read as “find a better finite register,” and not even as “occupy more env states.” The current evidence says the bottleneck is the interaction law that sets the traced detector-side branch-weight structure: larger env dimensionality alone fails, larger occupied support alone does not obviously help, and the tested simple entangling split plus repaired fixed-kick substrate memory also fail in their current forms. The next retained move is therefore one bounded mesoscopic durable-record or local-entangling mechanism whose coupling law is qualitatively different from deterministic bookkeeping, not another broader bigger-env sweep.

The next frontier is therefore best treated as a scaling architecture problem, not another broad sweep problem. The repo now includes explicit scaling targets, reduced failure mechanisms, architecture options, and a minimal scaling benchmark table:
- [SCALING_TARGETS.md](/Users/jonreilly/Projects/Physics/SCALING_TARGETS.md)
- [SCALING_FAILURE_MECHANISMS.md](/Users/jonreilly/Projects/Physics/SCALING_FAILURE_MECHANISMS.md)
- [ARCHITECTURE_OPTIONS.md](/Users/jonreilly/Projects/Physics/ARCHITECTURE_OPTIONS.md)
- [SCALING_BENCHMARK_TABLE.md](/Users/jonreilly/Projects/Physics/SCALING_BENCHMARK_TABLE.md)
- [DECOHERENCE_DECISION_NOTE.md](/Users/jonreilly/Projects/Physics/docs/DECOHERENCE_DECISION_NOTE.md)

Reviewer-facing framing docs:
- [ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md](/Users/jonreilly/Projects/Physics/docs/ARCHITECTURE_NOTE_DIRECTIONAL_MEASURE.md)
- [ASSUMPTION_DERIVATION_LEDGER.md](/Users/jonreilly/Projects/Physics/docs/ASSUMPTION_DERIVATION_LEDGER.md)
- [LITERATURE_POSITIONING_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LITERATURE_POSITIONING_NOTE.md)
- [REVIEW_HARDENING_BACKLOG.md](/Users/jonreilly/Projects/Physics/docs/REVIEW_HARDENING_BACKLOG.md)

#### Architecture scorecard (tested candidates)

| candidate | gravity scaling | interference | decoherence scaling | mechanism |
|---|---|---|---|---|
| 1/L^p baseline | **FAIL** | **PASS** | **FAIL** | retained unitary core, but gravity still saturates and tested discrete env tags wrong-scale |
| **1/L^p × exp(-0.8θ²)** | **PASS** | **PASS** | **FAIL** | lead provisional unitary candidate; directional path measure preserves Born/interference/`k=0→0` and prevents gravity collapse, but does not fix the tested record-scaling failure |
| G1: path-multiplicity-renormalized action | **FAIL** | not tested | not tested | divides action by path count; effective action → 0 on dense graphs, kills gravity entirely |
| **G2: coarse-grained propagator** | **PASS** | **FAIL** | **FAIL** | bins nodes by `y`, which keeps `R_grav` stable at large `N`, but `V_g2 = 0.0000` at `k = 3.0, 5.0` and the same coarse averaging reduces branch-distinguishing microstructure |
| D1: multi-local tensor env | not targeted | **PASS** | **FAIL** | env dimension grows (`9 → 336` states) but amplitude stays concentrated in a few dominant states; purity tracks fine env at every size |
| G2+env: coarse-grained + fine env | **PASS** | **FAIL** | **FAIL** | coarse-graining reduces effective paths, which reduces env state diversity |
| D4 surrogate: mass-exit trace | not targeted | **PASS** | **FAIL** | produces identical purity to fine env at every size; this tested surrogate reduces to a last-exit-node relabeling rather than a full spatial trace |
| Two-scale (`G2` + per-bin micro env) | **PASS** | **FAIL** | **FAIL** | gravity stays stable, but `pur_2s` still rises from `0.8401 → 0.9806` (`n_ybins = 6`) and `0.8517 → 0.9555` (`n_ybins = 8`); it inherits the `G2` phase-averaging failure |

**Retained positive results:**
- corrected 1/L^p unitary core still stands (gravity sign, Born rule, interference, `k=0→0`, phase valley)
- directional path measure `exp(-0.8θ²)` is the current lead provisional unitary architecture:
  - 2D unitary checks pass: Born, interference, `k=0→0`, gravity scaling guardrail, and bounded family transfer
  - a bounded 3D unitary smoke test now also passes on a fixed 3D DAG: zero-field coherent visibility reaches `0.9963` on the canonical `k` band, coherent-vs-incoherent detector-profile contrast stays nonzero across that full band (`TV >= 0.1104`), and source-superposition linearity holds to machine precision (`3.18e-14`)
  - 3D gravity-side smoke checks remain encouraging too: `k=0→0` passes, `R_angle` grows from `+0.29` to `+0.57` across the tested size sweep, and attraction appears on `5/8` seeds
  - a stricter fixed-`b` 3D modular mass-scaling follow-up did not cleanly recover a power law under one retained sweep, so the earlier `sqrt(M)`-style read remains provisional rather than promoted
  - the current caveats are explicit: decoherence scaling still fails in the tested record architecture, `R_c` compatibility is only marginal (`8/10`), and the raw `b` readouts are still wrong-direction even though a bounded geometry-normalized response-density diagnostic now passes and transfers to the second dense-family holdout
- G2-style coarse-graining is the first tested architecture family that fixes the gravity scaling guardrail
- a readout-only micro-preserving gravity prototype now also clears the bounded scaling guardrail on the same `N=8..25` family: near-mass `action_channel` bias grows in stable sign and magnitude from `-0.2456` at `N=12` to `-0.8002` at `N=25`, while the baseline detector centroid still collapses from `+0.7968` to `+0.3989`
- a tighter packet-local refinement is now bounded but not yet promoted: on the same random-DAG family, adaptive `packet_flow_action` improves the endpoint retention again (`|N25/N12| = 3.9748` versus `3.2582` for `action_channel`), but a branching-tree control keeps the broader `action_channel` as the best cross-family read (`|N12/N6| = 2.9514` versus `2.7878` for `packet_flow_action`)
- a support-structure compare now explains that split instead of only reporting it: on the random-DAG family, the retained packet captures a growing mass-side carried-flow share while the opposite side diffuses (`0.287 -> 0.382` upper versus `0.272 -> 0.162` lower from `N=12 -> 25`), and the full flow support stays about `3x` broader than the retained packet; on the branching-tree control both sides remain nearly symmetric (`~0.25` each) with only `~2x` compression, so the broader channel stays the honest cross-family read
- the directional `b` lane is now narrower but not dead: raw mass-side action and flow reads still strengthen with actual `b`, but once they are normalized by simple mass geometry they flip to the expected decreasing trend on the bounded dense-family generators already on disk. On the original narrow three-node mass family, center-offset response density (`action_channel / b` and `packet_flow_action / b`) still passes at `N=12` and `N=25`, while nearest-edge normalization also passes once near-overlap cases are treated as singular. A bounded holdout-transfer replay now says this is not just one-generator luck: on the second dense-family holdout, `A/b`, `A/edge`, `F/b`, and `F/edge` all still pass at both `N=12` and `N=25` for the original `mass_nodes = 3` window. A widened-source holdout follow-on at `mass_nodes = 5` then sharpens the finite-source split instead of killing it: on that same holdout, `N=25` loses the center-offset passes (`A/b`, `F/b`) while nearest-edge density (`A/edge`, `F/edge`) still passes. A more local support-gap denominator tied to the free packet's retained probe band is only partial on the dense random-DAG family: `action_channel / support_gap` still passes, but `packet_flow_action / support_gap` already fails at `N=12`. A follow-on denominator-geometry diagnostic explains why: within each `N` slice the free retained probe-band edge is effectively fixed by the graph family, so `support_gap = b - (mass_half_span + band_high_rel)` mixes mass placement with a size-dependent packet-band correction that even flips sign between the `N=12` and `N=25` low-`b` anchors. The asymptotic bridge card compressed that into one hierarchy, and the corrected mass-window transfer card sharpened it further: when the mass window is widened from `3` to `5` mid-layer nodes on the same random-DAG generator, some low-`b` small-`N` seeds become singular under source-support overlap, but the bounded family-level center-offset trend still passes once those singular trials are excluded. The crossover still reduces that family dependence to one bounded variable, `lambda = h_mass / b`, and the overlap-margin card gives the cleaner signed diagnostic `mu = edge_b / h_mass = 1 / lambda - 1`. Tree-like controls stay at large positive `mu`, narrow random-DAG families only graze `mu ~ 0` at low-`b`, and widened dense families are the ones that actually cross into `mu <= 0`, where the finite-source correction matters most. The new low-`b` onset compare closes the mechanism language another step: overlap onset tracks weak target-band occupancy plus coarse local `y` spacing. Tree layers densify near the target plane, so selected mass windows stay compact and `mu` remains positive; dense random-DAG layers keep only about `1-2` nodes in the target band, so widened source windows must stretch across large `y` gaps and are the ones that cross into `mu <= 0`.
- `k=0→0` remains preserved under both G1 and G2

**Current read:** the best current architecture split is now cleaner. On the unitary side, the flat path measure appears to have been the wrong assumption; the lead provisional replacement is corrected `1/L^p` transport plus a directional path measure `exp(-0.8θ²)`, which preserves the tested 2D unitary constraints, passes a bounded 3D unitary smoke test, and stops the gravity-side collapse on the bounded scaling family. The gravity distance-law caveat is now more specific than a blanket failure: raw readouts still grow with `b`, but bounded geometry-normalized response densities already fall with `b` on the tested families. The retained translation is now sharper: center-offset density is the asymptotic leading mass-geometry term, nearest-edge density `b - h_mass` is the robust finite-source correction once source width matters, and support-gap is a discrete packet-support correction whose stability depends on whether the family keeps `delta_packet` small. A new widened-source holdout replay makes that split concrete on the second dense-family holdout: at `mass_nodes = 5`, `N = 25` loses the center-offset passes while nearest-edge density still transfers. The reduced-variable picture is now two-layered: `lambda = h_mass / b` is the compact crossover control, while `mu = edge_b / h_mass = 1 / lambda - 1` is the cleaner signed overlap diagnostic. Tree-like controls keep large positive `mu`, narrow random-DAG families only graze `mu ~ 0` at low `b`, and widened dense families are the ones that actually cross into `mu <= 0`, where pure `response / b` becomes fragile and `response / edge_b` is the portable tested correction. So the open gravity question is no longer another denominator search, but explaining the family dependence of that overlap onset. On the non-unitary side, no tested record architecture scales correctly yet, and the bottleneck now looks like interaction law / traced branch-weight structure rather than raw env size. So the next good move is not another transport coarse-graining pass or another larger discrete register. It is to treat the propagator as a provisional retained unitary layer with a now-closed 3D smoke gap, and focus the next architecture loop on one mesoscopic durable-record or local-entangling interaction law plus a compact physical translation of the retained gravity response density.

### 5. Oscillatory persistence under the default self-maintenance rule

Under the current default self-maintenance rule `S={3,4}, B={3,4}`, the tested seeds do not settle to static fixed points; they either die or enter period-2/3 orbits. In that sense, default persistence is periodic renewal rather than stasis. Broader rule sweeps still contain fixed-point rules, growing rules, and other oscillator families, so this is a statement about the current default dynamics rather than the whole rule space. A bounded packet-tracking bridge on generated-DAG movers now sharpens the next step beyond that static persistence language. On the canonical mover family (`540` rows across four graph configs, three neighbor radii, three seed positions, and the canonical rule trio), coherent translating packets do exist (`124` rows), but they do not live on one magic scalar. The retained mover map is two-stage:

- opening survival guard: on the discovery pair (`dense-25` / `sparse-25`), the best compact live-vs-die clause is `early_live_fraction >= 0.625 and early_front_load >= 1.447`, with `0.8000` discovery accuracy and `0.6889` holdout accuracy on `wide-15` / `long-30`
- coherent-vs-diffuse splitter among live rows: the best compact mover clause is `early_front_load >= 0.962 and early_band_share <= 0.776`, with `0.8250` discovery accuracy and `0.7857` holdout accuracy

So the mover-side bridge now matches the same abstract vocabulary as the visibility bridge and the geometry card: completion/load first, bottleneck second. Here the completion/load term is local forward frontier support around the tracked packet, and the bottleneck term is how narrowly that support stays focused in the forward band. That is the real substrate needed for the next frontier: field-to-pattern coupling on coherent translating packets rather than on patterns that merely oscillate, diffuse, or die.

A first bounded field-coupled probe now says that this substrate is actually usable. Starting only from the coherent free movers in that same canonical family (`248` coupled trials per tested coupling), a static localized field placed a little ahead of the free packet path can steer those movers without collapsing the substrate. The best retained coupling in the bounded sweep is not the weakest one: at coupling `3.000`, `224/248` packets remain coherent survivors, only `18` diffuse, only `6` die, and the signed toward-mass shift rises to `+0.9556` (median `+0.6294`). The clearest steering lives on the denser forward neighborhoods (`neighbor_radius = 2.5`, mean signed shift `+1.1842`).

A direct pattern-sourced follow-on still sharpens that story, but the current repaired scripts change which source footprint survives. On the retained `neighbor_radius = 2.5` mover substrate (`170` coherent free mover trials), the nearby self-rule source is usually viable: `149` rows are fully persistent in the late window, `150` rows keep a usable late union (`>= 3` nodes), and the coupled mover still remains mostly coherent on those viable-source rows. Under the current code, the broad `last6_union` footprint is now the positive frozen baseline rather than the failure mode: `135/150` viable-source rows survive with mean signed shift `+0.4736`. The narrower `last3_union` footprint no longer gives a retained toward-source branch even as a frozen surrogate: `136/150` survive, but mean signed shift is only `-0.0811`.

A stronger live-vs-frozen source compare then says the field-to-pattern arrow is partly real already, but only on that broader late-source branch. Letting the same mature source keep evolving during the mover run weakens both footprints, but asymmetrically. The live sliding `last6` source stays net toward-source in substance (`126/150` survive, mean signed shift `+0.4420`), while the live sliding `last3` source weakens further (`124/150` survive, mean signed shift `-0.5125`). So the retained source-side bridge is no longer a narrow recent-footprint law. The current positive branch is the broader late `last6` source window, and the active frontier is to compress which late-support geometry keeps that live regenerated field attractive instead of flipping into retiming / away-shift on specific mover-rule slices.

A paired live-window geometry compare then closed the next seam without reopening any broader search. Keeping the source evolution fixed and widening only the live source window from `3` to `6` on the same `146` viable paired rows, the broad window beats the narrow one on `80/146` rows and lifts the mean signed shift from `-0.6000` to `+0.5040`. But that broad live branch does not collapse to one universal late-support scalar. The retained `last6` subset (`52/146` rows that stay coherent and toward-source) is the subset where the added `last4-6` support actually lands on the packet more strongly (`extra_field_mean_on_packet = 0.1006` versus `0.0249` on the nonretained rows), and the best pooled rule is only moderate: `extra_packet_side_gap <= -0.0080` reaches `0.7286` discovery accuracy and `0.6579` holdout accuracy. The remaining split is mover-rule-local. `self` carries most retained rows (`40/83`) but still does not close sharply, while `wide` already tightens under one clearer late-source corridor clause, `last6_corridor_share >= 0.7762` (`0.8113` local accuracy). So the current field-to-pattern read is now sharper: the broad live `last6` branch is real, the pooled packet-landing hint is real but weak, and the unresolved residue sits mostly inside mover-rule-local geometry rather than at the existence of the branch itself.

The self-branch follow-on now gives a clean stop rule on that residue. The dominant `self` slice still does not reduce to one retained shared law. On the present basis, neither `dense-25 + sparse-25` nor `long-30 + wide-15` forms a stable transferable self-family. Each pair only supports weak local hints, and those hints fail when transferred to the other pair. So the honest current architecture is: one real broad live `last6` source branch; one sharper local `wide` corridor clause; and one `self` branch that remains config-local rather than cleanly compressible. That means the next value is not more self-clause shaving, but keeping that stop rule explicit while moving back up to the common field-to-pattern architecture.

### 6. Stable mechanism families

The broadest recurring split is:

- `compact`, with a cleaner threshold-core structure
- `extended`, with more permissive and fallback-heavy behavior

This split persists across reruns and generated families.

### 7. Family growth without comparable family proliferation

As generated families widened:

- membership kept growing
- the number of main mechanism families changed much more slowly

The resulting picture is a stable mechanism map with expanding support, rather than continual creation of new families at each deeper frontier.

### 8. Shared structure in the low-overlap basin

Fine-grained mechanism work is currently concentrated on a fixed frontier snapshot at `variant_limit = 5504`. On that controlled sample:

- the hardest low-overlap center-spine `00` core has an exact closure family with a broad rescue side and a tighter, more local baseline cut
- the low-overlap support-family map transfers across the three main low-overlap branches:
  - `add1-sensitive`
  - `add4-sensitive`
  - `pair-only-sensitive`
- the dominant shared bucket already shows interpretable subtype drift:
  - `add1`: left-dominant, higher-support branch
  - `add4`: mid-dominant, more internally closed branch
  - `pair-only`: lower-support, more open-support branch
- the outside-gate residual for `pair-only-sensitive` now exact-closes under a branch-aware second pass:
  - baseline low-closure pocket: `closure_load <= 46.500`
  - spillover carve-out: `mid_anchor_closure_peak <= 0 and high_bridge_right_count <= 0`
  - recovered right-low side branch: `high_bridge_right_low_count >= 1 and support_load <= 14.500 and mid_anchor_closure_peak <= 1`
  - combined outside-gate result: `26/26` for `pair-only-sensitive` (`6/0/0`)
- projected back onto the full frozen bucket, the combined law now exact-closes every `pair-only-sensitive` row with no leakage:
  - high-closure gated branch: `3/3`
  - outside-gate branch-aware branch: `6/6`
  - full-bucket `pair-only-sensitive` result: `9/9` with `0` false positives
- the remaining unmatched residue is now much narrower:
  - `20` rows total
  - exactly `15 add1-sensitive` plus `5 outside-gate add4-sensitive`
  - the cleanest zero-false-positive residual `add4` clause is `anchor_closure_intensity_gap >= -6.500 and mid_anchor_closure_peak >= 9.000`, which captures `3/5`
  - the stubborn high-mid four-row knot (`local-morph-а`, `local-morph-༸` vs `local-morph-छ`, `local-morph-గ`) exact-closes in a slightly richer transfer basis with `edge_identity_event_count <= 78.000` (`2/2` add4, `0` false positives inside that cluster)
  - one bounded two-clause follow-on keeps that knot exactness and improves full-residual `add4` precision without recall loss:
    - `edge_identity_event_count <= 78.000 and edge_identity_support_edge_density >= 0.166667` (exact threshold `1/6`, rounded as `0.167` in earlier logs)
    - full residual result: `5/5` add4 recovered, `8` add1 false positives (precision `0.385`, baseline seed precision `0.312`)
  - a direct branch combiner with the earlier zero-false-positive residual clause does not improve on that branch:
    - `anchor_closure_intensity_gap >= -6.500 and mid_anchor_closure_peak >= 9.000` is a strict subset of the density-qualified branch
    - the combined `A or B` law is identical to branch `A`
  - one bounded branch-A leakage carve closes most remaining leakage without recall loss:
    - `edge_identity_event_count <= 78.000 and edge_identity_support_edge_density >= 0.166667 and mid_anchor_closure_peak >= 1.000`
    - full residual result: `5/5` add4 recovered, `1` add1 false positive (precision `0.833`, recall `1.000`)
    - the remaining overlap is concentrated in `base:taper-wrap:local-morph-͋`
  - the final overlap exact-closes under one bounded exclusion inside that branch:
    - exclude `closure_load <= 50.500 and edge_identity_support_edge_density <= 0.182`
    - refined outside-gate `add4` result: `5/5` with `0` false positives
  - projected together with the earlier high-closure and `pair-only` branches, the full frozen `rc0|ml0|c2` bucket now exact-closes:
    - high-closure `add4`: `3`
    - outside-gate `add4`: `5`
    - `pair-only`: `9`
    - default `add1`: `15`
    - full-bucket result: `32/32`, `0` misclassifications, `0` ambiguity
  - the exact branch-aware law also transfers unchanged across the nearby frontier ladder we tested:
    - `variant_limit = 4112`: `25/25`, `0` misclassifications
    - `variant_limit = 4992`: `28/28`, `0` misclassifications
    - `variant_limit = 5504`: `32/32`, `0` misclassifications
    - no first failure appeared within the tested `4112 -> 5504` slice
  - a widened frontier sweep still shows no failure:
    - `variant_limit = 1232`: `10/10`, `0` misclassifications
    - `variant_limit = 1488`: `12/12`, `0` misclassifications
    - `variant_limit = 3344`: `20/20`, `0` misclassifications
    - together with the later limits, no first failure appears anywhere in the tested `1232 -> 5504` slice
  - a full backward historical sweep also shows no failure:
    - `59` tested checkpoints below `1232`, with `lowest_exact_limit = 192`
    - the only duplicate hazard was `variant_limit = 192`, where the sweep skipped a malformed `2026-03-22` log and fell back to the valid `2026-03-21` log
    - together with the widened and nearby ladders, no first failure appears anywhere in the full available historical `192 -> 5504` slice
  - a generated-family eligibility profile plus repaired canonical transfer check shows the law fails immediately on nearby `taper-wrap` ensembles:
    - the first non-pocket generated cohort already appears at `base:taper-wrap:default`, with `2` geometry rows (`geometry-c`, `geometry-e`), both `pair-only-sensitive`
    - after fixing the transfer checker to treat undefined support-edge metrics as zero-valued rather than skipping the row, the canonical `default/broader/wider` ladder gives `rows_total = 6`, `misclassified_total = 6`, `first_failure_ensemble = default`
    - all six failures are the repeated `geometry-c/e` rows, predicted as `add1-sensitive` by the fallback branch because their support metrics collapse to zero (`closure_load = 0`, `mid_anchor_closure_peak = 0`)
  - a direct generated-vs-historical comparer shows those failures are not just weak versions of the historical branch but a genuine support-collapse edge:
    - across `default`, `broader`, and `wider`, all `6` failing rows are still just `geometry-c/e`, and every current support/order-parameter observable is exactly zero (`support_load = 0`, `closure_load = 0`, `edge_identity_event_count = 0`, `edge_identity_support_edge_density = 0`)
    - the historical frozen bucket contains no `pair-only-sensitive` or `add1-sensitive` row with zero support activity:
      - historical `pair-only`: `support_load 7 -> 14`, `closure_load 38 -> 54`, `edge_identity_event_count 65 -> 89`
      - historical `add1`: `support_load 7 -> 16`, `closure_load 34 -> 64`, `edge_identity_event_count 54 -> 95`
    - so the first generated-family transfer break is best read as a support-collapse domain edge rather than an in-family continuation of the historical `pair-only-sensitive` mechanism
  - a minimal explicit domain guard isolates that edge cleanly:
    - guarding rows with `support_load = 0`, `closure_load = 0`, and `edge_identity_event_count = 0` moves all `6` canonical generated failures (`geometry-c/e` across `default/broader/wider`) into an out-of-domain bucket
    - no historical frozen-bucket row is guarded, and the historical `32/32` exact-close remains unchanged under the guarded projection
  - but the guard does not stabilize nearby generated transfer beyond that first edge:
    - on `base:taper-wrap`, the first non-guarded generated failure appears at `ultra` and repeats at `mega` as `mode-mix-f` (`pair-only-sensitive` actual, `add1-sensitive` predicted)
    - on neighboring `base:skew-wrap`, non-guarded generated failures already appear at `default` (`local-morph-c`) and broaden at `broader+` (`mode-mix-d`)
    - so support-collapse is only the first nearby generated-family boundary, not the whole transfer failure story
  - a direct comparer against the historical frozen `pair-only-sensitive` rows shows those surviving generated failures are not just a single shifted load or density branch:
    - the `skew-wrap` failures are over-supported and high-closure but sparse on support-edge density (`support_load = 20`, `closure_load = 63 -> 70`, `edge_identity_support_edge_density = 0.103 -> 0.140`)
    - the surviving `taper-wrap:mode-mix-f` failures are the opposite extreme (`support_load = 0`, `closure_load = 5`, `edge_identity_event_count = 10`, `edge_identity_support_edge_density = 0.500`)
    - so no single load, closure, or density threshold exact-separates all surviving generated failures from the historical frozen `pair-only-sensitive` branch
    - but all `11` surviving generated failures do exact-close into one compact anchor-balance band: `anchor_closure_intensity_gap` always stays between `-2.000` and `2.333` (empirically `0 -> 2`)
    - every historical frozen `pair-only-sensitive` row lies outside that band (`-9.667 -> -4.000` or `2.667 -> 6.000`)
    - projecting that same band onto the queued contrast cohorts keeps it exact against `add1` but reveals one small frozen `add4` pocket:
      - every frozen historical `add1-sensitive` row also stays outside the band (`anchor_closure_intensity_gap = -12.000 -> -2.667`)
      - only `2/8` frozen `add4-sensitive` rows enter the band (`base:taper-wrap:local-morph-ዦ`, `base:taper-wrap:local-morph-ᓭ`)
      - those in-band `add4` rows are otherwise inside the generated target ranges but sit at `mid_anchor_closure_peak = 12`, above the generated-failure maximum `8`
      - adding one compact in-band ceiling restores exact separation across all frozen historical cohorts: `anchor_closure_intensity_gap >= -2.000 and anchor_closure_intensity_gap <= 2.333 and mid_anchor_closure_peak <= 10.000`
      - under that refined clause the generated failures stay `11/11`, while frozen historical `pair-only-sensitive`, `add1-sensitive`, and `add4-sensitive` rows fall to `0/9`, `0/15`, and `0/8`
      - on a four-row focused comparison against representative `base:skew-wrap:local-morph-c` and `base:skew-wrap:mode-mix-d`, one compact support-layout observable already exact-separates the skew-wrap generated failures from the in-band `add4` pocket: `anchor_deep_share_gap >= 0.250`
      - physically, those skew-wrap generated failures carry a right/deep bridge shoulder (`anchor_deep_share_gap = 0.500`, `high_bridge_right_count = 1`) that the in-band `add4` rows lack (`0`, `0`), so the generated rows spread closure away from the mid anchor (`mid_anchor_closure_peak = 8`) while the frozen `add4` pocket traps it at `12`
      - on the same representative row set plus one representative `base:taper-wrap:mode-mix-f`, one compact low-support observable exact-separates `mode-mix-f` from both the skew-wrap shoulder and the in-band `add4` knot: `closure_load <= 24.500`
      - physically, `mode-mix-f` stays inside the anchor band by collapsing to a zero-support, low-closure floor (`support_load = 0`, `closure_load = 5`, `edge_identity_event_count = 10`) rather than by carrying the skew-wrap right/deep shoulder, so the refined band now has two generated realizations on the current bounded basis: a right/deep bridge shoulder and a nearly empty low-support throat, both distinct from the frozen `add4` mid-anchor knot
      - the bounded immediate generated basin (`taper-wrap`, `skew-wrap`, `taper-hard`, `skew-hard` through `mega`) contains no guard-surviving correctly classified comparison rows at all; every non-collapse row there is itself another transfer failure
      - one sparse outer generated guardrail slice over `rect-wrap`/`rect-hard` at `ultra` and `mega` adds no new refined-band generated row:
        - the only non-collapse outer failures are `base:rect-wrap:local-morph-f` at `ultra` and `mega`
        - both still sit on the base anchor-gap band boundary (`anchor_closure_intensity_gap = -2.000`) but fail the refined ceiling with `mid_anchor_closure_peak = 12.000`
        - a focused outer-rect comparison against the current shoulder/throat/knot representatives exact-separates the outer pair with one load observable: `closure_load >= 75.000`
        - physically, the outer guardrail still does not create a third generated realization inside the refined band; instead it marks a heavier knot-side continuation beyond the ceiling, sharing the frozen `add4` pocket's `mid_anchor_closure_peak = 12.000` and `anchor_deep_share_gap = 0.000` while retaining `high_bridge_right_count = 1.000` and much larger load (`support_load = 26.000`, `closure_load = 80.000`)
        - widening that same sparse rect guardrail one ensemble step to `wider|ultra|mega` still produces no beyond-ceiling non-collapse row outside the same `rect-wrap:local-morph-f` pair, so the present high-load continuation remains rect-local on that immediate bounded sparse slice
      - the next tested non-rect late guardrails also stay empty:
        - on the slightly wider `large` family at `ultra|mega`, the non-rect late slice (`taper-hard-large`, `taper-wrap-large`, `skew-wrap-large`) yields `scanned_nonrect_combinations = 6` and `first_nonrect_row = none`
	        - one tier later, that wider late slice still stays empty all the way through the tested deeper ladder: on `large` at `giga`, `tera`, `peta`, and `exa`, the same non-rect late slice yields `scanned_nonrect_combinations = 3` at each tier and `first_nonrect_row = none` at all four
        - on the differently placed `mirror` family at `ultra|mega`, the non-rect late slice (`skew-hard-mirror`, `skew-wrap-mirror`) yields `scanned_nonrect_combinations = 4` and `first_nonrect_row = none`
        - the mirrored late slice stays empty all the way through the tested deeper ladder: on `mirror` at `giga|tera`, the same non-rect late slice yields `scanned_nonrect_combinations = 4` and `first_nonrect_row = none`, and at `peta|exa` it yields `scanned_nonrect_combinations = 2` at each tier with `first_nonrect_row = none`
	      - but the more distant base late slice now shows a broader persistent non-rect beyond-ceiling branch:
	        - on the broader `base` `peta|exa` non-rect sweep, `nonrect_beyond_ceiling_rows = 3` and `high_load_hits = 3/3`
	        - the observed late non-rect beyond-ceiling rows are:
	          - `base:peta:base:taper-hard:local-morph-f`
	          - `base:exa:base:taper-hard:local-morph-f`
	          - `base:exa:base:skew-wrap:local-morph-k`
	        - the taper-hard member repeats unchanged across `peta|exa`: `support_load = 22.000`, `closure_load = 76.000`, `mid_anchor_closure_peak = 12.000`, `anchor_closure_intensity_gap = 4.000`, `anchor_deep_share_gap = 0.667`, `high_bridge_right_count = 2.000`
	        - the new skew-wrap member at `exa` still keeps the same high-load continuation while rotating the anchor geometry: `support_load = 21.000`, `closure_load = 84.000`, `mid_anchor_closure_peak = 12.000`, `anchor_closure_intensity_gap = -2.000`, `anchor_deep_share_gap = -0.667`, `high_bridge_right_count = 0.000`
	        - a direct row-level compare against the current shoulder/throat/knot representatives exact-separates the whole observed late branch with one tighter load cut: `closure_load >= 73.000`
	        - inside the observed late branch, the three realized forms each exact-separate with one feature:
	          - outer-rect tail: `support_load >= 24.000`
	          - taper-hard branch: `anchor_closure_intensity_gap >= 3.000`
	          - skew-wrap branch: `anchor_deep_share_gap <= -0.334`
	        - so `closure_load >= 75.000` still survives on the whole observed late non-rect branch, but the sharper current read is that it is one shared late high-load continuation with three distinct support-layout realizations rather than one undifferentiated tail
	      - on the already finished non-base late guardrails, there is still no broader-family transfer evidence for that branch:
	        - across `large` through `exa` and `mirror` through `exa`, the finished first-hit probes cover `30` non-rect combinations total and every one of those guardrails still reports `first_nonrect_row = none`
	        - the benchmark inventory itself now closes that current non-base frontier: outside `base`, the only available packs are `large` and `mirror`, the current late frontier only runs through `exa`, and all `12` non-base pack/ensemble pairs on `ultra..exa` are already covered with zero hits
	        - a bounded helper-validation detour now hardens that wall rather than changing it:
	          - the shared generated-family helper seam was real: non-base `build_rows_with_trees(...)` calls were still routing `_evaluate_extended_ge6_dpadj_nodes(...)` through `pack_name="base"`
	          - after threading the true pack name through that helper, all nine finished non-base first-hit probes reran with the same scanned-combination counts and still `first_nonrect_row = none`
	          - the helper-fixed `large:exa` exhausted-slice compare, full exhausted-wall mid-anchor translation compare, and full packet-neighborhood compare also match their earlier outputs in substance, so the present empty non-base wall does not depend on the stale helper path
	        - a direct exhausted-slice compare now shows what that empty wall is hiding:
	          - the nearest `large:exa` miss, `large:taper-wrap-large:local-morph-g`, already clears the observed late branch load floors (`support_load = 26.000`, `closure_load = 87.000`) but stalls at `mid_anchor_closure_peak = 8.000`, exactly `4` below the late-branch value `12.000`
	          - the nearest `mirror:exa` miss, `mirror:skew-hard-mirror:local-morph-f`, also stalls at `mid_anchor_closure_peak = 8.000` while remaining below the late load floor (`support_load = 17.000`, `closure_load = 59.000`)
	          - comparing the five observed base late rows against those two nearest exhausted-wall misses exact-separates with one scalar clause: `mid_anchor_closure_peak >= 10.000`
	          - a tighter row-level compare against the closest `large:exa` miss shows that the miss is not short on absolute bridge-bridge closure scale:
	            - the late `rect-wrap` and `taper-hard` rows realize `mid_candidate_bridge_bridge_closed_pair_max = 12.000`
	            - the `large` miss also realizes a `12.000` bridge-bridge closed-pair maximum, but on the left anchor band instead: `left_candidate_bridge_bridge_closed_pair_max = 12.000`, `mid_candidate_bridge_bridge_closed_pair_max = 8.000`
	            - with the richer packet metric set, the focused structural separator is the attached-packet lift: `delta_mid_left_attached_max >= 0.000`, where `delta = mid - left`
	          - widening that packet compare to the full exhausted wall gives one cleaner structural separator still:
	            - every observed late row has `mid_candidate_attached_max = 8.000`
	            - both exhausted-wall misses stop at `mid_candidate_attached_max = 7.000`
	            - `mid_candidate_attached_max >= 7.500` exact-separates the whole observed late branch from the whole exhausted wall
	            - the corresponding mid-anchor bridge-bridge closed-pair maxima remain `12.000` on the late side and `8.000` on the exhausted-wall side
		          - the neutral-balance pair sharpens that wall further:
		            - the late `base:exa:base:skew-wrap:local-morph-k` row and the `mirror:exa` miss keep the same coarse layout: `high_bridge_left/mid/right = 2/1/0`, `left_candidate_count = 2`, `mid_candidate_count = 3`
		            - they also keep the same dense-count profile (`left_candidate_dense_count = 2`, `mid_candidate_dense_count = 2`) and the same mid closed-ratio ceiling (`mid_candidate_closed_ratio_max = 0.500`)
		            - so the `12.000 -> 8.000` drop is not another band-placement or density change; the late row upgrades the dominant left/mid packet from `7` attached bridges and `8` bridge-bridge closed pairs to `8` attached bridges and `12` bridge-bridge closed pairs
		          - a direct packet-neighborhood compare now localizes that lift:
		            - the dominant late mid packet is the same full eight-support octagon across all five observed late rows
		            - both exhausted-wall misses share the same seven-support depleted mid template
		            - every observed late row completes that exhausted template in the same way:
		              - add the inward left-flank support node at relative `(-1, 0)`
		              - restore the four incident bridge-bridge support closures
		            - a follow-on topology translation compresses that coordinate description into one local hinge law:
		              - the inserted support is a four-incident flank hinge
		              - it touches two same-column neighbors and two inward neighbors
		              - so the late branch repairs the exhausted wall by restoring one local vertical flank ladder plus two inward bridge-bridge closures into the packet interior
		            - the closest `large` miss still keeps the full octagon on the left anchor band, while the `mirror` miss also leaves its strongest left packet one support short
		            - so the whole current late-vs-exhausted transfer reduces locally to one node-and-four-edge mid-packet completion, not another layout change
	        - so outside the observed `base` `peta|exa` slice, the current late-branch law still has no non-base counterexample, but the sharper transfer read is now that the present non-base generator family ceilings at `mid_anchor_closure_peak = 8.000` because it never lifts `mid_candidate_attached_max` above `7.000`, and with that leaves the corresponding mid-anchor bridge-bridge closure maximum at `8.000` instead of `12.000`
	    - so the post-guard transfer break is now best read as a second nearby domain boundary: a moderate anchor-balance regime with one high-mid-anchor frozen `add4` pocket plus two generated realizations inside the refined band, a skew-wrap right/deep shoulder and a `mode-mix-f` low-support throat, while the sparse outer `rect-wrap` failures and the broader distant `base` late branch form a heavier beyond-ceiling continuation beyond that refined ceiling; the exhausted `large`/`mirror` wall now sharpens that farther continuation by showing that the nearest non-base misses can imitate or even exceed the late branch on gross load, but still fail to fill the same inward left-flank support node that turns the dominant mid packet from `7/8` into `8/12`

The open problem in this basin is no longer whether the family structure exists, whether the frozen bucket exact-closes, why `mode-mix-f` sits inside the anchor band, whether the outer `rect-wrap:local-morph-f` pair is the same mechanism as the frozen `add4` pocket, or whether any non-rect late guardrail ever broadens that outer continuation. The zero-support collapse edge is already isolated, the later moderate anchor-balance band plus `mid_anchor_closure_peak <= 10.000` ceiling still reduces to a skew-wrap right/deep bridge shoulder, a `mode-mix-f` low-support throat, and a frozen `add4` mid-anchor knot, and the `rect-wrap/rect-hard` guardrail still resolves into a heavier beyond-ceiling continuation under `closure_load >= 75.000`; now the broader `base` `peta|exa` non-rect sweep also participates, and the direct compare shows that the current observed late branch exact-separates from the earlier shoulder/throat/knot representatives under `closure_load >= 73.000` while splitting internally into an outer-rect load tail, a positive-intensity taper-hard branch, and a negative-deep skew-wrap branch. The helper-validation detour closed the strongest integrity seam without moving the science: after fixing the stale non-base pack routing inside the shared generated-family helper, the finished `large`/`mirror` first-hit guardrails, exhausted-slice compare, full exhausted-wall translation compare, and packet-neighborhood compare all survive unchanged in substance. Finished non-base late guardrails therefore still contribute no candidate row at all, but the exhausted `large:exa` and `mirror:exa` wall now shows that the missing ingredient is not gross load alone: the nearest non-base misses stall at `mid_anchor_closure_peak = 8.000`, while every observed late-branch row sits at `12.000`, and `mid_anchor_closure_peak >= 10.000` already exact-separates the observed late branch from those nearest exhausted-wall misses. The tighter row-level translation is sharper still: the closest `large` miss already carries the same `12.000` bridge-bridge closure maximum as the late branch, but it is parked on the left anchor band instead of the mid anchor band, and the richer packet metric shows that this focused split is already captured by `delta_mid_left_attached_max >= 0.000`. Once the compare is widened to the whole exhausted wall, the stable structural separator gets cleaner rather than more complex: `mid_candidate_attached_max >= 7.500`, with every observed late row at `8.000` and both exhausted-wall misses at `7.000`. The packet-neighborhood compare now makes the local mechanism explicit across the whole observed late branch: both exhausted-wall mid packets share the same seven-support template, every observed late row completes it by adding the inward left-flank support node at relative `(-1, 0)` plus its four incident bridge-bridge support closures, and the new topology translation compresses that further into one four-incident flank hinge that reconnects the local vertical flank ladder to the packet interior. A bounded adjacent-row confirmation pass now settles the wording choice: on the discovery wall plus a named nearby generated holdout, `mid_anchor_closure_peak >= 10.000`, `mid_candidate_bridge_bridge_closed_pair_max >= 10.000`, `mid_candidate_attached_max >= 7.500`, and the four-incident flank hinge are all equivalent. They all still reject the exhausted wall, and they all already light up the held-out `outer-rect` pair at `ultra|mega`. So the packet-lift / hinge language is real, but it is the common coarse law of the broader beyond-ceiling continuation rather than a unique marker of the late non-rect branch by itself. One bounded within-family compare now closes the active subbranch separator on the present five-row basis: the held-out `outer-rect` pair and the later `taper-hard` / `skew-wrap` rows all keep the same `8/12` packet and four-incident flank hinge, so packet completion itself is no longer the splitter. Above that shared law, the branch coordinates exact-close with one feature each on the current basis: the `outer-rect` pair keeps one low right bridge and also exact-separates under `support_load >= 24.000`; the `taper-hard` pair exact-separates by two right bridges (`high_bridge_right_count >= 1.500`), with the weaker within-family shadow `anchor_closure_intensity_gap >= 1.000`; and the remaining `skew-wrap` row exact-separates by negative deep share (`anchor_deep_share_gap <= -0.334`, equivalently no right bridge). A paired wider-base guardrail now sharpens that read rather than reopening it: both `wider:base:skew-wrap:local-morph-c` and `wider:base:skew-wrap:mode-mix-d` fall back to the depleted `7/8` packet at `mid_anchor_closure_peak = 8.000`, `mid_candidate_attached_max = 7.000`, `mid_candidate_bridge_bridge_closed_pair_max = 8.000`, and no four-incident flank hinge. So neither nearest wider base shoulder adds a fourth shared-packet subbranch. A bounded log-backed closure then rewrites the taper-hard residual more physically on the seven-row control set made of those five shared-packet rows plus both wider shoulders: the shared packet gate still exact-isolates the family, but within it the taper-hard pair exact-separates not only by `anchor_closure_intensity_gap >= 1.000` but also by the cleaner `high_bridge_right_count >= 1.500`. The crucial difference is that the two-right-bridge clause already stays exact on both wider shoulders without needing the packet gate, while the positive-intensity clause still leaks there. So the present beyond-ceiling continuation is best read as one shared packet regime already split into `outer-rect`, `taper-hard`, and `skew-wrap` subbranches, with taper-hard specifically forming the two-right-bridge arm of that regime rather than merely a positive-intensity branch. A finished-log audit now closes the current already-computed outside-family boundary as well: across the exhausted-wall misses, low-support throats, nearby shoulders, and paired wider sentinels, no row hits any shared packet law and none reaches `high_bridge_right_count >= 1.500`, while the helper-fixed non-base first-hit guardrails still report `first_nonrect_row=none`. So the only logged two-right-bridge rows remain the known `base` `peta|exa` taper-hard pair inside the current five-row shared-packet family. The paired farther `ultra` base shoulders now say the same thing one step deeper: both `ultra:base:skew-wrap:local-morph-c` and `ultra:base:skew-wrap:mode-mix-d` again miss all four shared packet laws, stall at the depleted `7/8` packet with no four-incident flank hinge, and stay below the cleaner taper-hard clause with only one right bridge. So the current three-way shared-packet split still does not widen across the checked `ultra` shoulder pair either.

## Current Regime Architecture

The current low-overlap map is:

- Historical exact law: the branch-aware frozen `rc0|ml0|c2` law exact-closes the historical ladder from `192` through `5504`. This is the in-domain historical classifier.
- Support-collapse out-of-domain guard: the first nearby generated failures (`geometry-c/e`) are zero-support collapse rows, so they are best treated as a domain guard rather than as an extension of the historical `pair-only-sensitive` mechanism.
- Subcritical balance basin: after that guard, the surviving nearby generated `pair-only-sensitive` failures sit in a refined anchor-balance regime
  `-2.000 <= anchor_closure_intensity_gap <= 2.333 and mid_anchor_closure_peak <= 10.000`.
  The retained generated realizations are a right/deep shoulder (`anchor_deep_share_gap >= 0.250`) and a low-support throat (`closure_load <= 24.500`). The frozen mid-anchor knot sits above this ceiling at `mid_anchor_closure_peak = 12.000` and marks the exit from the basin rather than another member inside it.
- Supercritical completed-packet regime: above that ceiling, the stable coarse law is the shared `8/12` mid-packet lift
  (`mid_candidate_attached_max >= 7.500`; observed rows also satisfy `closure_load >= 73.000`).
  Inside that shared packet regime, the retained subbranches are:
  - outer-rect tail: `support_load >= 24.000`
  - taper-hard arm: `high_bridge_right_count >= 1.500`
  - skew-wrap arm: `anchor_deep_share_gap <= -0.334`
- Exhausted-wall boundary: the nearest non-base misses stall at the depleted `7/8` packet (`mid_candidate_attached_max = 7.000`, `mid_anchor_closure_peak = 8.000`) with no flank hinge, so the current beyond-ceiling continuation is still base-local against the finished non-base wall.
- Shared reading: in the same crosswalk vocabulary as the generated-DAG bridge, completion/load sets the floor, balance selects the branch, and bottleneck/placement terms sharpen the boundary.

## Active Technical Problem

The main active technical problem is no longer widening the frontier ladder. It is compressing one shared mechanism language across:

- the geometry-side retained card
- the generated-DAG detector-balance bridge
- the current domain guards and branch boundaries

The relevant questions are:

- whether the generated-DAG bridge is stably a two-branch packet regime rather than a one-scalar story
- whether `center_balanced_log_paths` and `center_path_balance` are best read as the same completion/load-plus-balance architecture already retained on the geometry side
- whether the new mover-side packet bridge and the detector-side visibility bridge are already the same smaller completion/load-plus-bottleneck language in two readout channels
- whether the current geometry card is the right smallest domain map:
  - support-collapse guard
  - subcritical balance basin
  - supercritical completed-packet regime
  - exhausted-wall boundary
- which observables should be retained as branch selectors versus demoted to detector-side or placement modifiers
- what the smallest confirmation-style holdout pass is that can test the retained architecture without reopening broad ladder growth
- how to write the stop rule on the field-to-pattern lane most cleanly now that `wide` has a retained local corridor clause, the broad live `last6` branch itself is real, and the remaining `self` residue is best read as config-local rather than further compressible on the current basis

## What Is Still Unresolved

The main unresolved points are:

- the spent-delay action family is favored in the benchmark, but not derived from deeper first principles
- the model now has an exact retained-update / proper-time scalar kinematically, but its relation to the nonlinear gravity action and the observed two-source superposition failure has not yet been reduced to one clean dynamical law
- the corrected `1/L^p` propagator is now the best retained gravity rule, but its detailed response law is only partly universal: the sign fix, `k=0` pure-phase limit, Born compatibility, interference compatibility, and weak-coupling `k^2` scaling all survive, while the stronger lattice-side force surrogate does not transfer cleanly to generated DAGs (`R^2 ≈ 0.20`)
- the gravity field has a quantitative shape on the tested grids, but the right large-scale response observable is still unresolved. The earlier range-plateau story was already retracted, and the newer 2D lensing interpretation has also been retracted: attraction is real, but the current scattering observable does not yet define a clean outgoing deflection angle
- the higher-dimensional story is now split more cleanly than before: modular 3D and 4D substantially improve decoherence, 4D modular channels currently give the strongest large-`N` CL-bath lane on disk, and higher-dimensional chokepoint Born-rule checks are clean; but even the newer binned 4D true-visibility check is mostly weak or near-zero, and the distance law remains effectively flat/topological across the tested linear rescue lanes
- the 5D picture is still density-sensitive: a dense pilot found one positive corner, and the newer robustness map broadens that window around the pilot settings, but it still lives inside a narrow dense modular neighborhood rather than a generic regime
- the distance-law closure is now broader than the earlier 4D sweep alone: propagator-power sweeps, fixed-mass locality-shell sweeps, a minimal local saturation nonlinearity, and an induced/effective-distance readout all fail to recover a clean `1/b` law. The remaining open lane is no longer another local-weight or shell tweak; it is either an analytic explanation of the flat/topological force law or a deeper architecture change
- a first causal-field alternative is interesting but not retained: once the impact-parameter sweep is rerun with fixed mass count and fixed source geometry, the earlier apparent `~1/b` falloff disappears, and the same forward-only field also weakens the retained mass-scaling lane relative to the Laplacian baseline
- the current record story is now topologically split rather than uniformly open: graph-local environment variants still fail or wrong-scale on dense random families, but the IF / CL reduced-description route works much better on the gap-controlled modular family. The refined phase-diagram scripts now use actual traced purity `pur_cl`, and the unresolved problem is no longer “find any decoherence architecture,” but whether the working channel-separated topology can emerge dynamically from a hard-gap node placement / node removal rule instead of being imposed by hand. Soft pruning on already connected graphs is no longer a live asymptotic escape hatch: it helps at intermediate `N`, then the ceiling returns and aggressive pruning disconnects the graph
- on that same retained modular decoherence lane, the old both-slits-open detector-profile contrast remained high enough to be misleading: once replaced with a true single-vs-double-slit visibility gain, the large-`N` interference advantage becomes weak at `N=12`, near-zero by `N=18`, and gone or slightly negative by `N>=25`. So the large-`N` modular story is now “gravity plus decoherence on the same family,” not “gravity, decoherence, and strong interference all remain simultaneously large on the asymptotic bath lane”
- the newest higher-dimensional runs sharpen rather than erase that caveat: 4D large-`N` decoherence looks genuinely strong on the retained modular family, but the current 4D true-visibility script still gives `V_gain ~ 0`, and its detector-profile handling should be treated as provisional until it is rebinned / envelope-checked more carefully
- the default self-maintenance rule now looks oscillatory rather than fixed-point, but the wider rule space still contains stable and growing regimes, so the minimal rule-level principle behind persistent identity has not yet been reduced to one clean law
- low-overlap subtype competition is now much more compressed on the frozen `5504` bucket and exact across the available historical frontier ladder; the first nearby generated edge (`geometry-c/e`) isolates cleanly under a support-collapse guard, and the surviving non-guarded generated pair-only failures (`mode-mix-f`, `local-morph-c`, `mode-mix-d`) now exact-separate from frozen historical `pair-only-sensitive`, `add1-sensitive`, and `add4-sensitive` rows once the moderate anchor-balance band is tightened with `mid_anchor_closure_peak <= 10.000`. Above that ceiling, the current coarse continuation is now cleaner: the held-out `outer-rect` pair at `ultra|mega` shares the same `8/12` mid-packet lift and four-incident flank hinge as the five observed late rows, so the packet-completion law should now be read as the common beyond-ceiling mechanism rather than as a late-only signature. The bounded within-family compare closes the immediate separator on the present basis: the shared packet family already splits into an `outer-rect` low-right-bridge tail, a `taper-hard` two-right-bridge branch, and a `skew-wrap` negative-deep no-right-bridge branch. A paired wider-base guardrail now says the immediate answer is still no fourth shared-packet branch: both `wider:base:skew-wrap:local-morph-c` and `wider:base:skew-wrap:mode-mix-d` drop back to `mid_anchor_closure_peak = 8.000`, `mid_candidate_attached_max = 7.000`, and no flank hinge. A follow-on log-backed closure then sharpens the taper-hard branch itself: the positive-intensity clause still leaks on both wider shoulders unless the shared packet gate is written explicitly, but the cleaner physical clause `high_bridge_right_count >= 1.500` already stays exact across the whole seven-row control set. So the present beyond-ceiling split is now best read as one shared packet regime whose taper-hard arm is specifically the two-right-bridge branch. A finished-log audit then closes the current already-computed outside-family boundary: the exhausted-wall misses, low-support throats, nearby shoulders, and paired wider sentinels all miss the shared packet laws and stay below two right bridges, while the helper-fixed non-base first-hit frontier remains empty. The paired farther `ultra` shoulders now say the same thing one step deeper too: both `ultra:base:skew-wrap:local-morph-c` and `ultra:base:skew-wrap:mode-mix-d` again miss every shared packet law, stay at one right bridge, and still leak only the weaker intensity clause. A fresh scenario-sharded base scan over `ultra|mega|peta|exa` then finds exactly one genuinely new nearby control beyond that paired-shoulder boundary, `exa:base:skew-hard:local-morph-k`. A three-chunk follow-on now resolves what that near miss means. On the six-row family-plus-near-miss set, the old four-rule packet equivalence splits into two layers: `mid_candidate_attached_max >= 7.500` is the only exact separator that survives unchanged, while `mid_anchor_closure_peak` and `mid_candidate_bridge_bridge_closed_pair_max` become exact again only after tightening from `>= 10.000` to `>= 11.000`. A full already-finished boundary audit shows all three of those rules exact against every current outside-family control. The dominant-packet alignment compare then closes the remaining wording seam. The fresh near miss is not one family-like packet competing with an unrelated rotated packet; it is three tied seven-support one-node deletions of the shared family packet:
  - cell `(2, -3)` misses support node `(-1, -1)` and its two incident closed edges
  - cell `(2, 1)` misses support node `(-1, 1)` and its two incident closed edges
  - cell `(4, 1)` preserves the hinge but misses support node `(1, -1)` and its two incident closed edges
  A follow-on deletion-class scan over the already-finished outside boundary shows that this row is currently unique on the logged controls. The older nearby/wider shoulders are harsher `7/8` side deletions that best drop `(0, -1)` or `(0, 1)`, the exhausted-wall misses are `7/8` hinge deletions that best drop `(-1, 0)`, and the low-support throats are deeper multi-node losses. So the fresh `skew-hard` row is the first visible `7/10` corner-deletion rung rather than another instance of the older side/hinge depletion. Hinge presence alone is not enough. The semantics audit makes the law choice explicit: `any dominant packet has hinge` leaks on this near miss, while exact family-template or zero-missing-node statements are more brittle and combinatorial than the unchanged scalar rule. The cleanest current family statement is still the row-level attachment law `mid_candidate_attached_max >= 7.500`, with the deeper packet story understood as one-node completion from `7/10` to `8/12`. A bounded representative compare then fixed the cleanest scalar for that deeper outside ladder. Missing-node position is still the right mechanism label, but it over-splits the harsher rung because side and hinge deletions remove different node roles while staying at the same depletion level, and simple directional attachment tallies are not stable either because the tied corner near miss reuses one hinge column tally and one side row tally across its orientations. The clean scalar is instead local shared-packet closure completion, already visible at row level as `mid_candidate_bridge_bridge_closed_pair_max`: side/hinge stay at `8.000`, the corner near miss lifts to `10.000`, and the realized family completes `12.000`. A finished-boundary closure-deficit summary then sharpened that read. Across the realized family plus the one-node outside boundary, best-aligned lost closed edges matches closure deficit exactly: `12/0` for the five family rows, `10/2` for the corner near miss, and `8/4` for the six side-or-hinge rows. But the low-support throats do not continue that ladder. `ultra|mega:base:taper-wrap:mode-mix-f` collapses to `0` bridge-bridge closed edges with a `12`-edge completion gap while the family-aligned packet comparison exposes only `7` explicit lost edges, so those rows remain deeper multi-node collapse outside the clean one-node closure-deficit regime. The exact family separator still stays `mid_candidate_attached_max >= 7.500`.
- the present mechanism language is more geometric and topological than it was earlier, but it is not yet a clean bridge to standard continuum physics
- the strongest fine-grained mechanism results are exact on the available historical frontier ladder, but not yet a general theorem over nearby generated families because nearby generated transfer still shows in-domain failures after the empirical support-collapse guard is applied

## What Is Still Cheating

This is the explicit "do not flatter ourselves" block.

If you want the more formal reviewer-facing version of this same issue, see:

- [ASSUMPTION_DERIVATION_LEDGER.md](/Users/jonreilly/Projects/Physics/docs/ASSUMPTION_DERIVATION_LEDGER.md)
- [LITERATURE_POSITIONING_NOTE.md](/Users/jonreilly/Projects/Physics/docs/LITERATURE_POSITIONING_NOTE.md)
- [REVIEW_HARDENING_BACKLOG.md](/Users/jonreilly/Projects/Physics/docs/REVIEW_HARDENING_BACKLOG.md)

1. **The benchmark geometries are still partly hand-authored.**  
   The project now has procedural and randomized families, but the core benchmark worlds are still chosen by hand.

2. **The corrected gravity propagator is still selected, not derived.**  
   The geometry-only attenuation `1/L^p` is now much better motivated than the old `1/delay^p` rule because it fixes the gravity sign while preserving Born-like interference, but it is still chosen because it works, not because deeper network dynamics have forced it uniquely.

3. **The delay field chooser is still hand-chosen.**  
   The delay field is derived from persistent patterns, but the rule family and locality preferences used to choose among candidate patterns are still designed rather than derived.

4. **Winner-level robustness still depends on hand-chosen criteria.**  
   Center gap, arrival span, selector policy, and the choice of combined status observable can still change which surviving branch wins on the same candidate pool.  
   Family-level structure is more stable than exact winner identity.

5. **The perturbation ensembles are still modest and structured.**  
   They are broader than they were early on, but they are still first-pass ensembles rather than exhaustive robustness studies.

6. **Weight robustness is still tested in a narrow high-end band.**  
   The current checks concentrate near the spent-delay end of the retained-weight family rather than exploring the whole space evenly.

7. **The random perturbation ensembles are still small and seeded.**  
   They are useful probes, but not yet large-scale random-graph studies.

8. **The geometry-randomization layer is still narrow.**  
   It currently jitters existing graph families rather than exploring a broad random geometry generator.

9. **The procedural graph generator is still small and structured.**  
   It is a useful independent-family probe, not a broad generator of arbitrary graph worlds.

10. **The sweep budgets are still hand-chosen runtime compromises.**  
    Smaller graphs, reduced rule families, and shorter persistence windows still trade completeness for tractability.

11. **Complex amplitudes are still assumed rather than derived.**  
    The toy has a measurement-like story, but not a derivation of the full complex-amplitude machinery.

12. **The strongest current hard-core mechanism results are still frozen-snapshot results.**  
    They may generalize, and some parts already transfer well, but the finest-grained structure is still being studied on a controlled frozen frontier.

13. **The project is still much stronger as toy mechanism science than as a bridge to known physics.**  
    The internal map is real enough to be interesting; the translation to standard physical law is still unfinished.

14. **The good decoherence-supporting topology is still imposed rather than generated.**  
    Gap-controlled modular DAGs are now the first family where gravity and decoherence both work together, but the separating gap is currently built into the generator. Nine emergence-style attempts now fail to produce a stable local law: five feedback-style connection-growth rules, several placement rules, and a later node-removal surrogate that only helps at intermediate `N` before the ceiling returns. The next real theory hurdle is whether a hard-gap node placement or node-removal law can generate the right-sized, slit-centered barrier endogenously, or whether that gap should be treated as part of the effective physics.

## Where The Detailed History Lives

This README is intentionally not the full research diary.

If you want the detailed chronology, active work queue, and worker handoff state, use:

- [AUTOPILOT_WORKLOG.md](/Users/jonreilly/Projects/Physics/AUTOPILOT_WORKLOG.md)
- [physics_autopilot_handoff.md](/Users/jonreilly/Projects/Physics/logs/physics_autopilot_handoff.md)
- [memory.md](/Users/jonreilly/.codex/automations/physics-autopilot/memory.md)
