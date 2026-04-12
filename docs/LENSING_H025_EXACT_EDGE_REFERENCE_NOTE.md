# Lensing H=0.25 Exact-Edge Reference

**Date:** 2026-04-10
**Status:** retained bounded reference — the retained `H=0.25`,
`T_phys=15`, Fam1 seed `0` lensing window now has one dedicated exact-edge
reference note. This does **not** add a new mechanism claim. It freezes the
exact table that downstream midpoint-binning, `k`-sweep, and family-shape
lanes should use as their baseline.

## Artifact chain

- [`scripts/lensing_adjoint_kernel_reduced_model.py`](../scripts/lensing_adjoint_kernel_reduced_model.py)
- [`logs/2026-04-08-lensing-adjoint-kernel-T15-H025-b3456.txt`](../logs/2026-04-08-lensing-adjoint-kernel-T15-H025-b3456.txt)
- [`docs/LENSING_ADJOINT_KERNEL_NOTE.md`](LENSING_ADJOINT_KERNEL_NOTE.md)
- [`docs/LENSING_ADJOINT_KERNEL_SHAPE_NOTE.md`](LENSING_ADJOINT_KERNEL_SHAPE_NOTE.md)

## Question

Before any midpoint-binned replay or retained-surface sweep, what exact
`H=0.25` edge-level reference object should be held fixed?

The intended baseline is

```text
exact_edge(b) = sum_e c_e / r_e(b)
```

on the retained surface:

- `T_phys = 15`
- `H = 0.25`
- Fam1 (`seed = 0`, `drift = 0.20`, `restore = 0.70`)
- `beta = 0.8`
- `b in {3,4,5,6}`

Here `c_e` is the fixed signed edge coefficient from the free propagator plus
detector adjoint, and all `b` dependence enters only through `r_e(b)`. This is
the exact edge-factorization object consumed by
`lensing_adjoint_kernel_reduced_model.py`.

## Reference table

The retained exact `H=0.25` adjoint-kernel replay already records the target
values on this surface:

| `b` | `exact_edge(b)` |
| ---: | ---: |
| `3` | `+5.986043` |
| `4` | `+3.819639` |
| `5` | `+2.826383` |
| `6` | `+2.211718` |

On these four points the reference fit is:

- `exact_edge(b) ≈ 28.505 * b^(-1.4335)`
- `R^2 = 0.9984`

So the exact-edge object reproduces the retained fine-`H` lensing law on the
same restricted `b = {3,4,5,6}` window.

## Why this is the right baseline

Two pieces of the existing artifact chain already pin down the reference:

1. [`logs/2026-04-08-lensing-adjoint-kernel-T15-H025-b3456.txt`](../logs/2026-04-08-lensing-adjoint-kernel-T15-H025-b3456.txt)
   freezes the exact `H=0.25` four-point values above on the retained surface.
2. [`docs/LENSING_ADJOINT_KERNEL_NOTE.md`](LENSING_ADJOINT_KERNEL_NOTE.md)
   already shows, on the same `T_phys = 15`, `H = 0.25`, `b = 3` reference
   setup, that the exact adjoint-kernel replay matches the retained
   `kubo_true` observable to machine precision.

That is enough to treat the four-point `exact_edge(b)` table as the baseline
reference object for downstream compression work. This note deliberately does
not widen to new `b`, new `H`, new families, or new `k`.

## What this changes

This closes one narrow prerequisite only:

- midpoint binning should now compare against this exact-edge table
- retained-surface `k` or family sweeps should start from this same baseline

What it does **not** change:

- no new derivation of the `-1.43` exponent
- no family-portability claim for kernel shape
- no reopening of broader lensing rescue branches

## Next move

The next honest lensing action is now the already-queued
`lensing-edge-binned-reduction-h025` lane:

> keep the exact-edge table above fixed, test one midpoint-binned signed
> `(x,z)` compression only, and report its error against this reference object.

## Bottom line

> "On the retained `T_phys = 15`, `H = 0.25`, Fam1 seed `0`,
> `b = {3,4,5,6}` surface, the exact baseline for downstream lensing
> reductions is the edge-factorization table
> `exact_edge(b) = {5.986043, 3.819639, 2.826383, 2.211718}`. This is a
> bounded reference freeze, not a new mechanism claim."
