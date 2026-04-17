# Nature-Level Discovery — Ranked Directions After Full Synthesis

**Date:** 2026-04-11
**Source:** Cross-architecture repo audit + 15-direction Opus brainstorm + session results

## What We Now Have (After This Session)

1. Parity coupling correction (literature contribution)
2. 17/17 canonical card with sign-selective well/hill test
3. Self-gravity contraction 9/9 (w=0.40-0.76)
4. Weak-coupling sign-sensitive regime `14/15` on irregular graphs (G=5-10)
5. Historical/path-sum geometry-superposition signal at `4.37%` contrast
6. Field equation justified variationally at lowest local quadratic order
7. Light cone framed as standard lattice QFT
8. Full suite 29/38 (1D), 28/38 (3D)

## Tier 0: Reframe (No Code — Pure Argument)

### Direction 0: B1 Is Not a Bug — It IS Discrete General Covariance

The sign-absorption by epsilon(x) on irregular graphs is the discrete analog
of diffeomorphism invariance. On a bipartite graph, multiple valid staggering
assignments (different epsilon fields) exist. The physics should be
independent of which staggering is chosen — this IS a gauge symmetry.

The gauge-invariant observables are: contraction ratio, spectral gap shift,
binding energy, correlation length, critical exponents. These are ALL
sign-selective (attract contracts more, wider gap, topology-dependent beta).
The "force direction" is the gauge-dependent part — like a coordinate choice.

Reframe: "Gravity on discrete structures is not a force with a direction.
It is a topological phase transition whose universality class depends on
graph topology. The sign-freedom of the parity coupling is the discrete
analog of coordinate freedom in general relativity."

This is a provocative theoretical argument, but it is not yet a retained repo
claim. Treat it as a speculative framing until it is backed by a stronger
frozen observable stack.

## Tier 1: Immediate Computation (Existing Code + Modest Extension)

### Direction 1: Entanglement Entropy — Area Law from Self-Gravity

Compute von Neumann entropy of a spatial bipartition of the self-gravitating
staggered field. Does S scale with boundary area or volume?

- Free propagator: area law expected (standard lattice FT)
- Self-gravitating: does gravity modify the prefactor? If so, connects
  to Bekenstein-Hawking. If gravity introduces a log correction, connects
  to the central charge.

**Effort:** Low. CN evolution exists. Bipartition is straightforward.
Eigensolve of reduced density matrix for n<=64 on graphs.

### Direction 2: Topology-Dependent Critical Exponents (Extension)

Extend the existing beta probe to more families and sizes for proper
finite-size scaling collapse. Check whether beta correlates with known
graph invariants (spectral gap, Cheeger constant, genus).

If different families collapse onto DIFFERENT master curves, that confirms
a new kind of universality class where topology enters the exponent —
unprecedented in statistical physics.

**Effort:** Low. Infrastructure exists. Need more data points.

### Direction 3: Gravitational Decoherence Rate (Experimental Prediction)

Place a mass in a superposition of two locations on the staggered lattice.
Compute the rate at which off-diagonal elements of the density matrix decay.
Map Gamma(m, r, G) and compare to Diosi-Penrose.

A prediction distinguishable from Diosi-Penrose would be directly testable
by tabletop experiments (Bouwmeester, Arndt, Aspelmeyer groups).

**Effort:** Medium. Self-gravity loop exists. Need density matrix tracking.

### Direction 4: Geometry Superposition — Extend and Quantify

The currently rerunnable result is a **path-sum DAG-ensemble** signal at about
`4.4%` coherent-vs-incoherent contrast with detector-phase differences up to
about `0.26 rad`. That is real, but it is not a staggered result. Extend:
- Multiple source positions and strengths
- Quantify the gravitational phase shift dphi vs source parameters
- Build the actual staggered geometry-superposition harness instead of relying
  on the older path-sum ensemble script
