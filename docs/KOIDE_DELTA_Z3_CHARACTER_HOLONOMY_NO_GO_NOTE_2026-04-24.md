# Koide delta Z3 character-holonomy no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_z3_character_holonomy_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether the physical selected-line Berry endpoint is forced by naturality
as a `U(1)` holonomy character of the retained `Z_3` cyclic symmetry.

If this worked, `theta_end-theta0` would be a character-lattice phase and could
be identified with the ambient APS scalar `eta_APS=2/9`.

## Executable theorem

The retained ambient scalar is exact:

```text
eta_APS = 2/9.
```

But a `U(1)` character of `Z_3` sends the generator to

```text
0, 1/3, or 2/3    mod 1.
```

Equivalently, a generator endpoint `x` must satisfy

```text
3x in Z.
```

For `eta_APS=2/9`,

```text
3 eta_APS = 2/3,
```

so `eta_APS` is not a character endpoint.

## Quadratic refinement check

A quadratic refinement can be written schematically as

```text
q(1) = A/9 + B/3.
```

It can hit `2/9` only after choosing

```text
A = 2 - 3B.
```

For example `A=2,B=0` gives `q(1)=2/9`, but its polarization is nonzero:

```text
q(2)-2q(1) = 4/9.
```

That is APS-style quadratic support, not a `Z_3` character holonomy endpoint.

## Residual

```text
RESIDUAL_CHARACTER_FRACTION = three_eta_not_integral
RESIDUAL_SCALAR = theta_end - theta0 - eta_APS
RESIDUAL_ENDPOINT = theta_end - theta0 - eta_APS
```

## Why this is not closure

The retained character lattice misses `2/9`.  Enlarging to a quadratic
refinement can represent `2/9`, but only with an extra coefficient and without
identifying the selected-line endpoint.  The physical Berry/APS functor remains
the missing bridge.

## Falsifiers

- A retained natural transformation from equivariant APS data to selected-line
  Berry endpoints that is not restricted to `Z_3` characters and fixes the
  quadratic coefficient uniquely.
- A physical proof that the selected-line endpoint should be a quadratic
  refinement value rather than a character, with unit normalization.
- A boundary functor deriving `theta_end-theta0=eta_APS` directly from the
  retained `Cl(3)/Z^3` data.

## Boundaries

- The runner covers `Hom(Z_3,U(1))` character holonomies and a minimal
  quadratic-refinement sanity check.
- It does not exclude a future non-character Berry/APS functor; it shows that
  ordinary character naturality cannot be that functor.

## Hostile reviewer objections answered

- **"The eta value is a phase fraction."**  It is a fraction, but not a
  `Z_3` character fraction.
- **"Quadratic data can give ninths."**  Yes, but choosing the quadratic
  coefficient is an extra law, and a quadratic refinement is not a character
  endpoint.
- **"Does this weaken APS support?"**  No.  It protects APS support from being
  overclaimed as the physical selected-line endpoint.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_z3_character_holonomy_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_DELTA_Z3_CHARACTER_HOLONOMY_NO_GO=TRUE
DELTA_Z3_CHARACTER_HOLONOMY_CLOSES_DELTA=FALSE
RESIDUAL_SCALAR=theta_end-theta0-eta_APS
RESIDUAL_CHARACTER_FRACTION=three_eta_not_integral
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
```
