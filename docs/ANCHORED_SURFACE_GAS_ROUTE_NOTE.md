# Quotient-Surface Gas Route at `beta = 6`

**Date:** 2026-04-16  
**Status:** exact quotient object + exact finite-lattice law + exact occupation compression  
**Script:** `scripts/frontier_anchored_surface_gas_route.py`

## Question

After the cubical quotient theorem and the quotient surface engine, do we now
have a closed analytic plaquette at the fixed physical point `beta = 6`?

## Exact answer

Yes at the exact finite-periodic-lattice law level.

The branch now knows the correct exact geometric object:

> the quotient-distinct connected anchored same-boundary surface gas.

`docs/CHARACTER_INTERTWINER_FOAM_LAW_NOTE.md` closes the missing finite-`beta`
law on the same finite periodic evaluation surface: the plaquette is an exact
absolutely convergent character/intertwiner foam ratio.

What is still missing is a faster evaluator for that exact law.

The first exact piece of that weight law is now carved out in
`docs/FUNDAMENTAL_DISK_ACTIVITY_THEOREM_NOTE.md`: the local anchor
`p = P_1plaq(6)` is the exact normalized fundamental character coefficient, and
the isolated simply-sheeted disk sector through `n <= 5` has exact activity
`p^A`.

## Exact fixed inputs

This route freezes the already-established physical point:

`beta = 6`.

Its exact local anchor is the one-plaquette block:

`p = P_1plaq(6) = 0.422531739649983`.

The canonical same-surface plaquette currently carried elsewhere is:

`<P> = 0.5934`.

## Exact quotient-surface object

From `docs/CUBICAL_QUOTIENT_THEOREM_NOTE.md` and
`docs/QUOTIENT_SURFACE_ENGINE_NOTE.md`, the exact geometric object is the
anchored quotient class

`[S] = [q + dV]`.

So the analytic plaquette route is no longer a rooted-filling problem.
It is a quotient-surface gas problem.

## Quotient count series through `n = 5`

The earlier level-by-level quotient surface series slightly overcounted
surfaces that reappear at multiple rooted filling sizes. The exact cross-level
duplicate polynomial in the current window is

`64 p^10 + 56 p^12`.

So the exact **unique** quotient surface series through `n = 5` is

`G_surface_unique^(n<=5)(p) = 1`
`+ 4 p^4`
`+ 60 p^8`
`+ 80 p^10`
`+ 1092 p^12`
`+ 2792 p^14`
`+ 24468 p^16`
`+ 70180 p^18`
`+ 421432 p^20`
`+ 68832 p^22`
`+ 884 p^24`.

For comparison, the old level-by-level quotient series was exactly

`G_surface_level(p) = G_surface_unique(p) + 64 p^10 + 56 p^12`.

So the exact direct route is now cleaner than before: there is a unique
quotient-surface series, a disk subsector inside it, and a separate
non-disk / higher-sheet remainder.

## Formal local-block substitution at the physical point

If one makes the **formal but not yet fully proved** substitution on the full
unique quotient series

`activity([S]) = p^(|S|-1)`,

then at `beta = 6` the partial sums through `n = 5` are:

- raw rooted formal partial:
  - `H_raw_partial = 1.330208557468936`
  - `P_raw_partial = 0.562055335884644`
- unique quotient-surface formal partial:
  - `H_surface_unique_partial = 1.306925044135047`
  - `P_surface_unique_partial = 0.552217312490512`

So removing quotient overcounting and hidden fillings changes the formal partial
value by

`0.009838023394131`.

The formal unique quotient partial is still below the canonical same-surface
value by

`0.041182687509488`.

## What is now exact, and what is not

### Exact now

1. `beta = 6` as the fixed physical point for this package
2. the local anchor `p = P_1plaq(6)`
3. the quotient-distinct connected anchored surface object
4. the unique quotient count series through `n = 5`
5. the exact finite-periodic-lattice character/intertwiner foam law
6. the exact no-go against any exact small finite `B/X` low-carrier closure
7. the exact Poissonized occupation/intertwiner compression with finite local
   alphabets `Omega_K` and explicit truncation tails
8. the exact Poissonized link-channel compression with finite local link
   alphabets `Lambda_K`

### Still not exact on the compressed route

The branch does **not** yet have a fast evaluator that turns the exact
compressed law into the final canonical number without a heavy non-perturbative
summation.

`docs/FIRST_NONDISK_Z3_LIFT_THEOREM_NOTE.md` now sharpens that gap again:
the first genuine non-disk window at `p^14` is **not** carried by a pure
fundamental-sheet lift on the quotient surface alone. Exactly `52` of the first
`72` non-disk surfaces admit no pure fundamental `Z_3` face-orientation lift.

`docs/FIRST_NONDISK_CHARACTER_FOAM_THEOREM_NOTE.md` sharpens it once more:
even the minimal plaquette-character face alphabet `{3, 3bar, 8}` carries only
the `20` genus/crossing surfaces and still misses the `52` singular surfaces.

`docs/FINITE_BX_LOW_CARRIER_NO_GO_NOTE.md` closes the last finite-compression
hope:

> the exact one-plaquette Wilson weight already has infinitely many strictly
> positive symmetric-representation coefficients, so no exact finite face
> alphabet, and therefore no exact small finite `B/X` low-carrier closure, can
> reproduce the full law.

`docs/POISSONIZED_OCCUPATION_INTERTWINER_COMPRESSION_NOTE.md` now closes the
plaquette-state representation gap:

> the exact infinite-carrier law admits an exact Poissonized plaquette
> occupation/intertwiner compression with countable local states and finite
> local alphabets `Omega_K` after truncation.

`docs/POISSONIZED_LINK_CHANNEL_COMPRESSION_NOTE.md` then closes the remaining
local link-state gap:

> for every truncation `K`, the exact local link tensor lives on a finite
> channel alphabet `Lambda_K` built from the invariant spaces
> `Inv(3^(⊗r) ⊗ 3bar^(⊗s))`.

So the remaining missing object on the compressed route is now more precise:

> a faster contraction/evaluation scheme for that already exact finite-state
> tensor network.

## Why this matters

This note now separates the finish line into two levels:

1. exact law on the full finite periodic lattice: closed
2. exact small finite low-carrier quotient-foam compression: impossible
3. exact useful resummed/state-compressed occupation law: closed
4. exact finite local link-channel compression: closed
5. faster exact evaluator for that finite-state tensor network: still open

The remaining compression gap is no longer:

- the constant-lift ansatz
- the rooted transfer object
- the local directed-cell closure
- the one-shell face-state summary
- the raw filling quotient

It is now only:

> finding a faster exact way to contract the already compressed finite-state
> tensor network.

That is a materially cleaner target than the branch had before the quotient
package.

There is one important extra sharpness now recorded in
`docs/QUOTIENT_SURFACE_TRANSFER_NO_GO_NOTE.md`:

> the quotient surface key is the right physical polymer label, but it is not a
> sufficient rooted transfer state.

So any exact closure must either work directly at the non-rooted surface-gas
level or retain extra hidden-filling state in any rooted recursion.

The first exact evidence that such an enriched rooted state may be finite is now
recorded in `docs/HIDDEN_SHELL_CHANNEL_THEOREM_NOTE.md`: at the first hidden
quotient layer, the extra rooted data reduces to a finite local cube-shell
alphabet rather than an unstructured memory term. The exact next propagation
result is now `docs/HIDDEN_TWO_SHELL_PROPAGATION_THEOREM_NOTE.md`: the first
rooted image of that hidden sector is still local, but it lifts to an exact
two-shell sector rather than closing on the bare `12`-state one-shell alphabet.
That second layer is now itself exact and finite in
`docs/HIDDEN_TWO_SHELL_CHANNEL_THEOREM_NOTE.md`: the propagated two-shell
sector collapses to a finite but much richer local alphabet:
`226` ordered local orbits / `121` unordered pair-orbits with `184` distinct
exact one-step transfer histograms.

## Honest status

This note now supports the exact same-surface law, but it does **not** yet
promote a compact low-carrier closure for canonical `P`.

It records the strongest exact/fair statement available now:

1. the quotient-surface gas is the correct exact geometric object
2. its exact unique combinatorial series is known through `n = 5`
3. the isolated simply-sheeted disk sector now has an exact finite-`beta`
   activity law through `n <= 5`
4. the full finite periodic lattice now has an exact absolutely convergent
   character/intertwiner foam law
5. the exact unique quotient-surface sector is separated from the small
   cross-level duplicate artifact in the current window
6. the first genuine non-disk window now has an exact `Z_3` lift split:
   `20/72` surfaces admit a pure fundamental lift and `52/72` do not
7. the first genuine non-disk window now has an exact character-foam split:
   the minimal plaquette-character face alphabet `{3, 3bar, 8}` carries the
   `20` genus/crossing surfaces and misses the `52` singular surfaces, whose
   exact first defect signatures are `B^1X^3` and `B^4`
8. the rooted hidden sector now has an exact finite local shell hierarchy for
   its first two layers, with explicit one-step transfer data on both, but the
   second layer is already combinatorially large
9. the full exact law does not compress to any exact small finite `B/X`
   low-carrier closure
10. the full exact law does admit an exact Poissonized
    occupation/intertwiner compression with finite local alphabets `Omega_K`
    and explicit truncation tails
11. the truncated exact law also admits finite local link-channel alphabets
    `Lambda_K` built from invariant spaces `Inv(3^(⊗r) ⊗ 3bar^(⊗s))`
12. a faster exact evaluator for that finite-state tensor network is still open

## Commands run

```bash
python3 scripts/frontier_anchored_surface_gas_route.py
```

Output summary:

- exact quotient series through `n = 5`
- formal local-block substitution at `beta = 6`
- formal quotient partial `0.552217312490512`
- exact finite-periodic-lattice law
- exact no-go against small finite `B/X` low-carrier closure
- exact Poissonized occupation/intertwiner compression
- exact Poissonized link-channel compression
- remaining fast-evaluator gap identified