- Verify TVq (quantum vs classical) scales with source strength
- Connect to BMV experiment design: what mass/separation would produce
  detectable entanglement via geometry superposition?

**Effort:** Low. Script exists. Need parameter sweeps.

## Tier 2: Medium-Effort Extensions

### Direction 5: Z2 Sublattice = Mirror Decoherence Protection

The mirror Z2 proved decoherence protection (MI=0.773, 6x random). The
staggered sublattice parity IS a Z2 symmetry. Test whether it provides
the same rank-2 channel preservation.

### Direction 6: Quantum Zeno from Self-Gravity

Tune self-gravity coupling continuously. At weak G: quantum spreading.
At strong G: Zeno localization. The critical G should be topology-dependent
(connecting to the critical exponents). In the Zeno regime, does the
localized packet follow a geodesic? → discrete derivation of classical
mechanics from quantum mechanics + gravity.

### Direction 7: Spectral Geometry — Weyl's Law on Graphs

Compute full spectrum of staggered Hamiltonian. Check Weyl's law
N(E) ~ E^(d_s/2). Compute spectral dimension d_s and check convergence
to d_eff from graph growth. This is a concrete realization of Connes'
noncommutative geometry program.

### Direction 8: Gravitational Memory from Retarded Wave

Create a propagating Phi perturbation on the retarded wave equation.
Measure whether geodesic separation between test wavepackets is permanently
altered after the wave passes — the discrete Christodoulou memory effect.

## Tier 3: High-Risk, High-Reward

### Direction 9: Confinement from Phase-Valley Mechanism
### Direction 10: Non-Abelian Gauge from Multi-Component Staggering
### Direction 11: Anyonic Statistics from Graph Braiding
### Direction 12: Holographic Principle from Graph Boundary

## Cross-Architecture Table (What's Proven Where)

| Feature | Staggered | Chiral 1+1D | Mirror Z2 | TM |
|---------|-----------|-------------|-----------|-----|
| Born | 1e-15 | 1e-16 | 3e-15 | 4e-17 |
| KG dispersion | exact | exact | N/A | N/A |
| Light cone | LR 97% | strict v=1 | N/A | N/A |
| Gauge | pers. curr. | AB 88.5% | N/A | N/A |
| Geom. superpos. | path-sum DAG `4.37%` only | TV=0.039 | N/A | N/A |
| Self-gravity | w=0.40-0.76 | N/A | N/A | N/A |
| Sign selective | G=5-10 | N/A | N/A | N/A |
| MI | 0.16-0.62 | N/A | **0.773** | N/A |
| Decoherence | 23%→18% | 82.8% (2+1D) | near-flat | N/A |
| Area entropy | **UNTESTED** | N/A | N/A | sub-area |
| Critical beta | 0.33-0.73 | N/A | N/A | N/A |
| Dynamic growth | partial | N/A | N/A | **works** |
| Metric recovery | **UNTESTED** | r=0.956 | N/A | r=0.997 |

## Recommended Paper Structure

**Title:** "Staggered fermions on graphs derive Dirac physics, gravitational
attraction, and geometry superposition from discrete structure"

**Core claims:**
1. Dirac dispersion derived from graph staggering (not assumed)
2. Gravitational attraction on the cubic card plus a strong weak-coupling
   sign-sensitive regime on irregular graphs
3. Self-gravity contracts wavepackets (w=0.40-0.76, 9/9 families)
4. A geometry-superposition signal exists in the older path-sum DAG ensemble,
   motivating a true staggered geometry-superposition test
5. Topology-dependent critical exponents (new universality class)
6. Field equation justified variationally at lowest local quadratic order

**Novel contributions:**
- Parity coupling correction to staggered scalar gravity (Zache 2020 applied
  to self-gravity for the first time)
- Weak-coupling irregular sign sensitivity (new regime identification)
- The B1 reframing as discrete general covariance (theoretical contribution)
