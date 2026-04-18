# Periodic 2D Wraparound Fix Note (2026-04-11)

## Scope

This note records the validated periodic-lattice minimum-image bug and the
current-main reruns after fixing it.

Bug class:

- periodic adjacency was built with modulo indexing
- hopping weights were then computed from raw coordinate differences instead of
  minimum-image distances
- a wraparound nearest neighbor on a `side x side` torus could therefore be
  treated as having distance `side - 1` instead of `1`

Current-main fix:

- shared helper: [`scripts/periodic_geometry.py`](../scripts/periodic_geometry.py)
- periodic weighted runners now use minimum-image separations consistent with
  the torus adjacency actually being evolved

## Corrected live surfaces on `main`

Canonical corrected periodic surfaces now include:

- [`scripts/frontier_self_consistency_test.py`](../scripts/frontier_self_consistency_test.py)
- [`scripts/frontier_eigenvalue_stats_and_anderson_phase.py`](../scripts/frontier_eigenvalue_stats_and_anderson_phase.py)
- [`scripts/frontier_born_rule_alpha.py`](../scripts/frontier_born_rule_alpha.py)
- [`scripts/frontier_holographic_probe.py`](../scripts/frontier_holographic_probe.py)
- [`scripts/frontier_boundary_law_robustness.py`](../scripts/frontier_boundary_law_robustness.py)
- [`scripts/frontier_staggered_geometry_superposition_retained.py`](../scripts/frontier_staggered_geometry_superposition_retained.py)
- [`scripts/frontier_bmv_entanglement.py`](../scripts/frontier_bmv_entanglement.py)
- [`scripts/frontier_branch_entanglement_robustness.py`](../scripts/frontier_branch_entanglement_robustness.py)

Historical periodic surface also rerun under the fix:

- [`scripts/frontier_bmv_threebody.py`](../scripts/frontier_bmv_threebody.py)

That standalone three-body heuristic runner changes materially under the fix,
but it remains non-canonical and does not override the robustness harness.

## Corrected rerun status

### Diagnostic trio

#### 1. `frontier_self_consistency_test.py`

Corrected interpretation on the fixed `10x10` torus:

- deterministic split between self-consistent and static-from-initial survives
- structured field still cleanly separates from the corrected structured-null
  controls
- the lane remains a fixed-surface torus comparison, not a continuum closure

Use the corrected structured-null surface:

- [`docs/SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md`](SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md)

#### 2. `frontier_eigenvalue_stats_and_anderson_phase.py`

Corrected interpretation on the fixed periodic surfaces:

- no chaos transition is rescued by the fix
- the finite Anderson-vs-disorder window remains, but as a torus phase-map
  result only
- the corrected maximum spacing statistic still stays below the Poisson/GOE
  midpoint

#### 3. `frontier_born_rule_alpha.py`

Corrected interpretation on the fixed `10x10` torus:

- the minimum-image fix does not rescue the Born-rule lane
- `alpha = 2.0` remains non-unique on the corrected surface
- the lane stays a corrected negative / boundary-of-validity result

### Corrected bounded companion package

#### 4. Boundary-law probes

Corrected reruns now live in:

- [`docs/HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md`](HOLOGRAPHIC_PROBE_NOTE_2026-04-11.md)
- [`docs/BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md`](BOUNDARY_LAW_ROBUSTNESS_NOTE_2026-04-11.md)

What survives after the fix:

- boundary scaling is still preferred over volume scaling on the Dirac-sea probe
- the audited robustness sweep still gives `100/100` BFS-ball fits above
  `R^2 = 0.95`
- the stronger live read is a corrected bounded boundary-law companion on the
  periodic staggered surface, not a broader holography claim

#### 5. Fixed-adjacency branch-superposition lane

Corrected rerun now lives in:

- [`docs/STAGGERED_GEOMETRY_SUPERPOSITION_NOTE_2026-04-11.md`](STAGGERED_GEOMETRY_SUPERPOSITION_NOTE_2026-04-11.md)

What survives after the fix:

- the 1D control remains weak/null
- the 2D fixed-adjacency field-branch effect remains bounded positive at the
  audited operating point
- this is still a field-branch result on fixed adjacency, not topology
  superposition

#### 6. Branch-mediated entanglement package

Corrected reruns now live in:

- [`docs/BMV_ENTANGLEMENT_NOTE_2026-04-11.md`](BMV_ENTANGLEMENT_NOTE_2026-04-11.md)
- [`docs/BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md`](BRANCH_ENTANGLEMENT_ROBUSTNESS_NOTE_2026-04-11.md)
- [`docs/BMV_THREEBODY_NOTE_2026-04-11.md`](BMV_THREEBODY_NOTE_2026-04-11.md)

What survives after the fix:

- the 2-body externally imposed two-branch witness still has `delta_S > 0`
- the canonical robustness harness still gives W-type tripartite structure and
  `tau_3 = 0`
- the old standalone three-body heuristic runner is historical only and should
  not be used as the canonical classifier

## What remains limited after the fix

These issues are not solved by the minimum-image correction itself:

- periodic torus results remain periodic torus results
- the boundary-law package is still a bounded many-body-style companion, not a
  holography proof
- the branch-entanglement package is still an externally imposed two-branch
  protocol, not a full BMV / mediator-null witness
- the Born-rule alpha sweep still does not become a measurement-theory result

## Current mainline recommendation

- Treat this note as the canonical bug-fix entrypoint for the live periodic
  weighted package on current `main`.
- Use the corrected companion notes listed above for exact rerun numbers.
- Do not cite pre-fix periodic numbers from older notes, review comments, or
  session summaries.
- If an older periodic frontier script is reopened later, audit it against
  [`scripts/periodic_geometry.py`](../scripts/periodic_geometry.py) before
  trusting any weighted-torus claim.
