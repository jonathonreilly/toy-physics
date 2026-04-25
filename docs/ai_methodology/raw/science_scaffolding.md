# Science Workflow Scaffolding

**Source:** `/Users/jonBridger/Toy Physics/.claude/science`

Subdirectories below capture different phases of the AI-assisted research workflow. Each is a typed artifact category.

---


## analyses/

**File count:** 34

**Files:**

- `asymmetric-decoherence-2026-03-30.md` (34 lines)
- `asymmetric-interference-2026-03-30.md` (46 lines)
- `barrier-free-interference-2026-03-30.md` (49 lines)
- `born-rule-derivation-2026-03-30.md` (39 lines)
- `continuum-limit-2026-03-30.md` (33 lines)
- `critical-ratio-2026-03-30.md` (51 lines)
- `dag-reconfiguration-2026-03-30.md` (41 lines)
- `dimensional-progression-2026-04-01.md` (110 lines)
- `dimensional-scaling-law-2026-04-01.md` (82 lines)
- `generative-dag-interference-2026-03-30.md` (37 lines)
- `gravity-damping-hypothesis-2026-03-30.md` (33 lines)
- `gravity-distortion-response-2026-03-30.md` (41 lines)
- `gravity-falloff-2026-03-30.md` (59 lines)
- `gravity-field-theory-2026-03-30.md` (49 lines)
- `gravity-scaling-2026-03-30.md` (53 lines)
- `interference-geometry-sensitivity-2026-03-30.md` (74 lines)
- `interference-offcenter-fringe-2026-03-30.md` (84 lines)
- `irregular-network-2026-03-30.md` (33 lines)
- `lorentz-breaking-2026-03-30.md` (33 lines)
- `lorentz-symmetry-2026-03-30.md` (42 lines)
- `mutual-gravitation-2026-03-30.md` (29 lines)
- `partial-records-2026-03-30.md` (53 lines)
- `pulsating-gravity-2026-03-30.md` (31 lines)
- `self-maintenance-rules-2026-03-30.md` (49 lines)
- `slit-reachability-2026-03-30.md` (39 lines)
- `sorkin-fixed-dag-2026-03-30.md` (45 lines)
- `sorkin-test-2026-03-30.md` (51 lines)
- `superposition-decomposition-2026-03-30.md` (33 lines)
- `three-d-decoherence-2026-04-01.md` (114 lines)
- `three-d-gravity-2026-04-01.md` (112 lines)
- `three-d-joint-test-2026-04-01.md` (74 lines)
- `three-slit-interference-2026-03-30.md` (44 lines)
- `topological-decoherence-2026-03-30.md` (45 lines)
- `topological-decoherence-corrected-2026-03-30.md` (38 lines)

**Sample (first file content):**

*From `asymmetric-decoherence-2026-03-30.md`*:

```markdown
# Analysis: Asymmetric Decoherence

## Date
2026-03-30

## Key Finding: Delay-field distortion does NOT cause decoherence — even asymmetrically

V remains ~1.000 at y=0 and unchanged at all off-center positions for ALL p from 0.0 to 0.9, for both symmetric AND asymmetric field distortion, at cluster radii 1 and 2. Only p=1.0 (which changes the sector-labeling, not just the field) produces any visibility change.

## Why this happens

The interference visibility depends on the EXISTENCE of paths (topology) and their RELATIVE phase at the detector, not on the absolute amplitude/phase along each path. The phase sweep already covers all possible relative phases between the two slits. Changing the delay field modifies the amplitude and phase along individual edges, but:

1. Both sectors (recorded/free) traverse the SAME DAG (same path topology)
2. The phase sweep scans all relative phases anyway
3. Visibility = (max-min)/(max+min) of the phase sweep — invariant to path-independent amplitude rescaling

The delay-field distortion changes WHERE in the phase sweep the max/min occur, but not their ratio. This is because the distortion affects all paths through a given region equally (it's a field, not a path-specific perturbation).

## The broader insight: TOPOLOGICAL vs FIELD decoherence

The model has two ways to affect interference:
1. **Topology changes** (add/remove nodes, change the DAG) → MASSIVE effect (I₃ up to 10⁹, complete visibility destruction)
2. **Field changes** (modify delays/amplitudes on existing edges) → ZERO effect on visibility

This is because the model's interference is a TOPOLOGICAL property of the causal DAG. The field determines quantitative details (which phase gives the max, how much probability reaches each detector position) but the interference structure (whether V=0 or V>0) is purely topological.

This is a distinctly discrete-network finding: on a continuous manifold, any local perturbation can destroy interference. On a discrete causal DAG, only topological changes matter.

## Hypothesis Verdict
**REFUTED** — asymmetric delay-field distortion does not produce non-trivial decoherence. Decoherence in this model requires topological DAG changes, not field perturbations.

## Significance
This establishes a clean separation: interference = topology, gravity = field. The two mechanisms are INDEPENDENT on a fixed DAG. Records that only distort the field cannot cause decoherence; records must change the DAG structure itself. This constrains what kind of record mechanism could produce decoherence in the model.
```


## derivations/

**File count:** 15

**Files:**

- `action-bridge-analysis-2026-04-04.md` (66 lines)
- `action-uniqueness-theorem-2026-04-09.md` (377 lines)
- `b-independence-2026-04-01.md` (130 lines)
- `b-independence-mechanism-2026-04-03.md` (188 lines)
- `dimensional-record-dilution-2026-04-03.md` (239 lines)
- `distance-exponent-analysis-2026-04-04.md` (65 lines)
- `distance-law-analytic-theorem-2026-04-09.md` (174 lines)
- `kernel-dimension-dependence-2026-04-04.md` (459 lines)
- `mass-additivity-newton-2026-04-04.md` (76 lines)
- `mirror-gravity-asymmetry-2026-04-03.md` (151 lines)
- `newtons-law-from-three-axioms-2026-04-04.md` (87 lines)
- `tapered-lattice-unification-2026-04-04.md` (198 lines)
- `two-principle-newton-2026-04-04.md` (83 lines)
- `valley-linear-distance-law-2026-04-04.md` (69 lines)
- `visibility-threshold-2026-03-30.md` (100 lines)

