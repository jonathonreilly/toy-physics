# Planck-Scale Spacetime / Time-Lock Unit-Map Lane

**Date:** 2026-04-23  
**Status:** science-only theorem-grade narrowing on the derived-time route  
**Audit runner:** `scripts/frontier_planck_spacetime_time_lock_unit_map_lane.py`

## Question

The user-level intuition is reasonable:

> if the framework really derives one physical time direction rather than
> assuming it, could that be the missing ingredient that ties the spatial
> lattice step to an exact Planck length/time pair?

Equivalently:

- maybe the derived single clock removes the last unit ambiguity;
- maybe the exact `3+1` lift fixes a canonical temporal step;
- maybe the physical Planck pair is really a spacetime lock, not a purely
  spatial statement.

## Bottom line

Partly, but not all the way.

The derived-time route does produce a real new theorem candidate:

> it collapses an **anisotropic two-parameter spacetime unit map**
> `(a_s, a_t)` to a **single common spacetime ray**.

But it still does **not** fix the absolute scale of that ray.

More precisely:

1. anomaly cancellation plus the single-clock Cauchy requirement derives
   exactly one time direction;
2. the exact scalar `3+1` bridge fixes the relative temporal/spatial weight on
   the minimal APBC block to

   `beta = (c a_t / a_s)^2 = 1`;

3. therefore the physical spacetime unit map is locked to

   `a_s = c a_t`;

4. however all currently retained spacetime observables remain homogeneous
   under the common rescaling

   `a_s -> lambda a_s`, `a_t -> lambda a_t`, `lambda > 0`;

5. so derived time removes the **relative** space/time calibration freedom,
   but not the final **absolute** Planck anchor.

So the honest verdict is:

- **time-lock:** yes
- **time-alone Planck derivation:** no

In short:

- time-lock: yes
- time-alone Planck derivation: no

## Why time matters at all

Before derived time, there are in principle two different spacetime unit maps:

- spatial step `a_s`
- temporal step `a_t`

To compare them physically one also needs a speed conversion `c`, so the only
dimensionless anisotropy parameter is

`beta := (c a_t / a_s)^2`.

If `beta` were free, the theory would not have a unique spacetime lift even
after admitting one time direction. There would still be a hidden
space-versus-time calibration ambiguity.

The exact scalar `3+1` bridge is what kills that ambiguity.

## The anisotropic scalar bridge family

The retained exact scalar `3+1` note works on the minimal APBC block with the
kernel

`K_sc(omega) = 3 + sin^2(omega)`.

To expose the hidden unit question honestly, enlarge that to the anisotropic
same-surface family

`K_beta(omega) = 3 + beta sin^2(omega)`,

where

`beta = (c a_t / a_s)^2`.

This is the unique dimensionless way the single temporal direction can enter
relative to the three spatial directions on the minimal scalar block.

For this family the exact endpoint coefficients are:

- `A_2(beta) = 1 / (2 (3 + beta))`
- `A_inf(beta) = 1 / (2 sqrt(3 (3 + beta)))`

so the exact endpoint ratio is

`R(beta) := A_inf(beta) / A_2(beta) = sqrt((3 + beta) / 3)`.

The retained exact theorem value is

`R = 2 / sqrt(3)`.

Therefore

`sqrt((3 + beta) / 3) = 2 / sqrt(3)`
`=> 3 + beta = 4`
`=> beta = 1`.

So the exact scalar bridge does not just give a nice ratio. It fixes the
relative spacetime unit map:

`c a_t = a_s`.

That is the clean time-lock statement.

## What this really buys

This is a real theorem-grade gain.

It means the framework is no longer carrying two separate potential minima:

- a minimum spatial step `a_s`
- and an unrelated minimum temporal tick `a_t`

Instead, on the exact derived-time `3+1` surface, any such minima must come as
one locked spacetime pair

`t_* = a_* / c`.

So if a future absolute Planck derivation exists, it should most naturally
land as a **pair theorem**

- `l_* = a_*`
- `t_* = a_* / c`

rather than as two independent postulates.

