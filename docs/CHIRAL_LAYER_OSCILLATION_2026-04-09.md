# Chiral Walk Layer Oscillation — Gravity Sign Depends on N

**Date:** 2026-04-09
**Status:** Diagnosed, not resolved
**Type:** bounded_theorem
**Primary runner:** scripts/frontier_chiral_layer_oscillation.py

## Finding

The chiral walk's gravity sign is not invariant in the number of
propagation layers `N`. The current frozen runner checks the canonical
3+1D chiral-walk implementation at `n=15`, periodic boundary conditions,
`theta0=0.3`, strength `5e-4`, and mass offset `+3`; it observes both
signs across the finite sweep:

```
N=12: AWAY   (-2.89e-5)
N=14: TOWARD (+1.04e-5)
N=16: AWAY   (-1.82e-6)
N=18: TOWARD (+3.83e-5)
N=20: TOWARD (+2.55e-5)
```

The older inline table reported different exact signs and magnitudes for
some `N` values. Treat those historical numbers as unfrozen provenance;
the durable source claim is the bounded sign-noninvariance check above.

## Impact

This narrows the earlier `n=9` versus `n=15` discrepancy story: layer
count is a real finite-window variable, but the current frozen replay
does not by itself ratify the older exact `N=12`/`N=16` explanation.

This also blocks treating single-`N` 1+1D and 2+1D TOWARD cards as
universal gravity evidence without the corresponding multi-`N` check.

## Root-cause hypothesis

The chiral walk has a built-in oscillation period related to the coin
angle θ. The coin mixes ψ₊ and ψ₋ with period ~π/θ layers. Near mass,
θ is modified to θ(1-f), creating a phase mismatch that accumulates
differently at different N. At some N values the accumulated mismatch
produces TOWARD; at others, AWAY.

This is the chiral walk's analog of the transfer matrix's k-dependent
resonance: instead of oscillating with wavenumber k, the chiral walk's
gravity oscillates with propagation distance N.

The runner verifies the sign-noninvariance diagnostic. It does not prove
the mechanism hypothesis in this section.

## Implication

On this finite operating slice, the chiral walk does NOT produce a
gravity proxy that is independent of propagation distance. It produces
`N`-dependent sign changes, so this card cannot be used as a universal
Newtonian-gravity surface.

The paper must frame this honestly: the chiral walk produces gravity
that oscillates with distance, not Newtonian 1/r gravity.

## Open question

Is there a coin design where gravity doesn't oscillate with N?
The oscillation comes from the θ-dependent mixing period. If θ is
chosen so that the mixing period matches the lattice spacing, the
oscillation might average out. Or a different coupling mechanism
(not θ-modulation) might avoid the oscillation entirely.