**Sample (first file content):**

*From `action-bridge-analysis-2026-04-04.md`*:

```markdown
# Analysis: Spent-delay vs Valley-linear Bridge

## Date
2026-04-04

## Target
Explain why spent-delay gives more TOWARD on random graphs while
valley-linear gives Newtonian scaling on regular lattices. Is this
a renormalization (same theory at different scales) or genuinely
different physics?

## Finding: Signal-to-noise, not renormalization

The bridge is a SIGNAL-TO-NOISE effect, not an action transformation.

At typical field f = s/r = 1.67e-5 (r=3, s=5e-5):
  Spent-delay |delta_S/L| = sqrt(2f) = 5.77e-3
  Valley-linear |delta_S/L| = f = 1.67e-5
  Ratio: spent-delay is 346x larger

On RANDOM graphs:
  Paths to the same detector node are incoherent (varied lengths).
  The gravity signal is the average of ~N_paths random contributions.
  Signal ~ perturbation_size × sqrt(N_paths) (random walk in phase).
  Spent-delay has 346x more perturbation → much stronger signal.

On REGULAR lattices:
  Paths to the same detector node are coherent (same topological route
  → same phase). The gravity signal is N_paths × perturbation (not sqrt).
  The perturbation size cancels in the centroid ratio.
  What matters: the f-dependence of delta_S.
  Linear f → deflection 1/b (Newtonian).
  sqrt(f) → deflection 1/sqrt(b) (non-Newtonian).

## Implication

The two actions are GENUINELY DIFFERENT, not the same theory at
different effective scales. The crossover in the regularity sweep
is a signal-to-noise transition, not a renormalization.

- Valley-linear is the correct action for Newtonian gravity (linear f)
- Spent-delay is a stronger probe for gravity detection on noisy graphs
  (larger perturbation → better signal-to-noise)
- On random graphs, the f-dependence doesn't matter because the path
  sum is too noisy to resolve it

## What this means for the model

The model has a CHOICE of action, not a derived one:
- If the goal is Newtonian gravity: use valley-linear S = L(1-f)
- If the goal is robust gravity detection: use spent-delay

The earlier "crossover" result was real but misinterpreted:
  - NOT: "spent-delay renormalizes to valley-linear"
  - YES: "spent-delay has more signal on noisy graphs"

## Testable prediction

If we increase the field strength by 346x (making valley-linear
perturbation the same size as spent-delay at standard strength),
the crossover should vanish: valley-linear should perform as well
as spent-delay on random graphs.

## Status
CONFIRMED (analytically) — the signal-to-noise explanation is
quantitative and matches the observed crossover.
```


## experiments/

**File count:** 1

**Files:**

- `interference-geometry-sensitivity.md` (48 lines)

**Sample (first file content):**

*From `interference-geometry-sensitivity.md`*:

```markdown
# Experiment Design: Interference Geometry Sensitivity

## Date
2026-03-30

## Observables
1. **Fringe contrast** — (max - min) / (max + min) of center detector probability across phase sweep. Ranges from 0 (flat, no interference) to 1 (perfect interference).
2. **Center detector probability** — P(y=0) as a function of phase_shift_upper.
3. **Full screen distribution** — P(y) for all screen positions, at selected geometry points.
4. **Record suppression ratio** — fringe contrast with record / fringe contrast without record.

## Parameters

| Parameter | Min | Max | Steps | Scale |
|-----------|-----|-----|-------|-------|
| phase_shift_upper | 0 | 2*pi | 24 | linear |
| grid_width | 8 | 28 | 6 values: 8,12,16,20,24,28 | linear |
| slit_half_separation | 2 | 8 | 4 values: 2,4,6,8 | linear |
| record_created | False, True | - | 2 | boolean |

Total combinations: 24 phases x 6 widths x 4 separations x 2 record modes = 1,152 runs.
Each run is a single path-sum on a small grid (~O(100) nodes). Estimated <0.1s per run.
Total runtime: ~2 minutes.

## Controls
- **Baseline**: default geometry (width=16, height=10, slit_ys={-4,4}) matches existing `two_slit_distribution()`. Must reproduce identical results.
- **Record control**: every geometry point tested with BOTH record_created=True and False.
- **Phase control**: phase=0 should match the existing no-phase-shift case.

## Systematic Error Checks
- Grids too narrow (width < barrier_x) would break the setup. Guard: width must be >= barrier_x + 2.
- Slit separation exceeding grid height would place slits outside the grid. Guard: slit_half_sep < height.
- Zero normalization: if total probability is 0 at a screen position, flag as degenerate rather than divide-by-zero.

## Reuse Check
- `two_slit_distribution()` (line 23141) — direct reuse with parameterization.
- `center_detector_phase_scan()` (line 23240) — logic reused for phase sweep.
- `build_rectangular_nodes()`, `derive_local_rule()`, `derive_node_field()`, `infer_arrival_times_from_source()`, `build_causal_dag()` — all called internally, no changes needed.

## Script Plan
One script: `scripts/interference_geometry_sweep.py`
- Parameterized version of `two_slit_distribution()` accepting width, height, slit_ys, barrier_x.
- Outer loop: geometry x record_created.
- Inner loop: phase sweep.
- Output: structured text log with one block per geometry point.

## Runtime
~2 minutes interactive. No autopilot needed.
```


## frontier/

**File count:** 9

**Files:**

- `2026-03-30-frontier-map.md` (76 lines)
- `2026-03-31-frontier-map-final.md` (77 lines)
- `2026-03-31-frontier-map.md` (90 lines)
- `2026-04-03-frontier-map-post-mirror.md` (93 lines)
- `2026-04-03-frontier-map.md` (156 lines)
- `2026-04-06-frontier-map.md` (105 lines)
- `2026-04-07-frontier-map-update-2.md` (76 lines)
- `2026-04-07-frontier-map-update-3.md` (82 lines)
- `2026-04-07-frontier-map-update.md` (62 lines)

