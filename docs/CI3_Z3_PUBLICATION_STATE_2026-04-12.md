# CI(3) / Z^3 Publication State

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Status:** Codex-owned publication authority for the current flagship paper surface

## Framework sentence

> We take `Cl(3)` on `Z^3` as the physical theory. Everything else is derived.

This document is the current publication-facing state for that framework. It
supersedes older narrower retain audits where they conflict with the present
paper surface.

## External inputs used in the current paper

The framework sentence is ontological, not a claim that every phenomenological
normalization is already closed. The current paper still conditions some
downstream phenomenology on a small set of external inputs:

- cosmological boundary conditions:
  - `T_CMB = 2.7255 K`
  - `H_0 = 67.4 km/s/Mpc`
- electroweak-scale boundary input:
  - `v = 246 GeV`

The cosmological inputs specify which universe / epoch is being matched.
The electroweak-scale input is different in kind: it is the unresolved
hierarchy input, not merely a "where/when are we?" datum.

## Retained backbone

The current retained backbone is:

- weak-field gravity on the lattice surface:
  - Poisson is the unique self-consistent local field equation in the audited
    operator family
  - the lattice Green's function yields Newton's inverse-square law on `Z^3`
  - weak equivalence principle is retained as a weak-field corollary of the
    derived action
  - weak-field gravitational time dilation is retained on the same Poisson /
    Newton surface
- exact native `Cl(3)` / `SU(2)` on `Z^3`
- graph-first weak-axis selector
- graph-first structural `su(3)` closure
- left-handed charge matching on the selected-axis surface
- anomaly-forced `3+1` closure on the single-clock codimension-1 theorem surface
- retained `S^3` compactification / topology closure:
  - the cone-capped cubical ball yields a compact closed simply connected PL
    3-manifold for all `R >= 2`
  - the cone cap is unique up to PL homeomorphism on the accepted framework
    surface
  - Perelman + Moise identify the result as `PL S^3`
- full-framework one-generation closure:
  - the spatial graph fixes the left-handed gauge/matter structure
  - derived time supplies chirality
  - anomaly cancellation fixes the right-handed singlet completion on the
    Standard Model branch
- three-generation matter closure in the framework:
  - exact orbit algebra `8 = 1 + 1 + 3 + 3`
  - physical species structure on the lattice surface

## Exact supporting theorems now safe to carry

These are exact or exact-enough supporting results on the current paper
surface:

- exact/structural weak-field gravity chain:
  - Poisson self-consistency and operator-family uniqueness
  - Newton law from lattice Green's function asymptotics on `Z^3`
  - weak equivalence principle from the derived eikonal action
  - weak-field time dilation from the same action on the retained Poisson
    profile
- exact no-third-order-interference / `I_3 = 0` theorem on the Hilbert surface
  Note: this is **not** a standalone derivation of the Born rule from nothing;
  the safe statement is exact pairwise interference on the accepted Hilbert
  probability surface, and the runner name is historical.
- exact CPT theorem for the free staggered `Cl(3)` lattice on even periodic lattices
- exact native cubic `SU(2)` algebra
- exact graph-first `su(3)` commutant closure on the retained selector surface

## High-impact gates still open

The remaining live paper gates are:

1. DM relic mapping
2. renormalized `y_t` matching
3. CKM / quantitative flavor closure

Recent Claude work and direct Codex review materially narrowed the attack
surface. The audit bar now remains:

- DM relic mapping: still bounded even after Stosszahlansatz / Friedmann tightening
- renormalized `y_t`: still bounded even after coefficient / matching notes
- CKM: still bounded even after NNI / coefficient / `c_23` work

## Honest bounded lanes

The following are useful and may appear in SI or a bounded phenomenology
section, but they are not yet retained closure:

- weak-field GR-signature companions beyond Newton/Poisson:
  - conformal-metric / geodesic / light-bending notes
  - these remain useful, but the broader GR bundle is still not the paper-safe
    closure surface beyond the retained WEP / time-dilation corollaries
- direct lattice DM contact enhancement
- DM coarse-graining / Stosszahlansatz notes
- renormalized `y_t` running and matching notes
- CKM/Higgs `Z_3` selection arguments
- gauge-coupling normalization notes
- cosmology companions such as `w = -1`, graviton mass, `Omega_Lambda`, `n_s`
- Higgs / Coleman-Weinberg mass notes
- proton lifetime, Lorentz-violation, BH-entropy, gravitational-decoherence,
  magnetic-monopole, and GW-echo companion predictions

## Publication rule

For the flagship paper:

- the main text should lead with the retained backbone
- the external-input split must stay explicit:
  - `T_CMB` and `H_0` are cosmological boundary conditions
  - `v` is an electroweak-scale boundary input
- the three live gates must remain explicitly open or bounded
- no note or script may promote a bounded lane to `CLOSED` unless the theorem
  survives direct Codex review on this branch

## Promotion rule for `main`

Promotion from `review-active` to `main` should now proceed in controlled
batches:

- promote retained backbone docs and runners
- promote exact supporting theorems that do not widen the claim surface
- do **not** promote bounded or stale packet docs as if they were authority

## Current paper-safe summary

> `Cl(3)` on `Z^3` yields weak-field gravity through the Poisson/Newton chain,
> weak-field WEP and gravitational time dilation as corollaries of that same
> surface, exact `SU(2)`, graph-first structural `SU(3)`, a retained `S^3`
> compactification on the accepted topology infrastructure, a full-framework
> one-generation Standard Model closure, and a retained three-generation
> matter structure in the same framework. The remaining live paper gates are
> DM relic mapping, renormalized `y_t`, and quantitative flavor closure.
