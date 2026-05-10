# Session Summary: Topology Pivot
**Date:** 2026-04-01
**Status:** RETRACTED 2026-04-30 — retracted aggregate session summary; audit failed; this note is archived under `archive_unlanded/session-summary-stale-aggregates-2026-04-30/`. Claims below are NOT supported by current runners or current audit lane. Future readers should consult the live audit ledger and live notes, not this aggregate. See `## Retraction` section.

## Retraction

- Date archived: 2026-04-30
- Archive directory: `archive_unlanded/session-summary-stale-aggregates-2026-04-30/`
- Audit verdict (`verdict_rationale` from [audit_ledger.json](../../docs/audit/data/audit_ledger.json), claim_id `session_summary_2026-04-01_topology`, `audit_status: audited_failed`, `effective_status: retained_no_go`):

> "Issue: The candidate retained-grade architecture result is a session summary aggregating many gravity, decoherence, topology, pruning, and emergence claims without a single retained theorem, runner, frozen assertion surface, or audit-clean dependency chain. Why this blocks: a synthesis note that even flags optimistic standard-error wording and provisional follow-ups cannot itself establish the broad claim that gravity and decoherence work on the same graph family or that emergence lanes are closed. Repair target: split the summary into auditable claim notes, each with its own runner/log and explicit dependencies, then retain only the scoped results that survive audit; leave this file as session history. Claim boundary until fixed: it is safe to use this note as a dated roadmap and index of scripts/logs from the topology-pivot session; it is not safe to cite it as retained evidence for the architecture claims."

This file is a retracted aggregate session summary. Future readers should consult the live audit ledger ([audit_ledger.json](../../docs/audit/data/audit_ledger.json)) and live notes in `docs/`, not this aggregate. Do NOT cite the numerical results, tables, or threshold values in the original content below as live framework claims. The runners referenced in this note have been superseded or are no longer reproducible at the time of audit. If a future investigation revisits this physics, treat it as starting from scratch rather than as continuation of a "closed no-go".

---

This is the topology-pivot session note. Later higher-dimensional results are
tracked separately in
[HIGHER_DIMENSION_STATUS_2026-04-01.md](/Users/jonreilly/Projects/Physics/docs/HIGHER_DIMENSION_STATUS_2026-04-01.md).

## The architecture story

On discrete causal DAGs with path-sum propagation:

1. **Gravity works** via the corrected propagator (1/L^p attenuation,
   directional measure, spent-delay action). This is a pure phase effect.

2. **Decoherence is topology-controlled.** On dense random / graph-local
   lanes, the tested environment architectures converge too much as graphs
   densify. On modular gap-controlled DAGs, the CL bath achieves a retained
   low-purity lane, but the true large-`N` single-vs-double-slit visibility
   gain does not stay high.

3. **Both gravity and decoherence work on the same graph family**
   (gap-controlled modular DAGs). With wider seed counts, the joint window is
   broad within that family: tested modular gaps `0.0..5.0` keep positive
   gravity and a low decoherence floor, and larger imposed gaps generally
   strengthen both effects until connectivity breaks.

## Locked results

### Decoherence on modular DAG (12-seed asymptotic lane, N=12..100)
```
pur_min = 0.93 +/- 0.02 for N >= 25
true visibility gain is weak at N=12 and near-zero / gone by N>=18..25
S_norm stays in 0.2-0.5 range
```

### Joint gravity + decoherence window (24 seeds, modular family only)
```
Tested gaps 0.0..5.0 all keep positive gravity and pur_cl < 0.96
Larger imposed gap => stronger gravity and stronger decoherence
N=40, gap=5.0: gravity +3.47, pur_min 0.889, decoh +0.110
Crosslink probability is subleading across 0.0..0.10
```

Important scope note: the old both-slits-open detector-profile contrast stays
high, but the true single-vs-double-slit visibility gain does not.

### Gravity on modular DAG
```
N=25: delta = +3.20 — positive deflection toward mass
N=40: delta = +2.50 — gravity persists
```

Earlier SE estimates in the repo were somewhat optimistic because the script
used per-`k` samples rather than paired per-seed deltas. The sign and mean
shift look retained; the exact confidence language should be softened until the
patched gravity script lands.

### Uniform-random qualification
The earlier one-point `pur_min = 0.986` ceiling claim at `N=25` was too
strong for the later 24-seed read. What remains retained is not a single
ceiling value, but the broader diagnosis that graph-local architectures on
dense connected families still converge too much and underperform the larger-gap
modular lane.

