# Cycle 01 — Route R3: Clifford-volume chirality from sublattice parity

**Date:** 2026-05-02
**Route attempted:** R3 (chirality grading via sublattice parity ε(x))
**Goal:** Re-classify admission #3 as a structural Cl(3)/Z^3 fact
rather than a literature import on Cl(p,q) volume elements.

## Context

The bounded theorem invokes Lawson-Michelsohn (1989) for the Cl(p,q)
volume-element classification: in n=p+q generators, ω = γ_1 ... γ_n
satisfies ω γ_μ = (-1)^{n-1} γ_μ ω, so chirality requires n even.

In our framework, this argument is *replaceable* by structural facts about
Cl(3) on Z^3 that are already retained-clean.

## The replacement argument

The framework's chirality grading is **not** an abstract Cl(p,q) volume
element. It is the **sublattice parity**

```
    ε(x) = (-1)^{x_1 + x_2 + x_3}  on  Z^3.
```

The retained CPT note explicitly identifies ε(x) as the staggered γ_5:

> "Chirality: Even/odd sublattice = staggered gamma5."
> (`STAGGERED_FERMION_CARD_2026-04-10.md`, line 129)
> 
> "C operator: The sublattice parity epsilon(x) = (-1)^{x1+x2+x3}
> is a real, diagonal, involutory operator..."
> (`CPT_EXACT_NOTE.md`, line 52)

Two retained-clean facts close the chirality grading argument:

**Fact A (Cl(3) per-site).** From
`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29` (retained-clean):
the on-site Cl(3) spinor irrep has dim_C = 2; it is the Pauli irrep, unique
up to unitary equivalence. The on-site Hilbert space is exactly C^2.

**Fact B (Z^3 sublattice parity).** From `CPT_EXACT_NOTE` (retained-clean)
and `STAGGERED_FERMION_CARD_2026-04-10` (retained_bounded): on Z^3,
ε(x) = (-1)^{x_1+x_2+x_3} is a global involution that splits the lattice
into two sublattices Λ_e, Λ_o. The CPT theorem proves
ε^2 = +I, ε is diagonal, real, and involutory. It anticommutes with the
nearest-neighbor staggered Dirac operator D in the sense
ε D ε = -D (this is the C-symmetry equation P^2 = +I, C H C = -H in
the CPT note).

## What this gives

The full per-site fermion Hilbert space at site x is
H_x = C^2 (Cl(3) spinor) — a 2-dim Pauli irrep — with an additional
Z_2 grading provided by ε(x), which acts on the global Hilbert
space H = ⊕_x H_x = ⊕_x C^2 by

```
    Γ_5 := ⊕_x ε(x) · I_{C^2,x}.
```

This Γ_5 is:
- diagonal in the position basis (because ε(x) is a function of x);
- involutive: Γ_5^2 = +I (because ε(x) ∈ {±1});
- anticommuting with the staggered Dirac operator D:
  D = i Σ_μ η_μ(x) (translation), and
  ε(x) η_μ(x) ε(x±μ) = -η_μ(x) on each link → Γ_5 D Γ_5 = -D.

So **Γ_5 is a Z_2 chirality grading** on the lattice fermion Hilbert
space, derived directly from:
- Cl(3) per-site uniqueness (retained-clean), giving C^2 fibers;
- Z^3 bipartite structure (axiom A2), giving the global involution ε(x);
- staggered Dirac construction (retained_bounded), giving the
  anticommutation Γ_5 D Γ_5 = -D.

## What replaces the Cl(p,q) volume-element argument

The bounded note's Step 3 said: "chirality requires d_total = d_s + d_t
even, hence d_t odd."

In the framework, this becomes the more direct statement:

> **The Cl(3)/Z^3 chirality grading is the sublattice parity ε(x). Its
> existence requires Z^3 to be bipartite — which is automatic for the
> cubic lattice in three spatial dimensions — and the per-site irrep to
> have a definite parity assignment, which Cl(3) per-site uniqueness
> supplies. No appeal to a Cl(p,q) volume element with n = p+q is
> needed.**

The framework's chirality grading is therefore a structural fact about
Cl(3) on Z^3 itself, not a literature import.

## What the bounded note still wants from this step

Step 3 of the bounded theorem uses the chirality argument for two
things:

(a) Existence of γ_5 (Z_2 chirality grading on the spinor module).
(b) The constraint that "n_total must be even" from ω anticommuting
    with all γ_μ when n is even.

(a) is fully replaced by the sublattice parity argument above —
**retained-clean closed**.

(b) is the part that ties chirality to spacetime *dimension* — and on
the lattice, this argument *also* changes. The lattice version is:
the bipartite structure of Z^3 already exists *before* time is added.
Adding d_t time directions corresponds to adding d_t generators
of the form γ^0_a, a = 1...d_t, that anticommute with the spatial
γ^i (i=1,2,3). The full Clifford algebra of the spacetime spinor
module then has 3 + d_t spatial+temporal generators, and the
**effective bipartition / chirality grading on the spacetime spinor
module** is ε(x) ⊗ ε_t(t), where ε_t(t) is the analogous bipartition
of the time direction. This requires 3 + d_t to be even (same conclusion).

But, crucially, in *our* framework time is not a lattice generator.
Time enters only via the single-clock Hamiltonian U(t) = exp(-itH).
There is **no spacetime Cl(3+d_t)** in the framework's Hilbert
construction; there is only Cl(3) on the spatial Z^3 graph plus a
one-parameter unitary group.

This means the chirality argument **does not directly constrain d_t**
in the framework. The constraint on d_t comes from a different place
(see Cycle 4, Route R4 — single-clock + microcausality).

## Outcome of Cycle 1 (Route R3)

**Closed:** the framework has a structural Cl(3)/Z^3 chirality grading
ε(x) on retained-clean inputs (Cl(3) per-site uniqueness + CPT note +
Z^3 bipartite structure). The Lawson-Michelsohn Cl(p,q) volume-element
literature import is *replaceable* by these in-framework retained facts.

**Re-classification:** admission #3 ("Clifford-volume chirality") becomes
a Cl(3)/Z^3 structural fact, not a literature import. The term
"Clifford volume element" can be dropped from the bounded theorem and
replaced with "sublattice parity ε(x) on Z^3, which is the staggered γ_5
of the retained CPT theorem."

**Subtle item exposed:** the bounded theorem's Step 3 conclusion
("d_total = d_s + d_t even") relies on a *spacetime* Clifford structure
that the framework does not have. The framework's chirality lives entirely
on the *spatial* Cl(3)/Z^3 surface; d_t is constrained by *single-clock
unitarity*, not by spacetime Clifford volume parity. This is an honest
finding that *strengthens* the theorem's framework-internal coherence.

**Status of admission #3:** closed by re-classification as Cl(3)/Z^3
structural fact. **No literature import needed.**

The accompanying re-write of the theorem's Step 3 (in the synthesis
cycle) replaces the Cl(p,q) parity argument with the sublattice parity
argument, and re-routes the d_t constraint to Step 4.
