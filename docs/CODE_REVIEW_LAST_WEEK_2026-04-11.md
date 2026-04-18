# Code Review — Last Week Surface (2026-04-04 to 2026-04-11)

This note records the validated high-risk findings from the last-week review.
It is not a full changelog. It is a guardrail list for results that should not
be promoted or reinterpreted without fixes.

## Validated High-Severity Findings

1. `frontier_wilson_newton_law.py` is not a clean Newton-law runner.
   - The lattice is periodic, despite the stronger header claim.
   - The mass sweep only rescales orbital B's source contribution; it does not
     vary inertial response.
   - So the script cannot support either an image-free distance-law claim or a
     full `F ∝ M1 M2` claim.

2. `frontier_two_body_mutual_attraction.py` is not a genuine two-body test.
   - It evolves one wavefunction with two lobes.
   - Any separation signal is contaminated by self-focusing and lobe
     interference.

3. `frontier_branch_entanglement_robustness.py` hard-wires `tau_3 = 0`.
   - The current overlap-based formula makes GHZ impossible by construction for
     the two-branch ansatz.
   - So `0/25 GHZ` is not an empirical result.

4. Several periodic 2D staggered runners misweight wraparound neighbors.
   - The pattern is: periodic adjacency via modulo indexing, followed by
     hopping weights computed from raw coordinate differences instead of
     minimum-image distances.
   - Verified examples include:
     - `frontier_born_rule_alpha.py`
     - `frontier_self_consistency_test.py`
     - `frontier_eigenvalue_stats_and_anderson_phase.py`
   - This contaminates boundary-crossing couplings in those periodic 2D
     surfaces.

5. `frontier_entanglement_area_law.py` is not a bipartite entanglement
   entropy measurement.
   - It fits the entropy of a boundary transfer/channel object, not a true
     subsystem reduced density matrix.

6. `frontier_bmv_entanglement.py` overstates what it measures.
   - The script computes a branch-mediated toy witness.
   - It does not implement the full logic needed for a genuine BMV
     gravity-quantumness conclusion.

## Validated Medium-Severity Findings

1. `frontier_self_consistency_test.py` random controls are not moment-matched.
   - Using `abs(normal(mean, std))` changes both mean and variance, so the sign
     and correlation comparisons are confounded.

2. `frontier_staggered_dag.py` is not actually directed in the Hamiltonian.
   - The current construction stores edges both ways, so the retained signal is
     a layered-bias result, not a true DAG propagation test.

## Resolved Since Review

1. `frontier_two_field_retarded_probe.py` no longer scores R9 unconditionally.
   - On current `main`, R9 is now explicitly labeled as a diagnostic-only row
     for force-gap / shell / spectral characterization.
   - The runner score now covers only scored rows `R1`-`R8`, and the companion
     note labels R9 as unscored.

2. `frontier_two_field_wave.py` no longer reuses an already evolved field
   state in the family-robustness battery.
   - On current `main`, `W6` restarts each family from fresh `Φ=0`,
     `dΦ/dt=0` data, so the family check is independent of the first branch's
     evolved field history.
   - That rerun lowers the honest hard scores to `4/5`, `5/5`, `4/5`, so the
     wave note now sits as a bounded rerun-corrected result rather than a
     retained `5/5` closure.

## Verified False Positive From Agent Review

One agent claimed `frontier_wilson_two_body_open.py` still computed center of
mass on a torus. That finding was checked and rejected. The current
`center_of_mass_x()` in the open Wilson runner uses a linear mean on the open
surface.

## Immediate Hardening Implications

- Treat the periodic Wilson Newton runner as historical only.
- Treat the original two-body staggered runner as invalid for mutual-attraction
  claims.
- Do not promote the branch-entanglement GHZ/W classification as-is.
- Re-audit all periodic 2D staggered results touched by the wraparound-weight
  bug before upgrading them.