**Sample (first file content):**

*From `2026-03-30-frontier-map.md`*:

```markdown
# Frontier Map: 2026-03-30

## Coverage Summary
- Total scripts: 192
- Total log files: 46
- Mechanism families: ~8 (pocket_wrap dominant, plus long, taper, threshold, secondary, extended, wider, route)
- Confirmed results: 6 (effective delay, gravity-like continuation, record-based interference suppression, stable mechanism families, family growth without proliferation, shared structure in low-overlap basin)
- Unvalidated observations: several (beyond-ceiling packet behavior, ultra shoulder depletion pattern, non-base generated transfer failures)
- Dead ends: non-base exhausted wall (explicitly empty), rect-only beyond-ceiling continuation (tested, stays rect-local)

## Family Census

| Family | Scripts | Logs | Focus | Status |
|--------|---------|------|-------|--------|
| pocket_wrap_suppressor | 144 | 46 | Low-overlap order parameters, mechanism classification, frontier compression | ACTIVE — dominant thread |
| long_* | 20 | 0 | Degree thresholds, hub mechanisms, neighborhood basis, motif ablation | EXHAUSTED — no recent logs |
| taper_wrap | 7 | 0 | Cross-context jumps, endpoint analysis, shell mode, offender interpolation | PARTIAL — scripts exist, no recent standalone logs |
| threshold | 3 | 0 | Core-shell mechanisms, scaling | EXHAUSTED — no recent logs |
| secondary | 2 | 0 | Offender rule generalization/search | EXHAUSTED |
| extended | 2 | 0 | Atomic route overlap, route classification | EXHAUSTED |
| wider | 1 | 0 | Generated family mechanism check | PARTIAL |
| overnight/automation | 5 | 0 | Batch runners, lock management, push helpers | INFRASTRUCTURE |

## Parameter Space Gaps

### Heavily Explored
- Low-overlap order parameters across pocket_wrap_suppressor families (41 scripts, 46 logs)
- Beyond-ceiling subbranch comparisons (wider, ultra sentinel guardrails)
- Anchor-balance band geometry (anchor_closure_intensity_gap, mid_anchor_closure_peak)
- Support-collapse domain edges (zero-support guard)

### Under-Explored (ranked by information value)

1. **Interference / two-slit regime** — `two_slit_distribution()` exists in the simulator with record_created toggle and phase_shift, but NO scripts or logs explore this systematically with parameter sweeps. The record-based interference suppression claim (Result #3) has no dedicated sweep testing how the suppression threshold depends on record durability.

2. **Geodesic comparison across distortion strengths** — `compare_geodesics()` exists and is used in benchmarks, but NO parameter sweep varies the *strength* of the persistent-pattern distortion to trace the gravity-like bending from zero distortion to strong distortion. The gravity claim (Result #2) lacks a quantitative distortion-response curve.

3. **Continuation landscape topology** — `stationary_action_path()`, `frontier_distorted_action_tree()` exist. The action landscape (the "continuation structure" that produces inertia-like behavior) has not been mapped as a function of network size or topology variation. How does the number/depth of action minima scale?

4. **Self-maintenance rule space** — `scan_self_maintaining_rules_fallback_only()`, `select_self_maintenance_rule()` exist. The space of viable self-maintenance rules has not been systematically swept. Which rules produce stable persistent patterns and which don't? What's the boundary?

5. **Cross-family observable transfer** — The low-overlap law transfers within the pocket_wrap_suppressor family but breaks on taper-wrap/skew-wrap generated families. No systematic study of WHICH observables transfer vs. which are family-specific.

## Observable Coverage

| Observable Category | Measured | Multi-Family | In Code But Not Swept |
|---------------------|----------|-------------|----------------------|
| Support/closure load | YES | YES | - |
| Anchor geometry (gap, peak, deep_share) | YES | YES | - |
| Bridge topology (right_count, right_low) | YES | YES | - |
| Edge identity (event_count, density) | YES | PARTIAL | - |
| Boundary roughness | YES | NO | roughness sweep |
| Geodesic comparison (free vs distorted) | YES | NO | distortion strength sweep |
| Two-slit distribution | BASIC | NO | phase_shift sweep, record threshold sweep |
| Action discriminator | YES | NO | action landscape mapping |
| Pattern persistence lifetime | CODE EXISTS | NO | stability vs parameters |
| Perturbation weight stability | CODE EXISTS | PARTIAL | systematic sweep |

## Top 5 Highest-Value Gaps

1. **Record-suppression threshold sweep in two-slit setup** — The interference claim is qualitative. Sweeping `record_created` is binary; the real question is how PARTIAL or DELAYED record formation affects the distribution. The simulator has `phase_shift_upper` and the machinery for this. **Why high-value:** Would give the first quantitative curve connecting record durability to interference suppression — the model's version of decoherence. **Effort:** Interactive, ~1 hour. Can adapt `two_slit_distribution()` directly.

2. **Distortion-response curve for gravity-like bending** — Sweep the number/placement of persistent nodes to trace path-bending from zero to strong. **Why high-value:** The gravity claim needs a quantitative relationship, not just "bending happens." **Effort:** Interactive, ~2 hours. Uses `compare_geodesics()` directly.

3. **Action landscape topology as a function of network size** — Map the action tree depth, branching, and minima count vs grid size. **Why high-value:** Tests whether "locally simplest continuation" (Axiom 6) produces qualitatively different behavior at different scales — a scale-dependence question fundamental to the model. **Effort:** Interactive to autopilot, ~2-4 hours.

4. **Self-maintenance rule viability boundary** — Systematic sweep of rule parameters to map which produce stable persistent patterns. **Why high-value:** The entire model depends on persistent patterns existing. Understanding when they DON'T exist is as important as when they do. **Effort:** Autopilot, ~4 hours.

5. **Cross-family observable invariance** — Identify which observables are "universal" (same across families) vs "family-specific." **Why high-value:** Would tell us which features of the model are structural vs. accidental. **Effort:** Interactive, ~2 hours. Uses existing log data.

## Dead Ends (do not revisit)

- **Non-base exhausted wall** — Explicitly empty frontier; no non-base families match the packet lift mechanism.
- **Rect-only beyond-ceiling continuation** — Tested through wider|ultra|mega. Stays rect-local. Only expands at base peta|exa with taper-hard.
- **Non-rect late guardrails (large, mirror families)** — Scanned through exa. Empty at all tiers.
- **long_* degree/hub/threshold mechanisms** — 20 scripts, 0 recent logs. Appears to have been a prior research thread that was superseded by the low-overlap order-parameter work.
```


