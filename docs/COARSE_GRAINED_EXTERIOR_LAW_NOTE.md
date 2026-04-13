# Coarse-Grained Exterior Point-Source Law from the Exact Lattice Field

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_coarse_grained_exterior_law.py`  
**Status:** Bounded positive result; not full nonlinear GR

## Purpose

The previous Codex gravity work had already shown:

- the exact microscopic source side is much stronger than before
- the direct same-source strong-field metric still has a nonzero 4D vacuum
  residual
- neither source-family freedom nor a small nonlinear same-source ansatz tweak
  removes that residual

That still left one major ambiguity:

> is the real problem the exterior law itself, or just the matching from the
> microscopic lattice field to its macroscopic exterior representative?

This note answers that question in the strongest bounded form currently
available on the Codex branch.

## Coarse-grained exterior law

For a static exterior vacuum in three spatial dimensions, the unique radial
harmonic law is

`phi_eff(r) = a / r`.

So the natural coarse-graining question is:

1. start from the exact lattice field `phi(x)` for a strong-field source
2. shell-average it outside a matching radius `R_match`
3. project that shell-averaged exterior data onto the unique radial harmonic
   law `a/r`
4. build the corresponding static isotropic metric candidate from that
   projected field

If that projected metric is vacuum-close, then the remaining problem is not
the exterior law itself. It is the microscopic-to-macroscopic matching step.

## Two exact source families tested

The script applies this coarse-grained radial projection to two different exact
source families already constructed on `codex/review-active`:

1. the exact local `O_h`-symmetric source family used in
   `OH_SOURCE_CLASS_NOTE.md`
2. the broader exact finite-rank source family used in
   `FINITE_RANK_GRAVITY_RESIDUAL_NOTE.md`

So this is not a single special-source test.

## What the script finds

### 1. Exact local `O_h` family

At matching radius `R_match = 4.5`:

- direct exact same-source metric residual:

  `max |G_{mu nu}| = 7.17e-4`

- coarse-grained radial harmonic projection residual:

  `max |G_{mu nu}| = 4.56e-6`

- improvement:

  `~1.57e2`

### 2. Exact finite-rank family

At the same matching radius:

- direct exact same-source metric residual:

  `max |G_{mu nu}| = 2.79e-2`

- coarse-grained radial harmonic projection residual:

  `max |G_{mu nu}| = 1.19e-5`

- improvement:

  `~2.35e3`

So across both exact source families, the coarse-grained radial harmonic
projection is already vacuum-close in the exterior, while the direct
microscopic same-source metric is not.

## Interpretation

This is the strongest positive gravity result on the Codex branch so far after
the weak-field surface:

> the remaining strong-field problem is not primarily the macroscopic exterior
> harmonic law

The coarse-grained exterior law is already working.

What is still missing is:

1. why the exact microscopic lattice field should be replaced by its
   coarse-grained radial harmonic projection outside a finite matching radius
2. how that matching radius is determined from the lattice dynamics
3. how the near-source region is sewn to the macroscopic exterior law

That is a much sharper target than “derive all of GR.”

## What this closes

This closes another real ambiguity:

> the failure of the current strong-field closure is not mainly a failure of
> the exterior point-source vacuum law after coarse-graining

That law is already very good.

## What this does not close

This note still does **not** close:

1. the theorem-grade microscopic-to-macroscopic matching theorem
2. the near-source strong-field metric
3. full nonlinear GR

## Practical next step

The next Codex gravity move should therefore be:

1. derive the matching theorem that takes the exact lattice field to the
   coarse-grained radial harmonic exterior law
2. or derive the effective source/coarse-graining rule that makes that
   projection unavoidable from the lattice dynamics itself

That is now the cleanest remaining gravity target.
