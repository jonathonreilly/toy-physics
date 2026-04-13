# R Is a Direct Observable of H, Not a Chain Through g -> alpha_s -> sigma_v

**Date:** 2026-04-13
**Branch:** `claude/youthful-neumann`
**Scripts:** `scripts/frontier_dm_sigma_v_lattice.py`
**Lane:** DM relic mapping
**Resolves:** DM Blocker 1 (g_bare = 1 invariance question)

---

## Status

**BOUNDED** -- sharpens the invariant bridge to its minimal form.

This note argues that the g_bare = 1 question, as originally posed, rests
on a false premise: that the DM relic ratio R depends on a "coupling
constant" as a separate parameter. It does not. R is a direct observable
of the Hamiltonian H. The coupling is not an input to R -- it is an
intermediate label humans apply to a property of H.

---

## The Blocker, Restated

Codex's objection:

> "g_bare = 1 is not yet shown to be invariantly the same physical
> coupling that later enters annihilation / relic calculations."

This presupposes a chain:

    g_bare  -->  alpha_s  -->  sigma_v  -->  R

where g_bare is an input parameter, alpha_s is extracted from it, sigma_v
is computed from alpha_s, and R follows. The concern is that g_bare might
be a convention, making alpha_s ambiguous, making R ambiguous.

---

## The Resolution: Two Routes to sigma_v

### Route A: Through the plaquette coupling

This is the chain the blocker targets:

    H = sum eta_ij U_ij       (coefficient 1 is the framework)
         |
    generate equilibrium configs
         |
    measure <P>
         |
    extract alpha_V = -ln(<P>) / c_1
         |
    compute sigma_v = pi * alpha_V^2 / m^2   (Born cross section)
         |
    compute R = Omega_DM / Omega_b

Route A does invoke an intermediate "coupling" alpha_V. But alpha_V is
not an independent parameter -- it is a measurement on H. The invariant
bridge note (DM_INVARIANT_BRIDGE_NOTE.md) already showed that this chain
has no free normalization: given H, alpha_V is uniquely determined, so
sigma_v and R are uniquely determined.

The remaining question in Route A is: why does H have coefficient 1?
That is a foundational commitment.

### Route B: Through the lattice T-matrix (direct)

Route B eliminates the intermediate coupling entirely:

    H = H_0 + V              (lattice Hamiltonian)
         |
    define incoming state |psi_i> with lattice momentum k
         |
    compute T(z) = V + V * G(z) * V    where G(z) = (z - H)^{-1}
         |
    apply optical theorem: sigma_v = Im[<k|T(E + i*eps)|k>]
         |
    compute R from sigma_v

In Route B:

- sigma_v is computed as a matrix element of the lattice T-matrix.
- The T-matrix is built from the resolvent of H.
- The resolvent depends on H and nothing else.
- No "coupling constant" appears as a separate quantity.
- sigma_v is an observable of H in exactly the same sense that an
  energy eigenvalue or a correlation length is.

The optical theorem (Im T = T^dag T) follows from unitarity of the
S-matrix, which is automatic for any Hermitian H on a finite lattice.
This is a lattice identity, not a perturbative result.

Route B is implemented and verified in `frontier_dm_sigma_v_lattice.py`
(Approach 1), which demonstrates the optical theorem on finite lattices
with multiple sizes, momenta, and coupling strengths. The Lippmann-
Schwinger T-matrix and the exact contact-interaction formula agree to
machine precision.

---

## Why This Dissolves the g_bare Question

The blocker asks: is g = 1 "invariantly the same physical coupling" that
enters sigma_v?

Route B shows this question is ill-posed. There is no separate "coupling"
that enters sigma_v. The chain is:

    H  -->  T(z) = V + V*G(z)*V  -->  sigma_v = Im[<k|T|k>]

The quantity g = 1 is part of the definition of H. It is not a separate
parameter that must be "bridged" to sigma_v. It is embedded in H, which
determines T(z), which determines sigma_v, which determines R. The bridge
is the identity map: H is H.