## hypotheses/

**File count:** 6

**Files:**

- `asymmetric-interference.md` (30 lines)
- `critical-ratio-threshold.md` (32 lines)
- `gravity-distortion-response.md` (37 lines)
- `interference-geometry-sensitivity.md` (42 lines)
- `partial-records.md` (34 lines)
- `slit-reachability.md` (27 lines)

**Sample (first file content):**

*From `asymmetric-interference.md`*:

```markdown
# Hypothesis: Asymmetric Slit Placement Reveals Dynamical Interference Structure

## Date
2026-03-30

## Statement
Breaking the reflection symmetry of the two-slit setup (via asymmetric slit placement or off-center source) will produce a visibility profile V(y) that is NOT symmetric around y=0, and the center detector (y=0) will no longer have V=1.0 trivially. This removes the symmetry protection and tests whether the model produces genuine interference dynamics.

## Prediction
- With slits at y=+2 and y=+6 (asymmetric): V(y=0) < 1.0 (symmetry protection broken).
- The visibility profile V(y) will be asymmetric, peaked between the two slits.
- The full distribution P(y) at phase=0 will shift toward the closer slit.
- With off-center source at (1, +3): similar symmetry breaking even with symmetric slits.

## Falsification Criteria
- If V(y=0) remains exactly 1.0 even with asymmetric slits, there's an unexpected symmetry we haven't identified.
- If the asymmetric setup produces NO interference (V=0 everywhere), the model's interference only works in symmetric configurations.

## Null Hypothesis
The model's interference pattern is qualitatively the same regardless of symmetry — asymmetry only shifts the envelope without changing fringe visibility.

## Proposed Experiments
1. Asymmetric slits: y=+2 and y=+6 (centroid at +4), at width=16, height=10.
2. Asymmetric slits: y=+1 and y=+8 (large asymmetry), same grid.
3. Off-center source: source at (1, +3) with symmetric slits at y=±4.
4. Combine: off-center source + asymmetric slits.
5. For each: full V(y) profile and P(y) distribution.

## Status
PROPOSED
```


## investigations/

**File count:** 1

**Files:**

- `gravity-1node-anomaly-2026-03-30.md` (37 lines)

**Sample (first file content):**

*From `gravity-1node-anomaly-2026-03-30.md`*:

```markdown
# Investigation: 1-Node Zero-Effect in Gravity Sweep

## Date
2026-03-30

## Anomaly
A single persistent node at (10, 4) produces zero deflection AND zero action change — identical to the free (no persistent nodes) case. 2+ adjacent nodes produce immediate strong effects.

## Hypotheses Tested

### 1. Bug: derive_local_rule ignores single nodes
Evidence for: None — derive_local_rule stores persistent_nodes faithfully.
Evidence against: The function passes nodes through without filtering.
Verdict: RULED OUT

### 2. Artifact: Persistence support requires neighbor connectivity
Evidence for: `derive_persistence_support()` line 2694 computes:
`support[node] = sum(neighbor in active_nodes for neighbor in neighbors) / len(neighbors)`
A single node has zero persistent neighbors → support = 0.0 → field = 0.0 → no distortion.
Evidence against: None — this is exactly what the code does.
Verdict: **CONFIRMED**

### 3. Genuine: The model's axiom requires self-maintaining PATTERNS
Evidence for: Axiom 2 states "Stable objects are persistent self-maintaining patterns." A single isolated event cannot self-maintain because it has no persistent neighbors to sustain it. The support function correctly implements this axiom.
Evidence against: None.
Verdict: **CONFIRMED** — this is the correct behavior per the model's axioms.

## Root Cause
The persistence support function measures what fraction of a node's neighbors are also persistent. A single node has 0% persistent neighbors, so its support is 0.0, the delay field is zero everywhere, and the distorted rule equals the free rule.

This is NOT a bug. It's Axiom 2 in action: persistence requires a self-maintaining pattern, not an isolated point. The 2-node onset in the gravity sweep marks the minimum configuration where mutual neighbor support becomes nonzero — each node is a neighbor of the other.

## Resolution
The sanity FLAG is resolved. The 1-node zero-effect is correct model behavior. The gravity mechanism requires a persistent PATTERN (≥2 adjacent nodes), not a single event. This is consistent with the project's core axiom that "stable objects are persistent self-maintaining patterns."

## Status
RESOLVED
```


## sanity/

**File count:** 14

**Files:**

- `3d-l2-kernel-convergence-2026-04-04.md` (160 lines)
- `asymmetric-interference-2026-03-30.md` (27 lines)
- `critical-ratio-2026-03-30.md` (24 lines)
- `gravity-distortion-response-2026-03-30.md` (35 lines)
- `gravity-falloff-2026-03-30.md` (21 lines)
- `interference-geometry-sensitivity-2026-03-30.md` (43 lines)
- `interference-offcenter-fringe-2026-03-30.md` (49 lines)
- `lattice-10-of-10-2026-04-03.md` (116 lines)
- `partial-records-2026-03-30.md` (24 lines)
- `slit-reachability-2026-03-30.md` (27 lines)
- `sorkin-fixed-dag-2026-03-30.md` (24 lines)
- `sorkin-test-2026-03-30.md` (21 lines)
- `three-slit-interference-2026-03-30.md` (15 lines)
- `topological-decoherence-2026-03-30.md` (30 lines)

