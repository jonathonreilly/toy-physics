# Cycle 02 — Route R4: Ultrahyperbolic obstruction recast as
# single-clock unitarity

**Date:** 2026-05-02
**Route attempted:** R4
**Goal:** Replace literature ultrahyperbolic / Craig-Weinstein PDE
obstruction with a framework-internal argument using only retained-clean
inputs and the theorem's own assumption 1 (single-clock unitarity).

## Context

The bounded theorem's Step 4 invokes Craig-Weinstein 2009 / Tegmark 1997:
for d_t > 1, the wave equation is ultrahyperbolic; codimension-1
well-posedness fails for arbitrary local data. This is currently a
literature import.

## The replacement argument: single-clock = exactly one time direction

The bounded theorem's hypothesis already states (assumption 1):

> "states evolve by a single strongly continuous unitary one-parameter
> group U(t) = exp(-itH)."

This is a one-parameter group — meaning the parameter space is R, not
R^k for k > 1. By construction, there is **exactly one** t-axis.

Furthermore, the framework's Hilbert/locality/information surface (one
axiom reduction, retained per `physical_lattice_necessity_note`) gives:
**graph and unitary are one irreducible physical object**. The
Hamiltonian H is defined on the Z^3 graph; the parameter t is the
unique evolution parameter conjugate to H.

If we wanted d_t > 1, we would need d_t commuting one-parameter unitary
groups U_a(t_a) = exp(-i t_a H_a), a = 1...d_t, with [H_a, H_b] = 0
(so that joint evolution is well-defined). The bounded theorem's
assumption 1 forbids this directly: it says **one** strongly continuous
unitary one-parameter group, not d_t of them.

So the Step 4 argument simplifies to:

```text
Assumption 1 (single-clock unitary one-parameter group)
   ⇒ exactly one independent time direction
   ⇒ d_t = 1.
```

There is no need to invoke the ultrahyperbolic Cauchy obstruction at all.

## Why does the bounded version invoke Cauchy?

The bounded version invokes Cauchy because it wants to *exclude* d_t > 1
for hypothetical alternative continuum limits where someone might try
to add a second clock. But:

(i) Step 3 (Cl(p,q) chirality argument) admits d_t ∈ {1,3,5,...}
    odd — so the bounded note feels the need to additionally exclude
    d_t = 3, 5, etc.

(ii) Step 4's role is then to rule out d_t > 1 by appeal to
     codimension-1 Cauchy well-posedness.

In the **R3-revised** version of Step 3 (Cycle 1), the Cl(p,q) argument
is replaced by the sublattice-parity argument, which does **not** force
d_t to be odd. Instead, the framework's chirality grading lives
entirely on the spatial Cl(3)/Z^3 surface, and time enters only via
the single-clock Hamiltonian.

So in the R3-revised structure, the chirality argument no longer
constrains d_t at all; the d_t constraint comes entirely from
single-clock unitarity (assumption 1).

## What this gives

**The "ultrahyperbolic Cauchy obstruction" admission is not needed.**

The R3 + R4 combination shows:

```text
chirality (R3) constrains the spatial Cl(3)/Z^3 surface,
not d_t directly;

single-clock unitarity (assumption 1) directly forces d_t = 1.
```

This is *cleaner* than the bounded version: it doesn't go through Cl(p,q)
parity → d_t odd → Craig-Weinstein → d_t = 1. It just goes
**single-clock → d_t = 1** in one step.

## Outcome of Cycle 2 (Route R4)

**Closed:** admission #4 (ultrahyperbolic Cauchy obstruction) is shown
**dispensable**. With the R3-revised Step 3, single-clock unitarity
(assumption 1) directly fixes d_t = 1. The Craig-Weinstein /
Tegmark literature import is not used.

**Status of admission #4:** dispensable (case (c)). The theorem closes
without it, given the R3 revision.

**Open question for the synthesis:** does the theorem still want a
"d_t > 1 alternatives are mathematically inconsistent" defense? The
honest answer is: the theorem's own assumption 1 *defines* the framework
to have one clock; the question of whether d_t > 1 alternatives are
physically consistent in *general* is a different question (and one that
*does* require the Craig-Weinstein argument). The bounded theorem can
keep that as a remark, but it is not load-bearing.

## Caveat / honest limitation

If a critic challenges assumption 1 itself ("why must the framework have
a single clock?"), then the framework needs to defend assumption 1 from
deeper primitives. The strongest available answer is:

- on the accepted Hilbert/locality/information surface
  (`physical_lattice_necessity_note`, retained as bounded support, also
  cited as no-go classification), graph and unitary are one irreducible
  physical object;
- the Stone theorem on the Hilbert space gives a *unique* self-adjoint
  generator H for a one-parameter unitary group;
- the framework's Hamiltonian is a specific operator on the lattice
  Hilbert space, and there is no second commuting generator with an
  independent t' parameter that the framework constructs.

So assumption 1 is a *structural consequence* of the Hilbert/locality/
information surface, not an external postulate. **But this consequence
is not yet itself retained-positive on the actual current surface** —
`physical_lattice_necessity_note` is currently `unaudited` with a
`no_go` claim_type, and the one-axiom Hilbert/locality/information note
is also not retained-clean.

So the honest summary is:

- **Closed at theorem level**: the ultrahyperbolic Cauchy obstruction is
  dispensable; assumption 1 alone gives d_t = 1.
- **Open at hypothesis level**: assumption 1 itself is currently a
  framework axiom rather than a derived consequence on retained-clean
  primitives.

This is a *narrowing* of the bounded scope — the residual admission is
no longer about ultrahyperbolic PDE theory; it is about whether the
framework's "single clock" hypothesis is itself derivable from deeper
retained primitives. The new bounded scope is much narrower.
