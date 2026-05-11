# (3+1)D Promotions of Lane 5 (Lightcone) and Lane 6 (Retarded vs Instantaneous)

**Date:** 2026-04-07
**Status:** bounded mixed result — strict `(3+1)D` lightcone certified to `r=8` via delta pulse; the M-vs-I gap remains conditional on replacing or deriving the instantaneous comparator.
**Claim type:** bounded_theorem

**Review repair perimeter (2026-04-26 generated-audit context):**
Generated-audit context before this narrowing identified this chain-closure
blocker: "The live runner reproduces the
finite lightcone and M-vs-I tables, but the literal
instantaneous/c=infinity interpretation does not close: the I branch
is a stitched finite-time frozen c=1 wave-solve comparator, not a
derived elliptic Poisson or c->infinity solution." The repair target being
addressed is `runner_artifact_issue`: "replace the I
branch with an actual layerwise elliptic/Poisson instantaneous
solve, or prove and numerically bound convergence of the
frozen-wave late-time slice to the c->infinity comparator; then add
hard assertions for the lightcone and gap gates and audit the Lane
8 radiation lane separately for the combined three-signature
statement." This rigorization edit only sharpens the boundary of the
repair perimeter; nothing here promotes audit status. The
strict (3+1)D lightcone result is independent of the I-branch
comparator interpretation and is unaffected.

## Artifact chain

- [`scripts/wave_3plus1d_promotions.py`](../scripts/wave_3plus1d_promotions.py)
- [`logs/2026-04-07-wave-3plus1d-promotions.txt`](../logs/2026-04-07-wave-3plus1d-promotions.txt)

## Question

Lane 8 (the (3+1)D radiation falloff) was narrowed to a single observable
because the (3+1)D promotions of Lane 5 (delta-pulse lightcone) and
Lane 6 (retarded vs instantaneous on a moving source) had not been
done. This lane runs both promotions on the same (3+1)D operator
used in Lane 8.

The PDE is the same as Lane 8:
  (1/c²) ∂²f/∂t² − (∂²/∂x_perp² + ∂²/∂y² + ∂²/∂z²) f = source(t, x_perp, y, z)
with x as time, c = 1 lattice cell per layer, 7-point spatial stencil
on a 19³ transverse cube.

## A. (3+1)D lightcone (mirror of Lane 5)

Delta pulse at the source cell on layer src_layer = 4. Measure the
first dt where |f(iy=0, iz=offset)| at the x_perp=0 plane exceeds
eps = 1e-6. All cells before arrival are exactly 0.0.

| r (cells) | first dt | result |
| ---: | ---: | :---: |
| 2 | 2 | OK |
| 3 | 3 | OK |
| 4 | 4 | OK |
| 5 | 5 | OK |
| 6 | 6 | OK |
| 7 | 7 | OK |
| 8 | 8 | OK |

`first_dt = r` exactly for every offset out to r = 8 on the
**(3+1)D** operator. Strict lattice lightcone, identical to Lane 5
behaviour but on the full 3D Laplacian.

## B. (3+1)D retarded vs instantaneous (mirror of Lane 6)

Source moves linearly in z from iz_start=6 to iz_end=0 over 26
active layers (v/c = 0.23). Build two histories on the (3+1)D wave
equation:

- **M (retarded)**: standard wave-equation evolution with the moving source
- **I (instantaneous, c=∞)**: stitched layer-by-layer from cached
  late-time slices of static (3+1)D solves with the source frozen at
  each visited iz position

Beam runs through both fields on three grown geometries.

| Family | dM | dI | M − I | relative |
| --- | ---: | ---: | ---: | ---: |
| Fam1 | +0.001185 | +0.000825 | +0.000361 | **30.44%** |
| Fam2 | +0.001347 | +0.000991 | +0.000357 | **26.47%** |
| Fam3 | +0.001235 | +0.000856 | +0.000379 | **30.72%** |

All three families show **>25%** gap between retarded and
instantaneous beam deflection on the (3+1)D wave equation. The sign
is consistent across families (M > I in all three, opposite to the
(2+1)D case where M < I — the geometric weighting differs in 3D, but
the qualitative finding "retarded ≠ instantaneous" holds and is even
larger in magnitude than the (2+1)D Lane 6 result of 22–26%).

## What this closes

Combined with Lane 8 (the (3+1)D radiation falloff), the model now
has all three classical scalar-wave signatures certified on the
**physical (3+1)D operator** from one local PDE:

- **Lightcone**: strict, `first_dt = r` exactly to r = 8
- **Retardation**: M ≠ I on a moving source, 26–31%, three families
- **Radiation falloff**: ~ 1/r at far-field, slope −1.14 (Lane 8)

The "(3+1)D scalar-wave story closed in physical 3+1 dimensions" claim
that was retracted from Lane 8 is now properly backed by an explicit
artifact chain on the same operator.

## Honest limits

- v/c = 0.23 single value; full v-sweep not done
- Linear translation only (no orbital / accelerated source on the (3+1)D operator)
- Delta-pulse lightcone tested out to r = 8 (limited by 19³ box)
- Beam-side F~M and Born on the (3+1)D field are not in this lane
  (Lane 8's beam-side observables are still measured on the (2+1)D field)
- Single source, no backreaction
- The (3+1)D solver is pure-Python and slow (~30 s per full run);
  caching the static comparator per visited iz is the main optimization

## Cited authority chain (2026-05-10)

The active runner is
[`scripts/wave_3plus1d_promotions.py`](../scripts/wave_3plus1d_promotions.py)
(audit-lane runner cache: `status: ok`, elapsed ~26 s, exit 0,
unmodified runner SHA pinned by the cache). The frozen output is
[`logs/2026-04-07-wave-3plus1d-promotions.txt`](../logs/2026-04-07-wave-3plus1d-promotions.txt).
The runner reproduces both bounded tables verbatim:
the strict-lightcone `first_dt = r` table out to r=8 (Section A) and
the three-family Fam1/Fam2/Fam3 M-vs-I gap table (Section B,
26.47%/30.44%/30.72%).

Generated-audit context makes a precise scope distinction that this note
already mirrors but is now made explicit:

- **Section A (strict lightcone)** is independent of the I-branch
  comparator interpretation. The strict `first_dt = r` certification
  to r=8 on the (3+1)D operator is closed by the runner alone.
- **Section B (M-vs-I gap)** is the row the generated repair context flags. The
  M branch is the standard retarded (3+1)D evolution; the I branch is
  the layer-by-layer-stitched late-time frozen `c=1` wave-solve
  comparator described in Section B above and in the runner. The
  generated repair context states that this stitched I branch is not
  yet a derived elliptic/Poisson `c->infinity` solution. The retained
  reading of Section B until the repair target lands is therefore bounded:
  the (3+1)D wave evolution disagrees with the layerwise stitched
  late-time-frozen comparator by 26-31% across three grown families,
  with sign opposite to the (2+1)D Lane 6 result.

A future Section-B rigorization may either replace the I branch with
a layerwise elliptic/Poisson solve or prove convergence of the
frozen-wave late-time slice to the `c->infinity` limit with a
runner-asserted bound; until that repair target lands, the
combined three-signature statement (lightcone + retardation +
radiation falloff) remains conditional on the M-vs-I row.