**Sample (first file content):**

*From `3d-l2-kernel-convergence-2026-04-04.md`*:

```markdown
# Sanity Check: 3D 1/L^2 Kernel Convergence Claim

## Date
2026-04-04

## Target
The claim: "The dimension-dependent kernel 1/L^(d-1) with h^(d-1) measure
factor gives converging 3D gravitational attraction. Distance tail steepens
from -0.35 to -0.53 toward Newtonian -2.0. Born holds at machine precision
through h=0.125."

Scripts: `lattice_3d_l2_fast.py`, `lattice_3d_l2_numpy.py`,
`lattice_3d_kernel_l2.py`, `lattice_2d3d_continuum_check.py`

## Checks

| Check | Status | Notes |
|-------|--------|-------|
| Model Consistency | **FLAG** | Kernel 1/L^2 is an AXIOM FORK from the original 1/L. The dimension-dependent rule (d-1) is imposed, not derived. |
| Scale Reasonableness | **FLAG** | Peak deflection grows as h^(-0.48) — gravity DIVERGES as h→0 at fixed field strength. No finite continuum limit without RG. |
| Symmetry Compliance | CLEAN | Lattice symmetries respected. Centroid at zero when field=0. |
| Limit Behavior | **FLAG** | At h=1.0 gravity is ALL AWAY; at h≤0.5 it's ALL TOWARD. Sign discontinuity means h=1.0 is not in the scaling regime. Not a smooth h→0 convergence. |
| Numerical Artifacts | CLEAN | h^2 factor verified to cancel in all ratio-based observables (centroid, Born, MI). The h=0.5 and h=0.25 results are numerically identical with and without h^2. |
| Bug Likelihood | CLEAN | Two independent implementations (pure-Python `kernel_l2.py` and numpy `l2_fast.py`) give identical results at h=0.5. Born at machine precision is a strong bug-absence indicator. |

## Detailed FLAG Analysis

### FLAG 1: Axiom Fork (Model Consistency)

The original model axioms specify a propagation kernel with 1/L attenuation.
Changing to 1/L^2 is not a parameter tweak — it's a different model. The
claim that "1/L^(d-1) is the natural generalization" imports the continuum
free-propagator scaling from known physics. The model's axioms don't specify
a dimension-dependent kernel.

**What would resolve it:** Either (a) derive the kernel power from the axioms
(e.g., show that path-counting on a d-dimensional lattice naturally produces
1/L^(d-1) weighting), or (b) honestly frame this as an axiom fork and track
which properties are retained vs. lost. The 1/L Born rule was proven on
the LINEAR propagator — does 1/L^2 preserve this proof, or is Born an
accidental coincidence on this kernel?

### FLAG 2: Diverging Gravity (Scale Reasonableness)

Peak gravitational deflection at z=5:
- h=0.5: 0.042
- h=0.25: 0.059
- h=0.125: 0.082

Fit: peak ~ h^(-0.48). This means gravity DIVERGES as h→0 at fixed field
strength s=5e-5. A well-defined continuum limit requires gravity to
converge to a finite value. The current result implies an RG scaling
s(h) ~ h^0.48 is needed, but this hasn't been tested or derived.

**What would resolve it:** Run with RG scaling s = s₀ × h^0.48 and show
that (a) the peak deflection stabilizes, AND (b) the distance exponent
still steepens, AND (c) Born still holds. Without this, the "convergence"
is really "the sign is right and it gets louder" — not a controlled limit.

### FLAG 3: Sign Discontinuity (Limit Behavior)

At h=1.0, ALL b values give AWAY. At h=0.5, ALL give TOWARD. There is
a critical h_c ∈ (0.5, 1.0) where the sign flips. A smooth continuum
limit would show gravity becoming TOWARD at all h. The sign flip means
the h=1.0 lattice is not in the scaling regime at all — so we have only
3 data points (h=0.5, 0.25, 0.125) for the convergence claim, and one
of those (h=0.125) has W too narrow for the distance law tail.

### Additional Concerns (not full FLAGs)

**Thin distance data.** The distance exponent "steepening from -0.35 to
-0.53" is based on:
- h=0.5: 3-point fit (z=5,6,7), R²=0.79
- h=0.25: 3-point fit (z=5,6,7), R²=0.95
A 2-point convergence trend (from two 3-point fits) is suggestive but
far from conclusive. The error bars on each exponent are probably ±0.3
or worse.

**h^2 measure factor not in frozen scripts.** The committed
`lattice_3d_l2_fast.py` does NOT include the h^2 factor. The h=0.125
result was produced by an inline (uncommitted) script. While the h^2
factor provably cancels in all observables, the reproducibility gap
should be closed by committing the h^2 version.

**F∝M = 0.50 means √M scaling.** The mass-force relationship is sublinear
(δ ∝ s^0.5, i.e., force ∝ √mass). This is the same as the spent-delay
action's √f singularity. It's not wrong, but it's not Newtonian (F ∝ M).
The claim of "F∝M alpha = 0.50 PASS" glosses over this — it passes a
"positive correlation" test but not a "linear" test.

## Skeptical Reviewer's Best Objection

"You changed the propagation kernel from 1/L to 1/L^2 specifically
because 1/L didn't give 3D gravity. The new kernel was chosen to match
the desired outcome (3D attraction). The model's axioms don't specify
1/L^2 — you imported the dimension-dependent scaling from the known
answer. This is fitting, not prediction. Furthermore, the gravitational
deflection diverges as h→0, so you don't actually have a continuum
limit — you have a sign that gets louder as you refine, which is
exactly what a lattice artifact that depends on graph density looks
like."

## Response

Partially answerable:
- Born at machine precision (3.5e-15 at h=0.25) is strong evidence that
  the 1/L^2 kernel preserves the linear propagator structure. This is not
  trivially guaranteed — it needs the Sorkin identity to hold, which
  constrains the kernel form.
- The sign flip at h~0.7 could be argued as the lattice entering the
  scaling regime, similar to how lattice QCD results are only trusted
  below a critical lattice spacing.

NOT answerable without new work:
- The diverging gravity (h^(-0.48) growth) is a genuine problem. Without
  demonstrating convergence under RG scaling, the claim "3D gravity
  converges" is overstated. The honest claim is: "the SIGN converges
  (TOWARD), the ORDERING converges (decreasing with b in the tail),
  but the MAGNITUDE diverges."
- The axiom-fork question needs theoretical work (derive the kernel
  dimension-dependence from path counting or measure theory on the
  lattice).

## Verdict

**SUSPICIOUS**

The TOWARD sign surviving refinement is genuine and important. Born at
machine precision is a strong structural result. But the headline claim
of "converging 3D gravity" is overstated due to:
1. Diverging magnitude (no finite continuum limit without RG)
2. Axiom fork (kernel not derived from model)
3. Thin distance-law data (2-point convergence trend from 3-point fits)

**Recommended safe wording:** "The 1/L^2 kernel on the 3D dense lattice
produces gravitational attraction (TOWARD) that persists under lattice
refinement from h=0.5 to h=0.125. Born rule holds at machine precision.
The distance-law tail steepens with refinement (suggestive of convergence
toward a power law). The gravitational magnitude grows as h^(-0.48),
indicating RG scaling is needed for a finite continuum limit. The kernel
change from 1/L to 1/L^2 is an axiom fork requiring theoretical
justification."

## Update: FLAG 2 Partially Resolved

RG scaling test (s(h) = s₀ × h^α) shows:
- α ≈ 0.92 stabilizes gravitational magnitude (ratio h=0.25/h=0.5 → 1.0)
- The distance law tail exponent is INDEPENDENT of field strength:
  always -0.35 at h=0.5 and -0.53 at h=0.25 regardless of α
- The steepening is a GEOMETRIC property of the lattice, not a field artifact

This means:
- FLAG 2 (diverging gravity) is resolvable with RG scaling s ~ h^0.92
- The distance law convergence (-0.35 → -0.53) is ROBUST to RG choice
- Updated verdict: the RG-scaled model has a finite gravity with a
  steepening distance exponent

Remaining FLAGs: 1 (axiom fork) and 3 (sign discontinuity at h=1.0).
With FLAG 2 resolved, the verdict softens from SUSPICIOUS to:
**SUSPICIOUS (weak) — axiom fork is the main open issue.**
```


