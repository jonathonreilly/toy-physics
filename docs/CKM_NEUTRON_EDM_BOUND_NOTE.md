# CKM Neutron-EDM Bounded Lane

**Date:** 2026-04-15
**Status:** bounded lane on `main`
**Script:** `scripts/frontier_ckm_neutron_edm_bound.py`

## Role

This note is the observable follow-up lane to the retained strong-CP closure package.

It does **not** broaden the closure in
[STRONG_CP_THETA_ZERO_NOTE.md](STRONG_CP_THETA_ZERO_NOTE.md). The retained
core result remains:

- `\theta_eff = 0` on the axiom-determined Wilson-plus-staggered action surface
- no bare `\theta` appears there
- CKM CP remains weak-sector only

This lane asks the next concrete question:

> if the QCD `\theta` contribution vanishes on that retained surface, what is
> the surviving CKM-only scale for the neutron EDM?

## Input Surface

The estimate uses two ingredients:

1. **Retained strong-CP closure package**
   - `d_n(QCD) = 0` because `\theta_eff = 0` on the retained action surface
   - authority:
     [STRONG_CP_THETA_ZERO_NOTE.md](STRONG_CP_THETA_ZERO_NOTE.md)

2. **Promoted CKM closure package**
   - framework Jarlskog invariant `J = 3.331 x 10^-5`
   - authority:
     [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

It then applies a **standard EFT bridge** for the short-distance and
long-distance CKM neutron-EDM scalings. So this is a bounded lane, not an
exact theorem row.

## Current Estimate

Using the framework CKM package:

- short-distance estimate:
  `d_n^(SD) ~ 5 x 10^-33 e cm`
- long-distance estimate:
  `d_n^(LD) ~ 8 x 10^-33 e cm`

Headline bounded value:

`d_n(CKM) ~ 8 x 10^-33 e cm`

Current experimental upper bound:

`|d_n| < 1.8 x 10^-26 e cm`

So the bounded CKM-only estimate sits about seven orders of magnitude below
the current bound.

## Safe Claim Boundary

What this lane supports:

- on the retained `\theta_eff = 0` surface, the neutron EDM is a **CKM-only**
  observable
- a standard short/long-distance EFT bridge puts that CKM-only scale near
  `10^-32 - 10^-33 e cm`

What this lane does **not** support:

- a new exact strong-CP closure theorem beyond the retained action-surface note
- a first-principles lattice computation of the neutron EDM matrix elements
- a radiative or chiral master theorem beyond the retained action-surface note

## How It Fits the Package

This is a bounded secondary lane, similar in status to proton lifetime,
gravitational decoherence, and vacuum critical stability:

- scientifically useful
- reviewer-relevant
- not part of the retained flagship theorem core

## Commands Run

```bash
python3 scripts/frontier_ckm_neutron_edm_bound.py
```
