# PR #484 K-Z External Lift Review - 2026-05-03

**Status:** active science gate recorded in
[`docs/repo/ACTIVE_REVIEW_QUEUE.md`](../../../repo/ACTIVE_REVIEW_QUEUE.md).

**Disposition:** reject PR #484 as a bounded theorem, retained-status update,
or parent-chain promotion. Preserve the goal as an open external-lift
candidate.

## Reviewed Scope

- PR #484:
  `docs/GAUGE_SCALAR_BRIDGE_KZ_EXTERNAL_LIFT_THEOREM_NOTE_2026-05-03.md`
- PR #484:
  `scripts/frontier_gauge_scalar_bridge_kz_external_lift.py`
- Parent target:
  [`GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md`](../../../GAUGE_SCALAR_TEMPORAL_COMPLETION_THEOREM_NOTE.md)
- No-go target:
  [`GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md`](../../../GAUGE_SCALAR_TEMPORAL_OBSERVABLE_BRIDGE_NO_GO_THEOREM_NOTE_2026-05-03.md)

## Purpose

The branch's purpose is legitimate: use external lattice-bootstrap / SDP
literature to explore the gauge-scalar temporal bridge no-go's explicit escape
route for an independently selected `beta_eff(6)`, rather than fitting
`<P>`.

That purpose is not yet achieved as a theorem. The durable repo artifact is an
open review gate naming the exact missing evidence and the conditions under
which the route can be reconsidered.

## Review Findings

1. The PR pre-writes audit-grade and parent-promotion language.

   The proposed note uses status language such as `retained_bounded`,
   `retained_no_go`, inherited retained authority, downstream propagation, and
   parent status upgrade before independent audit. Review-loop may prepare
   audit-compatible source surfaces, but it must not grant retained/effective
   status or promote parent dependency chains.

2. The paired runner does not pass in the review environment.

   Running the branch script in the standard environment exits with one
   load-bearing failure:

   ```text
   SUMMARY: THEOREM PASS=3 SUPPORT=1 FAIL=1
   FAIL: install cvxpy (>= 1.6) to run B.
   ```

   CVXPY is an optional SDP dependency in this repo. A theorem whose
   load-bearing bridge is the SDP re-derivation cannot pass review when that
   bridge is unavailable or lacks a checked cached artifact.

3. The external numeric bracket is not primary-source anchored for the target
   regime.

   The branch correctly notes that the Kazakov-Zheng 2022 bracket
   `[0.59, 0.61]` is a benchmark in a different regime, not the SU(3),
   beta=6 bracket. It then chooses `W_lift = 0.05` as a conservative
   load-bearing width while also admitting that explicit SU(3), beta=6 numeric
   tables are not available from the accessible Guo-Li-Yang-Zhu material. That
   is a useful candidate import, but not a theorem-grade imported bound.

4. The parent chain cannot be upgraded by review-loop.

   The gauge-scalar temporal completion parent can only consume this route
   after the external input, runner support, dependency graph, and source
   vocabulary are audited cleanly. Until then, the parent chain should be
   treated as needing re-audit or additional science, not as promoted.

## Salvage Decision

Do not land the proposed theorem note or runner. They are not narrowly
correctable without adding missing science or installing/verifying the optional
SDP stack, and the retained-status vocabulary would still have to be rebuilt
from scratch.

The salvaged artifact is this review packet plus the live queue entry. That
keeps the route discoverable without adding a claim row or status-bearing
surface.

## Success Criteria For A Future Landing

Before this route can be landed as source science, a new or repaired package
needs all of the following:

- a passing runner in the repo's documented SDP environment, or a checked
  cached artifact with exact reproduction instructions;
- an explicit SU(3), beta=6 primary-source bracket, or a repo-owned SDP
  reproduction that derives the bracket at a stated cutoff and solver;
- source vocabulary that starts as `open`, `support`, or a proposed bounded
  theorem without audit verdicts, effective-status writes, or parent promotion;
- markdown-linked load-bearing dependencies that seed the audit graph;
- a parent-chain update that remains conditional or re-audit-gated until the
  independent audit lane ratifies the claim and dependency closure.

This packet is not an audit verdict and does not update any effective status.
