# Chiral Bottleneck Card Proposal

**Date:** 2026-04-10  
**Scope:** add an early-failure card in front of the moonshot battery so the main architectural limits are exposed before the large sweeps.

This proposal is based on:
- [FULL_TEST_MATRIX_2026-04-10.md](/Users/jonreilly/projects/Physics/.claude/worktrees/sleepy-cerf/docs/FULL_TEST_MATRIX_2026-04-10.md)
- [CHIRAL_WALK_SYNTHESIS_2026-04-09.md](/Users/jonreilly/projects/Physics/.claude/worktrees/sleepy-cerf/docs/CHIRAL_WALK_SYNTHESIS_2026-04-09.md)
- [CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md](/Users/jonreilly/projects/Physics/.claude/worktrees/sleepy-cerf/docs/CHIRAL_WALK_SYNTHESIS_2026-04-10_ADDENDUM.md)

The repeated pattern in the matrix is not “many unrelated failures.” It is a smaller set of structural bottlenecks:
- factorized transport in 3D
- overloaded `theta` coupling
- k-dependent gravity readouts
- boundary/recurrence sensitivity
- mixed observables being treated as the same measurement

The closure card should catch those first.

## Proposed Rows

| Row | Test | What it measures | Why it is early |
|---|---|---|---|
| B1 | 3D KG isotropy / coupled-coin dispersion | `E^2` vs `k^2` along axes and diagonal, plus isotropy ratio | This is the first gate for the factorized-coin bottleneck. If the coin is still separable, KG will fail before any downstream gravity claim can be trusted. |
| B2 | 3D gauge-loop / AB visibility | Wilson loop or enclosed-flux visibility on the same 3D harness | If AB only works in lower dimension or only with geometry tricks, the 3D transport law is still missing cross-pair coupling. |
| B3 | Fixed-`theta` k-achromaticity | Deflection vs carrier `k` at fixed `theta`, matched travel distance, same source geometry | This separates “wave-window” effects from a structural gravity law. The current matrix already shows `k`-dependence in CH-1D. |
| B4 | Split mass parameter vs gravity susceptibility | Hold free dispersion mass fixed while sweeping a separate gravity coupling | This tests whether `theta` is doing too many jobs at once. It directly targets the equivalence-principle pressure in the matrix. |
| B5 | Boundary-condition robustness / recurrence phase diagram | Periodic vs reflecting vs open at fixed `delta = d/n` and `lambda = L/n` | This catches torus wrap and recurrence artifacts before they are mistaken for physics. It is the right way to expose 3+1D sign-window instability early. |
| B6 | Multi-observable gravity consistency | Compare first-arrival, peak, current, centroid, and torus-aware centroid on the same run | This forces us to separate geometric drift from wave interference. If only one observable flips, the readout is the problem, not the transport. |

## Suggested Harness Mapping

These rows do not all need new infrastructure.

- **B1/B2:** extend [frontier_coupled_dirac_coin_3plus1d.py](/Users/jonreilly/projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_coupled_dirac_coin_3plus1d.py). That file already contains the coupled-coin hypothesis and a Bloch-analysis engine.
- **B3/B4:** reuse the corrected fixed-`theta` and carrier-`k` helpers already introduced in [frontier_chiral_final_moonshots.py](/Users/jonreilly/projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_chiral_final_moonshots.py).
- **B5:** reuse the torus-aware recurrence logic from [frontier_chiral_3plus1d_decoherence_sweep.py](/Users/jonreilly/projects/Physics/.claude/worktrees/sleepy-cerf/scripts/frontier_chiral_3plus1d_decoherence_sweep.py).
- **B6:** add a small readout wrapper on top of the existing closure-card helpers so the same run reports all observables.

## Recommended Pass Criteria

These are not meant to be “everything passes” rows. They are meant to fail fast when the architecture is still wrong.

- **B1:** coupled 3D coin should improve the isotropic KG fit relative to the current factorized baseline, and the axis/diagonal slopes should agree within a tight band.
- **B2:** AB visibility should remain nonzero under a genuine closed-loop flux test, not just a local phase decoration.
- **B3:** the deflection should be stable across `k` to within a small coefficient of variation if the architecture is really achromatic at fixed `theta`.
- **B4:** varying the gravity coupling should not require changing the free mass gap. If it does, mass and gravity susceptibility are still fused.
- **B5:** the sign map should be stable when expressed in `delta` and `lambda`, not just at one raw `n, L` operating point.
- **B6:** the gravity sign and magnitude should agree across observables after minimum-image correction. If only the centroid flips, the card should mark that as an observable mismatch.

## Axiom Pressure

The bottleneck card should force the axioms to answer sharper questions:

- **Axiom 6** needs a stronger statement about local continuation channels. The 3D failures suggest that axis-separable transport is not enough; the on-site operator likely has to be irreducible across the available channels.
- **Axiom 8** should not be read as “any distorted continuation gives gravity.” The card should distinguish geometric drift from wave readout.
- **Axiom 10** should remain a summary score, not a substitute for the structural checks above.

## Order Of Operations

If we only add four rows first, make them:
1. B1 coupled-coin 3D KG isotropy
2. B2 3D gauge-loop / AB visibility
3. B3 fixed-`theta` k-achromaticity
4. B4 split mass vs gravity susceptibility

If we add two more immediately, make them:
5. B5 boundary-condition robustness / recurrence phase diagram
6. B6 multi-observable gravity consistency

## Optional Seventh Row

If you want a dedicated growth gate, add:
- **B7 growth/backreaction separation**: evolve propagation first, then apply growth or record deposition after the state is measured, not while it is still coherent.

That row is useful, but it is secondary to the transport bottlenecks above.

## Bottom Line

The right early-card strategy is not “more moonshot coverage.” It is to force the architecture to answer six structural questions before the big sweeps:
- can the 3D coin actually couple dimensions
- can the 3D harness support a real gauge loop
- is gravity achromatic in `k`
- is gravity separable from mass
- are sign windows boundary artifacts
- are the gravity observables consistent

If those six are clean, the moonshots become much more meaningful. If any of them fails, the failure mode is local and actionable instead of being discovered late.
