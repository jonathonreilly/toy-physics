# Planck-Scale Gravity/Action Scale-Ray No-Go Theorem

**Date:** 2026-04-23  
**Status:** science-only theorem-grade no-go on the current admitted
gravity/action family  
**Audit runner:** `scripts/frontier_planck_gravity_action_scale_ray_nogo.py`

## Question

After the retained physical-lattice boundary, the weak-field gravity derivation,
and the canonical Einstein-Hilbert-style geometric/action equivalence, could
the **current admitted gravity/action family itself** already fix the absolute
lattice spacing `a`?

Equivalently:

- maybe the physical-lattice reading already kills every meaningful scale
  freedom;
- maybe the textbook geometric/action equivalence secretly fixes the last unit
  map;
- maybe the hierarchy, gravity, and cosmology identities together already hide
  a preferred physical length.

## Bottom line

No.

On the current admitted physical-lattice gravity/action surface, the retained
closed relations are homogeneous under one global positive unit-map rescaling

`a -> lambda a`,  `lambda > 0`.

That rescaling changes every dimensionful readout by its engineering dimension,
but it leaves the current exact same-surface relations unchanged.

So the current admitted family fixes a **scale ray**, not an absolute scale
anchor.

The branch-level consequence is sharp:

> any no-import derivation of `a^(-1) = M_Pl` must introduce a genuinely new
> non-homogeneous, unit-bearing same-surface observable beyond the current
> admitted gravity/action family.

## What this is not

This is **not** a regulator / continuum-limit theorem.

The retained physical-lattice note already closes that issue in the opposite
direction: the lattice is a physical substrate on the accepted package
surface, not a disposable regulator family.

The present theorem is narrower:

- even after the physical-lattice reading is accepted,
- there remains one external choice of how one lattice unit is mapped to
  meters / GeV,
- and the current admitted gravity/action family does not remove that choice.

So the no-go is about the **absolute unit map**, not about whether the lattice
itself is physically real.

## Inputs

This theorem uses only already-accepted or branch-local surfaces:

- [PHYSICAL_LATTICE_NECESSITY_NOTE.md](./PHYSICAL_LATTICE_NECESSITY_NOTE.md)
- [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)
- [ACTION_NORMALIZATION_NOTE.md](./ACTION_NORMALIZATION_NOTE.md)
- [UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md](./UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md)
- [PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md](./PLANCK_SCALE_DERIVATION_PROGRAM_2026-04-23.md)

The theorem depends on five repo facts:

1. the lattice is physical on the accepted package surface;
2. gravity closes weak-field Newton with `G_N = 1/(4 pi)` in lattice units;
3. SI conversion still needs one calibration;
4. the textbook Einstein-Hilbert-style comparison is geometric/action
   equivalence, not an absolute-scale theorem;
5. the hierarchy route fixes `a v`, not `a`.

## Exact scale ray

Fix one admissible lattice-unit solution of the current package and choose a
positive unit map `a`.

Then the induced physical quantities scale by engineering dimension:

- length / radius: `r_phys = a r_lat`
- mass / energy: `m_phys = m_lat / a`
- vacuum scale / Higgs vev: `v_phys = (a v)_lat / a`
- Newton constant: `G_phys = a^2 G_lat`
- cosmological constant / curvature: `Lambda_phys = Lambda_lat / a^2`
- graviton mass: `m_g,phys = m_g,lat / a`
- four-volume: `V_4,phys = a^4 V_4,lat`
- scalar curvature: `R_phys = R_lat / a^2`

So changing `a` moves the solution along one exact positive scale ray.

## The theorem

### 1. Newton's dimensionless gravity observable is scale-invariant

The weak-field lattice gravity stack gives

`phi ~ G M / r`.

Under

`G -> lambda^2 G`, `M -> M / lambda`, `r -> lambda r`,

the dimensionless potential is unchanged:

`G M / r -> (lambda^2 G) (M / lambda) / (lambda r) = G M / r`.

So the current Newton surface does not pick `lambda`.

### 2. The Einstein-Hilbert-style action is homogeneous of degree zero in the
global unit map

The current geometric/action equivalence is an Einstein-Hilbert-style action
family, so at the level of engineering dimensions

