# Exact Two-Particle Product Law Frontier Note

**Date:** 2026-04-11  
**Scope:** audit of `bdede1849feb4e6e0e61373b9f67477ab84658ec` and
`scripts/exact_two_particle_product_law.py`

## Verdict

**Hold off `main`.** This lane is scientifically useful, but it is not yet a
retainable mainline note because the reported `M1*M2` dependence is built into
the interaction ansatz itself and the setup is still a 1D open-boundary toy
model rather than the repo's primary staggered/open-cubic architecture.

The script does show a real exact-vs-Hartree distinction, but that is a
secondary control result. It does **not** yet establish an emergent product law
that the repo can safely promote as a bounded Newton-closure companion.

## Why Not Mainline Yet

The exact-diagonalization part is genuine:

- the evolution is carried out on the full `N^2` tensor-product Hilbert space
- the script does not use Hartree factorization for the main result
- the strong-coupling section usefully shows exact vs Hartree divergence

But the product-law claim is not independent of the model assumption:

- the interaction is hard-coded as
  `V(x1, x2) = -G * s1 * s2 / |x1 - x2|^p`
- that means the bilinear mass factor is already present in the Hamiltonian
- the fitted `gamma ≈ 1` is therefore a response to an encoded bilinear kernel,
  not yet a derivation of `M1*M2` from a source-only law

Concretely, this toy surface cannot move the factor out of the interaction
without changing the Hamiltonian class:

- if `s1*s2` is removed from `V`, the exact two-body run no longer has a
  bilinear source-response channel to fit
- if `s1*s2` stays in `V`, then the observed `gamma ≈ 1` is always compatible
  with the kernel assumption and cannot certify emergence
- on this 1D open-boundary surface there is no frozen/static-source control that
  isolates a source-only field while preserving the same exact two-particle
  observable

So the current toy model can prove exact-vs-Hartree separation, but it cannot
prove an emergent product law unless the interaction ansatz is redesigned.

There is also a model mismatch relative to the retained mainline Newton work:

- this is a 1D open-boundary toy lattice
- it is not the primary staggered/open-cubic architecture retained on `main`
- there is no frozen/static-source control that removes the built-in bilinear
  kernel and checks whether the product law survives as a dynamical outcome

## What This Lane Does Establish

This lane is still valuable as a bounded control:

- exact two-particle dynamics can differ from Hartree at strong coupling
- the observable used here is not a mean-field artifact
- the exact solver is a better comparator than the earlier Hartree-only lane

That makes it a useful frontier control. It does **not** make it a mainline
Newton product-law result.

## Required Next Experiment

To promote anything from this lane, the next experiment must remove the product
factor from the ansatz and re-test the response under controls:

1. Use a source-only kernel or self-consistent field update where the mass
   product is not already present in `V(x1, x2)`.
2. Add a frozen/static-source control alongside the exact two-body evolution.
3. Replay the same observable on the primary staggered/open-cubic surface, or
   explicitly justify why this 1D lane is the correct retained architecture.

Only if the `M1*M2` scaling survives after those controls should the lane be
retained as a bounded companion on `main`.

## Closest Retainable Claim

Retain only the exact-vs-Hartree comparison as a bounded control result.
Hold the product-law headline until a source-only interaction or equivalent
control removes the bilinear factor from the ansatz on a promotable surface.

## Suggested Control-Plane Wording

> Frontier exact two-particle diagonalization shows exact-vs-Hartree
> divergence and a clean bilinear response on a toy 1D lattice, but the
> `M1*M2` factor is encoded in the interaction ansatz. This is not yet an
> emergent Newton product law and remains frontier-only until a source-only
> control and a primary-architecture replay are completed.
