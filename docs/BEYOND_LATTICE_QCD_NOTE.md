# Beyond Lattice Gauge Theory: Two Concrete Results

**Status:** bounded review candidate  
**Script:** `scripts/frontier_beyond_lattice_qcd.py`

## The honest overlap

Both lattice gauge theory and this graph-first framework use graphs,
Laplacians, path integrals, and gauge phases. This overlap is real and
must be acknowledged. The distinction argued here is not just "derivation
direction." The bounded case made here is two concrete structural differences
on the audited surfaces below.

## Result 1: Gravity-QM inseparability

**What we show:** The gravitational field (Poisson potential sourced by
|psi|^2) modifies the propagator's quantum structure in ways that go
beyond simple deflection. Specifically, on a 32^3 lattice:

| Measure | Free (f=0) | With gravity | Change |
|---------|-----------|-------------|--------|
| Y-centroid at detector | 15.99 | 19.95 | +3.96 (deflection) |
| Profile shape diff (L2, centroid-aligned) | -- | 0.352 | Nonzero |
| RMS spread | 4.52 | 2.85 | -1.67 (focusing) |
| Fringe visibility | 0.29 | 0.98 | +0.69 (coherence change) |

The shape difference after centroid alignment is 0.35 -- gravity does not
merely shift the propagator, it changes its coherence structure.

**Why lattice QCD cannot do this:** In lattice QCD, the lattice is a fixed
computational scaffold. The lattice spacing `a` is a UV regulator that gets
sent to zero in the continuum limit. The lattice itself has no gravitational
content -- it cannot lens, focus, or modify quantum coherence. Quantum fields
live ON the lattice, but the lattice is inert.

In this framework, the action S = L(1-f) couples the quantum phase directly
to the Poisson potential. The graph IS the gravitational field. There is no
separable "lattice" that can be removed while keeping quantum mechanics intact.

**Bounded claim:** The graph-first framework produces gravity-QM coupling
from a single structure. Lattice QCD requires gravity to be added as a
separate theory (lattice quantum gravity is a different program entirely,
and does not use the same lattice as lattice QCD).

## Result 2: Structural Born rule (Sorkin I_3 = 0)

**What we show:** The path-sum propagator on the graph produces Sorkin
parameter I_3 = 0 to machine precision (~10^-16) across all tested
wavenumbers (k = 2 to 20) and slit spacings (2 to 5).

The Sorkin parameter measures third-order interference:
I_3 = P_ABC - P_AB - P_AC - P_BC + P_A + P_B + P_C

I_3 = 0 means all interference is pairwise, which is equivalent to the
Born rule (probability = |amplitude|^2).

A nonlinear (cubic) propagator gives I_3/P = 0.16, confirming the test
has discriminating power -- it can detect violations of the Born rule
when they are present.

**Why this differs from lattice QCD:** In lattice QCD (and all standard QFT),
the Born rule is an axiom of quantum mechanics. The path integral computes
amplitudes; the postulate that probabilities = |amplitudes|^2 is separate.
Lattice QCD does not derive the Born rule -- it assumes it.

In this framework, the path-sum propagator is a linear superposition of
complex amplitudes over graph paths. The linearity of this sum forces
I_3 = 0 as a mathematical identity. The Born rule is a theorem, not a postulate.

**Bounded claim:** The Born rule follows from linearity of the path-sum.
This is a structural property of the framework, not an input. (We
acknowledge that this argument is related to Gleason's theorem and the
general structure of Feynman path integrals -- the novelty is that it
emerges from the graph structure without assuming a Hilbert space.)

## Claim boundary

- reviewer-facing differentiation note, not a standalone retained physics claim
- gravity-QM inseparability is demonstrated on the tested ordered-cubic surface
- structural Born-rule point is a framework-level linearity result with explicit
  Sorkin diagnostics, not a claim of uniqueness over all path-integral formalisms

## What this does NOT claim

- We do not claim lattice QCD is wrong or that its results are invalid.
- We do not claim this framework can reproduce lattice QCD's precision
  predictions for hadron spectra, quark confinement, etc.
- We do not claim the dimension emergence result (d_s = 3 special) is
  unique to this framework -- that result depends on lattice topology
  and could be obtained in other graph-based approaches.

## Reviewer FAQ

**Q: Isn't the gravity-QM coupling just a semiclassical approximation?**
A: The coupling S = L(1-f) with f sourced by |psi|^2 is indeed
semiclassical. But the point is that this coupling is built into the
graph structure -- it is not an add-on. Lattice QCD has no analogous
coupling at any level of approximation.

**Q: Isn't the Born rule result just Feynman's path integral argument?**
A: Partially. Feynman showed that linear superposition of amplitudes
implies Born rule statistics. Our contribution is showing this concretely
on a graph propagator with explicit Sorkin tests, and combining it with
the gravity-QM coupling to get a package that lattice QCD cannot replicate.

**Q: Can't you just add gravity to a lattice?**
A: Not in the same way. Lattice quantum gravity is a separate research
program (e.g., causal dynamical triangulations, Regge calculus). It uses
different lattices with different purposes than lattice QCD. The point is
that this framework gets both from the SAME structure.
