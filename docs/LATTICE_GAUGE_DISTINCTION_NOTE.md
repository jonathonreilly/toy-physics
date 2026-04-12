# Distinction from Lattice Gauge Theory and Discrete Gravity Programs

**Date:** 2026-04-12
**Status:** reviewer-facing comparison note for Nature submission
**Purpose:** Preempt the question "how is this different from lattice QCD?"

---

## 1. What lattice gauge theory does

Lattice gauge theory (Wilson, 1974) is a regularization technique for
continuum quantum field theories. Its defining features:

- **Starts from a known continuum theory.** The Standard Model Lagrangian
  (or whichever gauge theory) is the input. The lattice discretizes that
  known theory onto a regular grid with spacing *a*.
- **Gauge fields live on links, matter on sites.** The fundamental
  variables are SU(3) group elements U_mu(x) on each link, and fermion
  fields psi(x) on each site. The Wilson plaquette action
  S_W = beta * sum_P Re Tr(1 - U_P) is a specific discretization of
  F_{mu nu} F^{mu nu}.
- **The lattice is a computational tool, not fundamental.** The physical
  content lives in the continuum limit a -> 0. Lattice artifacts (doubler
  fermions, finite-volume effects, topological freezing) are things to be
  removed, not studied for their own sake.
- **The continuum limit recovers the known theory by construction.** The
  action is designed so that a -> 0 gives back the classical action, and
  universality arguments (backed by decades of numerical evidence) ensure
  the quantum theory is recovered in that limit.
- **Gravity is absent.** Lattice QCD lives on a fixed flat background.
  The lattice has no dynamics of its own — it is scaffolding, not
  spacetime. If gravitational effects are desired, they must be put in by
  hand through a separate program (Regge calculus, dynamical
  triangulations, etc.).
- **Fine-tuning is required.** Bare parameters must be tuned as a -> 0
  to stay on the correct renormalization group trajectory. This is a
  practical necessity, not a deficiency — it is how continuum physics is
  extracted from the lattice regularization.

## 2. What this framework does differently

This framework begins from a discrete event-network ontology (10 axioms)
and asks what physics-like structure can be recovered without assuming a
prior continuum theory. The key structural differences:

- **No prior continuum theory.** There is no Lagrangian being
  discretized. The graph is the starting point, not an approximation to
  a manifold.
- **The graph is fundamental.** Unlike the lattice in lattice QCD, the
  discrete structure is not scaffolding to be removed. The theory lives
  on the graph. The continuum limit, if it exists, is a prediction to be
  tested, not a requirement to be satisfied.
- **The propagator emerges from path sums on the graph.** Complex
  amplitudes are assigned to paths via an action S = L(1 - f), where L
  is path length and f is a field sourced by a Poisson equation on the
  graph. This is not a discretization of a known propagator — the
  propagator is defined directly on the discrete structure.
- **Gravity is an output.** The gravitational deflection of
  propagating amplitudes, Newtonian mass scaling (F proportional to M),
  the weak equivalence principle, and gravitational time dilation are
  numerical outputs of the path sum, not inputs. The action S = L(1-f)
  was not designed to reproduce general relativity; the weak-field
  Schwarzschild metric structure was discovered after the action was
  selected on other grounds (phase valley + weak-field linearity).
- **The field equation is sourced locally.** The Poisson equation
  laplacian(f) = -source is solved on the graph itself. The transverse
  field profile is derived, not imposed — the 2D Poisson solution on
  each layer gives F proportional to M = 0.9997, better than the imposed
  1/r form (0.990).
- **The continuum limit is a prediction.** On ordered lattices, taking
  h -> 0 produces convergent observables: the weak-field deflection
  changes by only 2.7% between h = 0.25 and h = 0.125, the mass
  exponent F proportional to M brackets 1.000, and the Born rule holds
  at machine precision through all tested resolutions. This convergence
  was not guaranteed — it had to be demonstrated.

## 3. Specific technical differences

### Action and degrees of freedom

| Feature | Lattice gauge theory | This framework |
|---------|---------------------|----------------|
| Degrees of freedom | Group-valued link variables U_mu(x) | Complex path amplitudes with real-valued nodal field f |
| Action | Wilson plaquette S_W = beta sum Re Tr(1-U_P) | Path action S = L(1-f), field from graph Poisson equation |
| Gauge symmetry | Exact local SU(N) by construction | No gauge group assumed; U(1) phase structure explored separately |
| Matter coupling | Fermion fields on sites, coupled via link variables | Matter is a persistent source pattern; no separate fermion sector |
| Path integral | Over all link configurations {U} | Over all paths on the graph with fixed field configuration |

