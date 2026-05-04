# Teleportation Remaining-Open-Item Attack Note

**Date:** 2026-04-26
**Status:** planning / explicit remaining obligations
**Runner:** `scripts/frontier_teleportation_remaining_open_item_attack.py`

## Scope

This artifact attacks the remaining open items after the retention-theorem pass:

- derive or justify the variational selector completion;
- prove the signed sparse branch beyond finite sides;
- turn controller and detector envelopes into implementation evidence.

The scope remains ordinary quantum state teleportation only. No matter, mass,
charge, energy, object, or faster-than-light transport is claimed.

## Selector Completion Minimality

The selector completion is now clause-minimal on the audited invariants.

```text
bare_equivalent_selectors = 64
completion_clauses = 3
without_orientation = 2
without_action = 8
without_no_dwell = 4
final_selector_count = 1
all_clauses_necessary = True
```

The three clauses are still:

```text
1. retarded causal-positive orientation;
2. minimal generator/action norm over equivalent Bell-record writers;
3. no-dwell cubic-covariant nearest-neighbor carrier.
```

Dropping any one clause leaves a degeneracy. This supports retaining the
completion as a minimal lane principle, but it still does not derive the
completion from the original sole axiom.

## Side-12 Induction Target

The signed branch certificate remains:

```text
rows = 5
max_side = 12
gap_floor = 0.390/L^2
min_gap_margin = 2.750e-05
scaled_gap_min = 0.390440
scaled_gap_max = 0.463496
scaled_gap_monotone = True
bell_floor = 0.999702
Bell_monotone = True
```

The direct side-14 sparse eigensolve was attempted and exceeded the local turn
budget. It is not counted as evidence.

The remaining induction obligation is now:

```text
prove gap(L) * L^2 >= 0.390
and Bell*(L) >= 0.999702
for every even L >= 4 on the signed G=-1000 branch.
```

## Controller Requirements

The pulse/controller target specification is:

```text
record_length = 8
d_min = 5
correctable = 2
target_word_failure = 1.000e-06
slot_threshold = 2.622e-03
leakage_budget = 1.000e-05
crosstalk_budget = 2.000e-05
area_budget = 0.050937 rad = 2.918 deg
implemented_area_bound = 0.023000 rad
margin = 2.215
```

This is a target specification. It is not a fabricated controller or measured
noise spectrum.

## Material Requirements

The detector/material target specification is:

```text
domain_side = 5
spins_per_slot = 125
slots = 8
local_bonds = 2400
J_over_T >= 1.000
defect <= 2.000e-03
word_failure_bound = 7.498e-131
log10_overlap_bound = -655.141
arrhenius_wall = 1.929e-22
finite_local_envelope = True
```

This is a local Ising-domain material envelope. It is not a named material stack
or fabricated detector.

## Retained Status

The remaining work is now tightly scoped:

- either retain the three-clause selector completion, derive it from a stronger
  framework theorem, or do not promote the lane;
- prove the all-even-side signed-branch induction target;
- map the controller and material target specifications to an actual
  fabrication/noise/material model.

The lane remains planning / conditional theory, not unconditional nature-grade
closure.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [teleportation_native_record_apparatus_note](TELEPORTATION_NATIVE_RECORD_APPARATUS_NOTE.md)
