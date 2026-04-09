# Next Chunk Recommendation

**Date:** 2026-04-08  
**Status:** working recommendation after the direct-`dM` seed-`0` closure and the overnight continuum/Kubo downgrades

The next highest-value chunk is:

> `Fam1`, seed `1`, `H = 0.25` control ladder on the direct-`dM` lane.

## Why this is the top chunk

- It is the last missing same-resolution control point in the fine-`H`
  direct-`dM` surface.
- It closes the first-family pair under the same control stack that already
  hardened `Fam2`.
- It has the best ratio of information to runtime among the options still
  producing a new retained science result.

## Comparison

1. `Fam1 seed1 H=0.25` control ladder.
   - Highest immediate value.
   - Expected to tell us whether the first-family pair is fully controlled or
     whether the weak-branch surface still has a first-family exception.

2. Waiting for the exact comparator.
   - Highest long-run leverage on the wave-retardation magnitude story.
   - Not the best next chunk right now because it is infrastructure-heavy and
     does not itself create a new retained science point until the solver
     lands.

3. `dM(v)` at `H = 0.20`.
   - Useful as a refinement check.
   - Lower priority because the lane is already a retained negative at
     `H = 0.25`; this would mostly sharpen a downgraded claim rather than
     open a new one.

4. Born derivation write-up.
   - Cheap and worth doing eventually.
   - Lowest marginal scientific upside of the four because it is mostly
     documentation/derivation hygiene, not a new retained observable.

## Honest read

If we want one active chunk now, do `Fam1 seed1 H=0.25`.

If we want the biggest theoretical upside after that, the next chunk is the
exact comparator work, not more `dM(v)` refinement and not the Born write-up.

That keeps the current program ordered by return:

- first close the direct-`dM` family pair
- then push the exact comparator on the continuum lane
- keep `dM(v)` and Born work as secondary hardening

