# Lensing Adjoint Kernel Shape Compare

**Date:** 2026-04-09
**Status:** retained partial positive — on the retained reference setup
(`T_phys = 15`, `H = 0.25`, `BETA = 0.8`, Fam1, `b ∈ {3,4,5,6}`), the
normalized absolute adjoint kernel `|K_l|` changes only modestly across
impact parameter. Raw pairwise total-variation distances stay in
`0.024 .. 0.102`, the absolute-center span is only `0.496`, and the
absolute-width span is only `0.365`. So the retained `kubo_true(b) ≈ 28.4 ·
b^(-1.43)` law appears to live on a **quasi-fixed broad kernel** rather than
on a radically reshaping or ray-like response. Peak-aligned TV is not smaller
than raw TV, so this is **not** just a rigid translation of one kernel; there
is mild reshaping with `b`, but not enough to overturn the “broad nearly fixed
kernel” picture.

## Artifact chain

- [`scripts/lensing_adjoint_kernel_shape_compare.py`](../scripts/lensing_adjoint_kernel_shape_compare.py)
- [`logs/2026-04-09-lensing-adjoint-kernel-shape-compare.txt`](../logs/2026-04-09-lensing-adjoint-kernel-shape-compare.txt)
- Depends on:
  - [`docs/LENSING_ADJOINT_KERNEL_NOTE.md`](LENSING_ADJOINT_KERNEL_NOTE.md)
  - [`docs/LENSING_COMBINED_INVARIANT_NOTE.md`](LENSING_COMBINED_INVARIANT_NOTE.md)

## Question

After the exact adjoint-kernel lane established that the literal observable is
a broad detector-weighted wave response, the next mechanism question was:

> does the `≈ -1.43` slope come from sampling the same broad kernel against
> the changing `1/r_field(b)` factor, or from the kernel itself reshaping
> substantially as `b` moves from `3` to `6`?

This note freezes the first direct compare of normalized `|K_l|` across the
full retained slope-fit window.

## Setup

- `T_phys = 15`
- `H = 0.25`
- Fam1 geometry (`seed = 0`, `drift = 0.20`, `restore = 0.70`)
- `BETA = 0.8`
- `b ∈ {3,4,5,6}`

For each `b`, the script computes:

- the exact adjoint-weighted layer kernel `K_l`
- the normalized absolute profile `|K_l| / Σ|K_l|`
- moment summaries (peak, absolute center, absolute width, left/right split)
- pairwise total-variation distances on the normalized profiles

Two TV distances are reported:

- **raw TV**: compare the normalized `|K_l|` profiles directly
- **peak-aligned TV**: shift each profile so its peak layer is at zero, then compare

Interpretation:

- small raw TV: the kernel barely changes with `b`
- raw TV much larger than peak-aligned TV: mostly one broad kernel translating downstream
- peak-aligned TV still comparable to raw TV: mild real reshaping, not just translation

## Result

### Per-`b` summary

| `b` | peak `x` | abs-center | abs-width | `|K|` in `[x_src±5]` | left/right abs split |
| ---: | ---: | ---: | ---: | ---: | --- |
| `3` | `5.250` | `6.266` | `3.508` | `0.836` | `0.43 / 0.61` |
| `4` | `5.250` | `6.459` | `3.666` | `0.812` | `0.41 / 0.62` |
| `5` | `5.250` | `6.626` | `3.786` | `0.791` | `0.40 / 0.62` |
| `6` | `4.500` | `6.763` | `3.873` | `0.773` | `0.39 / 0.63` |

### Pairwise normalized `|K_l|` distances

| pair | raw TV | peak-aligned TV |
| --- | ---: | ---: |
| `3.0-4.0` | `0.045` | `0.045` |
| `3.0-5.0` | `0.078` | `0.078` |
| `3.0-6.0` | `0.102` | `0.147` |
| `4.0-5.0` | `0.034` | `0.034` |
| `4.0-6.0` | `0.058` | `0.111` |
| `5.0-6.0` | `0.024` | `0.083` |

### Range summary

- abs-center range: `6.266 .. 6.763` (span `0.496`)
- abs-width range: `3.508 .. 3.873` (span `0.365`)
- `|K|` in `[x_src±5]`: `0.773 .. 0.836` (span `0.064`)

## Interpretation

Three facts are now retained:

1. **The broad kernel is nearly fixed across `b`.**
   Raw TV stays below `0.11` for every pair, and for adjacent `b` values it is
   only `0.024 .. 0.045`. The kernel is not radically reshaping across the
   four-point slope-fit window.

2. **The broad kernel is not just rigidly translating.**
   Peak-aligned TV is not smaller than raw TV; for the `b=6` comparisons it is
   actually larger. So the kernel does not simply slide downstream with `b`.
   There is genuine mild reshaping.

3. **The right mechanism picture is now narrower.**
   The exponent `≈ -1.43` appears to come from sampling a **quasi-fixed broad
   detector-weighted kernel** against the `b`-dependent field factor, with a
   secondary contribution from mild kernel reshaping. That is much closer to a
   wave-mechanical Kubo picture than to any ray-optics story.

What this does **not** do:

- it does not derive the exponent analytically
- it does not show family portability of the kernel shape
- it does not test `k`-dependence or `BETA`-dependence of the shape itself

## What changes

This lane upgrades the mechanism story from:

- “the exact observable is broad and post-mass-skewed at one `b`”

to:

- “the exact observable stays broad and only mildly reshapes across the full
  retained `b` window that produces the `≈ -1.43` slope”

That is the first direct evidence that the combined invariant note’s
`28.4 · b^(-1.43)` law is living on a stable response kernel rather than on a
sequence of unrelated shapes.

## Best next move

The next clean mechanism steps are now:

1. derive the `b`-dependence from the full adjoint kernel, not from a ray model
2. run the planned `k` sweep on the retained slope to see whether the kernel
   shape or just the prefactor changes
3. test whether the same quasi-fixed-kernel picture survives a family sweep

No more `beta`, `T`, or `b`-window rescue attempts are warranted.

## Bottom line

> "Across the full retained slope-fit window `b ∈ {3,4,5,6}` at the
> reference setup (`T_phys = 15`, `H = 0.25`, `BETA = 0.8`), the normalized
> absolute adjoint kernel changes only modestly: raw pairwise TV is
> `0.024 .. 0.102`, the absolute-center span is `0.496`, the absolute-width
> span is `0.365`, and the fraction of `|K|` inside `[x_src±5]` only moves by
> `0.064`. So the retained `kubo_true(b) ≈ 28.4 · b^(-1.43)` law appears to
> live on a quasi-fixed broad detector-weighted kernel, not on a localized
> kick or a radically reshaping response. Peak-aligned TV is not smaller than
> raw TV, so the kernel is not merely translating; there is mild reshaping with
> `b`. This does not derive the exponent, but it sharply narrows the mechanism:
> the lensing fingerprint belongs to a broad wave-mechanical Kubo response,
> not to ray optics."