### Role of the lattice/graph

| Feature | Lattice gauge theory | This framework |
|---------|---------------------|----------------|
| Status of discrete structure | Regulator (to be removed) | Fundamental (the theory lives here) |
| Continuum limit | Required; recovers known theory | Predicted; tested numerically |
| Lattice spacing | UV cutoff, taken to zero | Graph connectivity scale; h -> 0 is explored, not mandated |
| Background geometry | Flat Euclidean (or Minkowski after Wick rotation) | None assumed; effective metric is an output |

### Phase accumulation

In lattice gauge theory, the phase along a path is determined by the
ordered product of link variables: exp(iS) comes from multiplying
U_mu(x) along a Wilson line. The phase is gauge-covariant and the
path-ordered exponential is the central object.

In this framework, the phase along a path of length L through a field f
is k * L * (1 - f_avg), where k is a wavenumber and f_avg is the
field averaged along the path. There is no gauge group, no
path-ordering, and no link variables. The phase is a scalar
accumulated from the local field.

### Fine-tuning

Lattice gauge theory requires tuning bare parameters (coupling
constant, quark masses) as a function of lattice spacing to stay on the
correct RG trajectory. This is well-understood and systematic.

This framework has a different tuning structure. The action form
S = L(1-f) is selected by two physical requirements (phase valley for
attractive gravity, weak-field linearity for Newtonian mass scaling).
The kernel power 1/L^(d-1) in dimension d is an empirically retained
candidate that stabilizes gravity under lattice refinement. Neither
selection involves tuning to match a known continuum answer — the
selections are internal consistency conditions.

### What each produces

Lattice gauge theory produces hadronic spectra, confinement, chiral
symmetry breaking, form factors, decay constants, and other properties
of the strong interaction — all derivable in principle from the QCD
Lagrangian that was the input.

This framework produces gravitational deflection, mass scaling,
the weak equivalence principle, gravitational time dilation, an
emergent conformal metric, Born-rule interference, and decoherence
from record formation — none of which were inputs. The distance law
is approximately 1/b on grown geometries (alpha = -0.96), with
wave-optics corrections that depend on graph regularity.

## 4. Relationship to other discrete gravity programs

### Causal Dynamical Triangulations (CDT)

CDT (Ambjorn, Jurkiewicz, Loll) sums over triangulated geometries
weighted by the Regge discretization of the Einstein-Hilbert action.
The input is GR: the action S_EH = integral(R sqrt(g)) is discretized
using deficit angles around hinges. CDT adds a causality constraint
(a preferred foliation) to tame the conformal-factor problem that kills
Euclidean dynamical triangulations.

**Similarity:** Both use discrete structures and study their
continuum limit. Both produce dimensional observables (spectral
dimension).

**Difference:** CDT discretizes a known action (Einstein-Hilbert).
This framework derives its action from internal consistency
requirements (valley-linear selection). CDT does not propagate quantum
amplitudes through the geometry — it sums over geometries. This
framework propagates amplitudes through a fixed (or slowly evolving)
geometry and asks what the amplitudes do.

### Causal set theory

Causal set theory (Bombelli, Lee, Meyer, Sorkin) posits that spacetime
is fundamentally a locally finite partial order (a causal set), with
the volume element carried by counting. Lorentz invariance is imposed
through the sprinkling hypothesis: causal sets are generated by Poisson
sprinkling into Minkowski space (or a Lorentzian manifold), and only
properties that survive this randomization are considered physical.

**Similarity:** Both start from discrete ordered structures. Both
explore path sums and interference on discrete substrates. The Sorkin
third-order interference diagnostic (I_3/P -> 0) used in this project
is borrowed directly from the quantum measure program.

**Difference:** Causal sets build in Lorentz invariance from the start
via the sprinkling hypothesis. This framework does not assume any
spacetime symmetry — the graph has its own structure, and any symmetry
must emerge. Causal set dynamics (sequential growth models) is a
measure over causal sets; this framework propagates fields on a single
graph (or graph family).

### Loop quantum gravity (LQG)

