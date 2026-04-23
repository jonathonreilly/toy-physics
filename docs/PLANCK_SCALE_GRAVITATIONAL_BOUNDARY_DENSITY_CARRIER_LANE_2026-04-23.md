# Planck-Scale Gravitational Boundary-Density Carrier Lane

**Date:** 2026-04-23  
**Status:** science-only lane reduction; local-geometry and naive-cell-counting
classes close negatively  
**Audit runner:** `scripts/frontier_planck_gravitational_boundary_density_carrier_lane.py`

## Question

Can exact conventional

`a = l_P`

come from a genuinely new **gravitational boundary-density carrier**, rather
than from the current free-fermion RT/Widom lane?

## Verdict

Yes, but only in a much narrower form than "some new boundary entropy
theorem."

The current first-principles result is:

1. **No purely local gravitational boundary density built from the admitted
   static geometric scalars can produce a universal Bekenstein-Hawking area
   law.**
2. **No naive tensor-product integer cell counting can give exact conventional
   `a = l_P`.**
3. Therefore the only serious surviving boundary-density carrier class is a
   **collective gravitational boundary carrier** with an exact effective
   surface entropy density

   `s_* = 1/4`

   on the physical boundary cells.

This is a real narrowing of the Planck program. It says the surviving
boundary route is not:

- the current RT/Widom carrier;
- a local curvature density;
- or a naive "one integer Hilbert factor per boundary cell" story.

It would have to be a genuinely gravitational, collective, same-surface
boundary state-counting theorem.

## Inputs

This lane uses only the currently retained gravity/action and entropy facts:

- [PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md](./PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md)
- [PLANCK_SCALE_BOUNDARY_DENSITY_ROUTE_REDUCTION_NOTE_2026-04-23.md](./PLANCK_SCALE_BOUNDARY_DENSITY_ROUTE_REDUCTION_NOTE_2026-04-23.md)
- [PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md](./PLANCK_SCALE_HORIZON_ENTROPY_LANE_2026-04-23.md)
- [BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md](./BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md)
- [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)

The upstream reductions already say:

- the current free-fermion RT coefficient path is wrong on this repo's
  carrier (`1/6`, not `1/4`);
- the surviving route must therefore be gravitational and new-carrier.

This note sharpens that again by classifying what the new carrier cannot be.

## Boundary class under test

Take a static approximately spherical boundary of radius `R` surrounding a
localized source `M` on the retained weak-field gravity surface. The admitted
large-`R` scalars have the standard scaling implied by the lattice Poisson /
Green-function route:

- potential:
  `phi ~ G M / R`
- normal field strength:
  `g_n := |partial_n phi| ~ G M / R^2`
- mean curvature:
  `H ~ 1 / R`
- Gaussian curvature:
  `K ~ 1 / R^2`
- surface-gravity-type normal acceleration:
  `kappa ~ G M / R^2`

The precise order-one constants are not important here. Only the scaling class
matters.

## Theorem 1: local geometric boundary-density no-go

Let a candidate local gravitational boundary entropy density be any monomial on
this admitted local scalar class,

`sigma_loc = C * phi^a * g_n^b * H^c * K^d * kappa^e`

with nonnegative exponents `a,b,c,d,e`.

Then the corresponding additive entropy on the spherical boundary scales as

`S_loc(R,M) = int_(dA) sigma_loc ~ C * G^(a+b+e) * M^(a+b+e) * R^(2 - a - 2b - c - 2d - 2e)`.

An exact Bekenstein-Hawking area law on fixed lattice spacing would require

`S_BH ~ s_* * A / a^2 ~ s_* * R^2 / a^2`

with coefficient independent of `M` and `R`.

That forces

- `a + b + e = 0` from `M`-independence;
- `a + 2b + c + 2d + 2e = 0` from `R^2` scaling.

Because all exponents are nonnegative, the only solution is

`a = b = c = d = e = 0`.

So the **only** area-law-compatible member of this entire local geometric
class is the trivial constant-density class.

### Consequence

