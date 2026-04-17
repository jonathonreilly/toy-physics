# DM Neutrino Two-Higgs Right-Gram Bridge Theorem

**Date:** 2026-04-15  
**Status:** exact positive bridge theorem on the canonical local two-Higgs
neutrino lane  
**Script:** `scripts/frontier_dm_neutrino_two_higgs_right_gram_bridge.py`

## Question

The DM denominator lane now knows the exact missing algebraic target:

- the current exact weak-axis `1+2` split lifts to the even circulant slice
  `mu I + nu(S + S^2)`
- that slice is still CP-degenerate
- the minimal exact `Z_3`-covariant extension that can support nonzero
  leptogenesis CP is the odd circulant direction `i(S - S^2)`

But is that odd-circulant object genuinely new and foreign to the local
neutrino atlas, or can the canonical neutrino two-Higgs lane already realize
it?

## Bottom line

It can, but only on an exact admissible subcone.

On the canonical local two-Higgs lane

`Y = diag(x_1,x_2,x_3) + diag(y_1,y_2,y_3 e^{i delta}) C`,

the right-Gram matrix `K = Y^dag Y` has the exact one-phase Hermitian form

```text
[ x_1^2 + y_3^2        x_1 y_1             x_3 y_3 e^{-i delta} ]
[ x_1 y_1              x_2^2 + y_1^2       x_2 y_2              ]
[ x_3 y_3 e^{i delta}  x_2 y_2             x_3^2 + y_2^2        ]
```

Any Hermitian circulant target is rephasing-equivalent to the canonical gauge

```text
K_can(d,r,delta) =
[ d  r  r e^{-i delta} ]
[ r  d  r              ]
[ r e^{i delta}  r  d  ]
```

with

- `d` the common diagonal entry
- `r = |h|` the common off-diagonal modulus
- `delta = arg(h^3)` the gauge-invariant triangle phase

The theorem is:

> the canonical two-Higgs lane realizes that circulant target if and only if
> `d >= 2 r`

So the local neutrino two-Higgs lane already contains the DM CP-supporting
odd-circulant family on an exact admissible subcone. It does **not** realize
the whole family automatically.

## Inputs

This note combines:

- the DM-side odd-circulant target from
  [DM_NEUTRINO_Z3_CIRCULANT_CP_TOOL_NOTE_2026-04-15.md](./DM_NEUTRINO_Z3_CIRCULANT_CP_TOOL_NOTE_2026-04-15.md)
- the canonical local two-Higgs neutrino lane from the local neutrino branch
- the right-sensitive / right-Gram perspective already isolated on the PMNS
  side

The point here is not PMNS closure. It is a DM-side bridge: can the same local
two-Higgs lane carry the right-Gram structure leptogenesis actually uses?

## Exact right-Gram law on the canonical two-Higgs lane

Let

`C = [[0,1,0],[0,0,1],[1,0,0]]`.

Then

`Y = D_x + D_y C`

with

- `D_x = diag(x_1,x_2,x_3)`
- `D_y = diag(y_1,y_2,y_3 e^{i delta})`

gives

`K = Y^dag Y`

exactly as

```text
[ x_1^2 + y_3^2        x_1 y_1             x_3 y_3 e^{-i delta} ]
[ x_1 y_1              x_2^2 + y_1^2       x_2 y_2              ]
[ x_3 y_3 e^{i delta}  x_2 y_2             x_3^2 + y_2^2        ]
```

So the local two-Higgs lane already carries:

- three diagonal right-Gram entries
- three off-diagonal moduli
- one rephasing-invariant phase

This is exactly the kind of non-universal right-Gram structure the universal
Yukawa no-go said was missing on the old DM lane.

## Canonical gauge for the circulant target

The DM odd-circulant family induces a Hermitian circulant right-Gram matrix
with first row

`(d, h, h^*)`.

By a diagonal generation rephasing

`P = diag(1, e^{i theta}, e^{i 2 theta})`

with `theta = arg(h)`, this becomes

```text
[ d  r  r e^{-i delta} ]
[ r  d  r              ]
[ r e^{i delta}  r  d  ]
```

with

- `r = |h|`
- `delta = 3 theta = arg(h^3)`

