# Gauge-Vacuum Plaquette Compressed Rim-Functional Uniqueness

**Date:** 2026-04-17  
**Status:** exact retained class-sector theorem on the plaquette PF lane; the
full local rim map `B_beta(W)` on the orthogonal-slice Hilbert space is still
open, but on every retained finite marked class sector the left boundary
functional is already the universal Peter-Weyl evaluation functional  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_compressed_rim_functional_uniqueness.py`

## Question

After the compressed rim-evaluation theorem, is the compressed left boundary
functional itself still open, or is only the full local slice lift still
missing?

## Answer

Only the full local slice lift is still missing.

Fix any retained finite marked class sector

`H_Lambda = span{chi_lambda : lambda in Lambda}`.

For each marked holonomy `W`, define the Peter-Weyl evaluation functional on
that retained class sector by

`K_Lambda(W) = sum_(lambda in Lambda) d_lambda conj(chi_lambda(W)) chi_lambda`.

Then for every retained coefficient vector

`v = sum_(lambda in Lambda) c_lambda chi_lambda`

the exact evaluation law is

`E_W(v) = sum_(lambda in Lambda) d_lambda c_lambda chi_lambda(W)
        = <K_Lambda(W), v>`.

So on the retained class sector the left boundary functional is already:

- explicit,
- universal,
- beta-independent,
- and unique.

Applied to the spatial-environment transfer law, this means the compressed
boundary class function is already

`Z_beta^env(W) = <K_Lambda(W), v_beta^Lambda>`,

with all `W`-dependence carried by `K_Lambda(W)` and all remaining
beta-dependent data carried by the propagated right boundary vector
`v_beta^Lambda`.

Therefore the live local gap is no longer compressed `W`-dependence. It is the
full orthogonal-slice lift:

- the theorem-grade local rim map `B_beta(W)` on the slice Hilbert space.

## Setup

From the exact spatial-environment transfer theorem already on `main`:

- one orthogonal-slice transfer operator `S_beta^env` exists,
- one rim-induced boundary state `eta_beta(W)` exists on the slice Hilbert
  space,
- and the environment boundary class function is exactly a boundary amplitude.

From the exact compressed rim-evaluation theorem:

- after compression to the retained marked class sector,
  `Z_beta^env(W) = <K_Lambda(W), v_beta^Lambda>`,
- where `K_Lambda(W)` is the retained Peter-Weyl evaluation vector.

The present question is whether that compressed left boundary functional can be
sharpened further.

## Theorem 1: exact retained class-sector evaluation functional

Let

`v = sum_(lambda in Lambda) c_lambda chi_lambda`

be any retained class-sector coefficient vector.

Define

`K_Lambda(W) = sum_(lambda in Lambda) d_lambda conj(chi_lambda(W)) chi_lambda`.

Then

`<K_Lambda(W), v>
 = sum_(lambda in Lambda) d_lambda c_lambda chi_lambda(W)`.

So the left boundary functional on the retained class sector is exactly the
Peter-Weyl evaluation functional.

## Corollary 1: the retained left boundary functional is unique

On the retained finite class sector, the character basis is orthonormal.

So if another retained vector `u_Lambda(W)` had the same matrix elements
against every retained basis character as `K_Lambda(W)`, then all retained
coordinates would agree and

`u_Lambda(W) = K_Lambda(W)`.

Therefore the retained left boundary functional is unique.

## Corollary 2: what remains open is the full slice lift, not retained `W`-dependence

This theorem does **not** derive the full local rim map on the orthogonal-slice
Hilbert space.

It derives only the retained left boundary functional on the marked class
sector.

So the remaining local issue is now sharper:

- not retained `W`-dependence,
- not another retained class-sector boundary functional,
- but the full local slice-Hilbert lift `B_beta(W)` whose action compresses to
  that retained evaluation functional.

## What this closes

- exact retained class-sector formula for the left boundary functional
- exact proof that the retained left boundary functional is universal and
  beta-independent
- exact proof that the retained left boundary functional is unique
- exact clarification that the remaining local issue is the full slice lift,
  not retained `W`-dependence

## What this does not close

- explicit full-slice rim map `B_beta(W)`
- explicit full-slice `B_6(W)`
- explicit orthogonal-slice kernel `K_6^env`
- explicit transfer object `S_6^env`
- explicit framework-point plaquette PF data

## Why this matters

This is a real derivation step.

The branch no longer has to treat the entire compressed left boundary side as
open. On the retained marked class sector, the left boundary functional is
already fixed and universal.

So the live local PF target is now more precise:

- derive the full local slice lift `B_6(W)`,
- not another retained class-sector `W`-dependence theorem.

## Command

```bash
python3 scripts/frontier_gauge_vacuum_plaquette_compressed_rim_functional_uniqueness.py
```
