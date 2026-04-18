# Code Review — Last Week Surface (2026-04-04 to 2026-04-11)

This note records the validated high-risk findings from the last-week review.
It is not a full changelog. It is a guardrail list for results that should not
be promoted or reinterpreted without fixes.

## Validated High-Severity Findings

None on current `main`.

## Validated Medium-Severity Findings

## Resolved Since Review

1. The periodic 2D wraparound-weight bug is no longer a live blocker on current
   `main`.
   - The weighted torus helper pattern is now corrected on the live periodic
     package via `scripts/periodic_geometry.py`.
   - The corrected current-main rerun surface now covers the original
     diagnostic trio plus the live bounded periodic companions:
     `frontier_holographic_probe.py`,
     `frontier_boundary_law_robustness.py`,
     `frontier_staggered_geometry_superposition_retained.py`,
     `frontier_bmv_entanglement.py`, and
     `frontier_branch_entanglement_robustness.py`.
   - `frontier_bmv_threebody.py` also moves numerically under the fix, but it
     remains historical/non-canonical and does not override the robustness
     harness.

2. `frontier_branch_entanglement_robustness.py` no longer presents `0/25 GHZ`
   as if it were an empirical exclusion result on current `main`.
   - The canonical runner, robustness note, and three-body note now say the
     same thing explicitly: for the fixed two-branch ansatz on this surface,
     `tau_3 = 0` is theorem-implied by the overlap algebra.
   - The live claim is therefore bounded W-type branch-mediated entanglement
     on an externally imposed two-branch protocol, not an empirical GHZ/no-GHZ
     discovery and not a full BMV witness.

3. `frontier_wilson_newton_law.py` is no longer part of the live Newton-law
   evidence chain on current `main`.
   - The historical periodic frontier runner is absent from the live
     `/Users/jonreilly/Projects/Physics/scripts/` surface and is now carried
     only as a historical caution in the Wilson notes/audits.
   - The current Wilson weak-field package instead hangs off the open-surface
     lane in `WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`,
     `WILSON_MU2_DISTANCE_SWEEP_NOTE_2026-04-11.md`, and
     `WILSON_TEST_MASS_CONTINUUM_NOTE_2026-04-11.md`, which already state the
     honest bounded-companion boundary.

4. `frontier_two_field_retarded_probe.py` no longer scores R9 unconditionally.
   - On current `main`, R9 is now explicitly labeled as a diagnostic-only row
     for force-gap / shell / spectral characterization.
   - The runner score now covers only scored rows `R1`-`R8`, and the companion
     note labels R9 as unscored.

5. `frontier_two_field_wave.py` no longer reuses an already evolved field
   state in the family-robustness battery.
   - On current `main`, `W6` restarts each family from fresh `Φ=0`,
     `dΦ/dt=0` data, so the family check is independent of the first branch's
     evolved field history.
   - That rerun lowers the honest hard scores to `4/5`, `5/5`, `4/5`, so the
     wave note now sits as a bounded rerun-corrected result rather than a
     retained `5/5` closure.

6. `frontier_self_consistency_test.py` no longer relies on non-moment-matched
   random controls.
   - On current `main`, the earlier `abs(normal(mean, std))` controls have been
     replaced by the structured-null rerun in
     `SELF_CONSISTENCY_STRUCTURED_NULL_NOTE_2026-04-11.md`.
   - The live runner now uses a torus-shifted static field and a phase-scrambled
     same-spectrum null, and the current rerun reproduces the note's corrected
     fixed-surface output.

7. `frontier_staggered_dag.py` no longer carries a live claim of genuinely
   directed-Hamiltonian DAG compatibility.
   - On current `main`, the runner and note now state the truth: the layered
     acyclic template is still useful as a bounded geometry control, but the
     Hamiltonian symmetrizes the adjacency, so the old retained causal-DAG
     compatibility framing has been withdrawn.

8. `frontier_two_body_mutual_attraction.py` is no longer part of the live
   mutual-attraction evidence chain on current `main`.
   - The old one-wavefunction/two-lobe staggered runner is now carried only as
     a historical exploratory pointer, and
     `TWO_BODY_MUTUAL_ATTRACTION_NOTE_2026-04-11.md` explicitly says it is not
     a genuine two-particle test.
   - The live two-body package now hangs off the bounded open-Wilson successor
     lane in `WILSON_TWO_BODY_OPEN_NOTE_2026-04-11.md`, which is itself
     explicitly framed as a genuine two-orbital channel but not full Newton
     closure.

9. `frontier_entanglement_area_law.py` is no longer part of the live
   boundary-law evidence chain on current `main`.
   - The old runner is now explicitly marked as a historical
     boundary-transfer entropy diagnostic rather than a true subsystem
     entanglement measurement.
   - The live bounded boundary-law package instead hangs off
     `frontier_holographic_probe.py` and its audited addendum, which are
     already framed as a many-body-style Dirac-sea boundary-law result rather
     than a full holography claim.

10. `frontier_bmv_entanglement.py` no longer overstates itself as a genuine
   BMV / gravity-quantumness witness on current `main`.
   - The runner and companion note now present it explicitly as a
     branch-mediated entanglement protocol with an externally imposed
     geometry/source branch.
   - The live bounded package keeps the positive `delta_S > 0` result while
     reserving full BMV / mediator-null claims for future redesigned
     witnesses.

11. The old torus gravitational-decoherence distance sweep is no longer a live
    blocker on current `main`.
   - The runner named in the stale audit entry,
     `frontier_gravitational_decoherence_rate.py`, is not on the live script
     surface.
   - The current mainline gravitational-decoherence companion instead hangs
     off `frontier_grav_decoherence_derived.py` and
     `GRAV_DECOHERENCE_DERIVED_NOTE.md`, which already frame the lane as a
     bounded BMV-class benchmark companion rather than a finite-size torus
     scaling claim.

12. `frontier_geometry_superposition.py` no longer carries the broken
    added-edge pseudo-variant on current `main`.
   - The added-edge DAG builder now samples valid forward skip edges explicitly
     instead of breaking out after the first failed random draw.
   - The rerun keeps the lane as a bounded exploratory/path-sum
     geometry-superposition signal, but the perturbed `added-10%` family is now
     a real constructed variant rather than a fragile near-empty comparison.

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
- Use the corrected periodic package note and corrected companion notes, not
  older pre-fix torus summaries.
