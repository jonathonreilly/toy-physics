# Two-Sign Comparison Note

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-10  
**Script:** `frontier_two_sign_comparison.py`

## Question

Does consistency select the coupling sign in the graph-native staggered /
self-gravity lane under the **old identity-coupling convention**?

The tested comparison is:

- attractive: `H_diag = mass * parity - mass * Phi`
- repulsive: `H_diag = mass * parity + mass * Phi`

If the repulsive sign were pathological while the attractive sign stayed
stable, that would be real evidence that the sign is selected rather than
assumed. It is now best read as a **negative control** for the retired
identity-coupling form, not as the final sign audit for the corrected
scalar/parity coupling.

## Main Result

It does **not**.

On the tested retained-size families, both signs are stable:

- norm drift stays at machine precision
- `Phi` stays bounded / convergent
- energy stays bounded
- spectral range stays comparable
- width evolution stays comparable

The strongest conclusion is negative:

**consistency does not select the sign at these parameters.**

## Force Implication

The irregular-graph force observables are not sign-selective.

On the tested families, the shell-based and edge-radial measures can remain
positive under both attractive and repulsive coupling. That means these
observables are dominated by the source-centered `Phi` profile, not by the
wavepacket's dynamical response to the sign with which `Phi` enters the
Hamiltonian.

So on irregular graphs:

- shell-radial sign rows are **not** evidence of attractive gravity
- edge-radial sign rows are **not** sufficient by themselves either
- the exact cubic-lattice force `F = -<dV/dx>` remains the only retained
  direction observable in the current stack

## What Survives

The following results remain meaningful after the two-sign audit:

- stability / boundedness of the interacting graph dynamics
- source linearity and additivity
- source-scale characterization (`G_eff`)
- topology-dependent onset / transition structure
- native gauge closure on cycle-bearing graphs
- Born / norm / Lieb-Robinson transport constraints

## What This Changes

It narrows the claim set:

- the irregular-graph cycle battery, retarded probe, and family-closure probe
  remain strong **structural interaction** results
- they are **not** retained evidence that the architecture predicts attractive
  gravity direction on irregular graphs

## Next Decision

The project now has a real fork:

1. **Derive the sign** from the staggered / Dirac structure itself
2. **Reframe** around sign-agnostic interacting-field results

The companion corrected-coupling check is now
`frontier_two_sign_parity.py`: it shows that direct external-source sign tests
become sign-sensitive again under the parity-coupled scalar channel. What is
still missing is one frozen irregular-graph directional observable that is as
clean as the exact lattice-coordinate force used by the canonical cubic card.
