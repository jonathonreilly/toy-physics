# Code Review — Last Week Surface (2026-04-04 to 2026-04-11)

This note records the validated high-risk findings from the last-week review.
It is not a full changelog. It is a guardrail list for results that should not
be promoted or reinterpreted without fixes.

## Validated High-Severity Findings

1. Several periodic 2D staggered runners misweight wraparound neighbors.
   - The pattern is: periodic adjacency via modulo indexing, followed by
     hopping weights computed from raw coordinate differences instead of
     minimum-image distances.
   - Verified examples include:
     - `frontier_born_rule_alpha.py`
     - `frontier_self_consistency_test.py`
     - `frontier_eigenvalue_stats_and_anderson_phase.py`
   - This contaminates boundary-crossing couplings in those periodic 2D
     surfaces.

## Validated Medium-Severity Findings

## Resolved Since Review

1. `frontier_branch_entanglement_robustness.py` no longer presents `0/25 GHZ`
   as if it were an empirical exclusion result on current `main`.
   - The canonical runner, robustness note, and three-body note now say the
     same thing explicitly: for the fixed two-branch ansatz on this surface,
     `tau_3 = 0` is theorem-implied by the overlap algebra.
   - The live claim is therefore bounded W-type branch-mediated entanglement
     on an externally imposed two-branch protocol, not an empirical GHZ/no-GHZ
     discovery and not a full BMV witness.

2. `frontier_wilson_newton_law.py` is no longer part of the live Newton-law
   evidence chain on current `main`.
   - The historical periodic frontier runner is absent from the live
     `/Users/jonreilly/Projects/Physics/scripts/` surface and is now carried
     only as a historical caution in the Wilson notes/audits.
   - The current Wilson weak-field package instead hangs off the open-surface
     lane in `WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`,
     `WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md`, and
     `WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`, which already state the
     honest bounded-companion boundary.

3. `frontier_two_field_retarded_probe.py` no longer scores R9 unconditionally.
   - On current `main`, R9 is now explicitly labeled as a diagnostic-only row
     for force-gap / shell / spectral characterization.
   - The runner score now covers only scored rows `R1`-`R8`, and the companion
     note labels R9 as unscored.

4. `frontier_two_field_wave.py` no longer reuses an already evolved field
   state in the family-robustness battery.
   - On current `main`, `W6` restarts each family from fresh `Φ=0`,
     `dΦ/dt=0` data, so the family check is independent of the first branch's
     evolved field history.
   - That rerun lowers the honest hard scores to `4/5`, `5/5`, `4/5`, so the
     wave note now sits as a bounded rerun-corrected result rather than a
     retained `5/5` closure.

5. `frontier_self_consistency_test.py` no longer relies on non-moment-matched
   random controls.
   - On current `main`, the earlier `abs(normal(mean, std))` controls have been
     replaced by the structured-null rerun in
     `SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md`.
   - The live runner now uses a torus-shifted static field and a phase-scrambled
     same-spectrum null, and the current rerun reproduces the note's corrected
     fixed-surface output.

6. `frontier_staggered_dag.py` no longer carries a live claim of genuinely
   directed-Hamiltonian DAG compatibility.
   - On current `main`, the runner and note now state the truth: the layered
     acyclic template is still useful as a bounded geometry control, but the
     Hamiltonian symmetrizes the adjacency, so the old retained causal-DAG
     compatibility framing has been withdrawn.

7. `frontier_two_body_mutual_attraction.py` is no longer part of the live
   mutual-attraction evidence chain on current `main`.
   - The old one-wavefunction/two-lobe staggered runner is now carried only as
     a historical exploratory pointer, and
     `TWO_BODY_MUTUAL_ATTRACTION_NOTE_2026-04-11.md` explicitly says it is not
     a genuine two-particle test.
   - The live two-body package now hangs off the bounded open-Wilson successor
     lane in `WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`, which is itself
     explicitly framed as a genuine two-orbital channel but not full Newton
     closure.

8. `frontier_entanglement_area_law.py` is no longer part of the live
   boundary-law evidence chain on current `main`.
   - The old runner is now explicitly marked as a historical
     boundary-transfer entropy diagnostic rather than a true subsystem
     entanglement measurement.
   - The live bounded boundary-law package instead hangs off
     `frontier_holographic_probe.py` and its audited addendum, which are
     already framed as a many-body-style Dirac-sea boundary-law result rather
     than a full holography claim.

9. `frontier_bmv_entanglement.py` no longer overstates itself as a genuine
   BMV / gravity-quantumness witness on current `main`.
   - The runner and companion note now present it explicitly as a
     branch-mediated entanglement protocol with an externally imposed
     geometry/source branch.
   - The live bounded package keeps the positive `delta_S > 0` result while
     reserving full BMV / mediator-null claims for future redesigned
     witnesses.

## Verified False Positive From Agent Review

One agent claimed `frontier_wilson_two_body_open.py` still computed center of
mass on a torus. That finding was checked and rejected. The current
`center_of_mass_x()` in the open Wilson runner uses a linear mean on the open
surface.

## Immediate Hardening Implications

- Treat the periodic Wilson Newton runner as historical only.
- Treat the original two-body staggered runner as invalid for mutual-attraction
  claims.
- Treat the branch-entanglement GHZ row as a theorem-check sanity line, not
  as an empirical exclusion result.
- Re-audit all periodic 2D staggered results touched by the wraparound-weight
  bug before upgrading them.