`S_GR ~ (1 / G) int d^4x sqrt(g) R`.

Under the same unit-map rescaling:

- `1 / G -> lambda^(-2) / G`
- `d^4x sqrt(g) -> lambda^4 d^4x sqrt(g)`
- `R -> lambda^(-2) R`

Therefore the full action is invariant:

`(1 / G) int d^4x sqrt(g) R`
`-> (lambda^(-2) / G) * lambda^4 * lambda^(-2) int d^4x sqrt(g) R`
`= (1 / G) int d^4x sqrt(g) R`.

So the current action family itself does not anchor `lambda`.

### 3. The hierarchy route fixes only the scale-invariant product `a v`

The current hierarchy/program surface fixes

`(a v)_lat`,

not `a` and `v` separately.

Under `a -> lambda a`,

`v_phys -> v_phys / lambda`,

while the invariant product stays fixed:

`a v_phys = (lambda a) (v_phys / lambda) = a v_phys`.

So the current hierarchy package moves on the same scale ray.

### 4. The retained cosmology/graviton identity is also scale-invariant

On the retained compactness/spectral-gap surface the graviton identity is of
the form

`m_g^2 = 2 Lambda`

in natural units.

Under the unit-map rescaling:

- `m_g^2 -> m_g^2 / lambda^2`
- `Lambda -> Lambda / lambda^2`

so the ratio is unchanged.

Therefore the current spectral-gap cosmology identity also lives on the same
scale ray.

### 5. No intrinsic stationary scale exists on the current admitted family

The scale-sensitive quantities on the current admitted family are pure power
laws in `lambda`:

- `G(lambda) ~ lambda^2`
- `m(lambda) ~ lambda^(-1)`
- `v(lambda) ~ lambda^(-1)`
- `Lambda(lambda) ~ lambda^(-2)`

The currently retained exact relations are homogeneous combinations of those
objects and therefore remain invariant along the ray.

So the current admitted family has no internal stationary point, endpoint
selector, or absolute unit anchor for `lambda`.

## The theorem-level statement

**Theorem (Scale-ray no-go for the current gravity/action family).**
Assume the current accepted physical-lattice framework surface together with:

1. the weak-field gravity derivation in lattice units;
2. the current Einstein-Hilbert-style geometric/action equivalence;
3. the current hierarchy product surface;
4. the retained compactness/spectral-gap gravity identities.

Then:

1. the induced physical unit map is parameterized by one positive scale `a`;
2. every currently retained gravity/action relation is homogeneous under the
   induced rescaling `a -> lambda a`;
3. the same-surface action, Newton potential, hierarchy product, and spectral
   gap identities remain exact along that ray;
4. therefore the current admitted gravity/action family fixes only a scale ray
   and contains no intrinsic absolute anchor for `a`.

Equivalently: a no-import derivation of `a^(-1) = M_Pl` cannot come from the
current admitted gravity/action family alone. It requires a genuinely new
non-homogeneous, unit-bearing same-surface theorem.

## What this closes

This closes one specific loophole:

- maybe the current gravity/action family is already one theorem away from
  deriving `a`, with the needed anchor hidden inside the existing admitted
  same-surface equations.

Answer: no.

The current family is not just incomplete. It is homogeneous under the global
unit-map ray.

So the next real theorem target is no longer vague. It is:

> derive one new unit-bearing, non-homogeneous same-surface observable that
> breaks the current scale ray.

## What this does not close

This theorem does **not** prove:

- that no future Planck derivation exists at all;
- that the gravity/action route should be abandoned;
- that the physical-lattice reading is false;
- that the Planck scale should never be more than a pinned observable.

It proves only the sharper current statement:

- the present admitted gravity/action family cannot fix the absolute scale on
  its own.

## Safe wording

**Can claim**

- the current gravity/action stack fixes a scale ray, not an absolute scale
  anchor;
- the Einstein-Hilbert-style action family is homogeneous under the remaining
  unit-map rescaling;
- any future no-import Planck derivation must add a genuinely new unit-bearing
  same-surface theorem.

**Cannot claim**

- that the current gravity/action lane already derives `a = l_Planck`;
- that Einstein-Hilbert-style equivalence alone removes the last calibration;
- that the current hierarchy or spectral-gap identities secretly fix `a`.