LQG quantizes general relativity by reformulating it as a gauge theory
(Ashtekar variables) and applying canonical quantization. The
kinematic Hilbert space is spanned by spin network states — graphs
with edges labeled by SU(2) representations and vertices by
intertwiners. The dynamics is encoded in a Hamiltonian constraint.

**Similarity:** Both have graph-like structures as the fundamental
objects. Both assign algebraic data to graph elements.

**Difference:** LQG starts from general relativity and quantizes it.
The spin network labels (j, i_v) encode geometric data (areas,
volumes) derived from the classical theory. This framework does not
quantize a classical theory — it asks what geometry-like behavior
emerges from path sums on a graph. There are no spin labels, no
SU(2) structure, and no Hamiltonian constraint.

### Regge calculus

Regge calculus (Regge, 1961) discretizes Einstein's equations directly
by replacing the smooth metric with edge lengths on a fixed
triangulation. The curvature is concentrated at hinges (d-2 simplices)
as deficit angles, and the Einstein-Hilbert action becomes a sum over
hinges: S = sum_h A_h * delta_h.

**Similarity:** Both are discrete and both involve geometry-like
quantities on graphs.

**Difference:** Regge calculus is a faithful discretization of GR —
the edge lengths are the metric, and the deficit angles are the
curvature. In the continuum limit, Regge calculus recovers Einstein's
equations by construction. This framework has no edge lengths that
encode a metric. The effective metric is an output of the propagator
(the conformal factor (1-f) on each step), not an input encoded in
the geometry.

### Wolfram Physics / digital physics

