# The Spectral--Trajectory Dichotomy in Discrete Self-Gravitating Quantum Mechanics

**Date:** 2026-04-11  
**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Branch:** `frontier/spot-checks`

**Audit-conditional perimeter (2026-05-02):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
note has no attached runner and no ledger dependencies, yet it
synthesizes many numerical and theoretical inputs into a structural
theorem about spectral gravity and many-body trajectory emergence."
This rigorization edit only sharpens the boundary of the conditional
perimeter; nothing here promotes audit status. The supported
content of this note is the **structural framing** — the spectral /
trajectory dichotomy as an interpretive synthesis of separately
audited results elsewhere in the repo. The note has no own runner
and no live deps=[], by design: each numerical row cited in §3
(sign selectivity 300/300; boundary-law shift; CDT spectral flow) and
§4 (Wilson two-body distance law; partner-source scaling; Penrose,
DP, BH) is a downstream pointer to a separately registered note. The
supported perimeter is the dichotomy framing as a synthesis of
already-audited downstream rows, not a load-bearing structural
theorem. A future repair would enumerate the cited downstream notes
explicitly as one-hop dependencies in the audit chain and let the
synthesis status track the chain-rule under those statuses; that step
is deferred and is the prescribed repair path.

---

## 1. Statement of the Claim

Consider a single free fermion on a finite graph, self-consistently coupled to
its own smoothed density through a positive kernel:

> **Axiom A.** States live in C^N on a finite graph; time evolution is unitary
> with a gapped nearest-neighbor Hamiltonian.
>
> **Axiom B.** The on-site potential satisfies V = G (K * |psi|^2) for a
> positive smoothing kernel K on the graph.

**Theorem (informal).** Within this framework:

(i) *Spectral observables* --- those determined by the eigenvalue structure of
    the Hamiltonian H[psi] or by its ground-state/Dirac-sea correlations ---
    reproduce gravitational phenomenology (area-law entanglement, spectral
    dimension flow, sign-selective attraction) at the single-particle level.

(ii) *Trajectory observables* --- those requiring a classical force law,
     collapse timescale, or decoherence rate between macroscopic branches ---
     fail at the single-particle level and require many-body (Hartree or
     beyond) physics to reproduce known gravitational scaling laws.

(iii) This split is not a deficiency of the model but a structural prediction:
      gravity is fundamentally spectral, and Newtonian trajectory physics is
      emergent from many-body coarse-graining.

The remainder of this document supplies evidence from the numerical record and
a physical argument for why the dichotomy arises.

---

## 2. Generic Spectral Results (Free-Fermion Baseline)

Certain spectral properties follow from the Eisert--Cramer--Plenio theorem
(2010) and require no gravitational content at all. It is essential to
separate these from the gravitational contributions.

**Area-law entanglement.** For any gapped free-fermion Hamiltonian on a
lattice, the Dirac-sea (filled negative-energy modes) entanglement entropy
satisfies S(A) ~ |boundary(A)| with corrections that decay exponentially in
the gap. This is a mathematical theorem, not a dynamical prediction. In the
model, boundary-law fits give R^2 > 0.95 in 100/100 configurations on the
audited BFS-ball surface, but this high quality is *expected* --- it would be
a failure if it did not hold.

**Branch entanglement saturation.** The two-branch entanglement entropy
S_quantum saturates near ln(2) = 0.693 nats (0.999 bits at G = 50). This
saturation is generic for any on-site potential that creates distinguishable
branch states; it does not require self-consistency or gravitational coupling
specifically.

**Eigenvalue statistics.** The model produces Poisson-class level spacing
rather than GOE/GUE Wigner--Dyson statistics. This confirms the system is in
the integrable/localized class, consistent with a free fermion in a
self-consistent potential. No dynamical chaos transition is observed.

These results serve as the null hypothesis against which genuinely
gravitational spectral content must be measured.

---

## 3. Spectral Results That Are Gravitational

Three spectral observables survive Anderson-disorder controls and cannot be
attributed to generic free-fermion physics:

### 3.1 Sign Selectivity (300/300)

On irregular graph families (random geometric, growing, layered cycle),
attractive parity coupling produces shell-force TOWARD counts that uniformly
exceed repulsive coupling counts. The audited surface gives 300/300 on the
stable shell metric at weak coupling G = 5, 10. A matched-variance static
random potential achieves only 6/10 sign discrimination. The mechanism is
structural: |psi|^2 >= 0 and K >= 0 guarantee V >= 0, so under parity
coupling H_diag = (m + V) epsilon(x), the positive V always widens the mass
gap at occupied sites, creating a velocity gradient toward the density peak.
Sign selectivity is a property of the *spectrum* of H[psi] and requires no
trajectory measurement.

### 3.2 Boundary-Law Coefficient Shift (2.7 sigma)

