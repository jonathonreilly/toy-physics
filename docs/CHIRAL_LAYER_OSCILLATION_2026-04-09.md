# Chiral Walk Layer Oscillation — Gravity Sign Depends on N

**Date:** 2026-04-09
**Status:** Diagnosed, not resolved
**Primary runner:** scripts/frontier_chiral_layer_oscillation.py

## Finding

The chiral walk's gravity sign oscillates with the number of propagation layers N:

```
N=12: TOWARD (+2.63e-4)
N=14: TOWARD (+4.08e-4)
N=16: AWAY   (-2.55e-5)  ← the n=15 script's N
N=18: AWAY   (-4.03e-4)
N=20: AWAY   (-4.46e-4)
```

Tested on 3+1D (n=15, periodic BC, θ₀=0.3, strength=5e-4, mass at z=10).

## Impact

This explains the n=9 vs n=15 discrepancy: n=9 used N=12 (TOWARD),
n=15 used N=16 (AWAY). The lattice size was irrelevant — the layer
count determined the sign.

This also means the 1+1D and 2+1D TOWARD results (10/10 closure cards)
used specific N values that happened to be in TOWARD windows. The cards
need to be checked across multiple N values.

## Root cause

The chiral walk has a built-in oscillation period related to the coin
angle θ. The coin mixes ψ₊ and ψ₋ with period ~π/θ layers. Near mass,
θ is modified to θ(1-f), creating a phase mismatch that accumulates
differently at different N. At some N values the accumulated mismatch
produces TOWARD; at others, AWAY.

This is the chiral walk's analog of the transfer matrix's k-dependent
resonance: instead of oscillating with wavenumber k, the chiral walk's
gravity oscillates with propagation distance N.

## Implication

The chiral walk does NOT produce universal gravity that's independent
of propagation distance. It produces N-dependent gravity — attractive
at some distances, repulsive at others. This is a fundamental property
of the architecture, not a boundary artifact.

The paper must frame this honestly: the chiral walk produces gravity
that oscillates with distance, not Newtonian 1/r gravity.

## Open question

Is there a coin design where gravity doesn't oscillate with N?
The oscillation comes from the θ-dependent mixing period. If θ is
chosen so that the mixing period matches the lattice spacing, the
oscillation might average out. Or a different coupling mechanism
(not θ-modulation) might avoid the oscillation entirely.