The Wolfram Physics Project and related programs (Zuse, Fredkin,
't Hooft) propose that physical laws emerge from the evolution of
discrete systems (hypergraph rewriting, cellular automata, etc.).

**Similarity:** Shared ambition to derive physics from discrete
local rules. Closest in spirit among all comparisons.

**Difference:** This project has a more developed numerical
pressure-testing program: explicit ablations, falsification criteria,
honest failure documentation, adversarial self-audit, and a
quantitative claim/evidence separation (the Assumption Derivation
Ledger). The specific mechanism (complex path amplitudes with
valley-linear action on graphs with Poisson-sourced field) is
technically distinct from hypergraph rewriting. However, the
comparison is fair: both are discrete-substrate programs that aspire
to derive physics, and both face the same fundamental reviewer
question about whether the desired physics has been smuggled in
through the choice of rules.

## 5. The honest overlap

The distinction between this framework and lattice gauge theory is
strong in some places and more subtle in others. Here is where the
lines blur:

**Both use discrete structures with locality.** Both have nodes/sites,
edges/links, and propagation rules that respect the graph structure.

**Both have a graph Laplacian as a natural operator.** The Poisson
equation laplacian(f) = -source on our graph is structurally identical
to what one would write on a lattice in lattice field theory. The
Laplacian itself is not novel.

**The path-sum structure resembles a lattice path integral.** The
amplitude sum_paths w(p) exp(i k S(p)) has the same mathematical
form as a discretized Feynman path integral. The key question is
whether the action S and the path measure w were chosen to reproduce
known physics (which would make this a disguised lattice
regularization) or whether they were selected on internal grounds
and happened to produce physics-like outputs.

**The action S = L(1-f) is close to a lattice geodesic action.** In
weak-field general relativity, the action for a particle in a
gravitational potential Phi is S = integral ds (1 + 2Phi/c^2), which
maps to L(1 - f) with identification f = -2Phi/c^2. A skeptical
reader could argue that the action was reverse-engineered from GR.

**The honest response to this skepticism:** The action was selected by
two requirements that do not reference GR: (1) phase valley (action
decreases near mass, producing attractive deflection), and (2)
weak-field linearity in f (producing F proportional to M). The
valley-linear universality class contains S = L(1-f), S = L exp(-f),
and S = L/(1+f), all of which give the same mass scaling. The specific
form S = L(1-f) is the simplest member of this class. The
correspondence with the weak-field Schwarzschild action is a
non-trivial output — it was recognized after the fact, not used as an
input. But the skeptic's point has force: the selection criteria, while
not directly referencing GR, are physical criteria that may implicitly
encode GR content. This is a genuine interpretive question that the
framework does not fully resolve.

**The Poisson equation is standard physics.** Solving laplacian(f) = -source
on a graph is the same equation one solves for electrostatics or
Newtonian gravity. The novel content is that the field sources the
propagator action, creating a self-consistent loop (field determines
action, action determines propagation, propagation determines
observable gravity). But the individual equations are familiar.

**The derivation direction is genuinely opposite, even where the
equations overlap.** Lattice gauge theory starts with QCD and asks:
can we compute on a lattice? This framework starts with a graph and
asks: what physics emerges? The mathematical objects may be similar,
but the logical status is different. In lattice QCD, the Laplacian
appears because it discretizes a known differential operator. Here,
the Laplacian appears because it is the natural operator on the graph
(the graph Laplacian is defined by the connectivity, not derived from
a continuum limit). The distinction is real but can be overstated.

## 6. Key sentences for the paper

The following sentences are calibrated for a Nature audience. Each
is defensible given the current evidence chain.

**Sentence 1 (Introduction, positioning):**
"Unlike lattice gauge theory, which discretizes a known continuum
Lagrangian, this framework begins with a discrete graph substrate and
derives gravitational phenomenology as an output of self-consistent
amplitude propagation — the continuum limit is a prediction, not a
construction requirement."

**Sentence 2 (Methods, action selection):**
"The action S = L(1-f) was not chosen to reproduce general relativity;
it was selected as the simplest member of the valley-linear
universality class — actions that create a phase valley near mass
(attractive gravity) and are linear in the field at weak coupling
(Newtonian mass scaling) — and its correspondence with the
weak-field Schwarzschild line element was recognized after the fact."

**Sentence 3 (Methods, field equation):**
"The gravitational field is sourced by a Poisson equation on the graph
itself, making the transverse field profile a derived consequence of
graph connectivity rather than an imposed boundary condition."

**Sentence 4 (Discussion, comparison):**
"The key structural difference from lattice regularization programs
is the logical status of the discrete structure: in lattice QCD the
graph is computational scaffolding whose artifacts must be removed; here
the graph is the physical substrate whose properties determine the
emergent phenomenology."

**Sentence 5 (Discussion, honest caveat):**
"We acknowledge that the individual mathematical ingredients — path
sums, graph Laplacians, Poisson-sourced fields — are well-established
tools in discrete physics; the claim is not novelty of technique but
reversal of logical direction, from 'discretize known physics' to
'derive unknown physics from discrete structure.'"

## 7. What a lattice QCD reviewer will push on

A reviewer from the lattice QCD community will likely raise these
specific objections. Each has a defensible response, but the
responses must be honest about their limits.

**Objection: "You're just doing lattice field theory with extra steps."**
Response: The mathematical tools overlap, but the logical program is
different. In lattice QCD, the action is derived from the Standard
Model. Here, the action is selected by internal consistency. The test
is whether the outputs (gravity, WEP, mass scaling, Born rule) are
non-trivially constrained by the inputs, or whether they were smuggled
in. The k=0 diagnostic (gravity vanishes when phase is turned off)
establishes that the gravitational signal is a genuine phase
interference effect, not an amplitude bias.

**Objection: "Your continuum limit is just lattice perturbation theory."**
Response: The h -> 0 convergence we demonstrate is not perturbative
fine-tuning. The mass exponent approaches 1.000 from both sides
(0.979, 0.991, 0.998, 1.018), the deflection converges to within 2.7%,
and the Born rule holds at machine precision throughout. But the
objection has force in one sense: we have only tested down to h = 0.125,
not to the asymptotic regime. The convergence is demonstrated, not
proven.

**Objection: "How do you know you haven't reverse-engineered GR?"**
Response: We cannot fully exclude this possibility, and we say so
explicitly (see the Assumption Derivation Ledger). The action form,
complex amplitudes, and Poisson field equation are assumed inputs. What
is not assumed is that they combine to produce gravitational time
dilation, the weak equivalence principle, or an isotropic conformal
metric. These outputs provide a non-trivial consistency check. But
the honest status is: the framework is a retained toy mechanism, not
a finished derivation of gravity from first principles.

---

**Summary:** The distinction from lattice gauge theory is primarily one
of logical direction and the status of outputs. Lattice gauge theory
discretizes known physics and computes. This framework assumes a
discrete substrate with local rules and asks what physics emerges.
The mathematical tools overlap substantially. The non-trivial content
is that specific emergent outputs (gravity, WEP, mass scaling, Born
rule, conformal metric) were not inputs, and that the framework is
internally falsifiable via the k=0 diagnostic and explicit prediction
criteria.
