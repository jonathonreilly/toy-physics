# Hierarchy No-Import Status Note

**Date:** 2026-04-22  
**Status:** exact retained no-import dimensionless hierarchy theorem; absolute
`v` row is bounded until the lattice-spacing anchor is derived  
**Script:** `scripts/frontier_hierarchy_no_import_status.py`

## Question

Can the hierarchy lane be honestly closed as retained with no imports on the
current accepted framework stack?

## Answer

Partially.

The current exact minimal-block chain closes the **dimensionless** hierarchy
statement

`a v = (7/8)^(1/4) * alpha_LM^16`

on the accepted same-surface plaquette chain.

What does **not** close on the current accepted stack is the absolute GeV row

`v = 246.282818290129 GeV`,

because that number still requires the extra identification

`a^(-1) = M_Pl`.

So the honest retained no-import hierarchy statement is the lattice-unit
relation `a v = (7/8)^(1/4) * alpha_LM^16`. The absolute electroweak scale is
currently a **bounded companion** conditioned on the separate Planck-lattice
reading.

This note supersedes
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
as the full-status authority for the hierarchy lane. The older note remains a
real source-response / selector subtheorem, but not the complete no-import
status statement for the lane.

## Theorem 1: the exponent `16` is exact on the minimal `3+1` block

On the exact `L_s = 2`, temporal-APBC minimal block, the staggered-Dirac
determinant satisfies

`|det(D + m)| = prod_omega [m^2 + u_0^2 (3 + sin^2 omega)]^4`

with `omega = (2n+1) pi / L_t`.

At zero mass and the minimal temporal block `L_t = 2`, both APBC temporal
modes have `sin^2 omega = 1`, so

`|det D| = prod_(omega = +/- pi/2) [4 u_0^2]^4 = (4 u_0^2)^8 = 4^8 u_0^16`.

So the power `16` is not a fit and not a taste-staircase slogan. It is the
exact `u_0` power of the minimal `2 x 2 x 2 x 2` hierarchy block. This is
equivalently the exact `2^4` hypercube/taste count of the minimal `3+1`
staggered block.

Because the same-surface coupling is

`alpha_LM = alpha_bare / u_0`

with `alpha_bare = 1 / (4 pi)` fixed on the canonical `g_bare = 1` surface,
the exact hierarchy suppression carries the same exact exponent:

`alpha_LM^16`.

So the exponent gap is now closed on the current hierarchy surface.

## Theorem 2: the selector factor is exact on the same surface

The exact local bosonic source-response curvature on the minimal block gives
the temporal coefficient

`A(L_t) = (1 / (2 L_t u_0^2)) sum_omega 1 / (3 + sin^2 omega)`.

The local bosonic/CPT-even selector picks the unique minimal resolved APBC
orbit `L_t = 4`, yielding the exact ratio

`A_2 / A_4 = 8/7`

and hence the exact selector factor

`C_APBC = (A_2 / A_4)^(-1/4) = (7/8)^(1/4)`.

So the retained no-import hierarchy statement on the current minimal block is

`a v = C_APBC * alpha_LM^16 = (7/8)^(1/4) * alpha_LM^16`.

Every quantity on the right-hand side is fixed on the accepted same-surface
hierarchy chain.

## Theorem 3: absolute-scale obstruction on the current accepted stack

The exact hierarchy statements above are all in lattice units.

If the lattice spacing is `a`, then the physical electroweak scale is

`v_phys = (a v) / a`.

Under a global rescaling of units

`a -> lambda a`,

the retained exact hierarchy data

- the determinant power `16`,
- the APBC selector factor `(7/8)^(1/4)`,
- `u_0`,
- `alpha_LM`,
- and therefore `a v`

stay unchanged.

But the physical GeV value rescales as

`v_phys -> v_phys / lambda`.

Therefore the current exact hierarchy chain fixes only the **dimensionless**
combination `a v`. It does **not** fix the absolute GeV value without one more
theorem that pins `a^(-1)`.

That missing theorem is exactly what the current package does not yet have on
the accepted minimal-input surface:

- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md) does **not**
  list `a = l_Planck` or `a^(-1) = M_Pl` as part of the current minimal
  accepted input stack.
- [GRAVITY_CLEAN_DERIVATION_NOTE.md](./GRAVITY_CLEAN_DERIVATION_NOTE.md)
  explicitly gives `G_N = 1/(4 pi)` only in lattice units and states that SI
  conversion requires one physical calibration.
- [ACTION_NORMALIZATION_NOTE.md](./ACTION_NORMALIZATION_NOTE.md) likewise fixes
  only the dimensionless action coefficient after **defining** `G` from
  observation; it does not derive the absolute lattice spacing from the
  accepted axioms.
- [docs/publication/ci3_z3/README.md](./publication/ci3_z3/README.md) already
  lists the hierarchy lane itself among the package pressure points because it
  still imports `M_Pl`.

So the `M_Pl` anchor is not removed by the current hierarchy theorems. It is a
separate lattice-spacing identification.

## Consequence for package status

The honest split is:

- **Retained no-import hierarchy theorem:**
  `a v = (7/8)^(1/4) * alpha_LM^16`
- **Bounded companion absolute row:**
  `v = 246.282818290129 GeV` only after the extra identification
  `a^(-1) = M_Pl`

That means the repo and paper should stop presenting the absolute `v` row as a
retained flagship quantitative centerpiece on the current package surface.

The safe flagship wording is:

> the framework retains an exact no-import dimensionless electroweak-hierarchy
> suppression theorem on the minimal `3+1` block, while the absolute GeV value
> remains conditioned on the separate Planck-lattice identification.

## What this changes

This note changes three things.

1. The exponent `16` is no longer an open hierarchy objection.
2. The retained hierarchy lane is now the no-import dimensionless statement
   `a v = (7/8)^(1/4) * alpha_LM^16`.
3. The absolute `v = 246.282818290129 GeV` row should be demoted from retained
   to bounded/bridge-conditioned until a retained theorem pins `a^(-1)`.

## Verification

Run:

```bash
python3 scripts/frontier_hierarchy_no_import_status.py
```

Expected outcome:

- exact exponent-`16` check passes on the minimal block
- exact selector factor check passes
- the no-import retained object `a v` is verified
- the absolute-scale obstruction is verified by explicit rescaling

## Supporting authorities

- [HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md](./HIERARCHY_MATSUBARA_DECOMPOSITION_NOTE.md)
- [HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md](./HIERARCHY_SPATIAL_BC_AND_U0_SCALING_NOTE.md)
- [HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md](./HIERARCHY_BOSONIC_BILINEAR_SELECTOR_NOTE.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md)
