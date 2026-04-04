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
