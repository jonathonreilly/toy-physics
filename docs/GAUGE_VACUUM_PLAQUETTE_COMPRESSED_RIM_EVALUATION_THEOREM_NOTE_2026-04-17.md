# Gauge-Vacuum Plaquette Compressed Rim-Evaluation Theorem

**Date:** 2026-04-17  
**Status:** exact compressed-boundary derivation on the plaquette PF lane; the
full local rim functional `B_beta(W)` is still open, but after compression to
the marked class sector the `W`-dependence is explicit through the canonical
Peter-Weyl evaluation vector  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_compressed_rim_evaluation_theorem.py`

## Question

Can any part of the rim functional actually be derived now, rather than only
named as the missing local object `B_6(W)`?

## Answer

Yes, after compression to the marked class-function sector.

The full local rim functional on the orthogonal-slice Hilbert space is still
not derived. But the `W`-dependence of the compressed boundary data is already
exact and canonical.

From the spatial-environment transfer theorem, the compressed coefficients
satisfy

`z_(p,q)^env(beta) = <chi_(p,q), (S_beta^env)^(L_perp-1) eta_beta>`.

Define the class-sector coefficient vector

`v_beta = sum_(p,q) z_(p,q)^env(beta) chi_(p,q)`.

Then for every marked holonomy `W`, the central boundary class function is
exactly

`Z_beta^env(W) = <K(W), v_beta>`,

where

`K(W) = sum_(p,q) d_(p,q) conj(chi_(p,q)(W)) chi_(p,q)`

is the canonical Peter-Weyl evaluation vector on the marked class sector.

So after compression:

- the `W`-dependence is already explicit,
- the remaining unknown is only the beta-dependent vector `v_beta`,
- equivalently the coefficients `z_(p,q)^env(beta)` or `rho_(p,q)(beta)`.

That is a genuine derivation step.

## Setup

From the exact spatial-environment transfer theorem already on `main`:

- the environment boundary class function is a boundary amplitude of one
  explicit positive transfer operator,
- its class-sector coefficients are exact matrix elements
  `z_(p,q)^env(beta)`.

From the exact character-measure theorem:

- `Z_beta^env(W)` is a central class function of the marked holonomy `W`.

So the class-sector problem is exactly in the setting of Peter-Weyl
decomposition on central functions.

## Theorem 1: exact compressed boundary-evaluation functional

Let

`v_beta = sum_(p,q) z_(p,q)^env(beta) chi_(p,q)`.

Define

`K(W) = sum_(p,q) d_(p,q) conj(chi_(p,q)(W)) chi_(p,q)`.

Then by the exact character expansion of the boundary class function,

`Z_beta^env(W)
 = sum_(p,q) d_(p,q) z_(p,q)^env(beta) chi_(p,q)(W)
 = <K(W), v_beta>`.

So the compressed boundary functional is explicit and canonical.

## Corollary 1: the compressed `W`-dependence is no longer open

After compression to the marked class sector, the missing datum is not the full
family `W -> eta_beta(W)`.

The `W`-dependence is already explicit in `K(W)`.

What remains unknown is only:

- the beta-dependent coefficient vector `v_beta`,
- equivalently `z_(p,q)^env(beta)`,
- equivalently `rho_(p,q)(beta)`.

## Corollary 2: what remains open is the full local rim functional, not the compressed evaluation map

This theorem does **not** derive the full local rim functional on the slice
Hilbert space.

It derives only the compressed class-sector boundary functional.

So the current local rim-coupling boundary theorem remains correct:

- the full local map `B_beta(W)` is still open,
- but after compression its `W`-dependence is already canonical.

## What this closes

- exact derivation of the compressed class-sector boundary functional
- exact clarification that the `W`-dependence is not part of the remaining
  compressed unknown
- exact reduction of the compressed boundary problem to one beta-dependent
  coefficient vector

## What this does not close

- explicit full-slice rim functional `B_beta(W)`
- explicit `B_6(W)`
- explicit `K_6^env`
- explicit `S_6^env`
- explicit framework-point plaquette PF data

## Why this matters

This is the first actual derivation step on the rim side.

The branch no longer has to treat the entire compressed boundary family as
unknown. After compression, the `W`-dependence is explicit and canonical.

So the remaining plaquette PF construction problem is narrower:

- full local derivation of `B_6(W)` on the slice Hilbert space,
- and the beta-dependent coefficient vector it induces after compression.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_compressed_rim_evaluation_theorem.py
```
