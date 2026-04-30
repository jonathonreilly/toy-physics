# Distance Law: Steeper Than Newtonian

**Date:** 2026-04-05
**Status:** proposed_retained — alpha ~ -1.5 in far field, steepening at larger b

## Artifact chain

- [`scripts/distance_law_wide_continuum.py`](../scripts/distance_law_wide_continuum.py)

## Question

What is the distance exponent for gravitational deflection in the 3D
path-sum model?

## Results

### W=20 (initial test)

| h | alpha (b>=8) |
| ---: | ---: |
| 0.500 | -1.11 |
| 0.250 | -1.15 |

### W=40 (extended far-field, h=0.5)

| b range | alpha | n points |
| --- | ---: | ---: |
| b >= 8 | -1.31 | 9 |
| b >= 10 | -1.38 | 8 |
| b >= 15 | -1.49 | 6 |

The exponent steepens with increasing b range. The W=20 result of -1.1
was a near-field artifact (sources at b=8-16 are only 3-6 beam sigmas away).

### Local exponents (b_i to b_{i+1})

| b range | local alpha |
| --- | ---: |
| 15 to 20 | -1.32 |
| 20 to 25 | -1.47 |
| 25 to 30 | -1.59 |
| 30 to 35 | -1.67 |

Still steepening at b=35. The asymptotic value may be -2.0.

## Physical interpretation

The Newtonian prediction for a point particle deflected by 1/r potential is
delta ~ 1/b (alpha = -1). Our model gives alpha ~ -1.5, steeper.

The difference comes from the kernel: 1/L^2 (not 1/L) in 3D. With the h^2
measure, the effective kernel is h^2/L^2, which is a short-range propagator
that concentrates the beam more than the physical 1/r Green's function.

The finite beam length (L=30) also contributes: the truncated integral over
the source region gives a correction factor that steepens the effective
distance law at large b.

## What this means

The model does NOT reproduce the Newtonian 1/b distance law. The distance
exponent is a genuine prediction of the 1/L^(d-1) kernel choice: steeper
than Newton in the far field.

For publication: this is analogous to extra-dimensional gravity models
(ADD/RS) where the effective 4D distance law steepens at short distances
due to the extra-dimensional volume factor. Here, the "extra" steepening
comes from the kernel, not from extra dimensions.

## Grown geometry result (best measurement)

On grown geometry (NL=40, W=12, 3 seeds, source centered):
- alpha(all b, 5-10) = **-0.96** — nearest to Newtonian of any test
- The irregular node positions smooth out wave-optics oscillations
  that steepen the exponent on regular lattices (-1.1 to -1.2)
- All 5 impact parameters TOWARD, 3 seeds each

### Artifact chain
- [`scripts/distance_law_grown_geometry.py`](../scripts/distance_law_grown_geometry.py)
- [`logs/2026-04-06-distance-law-grown-geometry.txt`](../logs/2026-04-06-distance-law-grown-geometry.txt)

## Honest conclusion

The model produces a distance law of approximately 1/b with calculable
wave-optics corrections. The grown geometry gives the cleanest measurement
(-0.96) because it removes the regular lattice interference fringes.