Self-consistent gravity reduces the Dirac-sea boundary-law coefficient by
12.46% relative to the free Hamiltonian (R^2 = 0.9682 vs 0.9995 for S vs
|boundary|). The Anderson control shows this shift is distinguishable from
random disorder at 2.7 sigma. The shift is modest but real: the spatial
correlations in V = G (K * |psi|^2) --- inherited from the nonlocality of the
kernel K --- create entanglement structure that i.i.d. disorder cannot
reproduce. This is a property of the *correlation matrix* of the Hamiltonian's
Dirac sea, not of any particular dynamical trajectory.

### 3.3 CDT-Like Spectral Dimension Flow

The Laplacian return probability on the graph, computed from the full spectrum
of H[psi], exhibits a sigmoid crossover from small-sigma (UV) spectral
dimension near 2 to large-sigma (IR) spectral dimension near 3--4, with
fit quality R^2 > 0.989. The crossover scale sigma_star shows convergence
under lattice refinement. This qualitative flow d_s: 2 -> 4 matches the
signature of Causal Dynamical Triangulations (Ambjorn, Jurkiewicz, Loll 2005)
and Horava--Lifshitz gravity.

Crucially, this is a spectral-geometric observable: it depends on the
eigenvalues {lambda_k} of the graph Laplacian modified by the self-consistent
potential, not on any particle trajectory. CDT, causal sets, and this model
agree on the flow because they share spectral structure, regardless of their
different dynamical content.

---

## 4. Trajectory Results That Fail at Single-Particle Level

### 4.1 Newtonian Force Law

The Wilson two-body Hartree test on open 3D lattices produces a clean mutual
attraction channel (25/25 attractive, 25/25 clean with SNR > 2). However, the
distance law is |a_mut| ~ d^{-3.4}, not the Newtonian d^{-2}. Per-side fits
show the exponent drifting *steeper* under refinement:

| Side | Exponent | R^2 |
|------|----------|-----|
| 11 | -3.139 | 0.9968 |
| 13 | -3.313 | 0.9960 |
| 15 | -3.500 | 0.9939 |
| 17 | -3.671 | 0.9920 |
| 19 | -3.837 | 0.9899 |

The Yukawa screening (mu^2 = 0.22, screening length 2.13 sites) accounts for
part of the steepening, but removing screening (mu^2 = 0.001) does not recover
Newton. The fundamental problem is that the Hartree two-orbital construction is
not a genuine many-body theory: the mutual channel couples two *orbitals*
through a shared mean field, not N particles through a quantum gravitational
interaction.

### 4.2 Partner-Source Scaling

At fixed distance, |a_mut| ~ m_B^{0.48} (R^2 = 0.9363), clearly sublinear
rather than the linear F ~ M expected from Newton. The half-power scaling is
consistent with a mean-field (Hartree) potential where each orbital contributes
sqrt-like rather than linearly to the shared potential.

### 4.3 Penrose Collapse Threshold

The Penrose criterion tau_collapse ~ hbar / E_G, where E_G is the
gravitational self-energy difference between two macroscopic branches, is not
reproduced. The model gives |E_self| ~ G (clean), but the Penrose ratio
E_self / hbar omega is not constant across the parameter space. The collapse
timescale tracks the staggered lattice gap 2m between sublattices rather than
the gravitational self-energy E_G. When 2m >> E_G --- the generic single-
particle regime --- the Zeno rate reflects lattice structure, not gravity.

### 4.4 Diosi--Penrose Decoherence Rate

The DP prediction Gamma ~ G M^2 / (hbar d) requires a density matrix for a
massive composite object. The single-particle model has one wavefunction, not a
partial trace over environmental degrees of freedom. The fitted distance
scaling is partial and does not match Gamma ~ 1/d. The G and mass scalings are
wrong because DP assumes Newtonian self-energy G M^2 / d with gravitational
mass M = N m, but the model's "mass" is the Dirac mass m of a single fermion,
not a composite gravitational mass.

### 4.5 Bekenstein--Hawking Entropy

BH entropy S = A / (4G) requires a thermodynamic ensemble of microstates. The
single-particle Dirac-sea entropy gives S ~ |boundary|^{1.76} --- an area-law
*entanglement* entropy, not a thermal entropy. The coefficient does not match
the BH prediction because no temperature, no horizon, and no microstate
counting exist at the single-particle level.

---

## 5. Trajectory Results That Succeed with Many-Body Physics

The single canonical card, operating with a *prescribed* external source
(not self-consistently generated), gives:

- F ~ M with R^2 = 0.917 (1D) to R^2 = 1.000 (3D at n = 9)
- 17/17 on the full battery at all tested lattice sizes
- C5 force TOWARD confirmed across 6 state families

