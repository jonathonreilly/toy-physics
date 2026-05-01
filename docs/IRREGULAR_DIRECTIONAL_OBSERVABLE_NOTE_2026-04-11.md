# Irregular-Graph Directional Observable Probe

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-11  
**Script:** `frontier_irregular_directional_observable.py`
**Status on current `main`: historical blocker surface for the off-center /
transport-style probe; later bounded core-packet separator exists on a
narrower centered packet surface**

## Question

Can the endogenous irregular-graph lane produce one sign-selective dynamical
observable that distinguishes attractive from repulsive coupling on the same
family, without relying on shell-profile positivity?

The probe uses:

- an off-center prepared wavepacket
- the endogenous loop `|psi|^2 -> Phi -> H`
- parity coupling as the corrected staggered scalar channel
- identity coupling as a negative control

The observables are dynamical, not field-profile-only:

1. short-time depth shift `Δ<depth>`
2. signed cut flux across BFS shells
3. frontier current bias at the source-adjacent shell

## Why this probe

The retained irregular batteries exposed a weakness: the shell-based force
proxies can stay TOWARD even when the coupling sign is flipped. That means
those proxies are measuring the `Phi` profile shape more than the matter
response.

This probe tries to force the sign question onto the wavefunction response
itself.

## Success Criterion

A candidate observable is sign-selective if, on the same graph family and at
the same operating point, the parity and identity couplings produce opposite
signs robustly across the retained families.

If no candidate achieves that, the correct conclusion is a blocker:

- the endogenous lane has stable dynamics
- but it still lacks a frozen graph-native directional observable

## Status

This is a fresh probe, not a retained battery replacement.
It is meant to decide whether the directional-observable track can be
promoted at all.

## Measured Result

Rerun on the retained irregular families with the endogenous self-gravity
loop and an off-center prepared packet:

| Metric | Sign-separated parity-vs-identity cases |
|--------|-----------------------------------------|
| `Δ<depth>` | `0/9` |
| signed cut flux | `0/9` |
| frontier current bias | `4/9` |

Observed values:

- `random_geometric`: depth shift and cut flux stayed positive under both
  couplings; frontier bias stayed near zero.
- `growing`: parity and identity often differed in magnitude, but not in sign
  for the depth/cut observables; frontier bias was the only partial separator.
- `layered_cycle`: cut flux and depth shift again failed to separate; frontier
  bias flipped only weakly and not robustly.

## Conclusion

No candidate observable is yet frozen as a robust sign-selective directional
measure on the endogenous irregular lane.

The strongest blocker is:

- the short-time wavefunction response still depends more on graph family and
  operating point than on the coupling sign
- shell proxies are not enough
- the best current dynamical candidate (`frontier current bias`) is partial
  only, not robust across families

So this specific off-center / transport-style probe is a **blocker result**,
not a retained win.

## Later Narrow Bounded Reopen

Current `main` now also carries a later, narrower bounded same-surface reopen:

- [`IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md`](IRREGULAR_SIGN_CORE_PACKET_GATE_NOTE.md)
- [`WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md`](WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md)

Those later notes do **not** overturn this blocker on the off-center transport
surface. They show instead that:

- a centered non-oscillating core packet can separate attractive from
  repulsive parity coupling on the audited irregular families
- weak-coupling shell-force separation is stable on a broader low-`G` audited
  surface
- broader transport / packet portability beyond those narrower surfaces
  remains open