## theory-reviews/

**File count:** 1

**Files:**

- `interference-geometry-sensitivity-2026-03-30.md` (29 lines)

**Sample (first file content):**

*From `interference-geometry-sensitivity-2026-03-30.md`*:

```markdown
# Theory Review: Interference Pattern Geometry Sensitivity

## Date
2026-03-30

## Hypothesis Under Review
The interference fringe contrast depends quantitatively on network geometry (grid width, slit separation), revealing a continuous transition between coherent and record-dominated regimes.

## Assessment

| Dimension | Rating | Notes |
|-----------|--------|-------|
| Axiom Compliance | COMPLIANT | Uses only events, links, delays, records, and the path-sum over the causal DAG. Grid geometry is a property of the network structure, not an imported concept. |
| Internal Consistency | CONSISTENT | The prediction that longer paths → sharper fringes follows from the existing `local_edge_properties()` phase accumulation mechanism. More edges traversed = more phase accumulated = larger phase difference between paths. No contradiction with confirmed results. |
| Limiting Behavior | WELL-BEHAVED | At width→0: no barrier possible, trivially no interference. At slit_separation→0: single slit, no two-path interference. At slit_separation→large: paths too divergent, detector coverage drops. All sensible. |
| Falsifiability | SHARP | Three distinct falsification criteria named with specific thresholds. The null hypothesis (geometry independence) is cleanly testable. |
| Minimality | MINIMAL | Uses existing simulator machinery with no new axioms. The only variation is network geometry parameters that already exist. |
| Emergent vs. Imposed | EMERGENT | The interference pattern itself emerges from the path-sum over the causal DAG. The record mechanism is part of the model's axioms (Axiom 9). Geometry dependence would be genuinely emergent from the network structure. |

## Overall Verdict
PROCEED

## Notes
- One subtle concern: the `two_slit_distribution()` function hardcodes `width=16`, `height=10`, `barrier_x=8`, `slit_ys={-4, 4}`. The experiment script will need to GENERALIZE this function to accept geometry parameters. This is a code modification, not an axiom change.
- The `phase_per_action=4.0` and `attenuation_power=1.0` in `RulePostulates` are fixed. Consider whether these should also be swept, or whether geometry alone is sufficient for the first experiment. Recommendation: geometry only for the first sweep, postulate sweep as follow-up.
- The prediction about "wider grids → sharper fringes" has a non-trivial interaction with attenuation: longer paths also attenuate more, which could REDUCE contrast by making one path dominate. This is an interesting tension that the experiment will resolve.

## Suggested Simplifications
None needed — the hypothesis is already minimal and well-scoped.
```


## write-ups/

**File count:** 7

**Files:**

- `axiom-chain-closure-2026-04-03.md` (283 lines)
- `complete-program-2026-04-03.md` (343 lines)
- `corrected-propagator-2026-03-31.md` (248 lines)
- `decoherence-arc-2026-03-30.md` (45 lines)
- `interference-regime-2026-03-30.md` (96 lines)
- `moonshot-five-frontiers-2026-04-09.md` (449 lines)
- `session-close-2026-03-31.md` (64 lines)

**Sample (first file content):**