These results succeed because the external source acts as a proxy for a
many-body gravitational field: the test particle responds to a prescribed
potential well whose depth scales linearly with the "source mass" parameter.
This is formally equivalent to the weak-field limit of a many-body Hartree
calculation where one mass is treated as fixed.

The two-body mutual channel succeeds partially on the open Wilson lattice
(8/8 attractive at each tested separation) but produces the wrong distance
law. This is the expected intermediate state: the Hartree approximation
captures the existence of mutual attraction but not its precise scaling,
because the Hartree mean field does not include exchange, correlation, or
graviton-mediated quantum corrections.

---

## 6. The Argument: Why Spectral Observables Work and Trajectory Observables Require Many-Body Physics

### 6.1 The Hamiltonian is correct; the Hilbert space is too small

The self-consistent Hamiltonian H[psi] = T + (m + V[|psi|^2]) epsilon(x) is
correctly constructed at the single-particle level: it is a gapped
nearest-neighbor operator whose spectrum encodes the local gravitational
environment through V. Spectral observables --- entanglement entropy, spectral
dimension, localization class, sign of the gap modulation --- depend only on
{lambda_k, |phi_k>}, the eigenvalues and eigenvectors of H. These are
properties of the operator, not of any particular state's time evolution in a
large Hilbert space. The single-particle Hilbert space C^N suffices to define
the spectrum.

Trajectory observables --- force laws, collapse rates, decoherence rates ---
require the dynamics of *probability distributions* over classical
configurations. Newton's F = G M_1 M_2 / r^2 is a statement about the
acceleration of a center-of-mass coordinate, which requires a composite
object (M = N m, N >> 1). The Penrose collapse timescale is a statement about
the off-diagonal element of a *density matrix* for a macroscopic superposition
(two branches with mass separation d). The DP decoherence rate is a statement
about the *partial trace* of a system-environment density matrix. None of these
constructions exist in a single-particle Hilbert space.

### 6.2 Formal statement

Let O be an observable on the model. Define:

- O is *spectral* if it depends only on the eigenvalue structure of H[psi]
  or on the correlation matrix of its Dirac sea (ground state/filled modes).
- O is *trajectory* if it requires the time evolution of a center-of-mass
  coordinate, partial trace over subsystem degrees of freedom, or comparison
  between macroscopic branches with different classical configurations.

**Claim.** For the two-axiom model:

(a) If O is spectral, it can be evaluated on C^N and inherits gravitational
    content from the self-consistency condition V = G (K * |psi|^2).

(b) If O is trajectory, its gravitational scaling laws require extension to
    the N-body Hilbert space (C^N)^{otimes N} (or its Hartree approximation)
    to define the relevant masses, separations, and partial traces.

The split is not gradual. It is a sharp algebraic distinction: spectral
observables are *traces* over the one-body operator (which commute with the
self-consistency construction), while trajectory observables are *expectations*
in a many-body state (which the one-body construction cannot represent).

### 6.3 Why the staggered lattice amplifies the dichotomy

The staggered epsilon(x) = (-1)^x creates two sublattices. Spectral quantities
integrate over the Brillouin zone: the sublattice oscillation averages out
under the trace, producing smooth functions of {lambda_k}. Trajectory
quantities sample individual sites: the oscillation appears directly in
correlation functions at momenta near the doubler pole at pi/a. This is the
familiar "taste-breaking" artifact of staggered fermions in lattice QCD, where
spectral quantities (hadron masses, string tension) are O(a^2) improved but
position-space correlators suffer O(a^0) artifacts at specific momenta.

The parity structure therefore *amplifies* the spectral--trajectory split
beyond the fundamental algebraic reason. Continuum extrapolation (a -> 0)
would remove the amplification but not the underlying dichotomy.

---

## 7. Connection to Born Rule Independence

The Born rule probe confirms the structural prediction. The Hartree
self-consistency loop maps psi -> V(|psi|^alpha) -> H(V) -> psi'. Testing
whether alpha = 2 (Born rule) is selected by gravitational self-consistency
gives a clean negative: lower alpha converges faster (Banach contraction
mapping), and the Lyapunov ranking alpha = 1.0 < 1.5 < 2.0 < 3.0 < 4.0 is
the textbook contraction-rate ordering for the nonlinear source term |psi|^alpha.

This negative result is predicted by the spectral--trajectory dichotomy:

- The Born rule is a *measurement postulate* (interface between quantum state
  and classical observables). It determines how probabilities are extracted
  from |psi|^2, not how H acts on states.
- Gravitational self-consistency is a *dynamics statement* about how psi and V
  co-evolve. It preserves the entire function |psi(x)| up to phases.
- Unitary dynamics cannot distinguish alpha values because the Hartree loop
  never performs a measurement. It never asks "what is the probability of
  finding the particle at x?" --- it only uses |psi(x)|^alpha as a source for
  the field equation.

