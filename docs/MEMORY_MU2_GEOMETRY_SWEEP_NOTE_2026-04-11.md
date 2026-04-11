# Memory `mu^2` / Geometry Sweep Note

**Date:** 2026-04-11  
**Status:** exploratory / protocol diagnostic

**Script:** `scripts/frontier_memory_mu2_size_sweep.py`

**Anchor scripts:**
- `scripts/frontier_gravitational_memory.py`
- `scripts/frontier_memory_sign_robustness.py`

## Question

Is the screened-memory failure mainly a Yukawa-range artifact, or is the
memory observable itself strongly geometry- and protocol-dependent?

## Sweep design

Two slices were checked:

1. `N = 61, 81, 101, 121` with the source and markers scaled with the ring
   size.
2. A fixed-geometry slice with `posA = 15`, `posB = 45`, `source = 30`
   while `N` grows.

For the larger rings, the evolution window also grows with `N`
(`steps = max(60, N)`), so this is a protocol-and-time sweep, not a pure
single-time static-size snapshot.

The screening ladder was:

- `mu^2 = 0.22, 0.10, 0.05, 0.01, 0.005, 0.001, 0.0`

For the static-screen length estimate, use:

- `ell_screen = 1 / sqrt(mu^2)` for `mu^2 > 0`
- `ell_screen = inf` at `mu^2 = 0`

## Results

### 1) Scaled-geometry slice

The memory signal gets slightly larger as `mu^2` is lowered, but it still
falls strongly with `N`:

- `N=61`: `+0.020854` at `mu^2=0`, `+0.016780` at `mu^2=0.22`
- `N=81`: `+0.010084` at `mu^2=0`, `+0.007071` at `mu^2=0.22`
- `N=101`: `+0.004608` at `mu^2=0`, `+0.002722` at `mu^2=0.22`
- `N=121`: `+0.001767` at `mu^2=0`, `+0.000865` at `mu^2=0.22`

Even when `ell_screen > d_src` for the smaller `mu^2` values, the signal does
not stop decaying with size on this scaled protocol.

### 2) Fixed-geometry slice

Keeping the geometry fixed changes the picture:

- `N=61`: `+0.020854` at `mu^2=0`, `+0.016780` at `mu^2=0.22`
- `N=81`: `+0.231199` at `mu^2=0`, `+0.244260` at `mu^2=0.22`
- `N=101`: `+1.255389` at `mu^2=0`, `+1.143707` at `mu^2=0.22`
- `N=121`: `+2.580905` at `mu^2=0`, `+2.599619` at `mu^2=0.22`

The fixed-geometry signal survives at all tested `mu^2` values and becomes
much larger on larger rings. The dependence on `mu^2` is weak compared with
the dependence on the protocol geometry.

## Interpretation

The memory failure is **not primarily a Yukawa-range artifact**.

What the sweep shows instead:

- the original size-fragility came from the protocol scaling the marker/source
  geometry with `N`
- the screened field contributes, but it is not the dominant cause of collapse
- when the geometry is held fixed, the signal survives and strengthens even
  at the original `mu^2 = 0.22`

## Conclusion

The memory lane remains exploratory, but the failure mode is now narrower and
more honest:

- `mu^2` matters
- geometry scaling matters more
- the old “screening alone killed memory” diagnosis is too strong

Future reruns should keep the geometry fixed and use a different arrival-time
observable if the goal is a publication-grade memory claim.
