# Support-Renormalized Amplitude Law for the Active Non-`O_h` Shell Correction

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_support_renormalized_active_amplitude.py`  
**Status:** Exact amplitude law on the current star-supported source class

## Purpose

The projected DtN correction-operator note already showed that the active
non-`O_h` shell correction is not a post hoc fit. What still remained open was
the scalar amplitude:

> how does the microscopic support renormalization fix the size of that active
> shell correction?

This note closes that gap on the current star-supported exact source class.

## Exact support-side statement

Let

- `S` be the seven-point star support
- `q_eff = (I - W G_S)^-1 m` be the exact renormalized support source vector
- `phi = G_0 P q_eff` be the exact exterior harmonic field
- `delta_sigma_active` be the raw active sewing-band orbit correction vector on
  the four active channels
  `(3,2,2)`, `(3,3,0)`, `(4,1,0)`, `(4,1,1)`

Then the exact microscopic map from `q_eff` to `delta_sigma_active` is a
rank-one linear operator:

`A_active = m_active * 1^T`

where `1^T` is the total-charge functional on the support and `m_active` is
the unit-charge raw active correction mode.

So for any exact star-supported source on this class,

`delta_sigma_active = A_active q_eff = (1^T q_eff) m_active`

That is:

> the active non-`O_h` shell amplitude is exactly the total renormalized
> support charge `Q_eff = 1^T q_eff`

There is no extra free scalar on the active quotient.

## Pair-quotient consequence

Because the projected DtN correction operator already has exact pairwise
antisymmetry, the same factorization holds on the reduced pair quotient:

`delta_sigma_pair = Q_eff m_pair`

So the pair-quotient amplitude is also fixed exactly by the same microscopic
support scalar `Q_eff`.

## Microscopic origin

The new script constructs the support-to-active response operator directly from
the exact microscopic lattice solve by feeding the seven support basis vectors
through:

1. the exact support Green columns `G_0 P`
2. the exterior projector
3. the exact DtN shell source
4. the active orbit-channel reduction

The resulting response matrix has:

- exact rank `1`
- exact factorization through the total-charge row `1^T`
- exact annihilation of the non-invariant support channels in the adapted
  support basis

So the amplitude law is not inferred from family data. It is already present in
the microscopic support-side operator.

## Family verification

The exact local `O_h` source family and the broader finite-rank family both
satisfy the same support-side law:

- compute `q_eff`
- compute `Q_eff = 1^T q_eff`
- predict `delta_sigma_active = Q_eff m_active`

This reproduces the directly measured raw active shell correction exactly for both
families.

## What this closes

This closes the last scalar ambiguity on the current star-supported source
class:

> the active non-`O_h` shell correction amplitude is derived exactly from the
> microscopic support renormalization

## What this still does not close

This note still does **not** close:

1. the final 4D Einstein / Regge lift of the corrected shell law
2. the extension beyond the current star-supported source class
3. a full general nonlinear GR theorem

## Updated gravity target

After this note, the support-side amplitude problem is removed from the live
blocker list on the current source class.

The remaining strong-field target is now sharply concentrated on:

- lifting the exact shell/junction law into the final nonlinear 4D spacetime
  closure
- and then extending that closure beyond the current star-supported class