## Why this still does not force exact Planck

Once `beta = 1` is fixed, the unit map is still parameterized by one common
positive scale:

- `x_phys = a x_lat`
- `t_phys = (a / c) tau_lat`

with one remaining `a > 0`.

Under the global rescaling

`a -> lambda a`,

the lock survives:

- `x_phys -> lambda x_phys`
- `t_phys -> lambda t_phys`
- `beta -> beta`

So the time-lock does not by itself pick any preferred `lambda`.

## Exact homogeneous survivors after time-lock

The current exact spacetime surfaces stay homogeneous after the lock:

1. **causal speed ratios** remain unchanged because
   `x_phys / t_phys = c (x_lat / tau_lat)`;
2. **the exact scalar `3+1` endpoint ratio** `R = 2 / sqrt(3)` is
   dimensionless and therefore independent of the common scale;
3. **the Lorentzian interval class**

   `ds^2 = -c^2 dt^2 + dx^2`

   rescales to

   `ds^2 -> lambda^2 ds^2`,

   so sign / nullness / causal class are unchanged;
4. **the Einstein-Hilbert-style action** is still homogeneous of degree zero
   under the common spacetime rescaling, exactly as in the earlier scale-ray
   theorem;
5. **the minimal APBC temporal frequency**

   `omega_min = pi/2`

   is exact only in lattice units. Its physical value scales as `c / a`, so it
   does not anchor `a`.

So derived time kills anisotropy, not the common ray.

## The theorem-level statement

**Theorem (Derived time-lock without absolute Planck anchor).**
Assume:

1. anomaly-forced single-clock time on `Cl(3)`/`Z^3`;
2. the exact scalar `3+1` bridge on the minimal APBC block;
3. the exact Lorentzian `3+1` lift / global closure on `PL S^3 x R`;
4. a single signal-speed conversion `c` relating spatial and temporal units.

Then:

1. the only admissible relative spacetime unit parameter on the minimal scalar
   bridge is `beta = (c a_t / a_s)^2`;
2. the exact retained endpoint ratio `R = 2 / sqrt(3)` forces `beta = 1`;
3. therefore derived time locks the physical spacetime unit map to
   `a_s = c a_t`;
4. but every currently retained spacetime observable remains homogeneous under
   the common rescaling `a_s -> lambda a_s`, `a_t -> lambda a_t`;
5. therefore derived time removes the relative space/time calibration freedom
   but does **not** by itself derive the absolute Planck scale.

Equivalently:

> derived time converts the Planck question from
> “what are the minimum length and minimum time independently?”
> to
> “what fixes the one common spacetime unit `a`?”

## What this closes

This closes one genuine loophole in the Planck program:

- maybe the single-clock `3+1` lift was the missing reason the spatial lattice
  step should become a canonical spacetime unit.

Answer:

- it is the missing reason the spatial and temporal units should be **locked**;
- it is **not** enough to make the common locked unit equal exact Planck.

That is a useful narrowing because it says the surviving Planck target should
now be sought on a **time-locked spacetime carrier**, not on separate spatial
and temporal minima.

## What this does not close

This note does **not** prove:

- that `a = l_P` is now derived;
- that `c` itself is derived here as an SI quantity rather than used as the
  signal-speed conversion between units;
- that the exact scalar `3+1` ratio alone is a full physical observable law;
- that a minimum time tick exists independently of the spatial step.

It proves only the sharper statement:

- time gives a **pair lock**, not the **absolute pair scale**.

## Safe wording

**Can claim**

- derived time collapses the relative space/time unit ambiguity to the exact
  lock `a_s = c a_t`;
- any future Planck closure should naturally appear as a locked pair
  `t_* = a_* / c`;
- the remaining missing theorem is an absolute anchor for the common spacetime
  ray, not a second independent time-scale theorem.

**Cannot claim**

- that the derived-time route already forces exact conventional Planck length;
- that the framework already contains an exact minimum time theorem independent
  of the spatial step;
- that the exact `3+1` scalar bridge alone removes the last absolute scale
  freedom.