No nontrivial local boundary density built from the admitted weak-field
geometric scalars can be the missing Planck-fixing carrier.

In particular, this kills the whole class:

- local curvature densities,
- local field-strength densities,
- local acceleration densities,
- and local mixed monomials on that same surface.

## Theorem 2: horizon specialization does not rescue the local class

One might hope that imposing a horizon relation rescues a local density.

On a horizon-like family with `R ~ G M`, the potential becomes order-one:

`phi_H ~ O(1)`,

while the other local scalars still scale like inverse powers of `R`:

- `g_n ~ 1/R`
- `H ~ 1/R`
- `K ~ 1/R^2`
- `kappa ~ 1/R`

So on the horizon family,

`S_hor ~ R^(2 - b - c - 2d - e) * F(phi_H)`

for some constant `F(phi_H)` determined by the order-one horizon potential.

To preserve exact area-law scaling `~ R^2`, one still needs

`b = c = d = e = 0`.

So even after imposing a horizon relation, the local carrier class collapses
to a **constant surface density** (possibly multiplied by a universal function
of the horizon potential), not to a nontrivial local geometric density.

### Consequence

If the boundary route works at all, it does not work because some local
curvature scalar miraculously reproduces the entropy coefficient. It works, if
at all, because the horizon supports an exact **constant effective surface
density** on its physical boundary cells.

## Theorem 3: naive independent cell counting cannot give exact conventional Planck

Suppose the surviving constant-density carrier is the simplest possible
boundary Hilbert-factor story:

- the boundary contains `N_dA` independent cells;
- each cell carries the same finite Hilbert-space factor of dimension `g`;
- entropy is tensor-product counting:
  `S = N_dA * ln(g)`;
- physical area is `A = N_dA * a^2`.

Matching Bekenstein-Hawking then gives

`N_dA * ln(g) = A / (4 l_P^2) = N_dA * a^2 / (4 l_P^2)`

and therefore

`a^2 / l_P^2 = 4 ln(g)`.

So exact conventional

`a = l_P`

would require

`ln(g) = 1/4`,

that is

`g = e^(1/4) = 1.284025...`

which is not an integer Hilbert dimension.

The minimal nontrivial integer choice `g = 2` gives instead

`a / l_P = 2 sqrt(ln 2) = 1.665109...`

which is Planck-order but not exact conventional Planck.

### Consequence

The surviving boundary-density route cannot be a naive tensor-product
integer-degeneracy story with one independent finite-dimensional factor per
boundary cell.

## Surviving carrier class

After these reductions, the only serious boundary-density candidate class left
is:

> a collective gravitational boundary carrier whose effective entropy density
> per physical boundary cell is exact and not reducible to either local
> curvature monomials or naive independent integer cell counting.

The clean surviving theorem target is therefore:

1. construct a genuinely gravitational horizon/boundary carrier on the same
   surface as the accepted gravity/action stack;
2. prove an exact collective state-counting law
   `S = s_* * N_dA + o(N_dA)`;
3. prove the exact effective density
   `s_* = 1/4`;
4. then infer `a = l_P` if one physical boundary cell has area `a^2`.

## What this closes

This note closes several tempting but wrong boundary-density stories:

- "maybe the right local curvature scalar gives the area law";
- "maybe some local field-strength density gives the coefficient";
- "maybe a simple one-cell/one-bit counting law already forces Planck."

All of those classes now close negatively.

## What this does not close

This note does **not** prove:

- that the collective gravitational boundary carrier already exists;
- that its effective density really is `1/4`;
- or that the boundary route is stronger than the action-phase route.

It only proves the sharper strategy statement:

> if exact conventional Planck comes from a boundary-density theorem at all,
> it must be a collective gravitational surface-density theorem with an exact
> renormalized coefficient, not a local geometric density and not a naive
> integer cell-counting law.

## Bottom line

The boundary-density route survives, but in a very narrow and much cleaner
form:

- not RT/Widom;
- not local curvature;
- not naive integer cell counting;
- only an exact collective gravitational surface-density theorem remains live.