Spectral observables (area-law coefficient, sign selectivity, CDT flow) hold
for *any* alpha because they depend on the spectrum of H, which exists
regardless of the probability measure used to interpret |psi|^2. Trajectory
observables (Penrose, DP, BH) depend on the Born rule through the density
matrix formalism: rho = |psi><psi| assumes alpha = 2 to define the
density operator, and partial traces inherit this assumption.

Gravity and quantum probability are therefore *logically independent* at the
axiomatic level, confirming the standard physics intuition from a new
direction. The spectral content of the model is robust under changes to
alpha; the trajectory content requires alpha = 2 as an additional input.

---

## 8. Prediction: BMV Experiments Should See Entanglement Before Force

The Bose--Marletto--Vedral (BMV) proposal tests whether gravity can mediate
entanglement between two masses in superposition. The spectral--trajectory
dichotomy makes a specific experimental prediction about the order in which
gravitational quantum effects should become observable:

**Prediction.** In a BMV-type experiment with two masses m at separation d:

(i) *Gravitational entanglement* (a spectral observable: it depends on the
    eigenvalue structure of the joint Hamiltonian coupling the two masses
    through the gravitational field) should be detectable at mass/separation
    scales where the gravitational phase phi = G m^2 T / (hbar d) accumulates
    to order unity.

(ii) *Gravitational force as a trajectory observable* (deflection of
     center-of-mass, measured as a classical acceleration) requires
     M = N m >> m_Planck or d << l_Planck to produce measurable classical
     deflection, because the force law is a many-body emergent quantity.

(iii) The entanglement signal should therefore precede the force signal as
      experimental sensitivity improves.

The model's branch-entanglement probe supports this ordering: the externally
imposed two-branch geometry superposition produces delta_S > 0 (quantum
entropy exceeding classical mixture entropy) for all tested couplings, with
S_quantum saturating at 0.693 nats (99.96% of the two-branch maximum ln(2))
at G = 50. This saturation is rapid and clean. By contrast, the two-body
mutual attraction channel on open Wilson lattices, while real (25/25
attractive), produces a non-Newtonian distance law (d^{-3.4} rather than
d^{-2}) and sublinear mass scaling (m_B^{0.48} rather than m_B^{1.0}), and
the staggered partner-kick channel on periodic lattices is confined to a
narrow maximal-separation resonance window.

The spectral channel (entanglement) saturates; the trajectory channel (force
law) does not converge to Newton. This is the model's version of the
prediction: entanglement is fundamental and accessible; force is emergent and
requires additional structure.

### Quantitative ordering

For two masses m at separation d, the relevant scales are:

- Entanglement: requires phi ~ G m^2 T / (hbar d) ~ 1, giving
  T_ent ~ hbar d / (G m^2). This is the coherence time needed for the
  gravitational phase to produce distinguishable branches.

- Force (classical): requires a ~ G m / d^2 to exceed measurement noise
  over the observation time, giving detectable acceleration only for
  macroscopic M = N m.

Since T_ent involves m^2 (the quantum phase from two interfering paths) while
the classical force involves m (single-particle acceleration), entanglement
should be observable at smaller masses than force, for fixed coherence time and
measurement sensitivity. The BMV experimental program is, from this
perspective, correctly ordered: it targets the spectral channel first.

---

## 9. Summary

The spectral--trajectory dichotomy is not an artifact of the staggered lattice
or the screened Poisson equation. It is a structural consequence of the gap
between one-body operator theory (where spectral observables live) and
many-body state theory (where trajectory observables live). The model's two
axioms suffice to construct a self-consistent Hamiltonian whose spectrum
encodes gravitational content (sign selectivity 300/300, boundary-law
coefficient shift at 2.7 sigma, CDT-like spectral flow at R^2 > 0.989). They
do not suffice to construct a many-body Hilbert space where Newtonian force
laws (d^{-2}, F ~ M_1 M_2), Penrose collapse, or Diosi--Penrose decoherence
can be defined.

This is the model's most important structural prediction: gravity is
fundamentally a spectral phenomenon at the discrete level. The inverse-square
law, geodesic motion, and Einstein field equations are emergent from spectral
flow plus area-law entanglement, coarse-grained over many-body degrees of
freedom. Attempting to derive trajectory-level GR from a single-particle
lattice Hamiltonian is a category error --- analogous to demanding fluid
dynamics from the Ising model at criticality, when the critical exponents
(spectral properties) are already correct and the hydrodynamic transport
(trajectory properties) requires coarse-graining.

The trajectory failures are not bugs. They are boundary markers showing where
the effective description transitions from "discrete spectral" to "continuum
dynamical." The BMV prediction --- entanglement before force --- is the
experimentally accessible consequence of this boundary.
