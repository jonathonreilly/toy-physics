# Exact Quotient-Distinct Same-Boundary Surface Engine on the `3+1` Plaquette Surface

**Date:** 2026-04-16  
**Status:** exact quotient counting theorem through five `3`-cells  
**Script:** `scripts/frontier_quotient_surface_engine.py`

## Question

Once rooted fillings are quotiented by exact `4`-cube boundary moves, what are
the actual physical anchored surfaces through the first five rooted levels?

## Exact answer

The raw rooted engine was counting fillings, not surfaces.

After quotienting by the exact same-boundary relation from
`docs/CUBICAL_QUOTIENT_THEOREM_NOTE.md`, the counted object is the distinct
anchored surface

`S = q + dV`.

The quotient engine shows:

1. the raw rooted counts are physical through `n = 3`
2. the first overcount appears exactly at `n = 4`
3. every quotient collision through `n = 5` is a simple pair differing by one
   unit `4`-cube boundary

## Theorem 1: exact quotient counts through `n = 5`

Let `Q(n, F)` be the number of quotient-distinct connected rooted surfaces with

- rooted filling size `|V| = n`
- `q in dV`
- boundary size `F = |dV|`

Then the exact quotient counts are:

- `n = 1`:
  - `Q(1, 6) = 4`
- `n = 2`:
  - `Q(2, 10) = 60`
- `n = 3`:
  - `Q(3, 12) = 64`
  - `Q(3, 14) = 1036`
  - `Q(3, 16) = 64`
- `n = 4`:
  - `Q(4, 12) = 16`
  - `Q(4, 14) = 56`
  - `Q(4, 16) = 2216`
  - `Q(4, 18) = 20292`
  - `Q(4, 20) = 2340`
- `n = 5`:
  - `Q(5, 12) = 64`
  - `Q(5, 14) = 56`
  - `Q(5, 16) = 512`
  - `Q(5, 18) = 4176`
  - `Q(5, 20) = 67840`
  - `Q(5, 22) = 421432`
  - `Q(5, 24) = 68832`
  - `Q(5, 26) = 884`

## Theorem 2: the first raw overcount is exactly at `n = 4`

Comparing raw rooted fillings to quotient-distinct surfaces gives:

- `n = 1`: `4 -> 4`
- `n = 2`: `60 -> 60`
- `n = 3`: `1164 -> 1164`
- `n = 4`: `25000 -> 24920`
- `n = 5`: `566644 -> 563796`

So the first raw overcount is exactly

`25000 - 24920 = 80`

at `n = 4`.

At `n = 5` the removed hidden-filling multiplicity is

`566644 - 563796 = 2848`.

## Theorem 3: every quotient collision through `n = 5` is a simple pair

The exact duplicate-class histograms are:

- `n = 4`: `{2: 80}`
- `n = 5`: `{2: 2848}`

So every quotient collision through `n = 5` is a multiplicity-`2` pair.

Moreover the exact duplicate launch-sector histogram on both levels is:

`{((1, 2),): ...}`

meaning each duplicate class consists of two raw representatives, both in the
`k = 1` root-launch sector.

The runner checks a sample duplicate pair at both `n = 4` and `n = 5` and in
each case finds the exact difference to be one unit `4`-cube boundary.

## Corollary: the first connected area-`5` theorem is unchanged by the quotient

The first nonlocal connected correction came from the `n = 1` area-`5` sector.

That sector is unchanged:

- raw count `= 4`
- quotient count `= 4`

So the exact coefficient

`1 / 472392`

survives the quotient unchanged.

The quotient begins only after that first exact constructive theorem.

## Exact formal quotient count generator through `n = 5`

If one records only the exact quotient-distinct surface counts, the resulting
formal count series is

`G_surface_partial(p) = 1`
`+ 4 p^4`
`+ 60 p^8`
`+ 144 p^10`
`+ 1148 p^12`
`+ 2792 p^14`
`+ 24468 p^16`
`+ 70180 p^18`
`+ 421432 p^20`
`+ 68832 p^22`
`+ 884 p^24`.

This is an exact combinatorial quotient-series. It is **not yet** an exact
finite-`beta` plaquette formula.

## Why this matters

This note closes the physical counting object.

The branch now knows exactly:

1. what should be counted
2. when the raw rooted engine first overcounts it
3. how large that overcount is through `n = 5`

So the remaining gauge problem is no longer “what is the right surface
quotient?” It is “what is the exact finite-`beta` activity law on that
quotient-distinct surface gas?”

The next exact obstruction on that route is now
`docs/QUOTIENT_SURFACE_TRANSFER_NO_GO_NOTE.md`, which proves that the quotient
surface key itself is not a sufficient rooted transfer state.

## Honest status

This note does **not** yet derive analytic `P(6)`.

What it closes exactly is the geometric counting step:

1. the physical anchored objects are quotient-distinct same-boundary surfaces
2. the raw rooted engine first overcounts them at `n = 4`
3. that overcount is completely explicit through `n = 5`

The next note isolates the remaining gap:

- `docs/ANCHORED_SURFACE_GAS_ROUTE_NOTE.md`

## Commands run

```bash
python3 scripts/frontier_quotient_surface_engine.py
```

Output summary:

- raw and quotient counts agree through `n = 3`
- first quotient collision at `n = 4`
- exact hidden-filling removals: `80` at `n = 4`, `2848` at `n = 5`
- every duplicate class through `n = 5` is a simple pair with a one-cube
  witness
