# Area-Law Multipocket Selector No-Go Note

**Date:** 2026-04-25
**Status:** residual no-go for Planck Target 2
**Runner:** `scripts/frontier_area_law_multipocket_selector_no_go.py`

## Purpose

The retained Widom no-go already says the current half-filled NN carrier gives
`c_Widom = 1/6`, not `1/4`. It also notes that one can invent a multi-pocket
Fermi surface whose projected-width integral gives `1/4`.

This note closes that residual loophole as a framework claim. A multi-pocket
carrier can be calibrated to `1/4`, but the calibration is equivalent to adding
a new pocket-measure or sector-weight selector. The retained `Cl(3)/Z^3`
primitive boundary count does not supply that selector.

## Safe statement

For a straight cut normal to `e_x`, the free-fermion Widom coefficient can be
written as

```text
c_Widom = <N_x> / 12,
```

where `<N_x>` is the Brillouin-zone average number of Fermi-surface crossings
along a `k_x` fiber. Therefore

```text
c_Widom = 1/4    iff    <N_x> = 3.
```

For a scalar band with ordinary interval fibers, `N_x(q)` is even almost
everywhere. Thus `<N_x> = 3` cannot be a full-pocket integer degeneracy. It
requires either:

1. a partial transverse pocket of exactly selected measure, or
2. a direct-sum/Schur sector weight tuned so that the normalized convex average
   equals `1/4`.

Both are extra selectors. They are not the same datum as

```text
Tr((I_16/16) P_A) = 4/16 = 1/4.
```

## Minimal multipocket calibration

Let the normalized transverse Brillouin measure be `1`. Take a baseline
simple pocket with one occupied `k_x` interval for every transverse momentum,
and add a second interval only on a transverse subset `Q` of normalized measure
`mu`. Then

```text
<N_x> = 2(1 + mu),
c_Widom(mu) = (1 + mu) / 6.
```

The Bekenstein-Hawking value requires

```text
(1 + mu) / 6 = 1/4
mu = 1/2.
```

So the exact result is not produced by the existence of multipockets alone. It
is produced by selecting the transverse measure `mu = 1/2`.

Changing `mu` gives a continuous family:

```text
mu = 0       -> c_Widom = 1/6,
mu = 1/2     -> c_Widom = 1/4,
mu = 1       -> c_Widom = 1/3.
```

The exact quarter is therefore a codimension-one condition in the residual
Widom class.

## Direct-sum calibration

A Schur/direct-sum stack can also hit `1/4` if it combines, for example, a
`c=1/6` simple-fiber block and a `c=1/3` two-interval block with exactly equal
boundary-rank weights:

```text
(1/6 + 1/3) / 2 = 1/4.
```

But this is again a selector: the exact equality of the weights is not forced
by the existing primitive boundary count. Species duplication by itself does
not help; it leaves the normalized coefficient unchanged when the boundary
rank is counted consistently.

## Why this is not Target 2 closure

The Planck conditional packet derives `1/4` from a specific finite primitive
trace:

```text
H_cell ~= C^16,
rank(P_A) = 4,
c_cell = Tr((I_16/16) P_A) = 1/4.
```

The multipocket Widom calibration derives `1/4` from a different statement:

```text
average Fermi-surface crossing number along the cut normal = 3.
```

Those statements are not equivalent. A bridge theorem would need to derive the
crossing-number or sector-weight selector from the same primitive boundary
semantics. Without that theorem, the multipocket construction is only a tuned
comparison carrier.

## Relation to gapped carriers

The same caution applies to the gapped route. Brandao-Horodecki-style
mass-gap or exponential-correlation results can justify an area law, but they
do not determine the exact ultraviolet entropy per primitive face. A gapped
horizon/edge carrier would still need a separate theorem deriving its
per-face entropy from the `16`-state primitive boundary count.

## What remains open

This note does not rule out a future positive result. It narrows what such a
result must prove:

1. derive a multipocket transverse-measure law, such as `mu = 1/2`, from the
   retained `Cl(3)/Z^3` primitive structure; or
2. derive a Schur/edge sector-weight law fixing the required convex average;
   or
3. construct a gapped horizon carrier whose leading area coefficient is
   literally the primitive trace `Tr((I_16/16)P_A)`.

Absent one of those selector laws, the residual multipocket Widom route is not
a physical derivation of Bekenstein-Hawking. It is a parameterized family that
can be made to contain the desired number.

## Package wording

Safe wording:

> Multi-pocket Widom carriers can be calibrated to `c_Widom = 1/4`, but only by
> imposing an additional pocket-measure or sector-weight selector. The retained
> `Cl(3)/Z^3` primitive boundary count does not yet derive that selector, so
> the multipocket route remains open only as a sharply specified residual
> target.

Unsafe wording:

> A constructed multipocket Fermi surface closes the Planck entropy carrier.

## Verification

Run:

```bash
python3 scripts/frontier_area_law_multipocket_selector_no_go.py
```

The runner checks the crossing-number formula, the minimal `mu=1/2`
calibration, instability under `mu` perturbations, the full-pocket integer
degeneracy obstruction, the direct-sum weight selector, and the separation
between Widom crossing data and the primitive `4/16` trace.

Current output:

```text
SUMMARY: PASS=22  FAIL=0
```
