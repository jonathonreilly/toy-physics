# Planck-Scale Horizon Entropy Lane

**Date:** 2026-04-23  
**Status:** science-only lane note; current carrier class closes to a sharper no-go

## Verdict

On the current admissible horizon-entropy carriers in this branch, there is
**no exact route to a `1/4` coefficient**.

The retained carrier class is the same free-fermion, half-filled, nearest-
neighbor lattice surface used by the bounded BH entropy companion:

- OBC `L x L` square lattice, straight cut, `chi_eff = L`
- OBC `L^3` cubic lattice, straight cut, `chi_eff = L^2`

On that class, the asymptotic coefficient is fixed by the Widom-Gioev-Klich
geometry:

- `c_Widom(2D) = 1/6` exactly for the square-lattice diamond Fermi surface
- `c_Widom(3D) ~ 0.105` for the cubic half-filled carrier

So the honest result for Target 2 is not an exact `1/4` derivation. It is a
sharper classification:

> the admitted carrier family is Widom-class, not black-hole-`1/4` class.

The finite-lattice number `S / S_max ~ 0.24` seen at small `L` is a
finite-size effect. It is not an asymptotic theorem on this carrier family.

## Current admissible carrier class

The current lane admits the following carrier statements and no stronger one:

1. free-fermion nearest-neighbor hopping at half filling on the retained
   square or cubic lattice;
2. transfer-rank normalization `chi_eff = L^{d-1}` on the straight cut;
3. entropy scaling governed by the Widom/Gioev-Klich coefficient for the
   corresponding Fermi surface geometry.

Within that class, the asymptotic coefficient is geometry-determined and does
not land on `1/4`.

## What this rules out

This lane does **not** support the claim that the current carrier class derives
`S_BH = A / (4 l_P^2)` exactly from the RT bond-dimension ratio.

What it does support is narrower:

- the small-lattice `~0.24` ratio is real but non-asymptotic;
- the large-lattice carrier limit is `1/6` in 2D and is not `1/4`;
- the current carrier class therefore cannot be promoted as an exact horizon
  coefficient theorem.

## What would have to change

A genuine exact `1/4` route would require changing the carrier class, not just
relabeling the current one. Examples outside the current lane include a tuned
multi-pocket Fermi surface or a different horizon carrier with an explicit
gravitating sector. Those are different problems.

## Audit runner

The honest verifier for this lane is
[`scripts/frontier_planck_horizon_entropy_lane.py`](../scripts/frontier_planck_horizon_entropy_lane.py).

It checks three things only:

1. `c_Widom(2D) = 1/6` exactly;
2. `c_Widom(3D)` is far from `1/4`;
3. the finite-`L` RT ratio trends toward the Widom class rather than toward an
   exact `1/4`.

## Bottom line

The right science-only lane conclusion is:

> no exact `1/4` coefficient route exists on the current admissible carriers;
> the sharper retained statement is a Widom-class no-go / classification.

