# Route Portfolio — 3+1d Retained-Positive

Each of the 4 admissions is a separate route. Closure of any subset
narrows the bounded scope.

## Route R1 — ABJ Inconsistency derived for the framework's gauge content

**Strategy:** Re-cast the ABJ argument as a *finite-lattice* statement on
Cl(3)/Z^3 rather than as a continuum import. Specifically:

- Use lattice ABJ identities (Karsten-Smit, Wilson) on the staggered surface.
- Show that on the framework's accepted Hilbert/locality surface, the
  axial current divergence is forced to be nonzero by the same trace
  arithmetic that the Cl(3) generators give.
- The "violation of unitarity" is recast as: gauge-noninvariance of the
  partition function is forced by the framework's own anomaly traces, and
  gauge-noninvariance is forbidden by the Hilbert/locality surface (gauge
  invariance is the definition of physical states).

**Confidence:** medium-high. The lattice ABJ form on staggered fermions is
well-known and the framework already has the trace arithmetic retained.

## Route R2 — Singlet completion uniqueness from Cl(3)/Z^3 structure

**Strategy:** The space of allowed RH completions is constrained by:
- The Cl(3) per-site uniqueness theorem (per-site Hilbert dim is exactly 2).
- The retained native gauge closure (SU(2) × SU(3) × U(1) gauge sector
  has no additional gauge factor available).
- The bipartite graph structure (no Green-Schwarz axion-like modes
  available without leaving A_min).

The argument should show: any RH completion that cancels anomalies and
fits into the Cl(3) per-site structure is necessarily a set of SU(2)
singlets (potentially with SU(3) triplet color) with hypercharges fixed
by the cancellation equations.

**Confidence:** medium. The "no additional gauge factor" step is bounded
support, not retained-positive.

## Route R3 — Clifford-volume-chirality from Cl(3) per-site uniqueness + sublattice parity

**Strategy:** This is the most directly tractable. The framework's chirality
grading is *not* an abstract Cl(p,q) volume element argument; it is the
sublattice parity ε(x) = (-1)^(x1+x2+x3) on Z^3, a structural fact of the
bipartite cubic lattice. The CPT note (retained-clean) explicitly identifies
ε(x) as "the staggered gamma_5".

So the theorem statement "chirality requires the spinor index dimension to
be even" can be re-derived using:
- Cl(3) per-site spinor irrep dim = 2 (retained).
- Sublattice parity ε(x) on Z^3 (structural, retained as "staggered gamma_5").
- The full Hilbert space at one site = 2 × (sublattice index) = 4-dim
  effective spinor that *factorizes* into 2 × 2.

The "Clifford volume element" mechanism becomes a corollary of the
**bipartite Z^3 structure** plus the **Cl(3) per-site uniqueness**.
This route effectively re-classifies admission #3 from "literature volume
element argument" to "Z^3 sublattice + Cl(3) uniqueness, both retained-clean."

**Confidence:** high. This is structural in the framework already.

## Route R4 — Ultrahyperbolic Cauchy obstruction recast as lattice causality

**Strategy:** Use the retained `axiom_first_microcausality_lieb_robinson_theorem_note_2026-05-01`
as the load-bearing input. On Z^3 with one Hamiltonian U(t)=exp(-itH), the
Lieb-Robinson bound forces a unique propagation cone with one
time direction. Adding a second time-like Hamiltonian H' with [H,H']≠0 in
general gives a multi-time evolution group; consistency of *both* clocks on
arbitrary local initial data on a single codimension-1 slice is a
contradiction with the LR bound's uniqueness.

Specifically: the framework axiom A4 (Hilbert/locality/information,
retained on the one-axiom surface) gives one unitary group U(t).
A two-clock evolution requires two commuting U(t1), U(t2) with shared
Hamiltonian generators that both satisfy LR cones; on Z^3, the only
LR-compatible single propagation cone has codim-1 slice = 3-dim.

This recasts the ultrahyperbolic obstruction from continuum
Craig-Weinstein PDE theory into **single-clock unitarity on the framework's
own retained surface** — and that already is part of the theorem's
hypothesis (assumption 1).

**Confidence:** medium-high. The reduction is essentially: assumption 1
*already does the work* of the ultrahyperbolic argument, because
single-clock = exactly one Hamiltonian → exactly one time direction at the
graph level. The continuum Craig-Weinstein bridge becomes redundant.

## Score & Order

Take routes in order of increasing difficulty:
1. **R3** (chirality from sublattice parity + Cl(3) per-site uniqueness):
   most likely to close clean. Try first.
2. **R4** (Cauchy from single-clock + microcausality):
   next-most likely; mostly a re-statement.
3. **R1** (ABJ-to-inconsistency on the lattice):
   medium difficulty; lattice ABJ is well-known but framework-internal
   adaptation needed.
4. **R2** (singlet uniqueness):
   hardest; "no other anomaly-cancelling completion in this framework"
   needs an exhaustion argument.

Synthesis cycle re-writes the note with whatever closes; bounded scope
documented for the rest.
