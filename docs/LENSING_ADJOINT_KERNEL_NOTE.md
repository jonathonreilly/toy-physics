# Lensing Adjoint Kernel Probe — Why The Slope Is Not A Ray-Deflection Law

**Date:** 2026-04-08
**Status:** retained partial positive — the literal first-order lensing observable is now identified exactly as an **adjoint-weighted edge sum**, not a ray-angle integral. On the decisive fine setup (`H=0.25`, `b=3`), the exact layer kernel reproduces `kubo_true` to machine precision at both `T_phys=15` and `T_phys=7.5`, and the kernel is **broad and post-mass-skewed**, not a narrow kick at the mass plane. This does not fully explain the `≈ -1.43` slope yet, but it does explain why simple Fermat/ray formulas failed: the detector-centroid observable is a wave-mechanical, detector-weighted response distributed over many layers after the mass, not a local deflection angle.

## Artifact chain

- [`scripts/lensing_adjoint_kernel_probe.py`](../scripts/lensing_adjoint_kernel_probe.py)
- [`logs/2026-04-08-lensing-adjoint-kernel-T15-H025-b3.txt`](../logs/2026-04-08-lensing-adjoint-kernel-T15-H025-b3.txt)
- [`logs/2026-04-08-lensing-adjoint-kernel-T7p5-H025-b3.txt`](../logs/2026-04-08-lensing-adjoint-kernel-T7p5-H025-b3.txt)
- [`logs/2026-04-08-lensing-adjoint-kernel-T7p5-H025-b3-beta040.txt`](../logs/2026-04-08-lensing-adjoint-kernel-T7p5-H025-b3-beta040.txt)
- [`logs/2026-04-08-lensing-adjoint-kernel-T7p5-H025-b3-beta160.txt`](../logs/2026-04-08-lensing-adjoint-kernel-T7p5-H025-b3-beta160.txt)
- Depends on:
  - [`scripts/kubo_continuum_limit.py`](../scripts/kubo_continuum_limit.py)
  - [`docs/LENSING_LONG_PATH_TEST_NOTE.md`](LENSING_LONG_PATH_TEST_NOTE.md)

## Question

The finite-path rescue failed because the measured slope at `H=0.25`
is approximately the same at `T_phys=7.5` and `T_phys=15`, while any
ray-deflection formula must give an `L`-dependent slope.

That leaves the real question:

> what is the literal first-order observable that the code computes, and
> what does its spatial weighting look like?

If the response were a localized ray kick near the mass plane, the
Fermat picture would still be the right starting point. If the response
were broad and detector-weighted, then the ray picture is the wrong
observable from the start.

## The exact observable

In [`true_kubo_at_H`](../scripts/kubo_continuum_limit.py), the retained
first-order lensing response is:

```text
kubo_true = d(cz)/ds
          = (1/T0) Σ_det (z_j − cz_free) · 2 Re[A_j* B_j]
```

where:

- `A_j` is the free propagator amplitude
- `B_j = d(amp_j)/ds` is the first-order perturbation propagator
- `T0 = Σ_det |A_j|²`
- `cz_free = Σ_det z_j |A_j|² / T0`

This can be written as an exact **adjoint-weighted edge sum**:

```text
kubo_true = Σ_l K_l
K_l = 2 Re Σ_{edges i→j into layer l} λ_j · A_i · U_ij
```

with:

- free edge transfer:
  - `W_ij = exp(i k L_ij) · w_ij · h² / L_ij²`
- perturbation edge term:
  - `U_ij = W_ij · (−i k L_ij / r_field,ij)`
- reverse detector sensitivity:
  - detector slice seed:
    - `c_j = ((z_j − cz_free) / T0) · A_j*`
  - backward recurrence:
    - `λ_i = c_i + Σ_{i→j} W_ij · λ_j`

So the literal lensing observable is **not**:

- a pure angle integral
- a pure remaining-distance weighting
- a pure free-beam intensity weighting

It is a detector-weighted wave response that combines:

- forward free amplitude `A`
- edge perturbation `U`
- backward detector sensitivity `λ`

## Result

### Machine-precision identity check

For both tested runs, the exact layer sum matches the retained `kubo_true`
to machine precision:

| Setup | `Σ_l K_l` | `kubo_true` | `|Δ|` |
| --- | ---: | ---: | ---: |
| `T=15, H=0.25, b=3` | `+5.986043` | `+5.986043` | `4.6e-14` |
| `T=7.5, H=0.25, b=3` | `+2.455550` | `+2.455550` | `1.5e-14` |

So the probe is exact, not heuristic.

### Spatial shape of the kernel

#### `T_phys = 15`, `H = 0.25`, `b = 3`

- mass plane: `x_src = 5.00`
- detector plane: `x_det = 14.75`
- peak signed layer: `x = 5.25`
- absolute-kernel center: `x = 6.266`
- absolute-kernel width: `3.508`

Top signed layers:

```text
x=5.25:+6.310e-01  x=5.00:+5.403e-01  x=5.50:+4.566e-01
x=5.75:+3.666e-01  x=4.75:+3.401e-01  x=6.00:+3.031e-01
```

#### `T_phys = 7.5`, `H = 0.25`, `b = 3`