## What we learned about emergence

Simple local or feedback-style growth rules do **not** produce persistent
channel separation. Nine emergence-style approaches have now been tested in
total. The reasons are now clearer:

- **Probabilistic barriers** (soft locality) are not enough — CLT
  still operates on the amplitude distribution
- **Amplitude feedback** carries source information, not slit
  information — source is y-symmetric so feedback is too
- **Post-barrier slit-conditioned connection feedback** also fails —
  on sufficiently connected graphs the slit asymmetry per node collapses
  toward `0.5`
- **Distinguishability-based placement** can create real gaps, but the first
  tested rules make them too small, too large, or in the wrong place
- **Topological barriers** (no nodes in gap) are needed — this is what the
  imposed modular gap provides
- **Global node pruning** can improve decoherence at intermediate `N`, but the
  ceiling returns by `N=80..100`, and aggressive/adaptive pruning drives the
  graph toward disconnection. It remains a nonlocal post-hoc surrogate rather
  than a local growth law
- **The first hard-gap placement-only diagnostic is not-ready** — the best
  useful-width gap is badly off-center, and stronger placement drives the
  graphs toward near-disconnection / `pur_cl -> 1`

The sharpened question is no longer “which connection bias works?”
It is whether graph dynamics can create or maintain **regions with no nodes at
the right size and location**.

## Open questions (prioritized)

1. **Hard-gap node placement / node removal**
   Connection feedback is now a closed lane. The next live emergence test is a
   rule that changes where nodes appear, disappear, or persist, so that a hard
   gap can form dynamically at the observed good scale instead of overshooting
   into disconnection. Soft pruning on an already connected graph is no longer
   a live asymptotic candidate. The next control law has to regulate both gap
   width and gap center, not just distinguishability-biased placement.

2. **Boundary-condition interpretation**
   If no self-regulating placement/removal rule appears cleanly, the remaining
   serious alternative is that the gap should be treated as part of the
   effective boundary condition of the emergent geometry.

3. **Asymptotic floor vs drift**
   The modular lane still needs more seeds at large `N`, but the pruning lane
   is now much clearer: its intermediate-`N` gains do not survive asymptotically.

4. **Continuum interpretation**
   Channel separation = discrete analogue of spatial locality /
   branch-preserving geometry. Formalize this connection.

5. **3D gravity on modular DAGs**
   The 3D gravity test (three_d_gravity.py) should be adapted
   to modular DAGs to check whether the deflection result
   generalizes to higher dimensions. A stricter fixed-`b` mass-scaling follow-up
   did not yet cleanly confirm a power law, so the earlier `sqrt(M)`-style read
   should remain provisional until a broader sweep reproduces it.

## Files delivered this session

### New scripts
- `scripts/topology_families.py` — three DAG generators (hierarchical, modular, preferential)
- `scripts/topology_pivot_test.py` — four-family comparison
- `scripts/topology_pivot_extended.py` — crosslink sweep
- `scripts/topology_plateau_confirm.py` — N=40 + gap sweep
- `scripts/topology_large_n.py` — N=60 with interference check
- `scripts/hard_gap_emergence_diagnostic.py` — bounded hard-gap placement diagnostic
- `scripts/topology_large_n_smooth.py` — 8-seed smoothed scaling
- `scripts/topology_asymptotics.py` — 12-seed N=100 with power law fit
- `scripts/dynamic_channel_emergence.py` — three local growth rules
- `scripts/amplitude_feedback_growth.py` — quantum-topology coupling
- `scripts/slit_conditioned_growth.py` — post-barrier slit-conditioned connection feedback
- `scripts/gravity_on_modular_dag.py` — gravity test on modular DAGs

### Updated scripts
- `scripts/caldeira_leggett_bath.py` — N=25 in purity sweep

### Documentation
- `archive_unlanded/if-program-unverifiable-closing-2026-04-30/IF_PROGRAM_CLOSING_NOTE.md` — canonical closure
- `docs/DECOHERENCE_FAILURE_ANALYSIS.md` — updated with topology pivot
- `docs/SESSION_SUMMARY_2026-04-01_TOPOLOGY.md` — this file

### Log artifacts
- `logs/2026-04-01-topology-pivot.txt`
- `logs/2026-04-01-topology-scaling-law.txt`
- `logs/2026-04-01-dynamic-emergence.txt`
- `logs/2026-04-01-hard-gap-emergence-diagnostic.txt`
- `logs/2026-04-01-topology-large-n-visibility.txt`
