# Two-Body Mutual Attraction Note

**Date:** 2026-04-11  
**Status:** exploratory, not retained  
**Scripts:**  
- `frontier_two_body_mutual_attraction.py`  
- `frontier_two_orbital_mutual_attraction.py`  
- `frontier_two_body_acceleration.py`

## Question

Can the staggered parity-coupled self-consistent field produce a genuine
two-body mutual-attraction signal that is not reducible to single-packet
self-focusing or baseline drift?

This is the clearest Nature-threshold experiment in the current framework:
two separated packets should pull toward each other through a shared
self-consistent `Phi` field.

## Important Correction

`frontier_two_body_mutual_attraction.py` is **not** a genuine two-particle
test. It evolves a single wavefunction with two lobes. That runner can still
be useful as a stress test, but it does not isolate a mutual interaction
channel between distinct bodies.

So it should not be used as evidence for emergent Newtonian attraction.

## Proper Hartree Control

`frontier_two_orbital_mutual_attraction.py` introduces the correct control
surface:

- two separate orbitals `psi_A`, `psi_B`
- `shared`: both evolve under one self-consistent `Phi[|psi_A|^2 + |psi_B|^2]`
- `self_only`: each orbital evolves only under its own field
- `frozen`: both evolve under the initial shared field
- `free`: no field

The clean residual is:

`residual(t) = sep_shared(t) - sep_self_only(t)`

If the shared field produces a genuine mutual attraction beyond self-focusing,
the residual should become cleanly and persistently negative.

## Hartree Two-Orbital Result

On the audited open-lattice surface used by the harness:

- `G=5`: final residual `+0.0837`
- `G=10`: final residual `+0.0256`
- `G=20`: final residual `-0.0360`
- `G=40`: final residual `-0.0055`
- `G=80`: final residual `+0.0074`

This is not a robust monotone attractive signal.

Only `G=20` shows even a mild negative residual, and it is small and
non-monotone across the sweep.

## 3D Early-Time Acceleration Follow-Up

`frontier_two_body_acceleration.py` tries a better short-time observable on a
3D staggered lattice:

- compare `shared` against `self_only`
- extract early-time mutual acceleration
- examine raw and smoothed second derivatives of the packet separation

This helps with the centroid-drift contamination problem, but it does **not**
yet close the lane.

Current result:

- raw and smoothed mutual-acceleration signs disagree across parts of the sweep
- dependence on `G`, `mu^2`, separation, and mass ratio is not clean
- the baseline is improved, but the observable is still too unstable to retain

So this is useful frontier instrumentation, not a publishable positive.

## Honest State

The two-body lane is still **open**.

What is ruled out:

- the one-wavefunction two-lobe proxy as a decisive test
- the claim that mutual attraction is already detected in the current repo

What survives:

- the question is still the correct high-value experiment
- the proper comparison is `shared` vs `self_only`
- centroid separation alone is too contaminated by baseline drift to carry the
  claim

## Next Requirement

Before this lane can be retained, it needs:

1. a zero-drift baseline surface
2. a stable early-time mutual-acceleration observable
3. a clear `shared < self_only` separation on that same surface
4. sensible scaling with coupling and initial separation

Until then, the two-body mutual-attraction lane remains exploratory.
