# 3D `1/L^2 + h^2` Narrow `h=0.125` Bridge Note

**Date:** 2026-04-05
**Status:** bounded negative for a narrow `h=0.125` bridge claim

This note is intentionally narrower than the broader `h^2+T` distance-law
frontier. It asks only whether the current dense 3D numpy family can support a
very narrow retained bridge claim at `h = 0.125` without overselling
continuum closure.

## Artifact chain

- [`scripts/lattice_3d_l2_numpy_h0125_audit.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_audit.py)
- [`scripts/lattice_3d_l2_numpy_h0125_bridge.py`](/Users/jonreilly/Projects/Physics/scripts/lattice_3d_l2_numpy_h0125_bridge.py)

## Question

Can the retained 3D dense `1/L^2 + h^2` lane support a narrow `h=0.125`
bridge claim with weak-field `F~M` near `1`, clean Born, and a stable gravity
sign, while staying honest about the boundary leakage / `P_det` underflow
problem?

## Replay summary

Two disjoint replays were used:

1. A reduced fixed-family audit at `phys_l = 4`, `phys_w = 1.5`,
   `max_d_phys = 3`
2. The existing bridge family at `phys_l = 6`, `phys_w = 3`,
   `max_d_phys = 3`

The reduced audit family is the decisive one for the narrow claim because it
reaches `h = 0.125` cleanly and directly tests the weak-field observables.

### Reduced audit family

| `h` | Born `|I3|/P` | gravity sign | `F~M` | note |
| --- | ---: | --- | ---: | --- |
| `1.0` | `nan` | `AWAY` | n/a | too few `TOWARD` points |
| `0.5` | `1.39e-15` | `AWAY` | n/a | too few `TOWARD` points |
| `0.25` | `2.50e-15` | `AWAY` | n/a | too few `TOWARD` points |
| `0.125` | `4.23e-15` | `AWAY` | n/a | too few `TOWARD` points |

The narrowest safe reading from that replay is:

- Born stays machine-clean where it is measurable
- the reduced family reaches `h = 0.125`
- the weak-field gravity lane does **not** recover on this family
- there are not enough `TOWARD` points to form a retained `F~M` bridge

### Bridge family

The larger fixed bridge family is now fully resolved on its focused
`h = 0.125` row, and it still does not rescue the narrow claim:

- `h = 1.0`: Born `6.65e-16`, gravity `AWAY`, `F~M` too few `TOWARD` points
- `h = 0.5`: Born `1.66e-15`, gravity `TOWARD`, `F~M = 0.50`
- `h = 0.25`: Born `3.48e-15`, gravity `TOWARD`, `F~M = 0.50`
- `h = 0.125`: Born `6.59e-15`, `k = 0` clean, gravity `TOWARD`,
  `F~M = 0.50`

That is still not a retained weak-field bridge to `F~M \approx 1`, even
though the focused `h = 0.125` row now completes cleanly on this family.

## Safe Read

The strongest honest statement on current `main` is:

- the dense 3D `1/L^2 + h^2` family is numerically well-defined at `h = 0.125`
- Born remains clean
- the fixed bridge family reaches `h = 0.125` with `TOWARD` sign and clean
  `k = 0`
- but the narrow weak-field bridge claim does **not** survive on the reduced
  family
- the bridge family also falls short of the narrow `F~M \approx 1` bar at
  `h = 0.125`

## Limit diagnosis

The final diagnostic made this failure more informative rather than less.

Three cheap rescue hypotheses were checked on the fixed bridge family:

1. **Bad weak-field window**
   - source strengths were weakened by two extra decades
   - the fitted exponent stayed pinned at about
     `0.5009 -> 0.50035 -> 0.50012`
2. **Bad source-distance choice**
   - moving the source inward to `z_mass = 1.5` on the full detector still
     gave `alpha ~ 0.50`
3. **Detector starvation / underflow**
   - the free detector support is enormous (`P_free ~ 8.9e221`)
   - so this is not a “no signal reaches the detector” failure

That gives a more interesting explanation of the limit:

- the fixed `h = 0.125` family keeps a clean `TOWARD` signal
- it keeps Born clean
- but the weak-field response collapses from an approximately linear
  `delta ~ s` law into an approximate `delta ~ s^(1/2)` law

So the best present-tense read is geometric / transport-limited rather than
strength-limited: this box is still wide enough to carry signal, but not wide
enough to preserve the Newtonian weak-field mass law.

## Honest Limitation

This is a credibility audit, not a continuum theorem.

It does **not** promote:

- an `h = 0.125` positive bridge claim
- a continuum-limit theorem
- a clean Newtonian weak-field closure on the reduced family

If a stronger `h = 0.125` continuation exists elsewhere, it still needs its
own frozen script/log/note chain before it should influence the retained claim
surface on `main`.

## Final Verdict

**bounded negative**

The narrow `h=0.125` bridge claim does not currently survive on `main`.
