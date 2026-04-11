# Two-Body Mutual Attraction Note

**Date:** 2026-04-11  
**Status:** exploratory, not retained  
**Scripts:**  
- `frontier_two_body_mutual_attraction.py`  
- `frontier_two_orbital_mutual_attraction.py`  
- `frontier_two_body_acceleration.py`
- `frontier_two_body_partner_kick.py`
- `frontier_two_body_partner_kick_size_scan.py`

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

## Symmetry-Averaged Partner-Kick Follow-Up

`frontier_two_body_partner_kick.py` improves the observable again:

- periodic 3D staggered lattice
- two separate orbitals
- compare `shared` against `self_only`
- use the partner-induced centroid kick rather than raw second differences
- average over:
  - two parity placements
  - both left/right orientations of the pair

This cancels much of the common-translation contamination that was still
present in the raw acceleration harness.

### What survives on this surface

On the **massless-field** surface `mu^2 = 0`, with separation `sep = 4` on the
`n=9` periodic 3D lattice, the mutual channel becomes clean:

- `G=10`: `7/8` toward steps, `4/5` early toward steps
- `G=20`: `8/8` toward steps, `5/5` early toward steps
- `G=30`: `8/8` toward steps, `5/5` early toward steps
- `G=50`: `8/8` toward steps, `5/5` early toward steps
- `G=100`: `8/8` toward steps, `5/5` early toward steps

Representative kick sizes on that same surface:

- `G=20`: mean early mutual kick `+4.96e-4`, final `+1.37e-3`
- `G=50`: mean early mutual kick `+1.23e-4`, final `+3.31e-4`

The common-shift diagnostic is also small on this surface, so this is a
meaningfully cleaner mutual-channel read than the older centroid or raw
acceleration proxies.

### What still fails

The signal is **not** general:

- with screening (`mu^2 > 0`), the same surface mostly loses the effect
- at shorter separations (`sep = 2, 3`), the `mu^2 = 0` signal disappears
- the partner-gradient diagnostic remains outward in sign and is not an exact
  force observable under parity coupling

So this is a narrow periodic/massless window, not Newton-law closure.

### First size check

`frontier_two_body_partner_kick_size_scan.py` checks the same massless periodic
surface on odd cubic sizes `side = 7, 9, 11`, using the maximal symmetric
separation `sep = floor(side/2)`.

What survives:

- `side=7, sep=3`
  - `G=10`: `8/8` toward, `5/5` early, mean early kick `+6.31e-3`
  - `G=20`: `8/8` toward, `5/5` early, mean early kick `+2.56e-3`
- `side=9, sep=4`
  - `G=20`: `8/8` toward, `5/5` early, mean early kick `+4.96e-4`
  - `G=50`: `8/8` toward, `5/5` early, mean early kick `+1.23e-4`

What does **not** yet justify retention:

- `side=11, sep=5` keeps the sign pattern at `G=20,50`, but the amplitude is
  tiny:
  - `G=20`: mean early kick `+4.12e-6`
  - `G=50`: mean early kick `+9.69e-7`
- those kicks are already far smaller than the lower-size signals, so the
  current size scan does **not** support a stable continuum-strength mutual
  channel

So the first size check says:

- this is not a pure side-9 resonance
- but it is still a narrow, rapidly decaying signal rather than a robust
  emergent force law

## Honest State

The two-body lane is still **open**, but it is no longer a pure null.

What now exists is:

- a **narrow positive window** on the symmetry-averaged periodic 3D surface
- no broad or screened two-body closure
- no retained distance-law or monotone separation scaling

What is ruled out:

- the one-wavefunction two-lobe proxy as a decisive test
- the claim that mutual attraction is already detected in the current repo

What survives:

- the question is still the correct high-value experiment
- the proper comparison is `shared` vs `self_only`
- centroid separation alone is too contaminated by baseline drift to carry the
  claim
- the massless symmetry-averaged partner-kick observable is the cleanest
  current mutual-channel probe

## Next Requirement

Before this lane can be retained, it needs:

1. size-scaling of the `mu^2 = 0`, `sep = 4` periodic window
2. clarification of why the signal disappears at shorter separations
3. a distance-law surface that is not just a single narrow resonance window
4. a bridge from this massless periodic signal to the broader screened graph
   program

Until then, the two-body mutual-attraction lane remains exploratory.
