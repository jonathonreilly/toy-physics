# CKM Neutron-EDM Corollary and Bounded Prediction

**Date:** 2026-04-15
**Status:** proposed_retained structural corollary + bounded quantitative prediction on `main`
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

2. **Promoted CKM atlas/axiom package**
   - framework Jarlskog invariant `J = 3.331 x 10^-5`
   - authority:
     [CKM_ATLAS_AXIOM_CLOSURE_NOTE.md](CKM_ATLAS_AXIOM_CLOSURE_NOTE.md)

These two package-grade inputs already close the structural corollary:

- on the retained `\theta_eff = 0` surface, `d_n(QCD) = 0` exactly
- therefore the surviving neutron EDM is a **CKM-only** observable

The note then applies a **standard EFT bridge** for the short-distance and
long-distance CKM neutron-EDM scalings. That quantitative continuation remains
bounded, not theorem-grade.

## What Is Retained Exactly

On the retained action surface plus the promoted CKM atlas/axiom package, the repo
now supports the following exact corollary:

> `d_n(QCD) = 0` exactly on the retained `\theta_eff = 0` surface, so the
> surviving neutron EDM is CKM-only.

This is not a new strong-CP theorem beyond
[STRONG_CP_THETA_ZERO_NOTE.md](STRONG_CP_THETA_ZERO_NOTE.md). It is the direct
observable corollary obtained by combining that retained strong-CP closure with
the promoted CKM atlas/axiom package.

## Bounded Quantitative Continuation

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
- equivalently, `d_n(QCD) = 0` exactly on that retained surface
- a standard short/long-distance EFT bridge puts that CKM-only scale near
  `10^-32 - 10^-33 e cm`

What this lane does **not** support:

- a new exact strong-CP closure theorem beyond the retained action-surface note
- a first-principles lattice computation of the neutron EDM matrix elements
- a radiative or chiral master theorem beyond the retained action-surface note

## How It Fits the Package

This note now has the same dual-status architecture as the confinement /
string-tension row:

- retained structural corollary:
  `d_n(QCD) = 0` and neutron EDM is CKM-only on the retained surface
- bounded quantitative continuation:
  `d_n(CKM) ~ 10^-32 - 10^-33 e cm` through the standard EFT bridge

So the exact corollary is package-grade, while the numeric prediction remains a
secondary bounded consequence.

## Universal Theta-Response Follow-Up

The broader source-scoped corollary is packaged in
`UNIVERSAL_THETA_INDUCED_EDM_VANISHING_THEOREM_NOTE_2026-04-24.md` (downstream consumer; backticked to avoid length-2 cycle — citation graph direction is *downstream → upstream*):
all EDM components sourced by QCD `theta_eff` vanish on the retained action
surface. That theorem does not set CKM weak EDMs or independent BSM CP-odd EFT
operators to zero.

## Commands Run

```bash
python3 scripts/frontier_ckm_neutron_edm_bound.py
```