So the odd-circulant DM target is compared naturally against the canonical
two-Higgs gauge with one surviving phase.

## Exact realization criterion

To realize the circulant target on the canonical two-Higgs lane we must have

- `x_1 y_1 = x_2 y_2 = x_3 y_3 = r`
- `x_1^2 + y_3^2 = x_2^2 + y_1^2 = x_3^2 + y_2^2 = d`

Write `t_i = x_i^2`. Then `y_i = r / x_i` and the diagonal equalities become

- `t_2 = F(t_1)`
- `t_3 = F(t_2)`
- `t_1 = F(t_3)`

for the map

`F(t) = d - r^2 / t`.

Since `F` is strictly increasing on `t > 0`, an ordered triple
`t_1 <= t_2 <= t_3` implies

`t_2 <= t_3 <= t_1`,

so all three are equal:

`t_1 = t_2 = t_3 = t`.

Therefore the circulant target is realized only on the symmetric local slice

- `x_1 = x_2 = x_3 = x`
- `y_1 = y_2 = y_3 = y`

with

- `d = x^2 + y^2`
- `r = x y`

So a real solution exists iff

`d^2 - 4 r^2 >= 0`,

equivalently

`d >= 2 r`.

This is the exact admissible subcone.

## Application to the DM odd-circulant family

For

`Y_CP = mu I + nu(S + S^2) + i eta(S - S^2)`,

the induced right-Gram matrix `K_CP = Y_CP^dag Y_CP` is Hermitian circulant.
Its canonical-gauge parameters obey the exact discriminant

`Delta = d^2 - 4 r^2`

and on this family

`Delta = -mu (mu - 4 nu) (12 eta^2 - mu^2 - 4 mu nu - 4 nu^2)`.

So the canonical two-Higgs lane contains the DM odd-circulant family exactly
on the subcone `Delta >= 0`.

The runner shows three useful regimes:

1. **Admissible generic point.**
   A generic odd-circulant CP-supporting point with `Delta > 0` is realized
   exactly by the symmetric two-Higgs slice.

2. **Forbidden point.**
   A generic odd-circulant point with `Delta < 0` is excluded exactly.

3. **Current benchmark boundary point.**
   The current DM sample choice `(mu, nu, eta) = (1, 0.25, 0.17)` sits on the
   exact boundary `Delta = 0`, where the two-Higgs realization collapses to
   `x = y`.

That benchmark point is only a sample from the current DM tool, not a derived
framework value. The theorem point is the existence criterion itself.

## What this closes

This is a real positive bridge for DM.

It closes the old vague blocker phrase

> find some non-universal neutrino Dirac flavor texture somehow

into a much sharper statement:

- the needed CP-supporting right-Gram structure is not foreign to the local
  neutrino atlas
- the canonical two-Higgs neutrino lane already contains it on an exact
  admissible subcone

So the remaining DM blocker is no longer “invent a flavor mechanism from
scratch.”

It is now:

1. derive or justify the local two-Higgs neutrino extension on the retained
   axiom surface
2. derive its right-sensitive seven quantities / residual sheet
3. show that the resulting right-Gram lands in the CP-admissible subcone
   `d >= 2 r`
4. then compute the full leptogenesis kernel on that exact branch

## What this does not close

This note does **not** derive:

- the two-Higgs extension itself from the current retained bank
- the seven two-Higgs quantities
- the residual right-sensitive sheet datum
- the exact odd-circulant coefficient from the axiom
- full zero-import `eta`

So DM is still not fully closed. But the theorem target is much narrower now.

## Safe wording

**Can claim**

- the local neutrino two-Higgs lane is a real positive DM bridge
- the exact DM odd-circulant CP-supporting family is realized on that lane on
  the exact admissible subcone `d >= 2 r`
- the current DM blocker is now the derivation/selection of that two-Higgs
  branch and its parameters, not the existence of any CP-supporting texture at
  all

**Cannot claim**

- the current retained bank already derives the two-Higgs branch
- the full leptogenesis kernel is now closed
- DM is fully derived with zero imports

## Command

```bash
python3 scripts/frontier_dm_neutrino_two_higgs_right_gram_bridge.py
```
