# Gate B: Evolving Network Dynamics — Current Status

**Date:** 2026-04-04
**Status:** Partial — mass scaling transfers, gravity sign needs structured connectivity

## The question

Can we grow (rather than impose) geometry that gives Newtonian gravity?

## What was tested

Primary frozen replay for the current connectivity-vs-noise read:

- [scripts/gate_b_connectivity_tolerance.py](/Users/jonreilly/Projects/Physics/scripts/gate_b_connectivity_tolerance.py)
- [logs/2026-04-04-gate-b-connectivity-tolerance.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-04-gate-b-connectivity-tolerance.txt)
- [docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md](/Users/jonreilly/Projects/Physics/docs/GATE_B_CONNECTIVITY_TOLERANCE_NOTE.md)

Structured-connectivity follow-up:

- [scripts/evolving_network_prototype_v4.py](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v4.py)
- [logs/2026-04-04-evolving-network-prototype-v4.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v4.txt)
- [docs/EVOLVING_NETWORK_PROTOTYPE_V4_NOTE.md](/Users/jonreilly/Projects/Physics/docs/EVOLVING_NETWORK_PROTOTYPE_V4_NOTE.md)

Latest bounded follow-up:

- [scripts/evolving_network_prototype_v5.py](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v5.py)
- [logs/2026-04-04-evolving-network-prototype-v5.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v5.txt)
- [docs/EVOLVING_NETWORK_PROTOTYPE_V5_NOTE.md](/Users/jonreilly/Projects/Physics/docs/EVOLVING_NETWORK_PROTOTYPE_V5_NOTE.md)

1. **Noisy NN lattice** (positions jittered, fixed connectivity):
   100% TOWARD at all jitter levels 0.0-0.5, F∝M=1.00, Born 0.
   Gravity degrades gracefully (~40% weaker at jitter=0.5).

2. **Templated growth** (copy prev layer + jitter, NN offsets):
   50-67% TOWARD, F∝M=1.00. Position drift accumulates across layers.

3. **K-NN grown** (relaxed positions, 9-nearest connectivity):
   25% TOWARD, F∝M=1.00. Asymmetric connectivity breaks coherence.

4. **Grid-snapped grown** (relaxed positions, snapped NN connectivity):
   50% TOWARD, F∝M=1.00. Inconsistent grid assignment.

## Key insight

**Position noise is tolerated. Connectivity structure is critical.**

The valley-linear action gives TOWARD gravity on any graph with:
- Forward-only edges (layer l → layer l+1)
- NN-like connectivity (fixed offsets, not distance-based neighbors)
- Approximately uniform node spacing (within 0.5h tolerance)

The growth rule must produce **structured connectivity**, not just
regular spacing. K-nearest-neighbor connectivity on relaxed positions
does NOT suffice — the resulting edge structure is too asymmetric.

## What F∝M tells us

F∝M = 1.00 transfers to ALL tested architectures, including K-NN
grown DAGs with only 25% TOWARD. The mass scaling is more robust
than the gravity sign — it depends on the action formula (linear in f)
but not on the connectivity structure.

## Path forward

The remaining gap is a growth rule that produces structured connectivity.
Options:

1. **Crystal-like templating with restoring force**: copy previous layer,
   add jitter, but pull toward grid positions. Prevents cumulative drift.

