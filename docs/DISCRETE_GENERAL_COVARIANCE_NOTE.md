# B1 as Discrete General Covariance — Theoretical Argument

**Date:** 2026-04-11
**Status:** Speculative framing, not yet a retained claim

## The Observation

On irregular bipartite graphs, the parity coupling (m + Phi) * epsilon(x)
absorbs the sign of Phi via the alternating epsilon factor. The dynamics
under +Phi and -Phi produce nearly identical gap-averaged behavior (both
contract, both produce TOWARD shell forces). Only in the weak-coupling
perturbative regime (G=5-10) does a 13-20% width asymmetry emerge.

The force DIRECTION (centroid displacement toward/away from source) is
not cleanly sign-selective on irregular graphs. The force MAGNITUDE effects
(contraction, gap widening, spectral response) ARE sign-sensitive.

## The Argument

On a bipartite graph G with vertex set V = V_even + V_odd, a staggering
assignment is a function epsilon: V -> {+1, -1} with epsilon(v) = +1 for
v in V_even and epsilon(v) = -1 for v in V_odd. On many bipartite graphs,
multiple valid staggering assignments exist (e.g., swapping V_even and V_odd).

The parity coupling H_diag = (m + Phi) * epsilon makes the Hamiltonian
DEPEND on which staggering is chosen. But the physical observables should
NOT depend on this choice — the staggering is a convention, like a
coordinate system.

This is the discrete analog of diffeomorphism invariance in GR:
- In GR, the metric g_mu_nu depends on coordinates, but physical
  observables (geodesic length, curvature invariants) do not.
- On a graph, the Hamiltonian depends on the staggering assignment,
  but physical observables should depend only on graph-invariant
  quantities.

## What IS Staggering-Invariant

Under staggering swap (epsilon -> -epsilon):
- Width ratio (contraction): INVARIANT (depends on |m + Phi| averaged
  over the graph, not on which sites are "even")
- Spectral gap: INVARIANT (eigenvalues of H don't change sign under
  global staggering flip; they get permuted)
- Binding energy difference: APPROXIMATELY invariant (small asymmetry
  at weak coupling)
- Critical exponent beta: INVARIANT (topology-dependent, not
  staggering-dependent)

Under staggering swap:
- Shell force direction: CHANGES SIGN (this is the gauge-dependent part)
- Centroid displacement: CHANGES SIGN

## The Claim (Speculative)

The sign of the gravitational force on irregular graphs is the
staggering-gauge-dependent part of the physics. The gauge-invariant
content is in the magnitude observables: contraction, spectral gap,
critical exponents, binding energy. These ARE sign-sensitive (attract
contracts more, wider gap) and are the correct observables for
gravity on discrete structures.

This reframes B1 from "we can't measure force direction on irregular
graphs" to "force direction is a gauge artifact on discrete structures,
and the gauge-invariant observables correctly capture gravitational
attraction."

## What This Does NOT Resolve

1. The staggering-swap is not literally a gauge symmetry of the full
   theory — it changes the Hamiltonian. A true gauge symmetry would
   leave the Hamiltonian invariant. The argument is that PHYSICAL
   observables are invariant, even though the Hamiltonian is not.

2. On regular lattices with coordinates, the force direction IS
   gauge-invariant (it doesn't depend on the staggering assignment).
   So the "gauge freedom" is specific to irregular graphs.

3. This argument would be stronger if we could prove that the space
   of valid staggerings on a bipartite graph forms a group, and that
   the parity coupling is the unique coupling respecting this group.
   That proof does not yet exist.

## Status

This is a speculative theoretical framing, not a retained result.
It motivates reframing the paper around gauge-invariant observables
(contraction, gap, critical exponents) rather than force direction.
The weak-coupling sign sensitivity (G=5-10, 14/15) provides additional
evidence that the perturbative regime does distinguish the signs.