To make this concrete:

1. Define H = sum eta_ij U_ij on the lattice. (This is the framework.)
2. Split H = H_0 + V where H_0 is the free part and V is the interaction.
3. Compute T(z) = V(I - G_0 V)^{-1} where G_0 = (z - H_0)^{-1}.
4. sigma_v = Im[<k|T(E + i*eps)|k>].

At no step does a "coupling constant" appear as a free parameter. The
interaction V is a piece of H, not parameterized by an independent g.

If someone changed the coefficient in H (say H' = 2 * sum eta_ij U_ij),
that would be a DIFFERENT Hamiltonian with DIFFERENT physics. It would
give a different T-matrix, a different sigma_v, and a different R. The
coefficient is not a convention -- it is part of the identity of the
theory. But this is just the statement that H is what it is.

---

## Relationship to Route A

Routes A and B must agree for the framework to be self-consistent.
Route A extracts an intermediate quantity alpha_V from <P> and feeds it
into sigma_v = pi * alpha_V^2 / m^2. Route B computes sigma_v directly
from the T-matrix.

In the weak-coupling (Born) limit, these agree:

- Route B at Born level: sigma_v ~ Im[<k|V*G_0*V|k>] ~ alpha^2 * rho(E)
- Route A: sigma_v = pi * alpha_V^2 / m^2

The Born approximation of the lattice T-matrix IS the Feynman diagram
calculation, just done directly on the lattice. The two routes are not
independent physical assumptions -- they are the same computation in
different languages.

Beyond Born level, Route B (non-perturbative T-matrix) is the more
fundamental object. Route A (Born cross section with extracted coupling)
is its leading-order approximation.

---

## What This Achieves

1. **Eliminates the normalization gap.** The blocker asked whether g = 1
   in H invariantly determines sigma_v. Route B shows sigma_v depends on
   H directly, not on a separately defined coupling. The gap does not
   exist.

2. **Reduces the bounded input to one.** The only input that remains
   bounded is: why is the framework Cl(3) on Z^3 with H = sum eta_ij U_ij
   rather than some other theory? This is the foundational commitment
   (framework premise), not a coupling-constant ambiguity.

3. **Aligns with Codex's framework-premise rule.** Codex accepts the
   framework premise "Cl(3) on Z^3 is the physical theory." The
   Hamiltonian H = sum eta_ij U_ij is part of that premise. If the
   framework premise is accepted, then H is fixed, and R follows as
   a direct observable.

---

## What This Does NOT Achieve

1. **Does not derive H from more primitive principles.** Why coefficient 1
   and not some other value? This is not answered. It is the same question
   as "why this theory?" -- a foundational commitment.

2. **Does not close the cosmological cancellation.** The ratio
   R = Omega_DM / Omega_b involves cosmological factors (H(T), g_*, etc.)
   whose cancellation is asserted but not derived at theorem grade.

3. **Does not close the Boltzmann/Stosszahlansatz bridge.** The
   coarse-graining from microscopic dynamics to the Boltzmann equation
   is improved but not fully internalized.

4. **Does not promote the DM lane to EXACT.** The lane remains BOUNDED
   with precisely identified residual inputs.

---

## Summary

The DM relic ratio R is a direct observable of the Hamiltonian H:

    H  -->  T-matrix  -->  sigma_v  -->  R

There is no separate "coupling constant" that must be independently
bridged from the Hamiltonian to the cross section. The quantity g = 1
is part of the definition of H, not a parameter that enters sigma_v
through a separate channel.

The question "is g = 1 invariantly the same coupling that enters sigma_v?"
dissolves: g = 1 does not enter sigma_v at all. H enters sigma_v, and
g = 1 is part of what makes H what it is.

The DM lane remains BOUNDED. The irreducible bounded input is the
framework commitment H = sum eta_ij U_ij, not a coupling-constant
ambiguity.

---

## Commands

```
python scripts/frontier_dm_sigma_v_lattice.py
```