2. **Edge structure rule**: instead of computing NN from positions, define
   edges by a LOCAL rule (each node connects to the node "opposite" it
   in the previous layer's neighborhood). This is connectivity-first growth.

3. **Accept the lattice**: the lattice IS the continuum limit. The
   dynamics question becomes "what produces regular structure at large
   scale?" rather than "can we grow a specific graph that works?"

## Honest status for reviewers

The model can produce Newtonian gravity (F∝M=1.0, ~1/b) on grown
geometry IF the connectivity is approximately grid-structured. The
tolerance for position noise is high (0.5h). The remaining challenge
is producing the grid-like connectivity from a local rule.

This is a genuine partial result, not a failure: the geometry
tolerance is quantified, the mass scaling transfers universally,
and the connectivity requirement is identified.

The newest v4 crystal-like growth rule is the first explicit
structured-connectivity prototype guided by that lesson. It remains mixed and
does not close Gate B, but it is a cleaner next-step prototype than the older
pure KNN or pruning-only lanes.

The newer v5 cross-growth follow-up is the current best bounded Gate B row:

- it improves the TOWARD rate over the matched KNN control on the same grown
  positions
- it also improves the local `F~M` slope over that control
- it does **not** cleanly beat the KNN control on mean delta

So the current safe Gate B read is:

- connectivity-first growth is better than generic recomputed KNN
- the advantage is now visible in a frozen artifact chain
- but the result is still mixed enough that Gate B remains open

## Update: frozen h=0.5 structured-growth replay

The newer h=0.5 structured-growth lane is now frozen on disk:

- [scripts/evolving_network_prototype_v6.py](/Users/jonreilly/Projects/Physics/scripts/evolving_network_prototype_v6.py)
- [logs/2026-04-04-evolving-network-prototype-v6.txt](/Users/jonreilly/Projects/Physics/logs/2026-04-04-evolving-network-prototype-v6.txt)
- [docs/EVOLVING_NETWORK_PROTOTYPE_V6_NOTE.md](/Users/jonreilly/Projects/Physics/docs/EVOLVING_NETWORK_PROTOTYPE_V6_NOTE.md)

It does **not** reproduce the branch headline of `100%` TOWARD across the full
tested matrix. The frozen rows are:

- `drift=0.3, restore=0.5`: `33/36` TOWARD, `mean_delta=+0.000021`, `F~M=1.00`
- `drift=0.2, restore=0.7`: `24/36` TOWARD, `mean_delta=+0.000010`, `F~M=1.00`
- `drift=0.1, restore=0.9`: `24/36` TOWARD, `mean_delta=+0.000008`, `F~M=0.99`
- `drift=0.0, restore=1.0`: `24/36` TOWARD, `mean_delta=+0.000007`, `F~M=0.99`

So the safe Gate B read is now:

- the h=0.5 structured-growth lane is genuinely TOWARD and near-linear
- the best tested row is stronger than the older bounded prototypes
- the full tested matrix is still mixed enough that Gate B remains open

## Diagnosis: v6 mixed result is a near-field effect (2026-04-04)

The v6 frozen replay uses near-slit mass positions (y=1.0, 1.5) and
varied field strengths (0.75-1.25x). These are near-field parameters
where even the FIXED lattice gives noisy gravity.

Controlled comparison at z≥2 with standard strength:
| Size | drift=0.3 | drift=0.2 | exact grid |
|------|-----------|-----------|------------|
| HALF=5 (v6) | 88% | 100% | 100% |
| HALF=12 | 96% | 100% | 100% |

The growth rule itself is not the bottleneck — the near-field
parameter choice in the v6 replay is what creates the mixed signal.

**Honest status:** Gate B is strong in the far field (z≥2) but
noisy in the near field (z≤1.5). This is a lattice-size effect,
not a growth-rule failure. The v6 mixed result is an honest
characterization of the near-field regime.

## Frozen far-field harness (2026-04-05)

Dedicated far-field artifact chain:

- [`scripts/gate_b_farfield_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_farfield_harness.py)
- [`logs/2026-04-05-gate-b-farfield-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-farfield-harness.txt)
- [`docs/GATE_B_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_FARFIELD_NOTE.md)

Results at h=0.5, 12 seeds × z=[3,4,5] = 36 tests per row:

| drift | restore | TOWARD | F∝M |
|-------|---------|--------|-----|
| 0.3 | 0.5 | 36/36 (100%) | 1.00 |
| 0.2 | 0.7 | 36/36 (100%) | 1.00 |
| 0.1 | 0.9 | 36/36 (100%) | 1.00 |
| 0.0 | 1.0 | 36/36 (100%) | 1.00 |

**Gate B far-field: CLOSED.** Grown geometry gives 100% TOWARD with
F∝M=1.00 at all drift/restore levels in the far field (z≥3).

The near-field (z≤2) remains mixed on both grown and fixed lattices.
This is a beam-optics effect, not a growth-rule or physics failure.

## Frozen v6 near-field comparator (2026-04-05)

Dedicated exact-vs-grown control:

- [`scripts/gate_b_v6_nearfield_comparator.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_v6_nearfield_comparator.py)
- [`logs/2026-04-05-gate-b-v6-nearfield-comparator.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-v6-nearfield-comparator.txt)
- [`docs/GATE_B_V6_NEARFIELD_COMPARATOR_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_V6_NEARFIELD_COMPARATOR_NOTE.md)

Frozen bucket summary for the retained `drift = 0.3`, `restore = 0.5` row:

| `y_mass` | exact control | grown row |
| --- | --- | --- |
| `1.0` | `0/3` `TOWARD`, mean `-0.000019` | `9/12` `TOWARD`, mean `+0.000006` |
| `1.5` | `3/3` `TOWARD`, mean `+0.000011` | `12/12` `TOWARD`, mean `+0.000023` |
| `2.0` | `3/3` `TOWARD`, mean `+0.000030` | `12/12` `TOWARD`, mean `+0.000035` |

This sharpens the near-field diagnosis:

- the mixed v6 signal is confined to the closest near-field bucket
- the ordered-lattice control is already worse on that bucket
- only one of the four retained grown seeds flips all three closest-bucket
  strengths

So the safe read is stronger than “near-field mixed” alone:

- the v6 misses are not evidence that the structured-growth rule collapses
  relative to the exact grid
- the mixed bucket is best read as a bounded near-field optics issue

## Generated-geometry companion package (2026-04-05)

The far-field Gate B lane now has dedicated companion replays for the retained
moderate-drift row:

- [`scripts/gate_b_grown_distance_law.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_distance_law.py)
- [`logs/2026-04-05-gate-b-grown-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-distance-law.txt)
- [`docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_DISTANCE_LAW_NOTE.md)
- [`scripts/gate_b_grown_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_grown_joint_package.py)
- [`logs/2026-04-05-gate-b-grown-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-grown-joint-package.txt)
- [`docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_GROWN_JOINT_PACKAGE_NOTE.md)

These companions sharpen the safe Gate B read:

- retained far-field sign / `F~M` closure remains the main result
- the retained moderate-drift grown row also keeps a positive declining
  distance-law fit close to the exact-grid row on the tested `z = 3..7` window
- the same retained grown row keeps Born at machine precision and leaves the
  joint `d_TV` / `MI` / decoherence read nearly unchanged from the exact grid

So the honest status is now:

- far-field generated geometry is a real bounded positive with companion
  support for distance and joint non-gravity observables
- the mixed near-field region is now localized to the closest tested bucket,
  where the exact control is already worse than the retained grown row
- full-family Gate B closure remains open

## Non-label connectivity candidate (2026-04-05)

The degree-balanced non-label forward candidate is now frozen too:

- [`scripts/gate_b_nonlabel_connectivity_v3.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v3.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v3.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v3.txt)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V3_NOTE.md)

Its bounded read is:

- exact grid: `12/12` TOWARD, `F~M = 1.00`
- no-restore label-NN control: `12/12` TOWARD, `F~M = 1.00`
- no-restore degree-balanced matching candidate: `10/12` TOWARD, `F~M = 0.75`

So the non-label candidate preserves most far-field sign rows, but it does
not retain the clean `F~M = 1.00` class on this family.

That makes it a bounded negative for the current non-label forward-connectivity
idea, not a replacement for the label-based far-field rule.

## One-step h=0.25 scaling companion (2026-04-05)

The same moderate-drift generated-geometry family now also has bounded
`h = 0.25` refinement companions:

- [`scripts/gate_b_h025_farfield.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_h025_farfield.py)
- [`logs/2026-04-05-gate-b-h025-farfield.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-h025-farfield.txt)
- [`docs/GATE_B_H025_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_H025_FARFIELD_NOTE.md)
- [`scripts/gate_b_h025_distance_law.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_h025_distance_law.py)
- [`logs/2026-04-05-gate-b-h025-distance-law.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-h025-distance-law.txt)
- [`docs/GATE_B_H025_DISTANCE_LAW_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_H025_DISTANCE_LAW_NOTE.md)
- [`scripts/gate_b_h025_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_h025_joint_package.py)
- [`logs/2026-04-05-gate-b-h025-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-h025-joint-package.txt)
- [`docs/GATE_B_H025_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_H025_JOINT_PACKAGE_NOTE.md)

Their bounded read is:

- far-field sign / `F~M` stay clean on the compact `h = 0.25` family:
  exact grid `12/12` TOWARD, grown `drift = 0.2` `12/12` TOWARD, both with
  `F~M = 1.00`
- the compact distance-law companion stays positive and declining:
  exact grid `b^(-0.42)`, grown `b^(-0.54)`
- the compact joint-package companion stays in the same qualitative Born /
  interference / decoherence regime as the exact grid

So the safe Gate B read is now:

- the retained moderate-drift generated-geometry lane is no longer just a
  coarse `h = 0.5` positive
- it now has one bounded `h = 0.25` refinement companion on the same family
- near-field and broader generated-geometry closure remain open

## Weak-connectivity boundary (2026-04-05)

The no-restore weak-connectivity lane is now frozen separately:

- [`scripts/gate_b_weak_connectivity_harness.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_weak_connectivity_harness.py)
- [`logs/2026-04-05-gate-b-weak-connectivity-harness.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-weak-connectivity-harness.txt)
- [`docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_WEAK_CONNECTIVITY_NOTE.md)

Its bounded read is:

- no-restore label-NN control still gives `12/12` TOWARD and `F~M = 1.00`
- the weaker no-restore KNN+floor candidate collapses to `0/12` TOWARD and
  `F~M = 0.00`

So the restoring force is not the whole story. The connectivity rule is the
critical piece, and the weaker position-based candidate does **not** carry the
far-field package on this retained family.

## Non-label forward-cone candidate (2026-04-05)

The no-restore grown-geometry lane now has a second bounded non-label
candidate:

- [`scripts/gate_b_nonlabel_connectivity_v2.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_nonlabel_connectivity_v2.py)
- [`logs/2026-04-05-gate-b-nonlabel-connectivity-v2.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-nonlabel-connectivity-v2.txt)
- [`docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NONLABEL_CONNECTIVITY_V2_NOTE.md)

Its bounded read is:

- no-restore label-NN control still gives `12/12` TOWARD and `F~M = 1.00`
- the no-restore forward-cone candidate gets only `8/12` TOWARD and `F~M = 0.50`

So the forward-cone rule is a bounded negative: it preserves some far-field
sign rows, but it does **not** keep the Newtonian mass-scaling class cleanly.

## No-restore hierarchy (2026-04-05)

The no-restore lane is now bounded more sharply too:

- [`scripts/gate_b_no_restore_farfield.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_no_restore_farfield.py)
- [`logs/2026-04-05-gate-b-no-restore-farfield.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-no-restore-farfield.txt)
- [`docs/GATE_B_NO_RESTORE_FARFIELD_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NO_RESTORE_FARFIELD_NOTE.md)
- [`scripts/gate_b_no_restore_joint_package.py`](/Users/jonreilly/Projects/Physics/scripts/gate_b_no_restore_joint_package.py)
- [`logs/2026-04-05-gate-b-no-restore-joint-package.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-gate-b-no-restore-joint-package.txt)
- [`docs/GATE_B_NO_RESTORE_JOINT_PACKAGE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/GATE_B_NO_RESTORE_JOINT_PACKAGE_NOTE.md)

Their bounded read is:

- far-field gravity is surprisingly robust without restore on the label-based
  family:
  - `drift = 0.0` through `0.3`: `6/6` TOWARD, `F~M = 1.00`
  - `drift = 0.5`: `5/6` TOWARD, `F~M = 1.00`
- the non-gravity joint package is not comparably robust:
  - `drift = 0.0` still matches the exact-grid row
  - once drift is turned on, `d_TV`, `MI`, and decoherence become sharply
    drift-sensitive on the frozen one-seed replay

So the clean hierarchy is now:

- restore is **not** required for the basic far-field sign / mass-law slice on
  the label-connectivity family
- restore still matters if the goal is to preserve the broader lattice-like
  interference / decoherence package
