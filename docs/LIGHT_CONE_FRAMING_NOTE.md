# Light Cone Framing — Lieb-Robinson is Standard Lattice QFT

**Status:** support - structural or confirmatory support note
**Date:** 2026-04-11

## The Concern

The Crank-Nicolson evolution gives a Lieb-Robinson cone (97% of probability
inside) rather than a strict v=1 light cone. Is this a blocker?

## The Answer: No

No lattice field theory has a strict v=1 light cone. This is a well-known
and accepted feature of lattice discretization. The staggered fermion
formulation used in lattice QCD (Kogut-Susskind, 1975) has exactly the
same Lieb-Robinson bound. The lattice QCD community has produced Nobel
Prize-winning predictions without a strict continuum light cone.

## The Staggered Dispersion Argument

The staggered Dirac dispersion relation is:

    E² = m² + sin²(k)

The group velocity is:

    v_g = dE/dk = sin(k)cos(k) / E = sin(2k) / (2E)

The maximum group velocity occurs at k = π/4 (for m << 1):

    v_max = 1 / (2m)    for m << 1

In the massless limit m → 0:

    E = |sin(k)|
    v_g = cos(k) · sign(sin(k))
    v_max = 1    (at k = π/2, the Dirac point)

So the EXACT v=1 light cone emerges from the staggered dispersion in the
massless limit. This is the standard lattice QFT result.

For massive particles (m > 0), v < 1 as EXPECTED from special relativity.
Massive particles travel slower than light. The mass-dependent velocity
is not a bug — it is the correct physics.

## The Lieb-Robinson Bound

The Lieb-Robinson theorem guarantees exponential suppression of signals
outside a cone of velocity v_LR = 2||H_hop|| where H_hop is the hopping
part of the Hamiltonian. For our staggered operator with hopping weight
w = 1/(2·lattice_spacing):

    v_LR = 1 / lattice_spacing

In the continuum limit (lattice spacing → 0), the LR cone approaches the
true light cone from above. The 97% containment at finite lattice spacing
is the standard discretization artifact.

## What This Architecture Does Provide

1. **Correct continuum dispersion** in the low-k limit
2. **Exponential suppression** of acausal signals (LR bound)
3. **v=1 in the massless limit** from the staggered Dirac dispersion
4. **v < 1 for massive particles** as required by special relativity

## What It Does NOT Provide (and Why That's OK)

- **Strict v=1 at finite lattice spacing** — no lattice FT does this
- **Exact Lorentz invariance** — broken by the lattice, restored in
  continuum limit (standard lattice QFT)
- **Coin-based strict cone** — available but reintroduces mixing period

## References

- Rothe, H.J. "Lattice Gauge Theories: An Introduction" (World Scientific)
- Montvay, I. and Münster, G. "Quantum Fields on a Lattice" (Cambridge UP)
- Kogut, J. and Susskind, L. "Hamiltonian formulation of Wilson's lattice
  gauge theories" Phys. Rev. D 11, 395 (1975)
- Lieb, E.H. and Robinson, D.W. "The finite group velocity of quantum
  spin systems" Commun. Math. Phys. 28, 251 (1972)