- mass plane: `x_src = 2.50`
- detector plane: `x_det = 7.25`
- peak signed layer: `x = 2.75`
- absolute-kernel center: `x = 3.655`
- absolute-kernel width: `1.832`

Top signed layers:

```text
x=2.75:+1.824e-01  x=3.00:+1.741e-01  x=3.25:+1.694e-01
x=3.50:+1.594e-01  x=3.75:+1.446e-01  x=2.50:+1.410e-01
```

## What these numbers mean

Two structural facts are now clear:

1. **The response peaks near the mass plane, but it is not localized there.**
   In both runs, the peak layer is one x-step after the mass plane
   (`x_src + H`), but the absolute response center sits well downstream:
   - `T=15`: center offset `+1.266`
   - `T=7.5`: center offset `+1.155`

2. **The response is broad.**
   The absolute-kernel width is a large fraction of the post-mass path:
   - `T=15`: width `3.508` over post-mass path `9.75` → `0.36`
   - `T=7.5`: width `1.832` over post-mass path `4.75` → `0.39`

So the observable behaves like:

- a **mass-adjacent peak**
- plus a **broad post-mass tail**

That is exactly the kind of structure a simple ray-deflection formula
cannot capture.

## Why we do not see textbook `1/b` lensing

The answer is now sharper:

The code is not measuring a localized deflection angle. It is measuring
the **detector centroid’s first-order wave response**, and that response
is distributed over many layers after the mass.

That kills the simple optics story in a precise way:

- A ray model assumes a localized transverse kick.
- The exact `K_l` kernel is broad and detector-weighted.
- Therefore the measured slope is controlled by the **adjoint-weighted
  wave response of the full propagator**, not by a local geometric kick.

This is why:

- the centered finite-path surrogate can sometimes fit numerically
- but the literal full-path Fermat reduction fails
- and the slope can stay near `≈ -1.43` across different `T_phys`
  while the ray formula changes

## What this does and does not establish

What this establishes:

1. The right observable is the adjoint kernel `K_l`, not a ray-angle integral.
2. The response is broad and post-mass-skewed even in the clean fine run.
3. The ray-optics failure now has a literal code-level explanation.

What this does not establish:

1. It does **not** yet derive the full `b`-slope `≈ -1.43`.
2. It does **not** yet show whether the normalized kernel shape is the
   same for all `b ∈ {3,4,5,6}`.
3. It does **not** yet isolate which propagator parameter controls the
   exponent most strongly (`BETA`, `k`, beam width, or something else).

## Initial `BETA` spot-check

To test whether the broad kernel is just an artifact of the default
angular weight, I reran the exact probe at the cheaper clean point
`T_phys = 7.5`, `H = 0.25`, `b = 3` for three values of `BETA`:

| `BETA` | `kubo_true` | peak layer | abs-center | abs-width | left/right abs split |
| ---: | ---: | ---: | ---: | ---: | --- |
| `0.4` | `+9.563675` | `2.75` | `3.509` | `1.653` | `0.34 / 0.73` |
| `0.8` | `+2.455550` | `2.75` | `3.655` | `1.832` | `0.33 / 0.72` |
| `1.6` | `+0.651091` | `2.50` | `3.606` | `1.887` | `0.36 / 0.69` |

What changes:

- the **overall response amplitude** changes strongly with `BETA`
  (about `15x` from `1.6` to `0.4`)

What does **not** change much:

- the kernel stays **broad**
- the kernel stays **post-mass-skewed**
- the absolute-center and width move only modestly

So `BETA` clearly controls coupling strength, but this first spot-check
does **not** support the idea that the default `≈ -1.43` slope is caused
simply by the kernel collapsing or widening in a trivial way. The broad
adjoint-weighted structure appears robust.

Lane M then carried the slope-side `BETA` sweep through the deflection
harness itself and closed the simple narrow-beam rescue:
[`/Users/jonreilly/Projects/Physics/docs/LENSING_BETA_SWEEP_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/LENSING_BETA_SWEEP_NOTE.md).
The apparent `beta=5` near-`1/b` point is an isolated coarse-grid spike,
not a stable asymptotic branch.

## Best next move

The cheapest decisive next lane is now:

1. fan out the exact kernel probe over `b ∈ {3,4,5,6}` at `T=15, H=0.25`
2. compare normalized `K_l` shapes across `b`
3. only after that, test whether kernel width/skew metrics track the retained
   `≈ -1.43` exponent more directly than raw `BETA` does

If the normalized kernel shape is stable across `b`, then the slope is
coming mainly from how the edge factor `1/r_field(b)` is sampled against
a fixed broad kernel. If the kernel shape itself changes strongly with
`b`, then the exponent is a deeper propagator-geometry effect.

## Bottom line

> "We now know why the simple lensing explanation failed. The literal
> first-order observable is an adjoint-weighted edge sum for detector
> centroid shift, not a localized ray deflection. On the decisive fine
> runs (`H=0.25`, `b=3`), the exact layer kernel reproduces `kubo_true`
> to machine precision and is broad and post-mass-skewed, with a width
> about 0.36–0.39 of the post-mass path. The slope therefore belongs to
> the wave-mechanical detector response of the propagator, not to a
> simple Fermat kick law. This does not derive the `≈ -1.43` exponent
> yet, but it does explain why textbook `1/b` ray optics is the wrong
> observable for this lane."