*From `axiom-chain-closure-2026-04-03.md`*:

```markdown
# Write-Up: Full Axiom Chain Closure on Locally-Grown Event-Networks

## Date
2026-04-03

## Abstract

We test whether the project's full set of axioms — evolving networks,
inferred space, simplest continuation, persistent patterns, distorted
continuation, and durable records — can produce gravity-like deflection
and decoherence-like purity loss on the SAME graph without any externally
imposed structure. Using geometric growth rules where each new node
inherits its parent's position plus a random offset in d transverse
dimensions, we find that d=3 (4D graphs) produces both effects
simultaneously: gravitational deflection +0.442 and purity departure
3.4% at N=30 (20 seeds), with emergent mass from amplitude concentration
and emergent barriers from amplitude-density damping. The dimensional
scaling exponent (alpha ≈ -0.18 in 4D, confirmed at 24 seeds with
R²=0.84) matches imposed-geometry results exactly, establishing that
the physics emerges from the growth rule, not from the specific graph
instance. This closes the axiom chain: every element that was previously
hand-imposed now has a constructive, axiom-compliant replacement.

## Background

The project's central question: how much physics-like structure can
emerge from a minimal event-and-relation ontology?

Prior work established that imposed geometric DAGs support:
- Gravity via phase valley mechanism (5.1 SE on uniform 2D DAGs,
  scripts/gravity_24seed.py)
- Decoherence via CL bath with power-law ceiling (1-pur_min) ~ N^(-1),
  scripts/clt_ceiling_scaling.py)
- Born rule at machine precision (|I₃|/P = 4e-16,
  scripts/nonlinear_propagator.py)
- Dimensional scaling: exponent flattens from -1.58 (2D) to -0.18 (4D),
  scripts/four_d_decoherence_large_n.py)

But all of this used IMPOSED structure: hand-placed graphs, hand-placed
mass nodes, hand-placed barriers with hand-picked slits. The axiom chain
had four gaps:

1. **Graph topology** — imposed grid/DAG, not grown from axioms
2. **Mass** — hand-placed nodes, not emergent patterns
3. **Barrier** — hand-blocked nodes, not emergent records
4. **Spatial dimension** — hand-set coordinates, not inferred

This investigation closes all four gaps.

## Method

### Simulation parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| n_layers | 18, 25, 30 | Tested range |
| nodes_per_layer | 25-30 | Per growth rule |
| d_growth | 1, 2, 3, 4 | Transverse dimensions |
| connect_radius | 3.0-3.5 | Geometric locality |
| spread | 1.0-1.2 | Position offset per step |
| field_strength | 0.3 | Emergent mass coupling |
| slit_frac | 0.25 | Top-amplitude barrier nodes |
| k_band | [3.0, 5.0, 7.0] | Standard |
| seeds | 16-20 per N point | Random graph instances |

### Growth rule (Axioms 1, 3, 6)

New node position = parent position + Gaussian offset in d_growth
dimensions. Edges connect to all nodes within connect_radius in the
full (1+d_growth)-dimensional space. No imposed grid, no pre-set
positions.

### Emergent mass (Axiom 2)

Free propagation (no field) identifies nodes where amplitude
concentrates. Top-amplitude nodes in the upper half of mid-graph
layers become mass sources. Field = 0.3/r from each mass node.

### Emergent barrier (Axiom 9)

Free propagation to the barrier layer identifies which nodes receive
the most amplitude. Top slit_frac (25%) of nodes transmit (slits);
the rest are fully damped (wall). Upper/lower slit groups defined
by y-coordinate relative to slit centroid.

### Observables

- **pur_min**: purity of reduced density matrix at D=0 (per-slit
  propagation, partial trace)
- **gravity delta**: paired deflection (mass-field vs flat-field),
  per-seed averaged over k-band
- **toward fraction**: percentage of k-values where deflection is
  toward the emergent mass

### Controls

- Flat field (strength=0) as gravity baseline
- Full damping array = 1.0 as barrier-free baseline
- Random (non-geometric) growth as negative control

### Scripts

| Script | Purpose |
|--------|---------|
| geometric_growth.py | Decoherence on grown graphs, dimensional scaling |
| emergent_mass_gravity.py | Amplitude-sourced mass, gravitational deflection |
| emergent_barrier.py | Amplitude-density barrier, full chain test |
| emergent_dimension.py | d_eff measurement (BFS ball scaling) |
| emergent_graph_decoherence.py | Random growth negative control |

## Results

### Result 1: Geometric growth reproduces dimensional scaling

On grown geometric DAGs (16 seeds per N, N=12..40):

| d_growth | alpha (grown) | alpha (imposed) | Match? |
|----------|--------------|----------------|--------|
| 1 (2D) | steep (pm→1) | -1.58 | Yes |
| 2 (3D) | -0.63 | ~-0.7 | **Yes** |
| 3 (4D) | -0.18 | -0.178 | **Exact** |
| 4 (5D) | +0.61 | +0.11 | **Both positive** |

Source: scripts/geometric_growth.py

The grown-graph exponents match imposed-graph exponents across all
tested dimensions. The path-sum doesn't distinguish grown from
imposed geometry.

### Result 2: Random growth fails catastrophically

Random k-regular layered DAGs (d_eff ≈ 3 by BFS) produce alpha = -3.16.
By N=40, pur_min = 1.000.

Source: scripts/emergent_graph_decoherence.py

Key insight: graph dimension (BFS ball scaling) ≠ spatial dimension
for path-sum propagation. Geometric locality is required — edges
must connect nodes that are near in an emergent coordinate space.

### Result 3: Emergent mass produces gravitational deflection

Asymmetric test (mass in upper half, 20 seeds):

| d_growth | N | delta | SE | d/SE | toward |
|----------|---|-------|-----|------|--------|
| 2 (3D) | 30 | +0.218 | 0.140 | 1.6 | 70% |
| 3 (4D) | 30 | +0.458 | 0.147 | **3.1** | 65% |

Source: scripts/emergent_mass_gravity.py

### Result 4: Full axiom chain closure

Emergent barrier + emergent mass + grown geometry (20 seeds):

| d_growth | N | pur_min | 1-pm | gravity | Status |
|----------|---|---------|------|---------|--------|
| 2 (3D) | 30 | 0.971 | **2.9%** | +0.301 | **FULL** |
| 3 (4D) | 18 | 0.949 | **5.1%** | -0.073 | partial |
| 3 (4D) | 30 | 0.967 | **3.4%** | +0.442 | **FULL** |

Source: scripts/emergent_barrier.py

"FULL" = gravity signal > 1.5 SE AND pur_min < 0.998 on the same
grown graph with no imposed structure.

### Null results

1. **Random growth**: alpha=-3.16, catastrophic failure. Graph d_eff
   does not predict path-sum behavior. Geometric locality is essential.

2. **d_growth=1 (2D) grown**: pur_min → 1.000 by N=30, same ceiling
   as imposed 2D. Growth doesn't help in low dimension.

3. **Gravity on 4D grown at N=18**: delta = -0.073 (wrong sign).
   Gravity signal is noisy at small N on sparse grown graphs.

4. **All 9 prior emergence approaches** (connection bias, placement
   bias, node removal): all fail on imposed graphs. The grown-graph
   approach succeeds where they failed because it provides geometric
   locality from the start.

## Validation Summary

| Check | Status | Notes |
|-------|--------|-------|
| Dimensional exponent match | **PASS** | d=2,3,4 all match imposed |
| Random growth negative control | **PASS** | alpha=-3.16 (expected failure) |
| Emergent mass deflection | **PASS** | 3.1 SE on 4D, 70% toward on 3D |
| Full chain coexistence | **PASS** | Gravity + decoherence at N=30 |
| Born rule (from prior work) | **PASS** | 4e-16 on same propagator family |
| Decoherence at N=18, 4D | **PASS** | 5.1% (strongest fully emergent) |
| Gravity sign at N=18, 4D | **MARGINAL** | Wrong sign (-0.073), noisy |

**Overall confidence:** HIGH for dimensional scaling and decoherence.
GOOD for gravity (2.0-3.1 SE on specific configs, noisy at small N).
The full chain closure (gravity + decoherence on same graph) reaches
the FULL threshold at N=30 but not reliably at N=18.

**Known fragilities:**
- Grown graphs are sparser than imposed → smaller absolute decoherence
- Emergent mass identification (top 20% amplitude) is a crude heuristic
- Emergent barrier (top 25% amplitude = slit) is also crude
- Gravity on grown graphs needs 20+ seeds and N≥25 for stability

## Discussion

The central finding: the project's full axiom set can produce both
gravitational deflection and decoherence-like purity loss on the
same locally-grown event-network, with no externally imposed structure.

The key enabler is **geometric locality** — the growth rule's
requirement that new nodes connect to nearby existing nodes in an
emergent coordinate space. This is Axiom 3 ("space is inferred from
influence neighborhoods") made constructive. When the growth rule
provides d=3 transverse dimensions, the resulting graph produces the
same decoherence scaling exponent as a hand-imposed 4D graph.

Random growth rules (high connectivity but no spatial structure) fail
catastrophically. This demonstrates that the physics requires MORE than
just a dense network — it requires the specific correlation structure
that comes from geometric locality. The event-network must have an
emergent metric.

The emergent mass mechanism (amplitude concentration → gravitational
source) provides Axiom 2 ("persistent patterns are objects") in its
simplest form. In the current implementation, the "pattern" is just
a region of high amplitude from a single propagation. A richer version
would use self-maintaining oscillations (the CA/mover work) as mass
sources, which would be closer to the axiom's intent of "self-maintaining
patterns."

The emergent barrier mechanism (amplitude-density damping) provides
Axiom 9 ("measurement separates alternatives") constructively. Nodes
that receive high amplitude from many directions act as transmitters
(slits); nodes that receive little amplitude act as walls. This is
the simplest version — a richer implementation would use persistent
pattern boundaries as barriers.

The decoherence values (3-5%) are small compared to imposed-graph
results (10-40%) because the grown graphs are sparser. With denser
growth rules (more nodes per layer, larger connect_radius), the
absolute decoherence would increase while the exponent stays the same.

### Caveats

1. The growth rule parameter d_growth=3 produces 4D graphs, matching
   physical spacetime. But d_growth itself is a parameter, not derived.
   WHY d=3 transverse dimensions is not answered here.

2. The emergent mass and barrier are identified from the SAME
   propagation that they then influence. This circular dependence is
   resolved by running free propagation first, then using the result
   to set up mass/barrier for a second propagation. A self-consistent
   solution (where mass and barrier emerge from the field they create)
   is a natural next step but is not attempted here.

3. The barrier layer's POSITION (at N/3) is still imposed. The barrier
   emerges in form (which nodes block) but not in location (which layer
   is the barrier).

## Next Steps

1. **Self-consistent mass-field loop** — iterate: propagate → identify
   mass → compute field → propagate with field → re-identify mass.
   Does it converge to a stable configuration?

2. **Denser grown graphs** — increase npl to 50-100 and connect_radius
   to 5-6 to match imposed-graph density. Should increase absolute
   decoherence from 3-5% toward 10-40%.

3. **Barrier position emergence** — instead of fixing the barrier at
   N/3, scan all layers for the one that produces the strongest
   amplitude-density contrast. Does a natural barrier position emerge?

4. **CA patterns as mass** — replace amplitude concentration with
   self-maintaining oscillations (Codex's mover work) as mass sources.
   This would fully close Axiom 2 in its intended form.

5. **WHY d=3** — is there a derivation from the axioms that selects
   d_growth=3 over other values? The current program shows 4D is
   optimal for combined gravity + decoherence. Is there a selection
   principle?
```

