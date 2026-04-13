# Dark Energy Equation of State: w = -1 from S^3 Spectral Rigidity

**Date:** 2026-04-12
**Lane:** Cosmological constant / dark energy equation of state
**Script:** `scripts/frontier_w_minus_one.py`

## Status

EXACT on the S^3-compactification theorem surface.
Inherits the S^3 assumption (bounded/open lane).

## Theorem / Claim

**Theorem (w = -1 from spectral rigidity).**
On the framework's S^3 compactification surface, the dark energy equation
of state is w = -1 exactly, with no corrections at any order.

## Assumptions

1. S^3 compactification (this is the bounded/open topology lane --- not yet
   derived from the framework axioms).
2. Standard identification: the cosmological constant Lambda arises from the
   first nonzero eigenvalue of the Laplacian on S^3.

## What Is Actually Proved

### The derivation (5 lines)

1. **Spectral gap.** On S^3 of radius R, the scalar Laplacian eigenvalues are
   lambda_l = l(l+2)/R^2 with l = 0, 1, 2, ...  The first nonzero eigenvalue
   is lambda_1 = 3/R^2.

2. **Topological invariance.** The coefficient 3 = l(l+2)|_{l=1} is determined
   entirely by the topology of S^3 (it is the Casimir of SO(4) acting on
   S^3 = SO(4)/SO(3)).  It does not depend on any dynamical quantity.

3. **Lambda = const.** Therefore Lambda = 3/R^2, where R is the compactification
   radius set once by the framework.  Lambda is a constant --- it has no time
   dependence because: (a) the topology cannot change continuously (discrete),
   (b) the eigenvalue coefficient 3 is integer-valued, (c) R is set at the
   framework level, not a dynamical field.

4. **w = -1.** For a cosmological constant (Lambda = const), the stress-energy
   tensor is T_{mu nu} = -(Lambda/8piG) g_{mu nu}.  This gives rho = Lambda/8piG
   and p = -rho, hence w = p/rho = -1.

5. **Exactness.** This is an algebraic identity, not an approximation.  There
   are no perturbative corrections, no loop corrections, no finite-size effects
   on the w = -1 relation.  The only input is Lambda = const; the output w = -1
   is exact.

### Lattice corrections

The lattice dispersion relation differs from the continuum at O(a^2).  At
cosmological scales:

- R ~ 4.4 x 10^26 m (Hubble radius)
- a ~ 1.6 x 10^-35 m (Planck length / lattice spacing)
- Correction: O((a/R)^2) ~ 10^-122

This is astronomically negligible.  Moreover, even this correction is itself a
constant (determined by the lattice geometry), so it does not introduce time
dependence and does not shift w away from -1.

## What Remains Open

1. **S^3 compactification.** The derivation is conditional on S^3.  The topology
   lane (S^3 from framework axioms) is still bounded/open.

2. **Numerical value of Lambda.** We predict w = -1 but we do NOT predict the
   numerical value of Lambda.  That requires knowing R, which is a framework
   parameter.  The observed Lambda ~ 10^-122 (in Planck units) is a coincidence
   of scale, not a prediction of the framework in its current form.

3. **No quintessence.** The framework has no dynamical scalar field that could
   produce w != -1.  The spectral-gap origin of Lambda is topological, not
   dynamical.  This is a falsifiable prediction: if observations establish
   w != -1, the S^3 compactification surface is ruled out.

## How This Changes The Paper

This is a clean conditional result suitable for the paper:

> **Conditional on S^3 compactification, the framework predicts w = -1 exactly.**

It belongs in the cosmology section as a downstream consequence of the topology
lane.  It does not upgrade the S^3 lane from bounded to closed, but it
demonstrates a sharp observational consequence of the S^3 assumption.

The result is falsifiable: any future measurement of w != -1 would rule out the
S^3 spectral-gap identification.

## Commands Run

```
python3 scripts/frontier_w_minus_one.py
```

Expected output: all PASS, zero FAIL.
