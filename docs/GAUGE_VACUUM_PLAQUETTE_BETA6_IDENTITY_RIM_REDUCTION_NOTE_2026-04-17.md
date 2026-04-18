# Gauge-Vacuum Plaquette Beta=6 Identity-Rim Reduction

**Date:** 2026-04-17  
**Status:** exact operator-side reduction theorem on the plaquette PF lane; for
explicit class-sector `beta = 6` PF closure, the only rim datum that must be
evaluated upstream is the identity-holonomy boundary state
`eta_6(e) = P_cls B_6(e)`, while generic marked-holonomy dependence is already
downstream through the universal Peter-Weyl evaluation functional  
**Script:** `scripts/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_REDUCTION_2026_04_17.py`

## Question

After the new integral-boundary and compressed-evaluation theorems, does
explicit class-sector `beta = 6` PF closure still require evaluation of the
full rim family

`W -> B_6(W)`?

## Answer

No, not for class-sector PF closure.

The exact transfer law already gives

`Z_beta^env(W) = <eta_beta(W), (S_beta^env)^(L_perp-1) eta_beta(e)>`.

So the propagated beta-side class-sector vector is

`v_6 = (S_6^env)^(L_perp-1) eta_6(e)`.

And the compressed rim-evaluation law already gives

`Z_6^env(W) = <K(W), v_6>`.

Therefore:

- the class-sector coefficients `z_(p,q)^env(6)` and the normalized PF data
  `rho_(p,q)(6)` are determined by the bulk operator together with the
  identity rim datum `eta_6(e)`,
- generic marked-holonomy dependence is already carried by the universal
  evaluation vector `K(W)`,
- so the full `W`-family of rim lifts is not an additional upstream
  requirement for explicit class-sector PF closure.

The full family `B_6(W)` can still matter if the goal is the full
pre-compression local slice lift at generic `W`. But it is not the remaining
upstream datum for the class-sector PF closure problem itself.

## Setup

From
[GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md](./GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TRANSFER_THEOREM_NOTE.md):

- the exact boundary amplitude is

  `Z_beta^env(W) = <eta_beta(W), (S_beta^env)^(L_perp-1) eta_beta(e)>`,

- so every marked-holonomy value shares the same propagated identity-boundary
  vector.

From
[GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_FULL_SLICE_RIM_LIFT_INTEGRAL_BOUNDARY_SCIENCE_ONLY_NOTE_2026-04-17.md):

- the full local rim lift is exactly
  `B_beta(W)` on the slice Hilbert space,
- and `eta_beta(W) = P_cls B_beta(W)`.

From
[GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_FUNCTIONAL_UNIQUENESS_NOTE_2026-04-17.md):

- on the retained marked class sector, the left boundary functional is already
  the universal Peter-Weyl evaluation functional `K(W)`.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_EVALUATION_SEAM_REDUCTION_SCIENCE_ONLY_NOTE_2026-04-17.md):

- the remaining explicit `beta = 6` seam is matrix-element evaluation of the
  operator-side objects,
- and the boundary coefficients are already written using `eta_6(e)`.

So the only remaining question is whether generic `W`-dependent rim data are
still required upstream once the class-sector transfer law is written in this
form.

## Theorem 1: exact identity-rim reduction of class-sector `beta = 6` closure

Let

`S_6^env = P_cls K_6^env P_cls`,

`eta_6(e) = P_cls B_6(e)`,

and define

`v_6 = (S_6^env)^(L_perp-1) eta_6(e)`.

Then the class-sector boundary coefficients satisfy

`z_(p,q)^env(6) = <chi_(p,q), v_6>`.

Therefore explicit class-sector `beta = 6` PF closure requires exactly:

- the compressed bulk matrix elements of `S_6^env`, equivalently the
  compressed matrix elements of `K_6^env`,
- the compressed identity rim datum `eta_6(e)`, equivalently `B_6(e)` after
  compression.

No generic `W`-dependent rim family enters this upstream class-sector closure
statement.

## Corollary 1: projective identity-rim reduction for normalized PF data

The normalized boundary coefficients are

`rho_(p,q)(6) = z_(p,q)^env(6) / z_(0,0)^env(6)`.

So multiplying `eta_6(e)` by any positive scalar rescales every
`z_(p,q)^env(6)` by the same factor and leaves `rho_(p,q)(6)` unchanged.

Therefore the normalized class-sector PF data depend only on the projective
class of the identity rim datum.

## Corollary 2: generic `W` dependence is downstream evaluation only

For every marked holonomy `W`,

`Z_6^env(W) = <K(W), v_6>`.

So once `v_6` is explicit, the full compressed boundary class function is
explicit automatically. The marked-holonomy family is already carried by the
universal beta-independent evaluation functional `K(W)`.

## Corollary 3: the full slice lift matters only through its compressed identity projection for class-sector closure

Because the class-sector closure law uses `eta_6(e) = P_cls B_6(e)`, any two
identity-holonomy full-slice lifts with the same compressed projection induce
the same class-sector vector `v_6`.

So class-sector closure does not depend on unrecovered off-class details of the
identity full-slice lift beyond what survives under `P_cls`.

## What this closes

- exact clarification that explicit class-sector `beta = 6` PF closure uses
  the identity rim datum `eta_6(e)`, not the full generic `W -> B_6(W)` family
- exact clarification that generic marked-holonomy dependence is already
  downstream through `K(W)`
- exact projective reduction of the normalized PF data to the identity rim
  state
- exact clarification that off-class full-slice details matter only through the
  compressed identity projection for class-sector closure

## What this does not close

- explicit closed-form compressed bulk matrix elements of `K_6^env`
- explicit closed-form identity rim datum `B_6(e)` or `eta_6(e)`
- explicit full-slice generic-`W` family `B_6(W)` if one wants the full local
  pre-compression lift
- explicit analytic closure of canonical `P(6)`
- the global sole-axiom PF selector theorem

## Why this matters

This is a real operator-side sharpening.

The current branch no longer has to describe the live local target as though
the whole `W`-parametrized rim family were still an upstream PF unknown.

It can now say the sharper thing:

- for class-sector PF closure, the remaining operator data are the compressed
  bulk matrix elements and the identity rim datum,
- the full marked-holonomy family is already recovered downstream once that
  beta-side vector is explicit.

That keeps the live constructive target on the plaquette lane narrow and
honest.

## Command

```bash
python3 scripts/GAUGE_VACUUM_PLAQUETTE_BETA6_IDENTITY_RIM_REDUCTION_2026_04_17.py
```

Expected summary:

- `THEOREM PASS=6 SUPPORT=4 FAIL=0`
