# Staggered Both-Masses Note

**Date:** 2026-04-11  
**Status:** frontier-only negative / partial on the blocked staggered surface  
**Script:** `scripts/frontier_staggered_both_masses.py`

## Question

Can the blocked `2x2x2` staggered trajectory observable support a genuine
both-masses law on the same open 3D cubic surface where the staggered
external-source Newton reproduction succeeded?

This is the direct follow-up to
`STAGGERED_NEWTON_REPRODUCTION_NOTE_2026-04-11.md`.

## Surface

- open 3D cubic staggered lattice
- literature-correct parity coupling
  - `H_diag = (m + Phi) * epsilon(x)`
- blocked `2x2x2` centroid readout along `z`
  - same clean axis as the staggered external-source Newton reproduction
- `side = 14`
- packet separation `d = 4`
- `G = 50.0`
- `mu^2 = 0.001`
- `source_scale = 5e-4`
- `dt = 0.10`
- `N_steps = 10`
- packet width `sigma = 1.30`
- mass grid `M_A, M_B in {0.2, 0.3, 0.4}`

## Control structure

Each mass pair is evolved in:

- `SHARED`: both orbital densities source one common `Phi`
- `SELF_ONLY`: each orbital sees only its own `Phi`

Primary observables:

- `a_A^mut = +(a_A^shared - a_A^self)`
- `a_B^mut = -(a_B^shared - a_B^self)`

where `a_A` and `a_B` are early-time blocked-centroid accelerations along `z`.

Derived observables:

- `a_close = 0.5 * (a_A^mut + a_B^mut)`
- `F_A = M_A * a_A^mut`
- `F_B = M_B * a_B^mut`

The test is intentionally honest:

- if both `a_A^mut` and `a_B^mut` are inward-positive and scale cleanly with
  partner mass, the blocked staggered observable supports a true both-masses
  lane
- if only `a_close` is clean while the packet-level split is inconsistent, the
  blocked observable is only a relative-coordinate proxy and does **not** close
  a both-masses law

## Exact output

```text
  M_A   M_B |     a_A^mut     a_B^mut     a_close |         F_A         F_B     relΔF
-------------------------------------------------------------------------------------
  0.2   0.2 | -8.856721e-07 +5.646028e-06 +2.380178e-06 | -1.771344e-07 +1.129206e-06  100.00%
  0.2   0.3 | -1.330352e-06 +8.426493e-06 +3.548071e-06 | -2.660703e-07 +2.527948e-06  100.00%
  0.2   0.4 | -1.775941e-06 +1.114473e-05 +4.684396e-06 | -3.551882e-07 +4.457893e-06  100.00%
  0.3   0.2 | -1.314317e-06 +8.455188e-06 +3.570436e-06 | -3.942950e-07 +1.691038e-06  100.00%
  0.3   0.3 | -1.973000e-06 +1.262637e-05 +5.326683e-06 | -5.918999e-07 +3.787910e-06  100.00%
  0.3   0.4 | -2.632222e-06 +1.670430e-05 +7.036038e-06 | -7.896666e-07 +6.681719e-06  100.00%
  0.4   0.2 | -1.728072e-06 +1.125535e-05 +4.763638e-06 | -6.912288e-07 +2.251070e-06  100.00%
  0.4   0.3 | -2.593318e-06 +1.681768e-05 +7.112180e-06 | -1.037327e-06 +5.045303e-06  100.00%
  0.4   0.4 | -3.458742e-06 +2.225580e-05 +9.398527e-06 | -1.383497e-06 +8.902318e-06  100.00%
```

Anchor fits:

- `a_A^mut` vs `M_B` at `M_A = 0.3`
  - `a_A^mut = -6.589527e-06 * M_B + 3.678758e-09`
  - `R^2 = 1.000000`
- `a_B^mut` vs `M_A` at `M_B = 0.3`
  - `a_B^mut = +4.195592e-05 * M_A + 3.673566e-08`
  - `R^2 = 1.000000`
- `a_close` vs `(M_A + M_B)`
  - `a_close = +1.755534e-05 * (M_A + M_B) - 5.219855e-06`
  - `R^2 = 0.964412`

Full-grid normalization:

- `a_A^mut / M_B`
  - mean `-6.551459e-06`
  - std `1.718668e-06`
  - `CV = 26.233%`
- `a_B^mut / M_A`
  - mean `+4.198457e-05`
  - std `1.122599e-05`
  - `CV = 26.738%`

Force-balance proxy:

- mean `|F_A - F_B| / (|F_A| + |F_B|) = 100.000%`
- max `= 100.000%`

Runtime:

- `32.6s`

## What survived

One weak but real positive survives:

- the blocked **relative** coordinate closes inward
- `a_close` grows with the total mass scale
- the fit against `(M_A + M_B)` is respectable (`R^2 = 0.964`)

So the blocked readout does capture a mutual channel in the **pair-relative**
coordinate.

## What failed

The actual both-masses closure fails cleanly.

### 1. Packet-level split is not physically consistent

`a_A^mut` and `a_B^mut` have opposite signs on the entire grid:

- packet A channel is outward on this sign convention
- packet B channel is inward

So the blocked packet-level observable does **not** give a clean symmetric
inward response for the two packets.

### 2. Full-grid partner-mass law is not stable

The anchor slices are perfectly linear, but that is misleading here. The full
grid shows large normalization drift (`~26%` CV on both channels), so the split
is not globally separable into one clean both-masses law.

### 3. Force balance fails completely

The force proxy mismatch is `100%` on every row because the packet-level split
does not produce a consistent equal-and-opposite pair.

That is a hard failure for any retained Newton closure claim.

## Interpretation

The staggered blocked observable solves the **single-packet external-source**
problem much better than the raw centroid, but that does **not** automatically
transfer to the two-body lane.

What seems to happen here is:

- the blocked observable is good enough to expose a relative closing channel
- but not good enough to decompose that channel into two honest packet-level
  forces

So the surface supports a weak relative-coordinate positive, not a retained
both-masses law.

## Retention decision

This result is **not retainable** as a both-masses closure.

Safe statement:

> On the open cubic staggered surface, the blocked `2x2x2` trajectory
> observable captures a small inward relative-closing channel that scales
> roughly with total mass, but it fails the packet-level sign and force-balance
> checks required for a retained both-masses law.

So this lane remains frontier-only.

## Practical consequence

The staggered architecture now has:

- a clean exact-force law on the canonical card
- a clean blocked external-source `d^-2` trajectory law on the open cubic
  surface
- **no** retained blocked both-masses closure

That means the next honest staggered step is not another mass-grid sweep on the
same observable. It is a different two-body readout:

- local momentum flux
- mid-plane current
- or a relative-coordinate observable derived directly from the blocked density

The current blocked centroid split is not enough.
