# Session Synthesis: Graph Laplacian Axioms (2026-04-10)

**Status:** support / historical synthesis note (downgraded 2026-04-28 per audit-lane verdict). The current staggered status is tracked by the force-based card and corrected full-suite baseline, not by the older `frontier_staggered_fermion.py` successor framing alone. The runner declared in this note is a legacy proxy harness and does not function as a current-main evidence surface.

## What happened

This session started from the chiral walk's 3 gravity blockers (chromaticity,
equivalence violation, N-oscillation) and ended with a new axiom set that passes
the full 16-row audited core card on three different graph topologies.

## The journey (in order)

1. **Coupled 6x6 coin scan**: Proved the 6-component chiral walk's KG failure
   (R^2=0.156) is a structural no-go. No 6x6 on-site unitary improves it.

2. **4-component Dirac walk**: KG R^2=1.000 (Hamiltonian Bloch), but gravity
   goes AWAY with standard coupling. Reversed coupling (m(1+f)) gives TOWARD
   but keeps the coin mixing period.

3. **Root cause diagnosis**: All 3 gravity blockers trace to ONE source — the
   coin's mixing period pi/m. Any gravity mechanism that works through the coin
   inherits chromaticity, equivalence violation, and N-oscillation.

4. **Scalar potential gravity**: Moving gravity from coin to potential (V=m*Phi)
   fixes equivalence and N-stability on the scalar KG. But the scalar KG
   "assumes" physics rather than deriving it.

5. **Graph Laplacian KG**: The third path — KG derived from the graph Laplacian
   (not coin, not FFT), with potential gravity, local leapfrog/CN evolution.
   Passes the core card on cubic lattice.

6. **Topology independence**: Same axioms tested on random geometric graph and
   dynamically grown graph. Same physics emerges on all three.

7. **Audit and correction**: Multiple rounds of review caught reversed Born gate,
   fake C11/C13/C15 tests, overclaiming. All fixed. Final scores frozen with
   audited definitions.

## The five axioms

1. **Events** — A finite set of nodes exists.
2. **Connections** — Nodes are connected by undirected links, defining a graph
   G = (V, E) and its Laplacian L_G = D - A.
3. **Field** — Each node carries a complex scalar amplitude psi(v).
4. **Persistence** — The field evolves unitarily via the graph Laplacian:
   H = L_G + m^2*I + V(x)*I, with U(dt) = Crank-Nicolson.
5. **Gravity** — A mass source creates a local potential:
   V(v) = -m * g * S / (d(v, source) + eps).

## What these axioms produce

**Important caveat**: The evolution is first-order Schrodinger (i*dpsi/dt = H*psi),
NOT second-order Klein-Gordon (d^2 psi/dt^2 = -H^2*psi). The Hamiltonian's eigenvalue
spectrum satisfies E = sqrt(m^2 + lambda(k)), which SQUARED gives the KG relation,
but the dynamics are Schrodinger-like. This is a graph-scalar Hamiltonian lane with
KG-like spectrum, not a fully demonstrated local KG dynamics.

- **KG-like spectrum**: E^2 = m^2 + lambda(k) where lambda(k) are the graph
  Laplacian eigenvalues. On a regular lattice: lambda = 2*sum(1-cos(k_j)).
  R^2 = 0.9998, isotropy 1.031 on cubic. (Spectrum verified, not dynamics.)
- **Born rule**: Sorkin I_3 / P = 4e-15 (machine zero). Structural from
  linearity of the CN evolution.
- **Gravitational attraction**: TOWARD, F proportional to M (R^2=1.000),
  achromatic (force CV=0.002), mass-independent acceleration (CV=0.000),
  monotonically growing with propagation depth, stable across N range.
- **AB-proxy gauge**: Slit-phase visibility 0.43-0.79 across graphs.
  Torus flux test shows partial gauge sensitivity (V_det=0.11). This is
  an AB proxy, not a full retained graph gauge closure.
- **Decoherence**: Phase noise suppresses coherences (94->7% on cubic).
- **Superposition**: Two-body gravity error < 0.1%.

## Frozen audited scores

Script: `frontier_axioms_16card.py` @ commit 3dbcd73 (C1 Sorkin fix) + 9c830fc (C11 dense grid)

| Row | Test | Cubic (3375) | Random (300) | Growing (150) |
|-----|------|:---:|:---:|:---:|
| C1 | Sorkin I3 | 4.5e-15 | 3.4e-15 | 3.7e-15 |
| C2 | d_TV | 0.66 | 0.78 | 1.00 |
| C3 | f=0 | 0.000 | 0.052 | 0.011 |
| C4 | F~M | R2=1.000 | R2=1.000 | R2=1.000 |
| C5 | TOWARD | yes | yes | yes |
| C6 | Decoherence | 94->7% | 13->5% | 31->3% |
| C7 | MI | 1.2e-8 | 0.10 | 0.12 |
| C8 | Purity CV | 0.24 | 0.05 | 0.01 |
| C9 | Grav grows | mono | mono | mono |
| C10 | Distance | 5/5 TW | 5/5 TW | 4/4 TW |
| C11 | KG/iso | R2=.9998, 1.031 | R2=1.000 | R2=1.000 |
| C12 | AB-proxy | V=0.43 | V=0.67 | V=0.79 |
| C13 | k-achrom | CV=0.002 | CV=0.006 | CV=0.003 |
| C14 | Equiv | CV=0.000 | CV=0.000 | CV=0.000 |
| C15 | BC robust | 3/3 per/open | T/T | T/T |
| C16 | Multi-obs | 2/3 | 2/3 | 2/3 |
| | **Total** | **16/16** | **16/16** | **16/16** |

## What the axioms do NOT produce

- **Spin / chirality**: Scalar field, no internal DOF. Needs Dirac extension.
- **Strict v=1 light cone**: KG lattice has v < 1. Dirac gives v=1 but we
  showed that scalar potential doesn't couple to spinors.
- **Causal set / DAG structure**: The growing graph is temporally ordered but
  the Laplacian doesn't enforce causality.
- **Dynamic growth / backreaction**: Static graph. Growth requires a rule for
  adding nodes, which is outside the current axiom set.
- **Cosmology, Hawking, geometry superposition**: N/A for a static scalar field.

## What The Follow-Up Probes Changed

Two follow-up probes sharpen the interpretation of the scalar graph lane.

- **True local KG vs CN**:
  [`frontier_graph_true_kg_vs_cn.py`](../scripts/frontier_graph_true_kg_vs_cn.py)
  shows that the current CN scalar lane and a true local doubled-state KG lane
  are not the same free theory. The CN lane is still useful because it matches
  several weak-field gravity rows, but it should now be treated as a clean
  scalar control/base layer rather than as a proven local KG formulation.

- **Two-field scalar + spinor prototype**:
  [`frontier_graph_scalar_plus_spinor.py`](../scripts/frontier_graph_scalar_plus_spinor.py)
  gives a positive proof of concept for a split architecture. A spinor matter
  sector can keep unitary norm and feel a TOWARD scalar gravity background on
  the same graph. The blocker is not transport anymore; it is backreaction,
  because the scalar background is still one-way and external.

- **Staggered fermion probe** (historical successor probe):
  [`frontier_staggered_fermion.py`](../scripts/frontier_staggered_fermion.py)
  is the most promising current no-coin genuine Dirac lane. It closes the free
  staggered dispersion exactly and gives strong 1D gravity behavior, but the
  current CN evolution still fails a strict light-cone gate. That makes it a
  strong successor probe, not the retained replacement architecture.

- **Staggered fermion force-based card** (current retained result):
  [`frontier_staggered_17card.py`](../scripts/frontier_staggered_17card.py)
  uses force F=-⟨dV/dz⟩ instead of centroid shift for the gravity rows.
  The centroid oscillates in a permanent period-4 pattern on the staggered
  periodic lattice; force converges at all tested sizes (n=7..17).
  Scores: 1D n=61 `17/17` (6/6 families), 3D n=9 `17/17` (6/6 families),
  3D n=11,13 `17/17` (4/6 families, energy projections skipped because
  `N_sites > 1000`). Full suite
  baseline: 1D `29/38`, 3D `28/38`.
  Rows C5/C9/C10/C15/C16 have different semantics from the repo-wide centroid
  card (see `STAGGERED_FERMION_CARD_2026-04-10.md`). C12 is a native
  persistent-current test on the actual card lattice. All tested state
  families, including anti/Nyquist in the full 1D and 3D `n=9` runs, are
  TOWARD under force.

- **Staggered graph portability probe**:
  [`frontier_staggered_graph_portability.py`](../scripts/frontier_staggered_graph_portability.py)
  is the current backlog probe for non-cubic graph families. The first retained
  run on bipartite random geometric, bipartite growing, and layered bipartite
  DAG-compatible graphs keeps the staggered force battery intact: Born/linearity
  `~5e-16`, norm `~1e-15`, force sign TOWARD, `F∝M = 1.000`, achromatic force
  `~1e-16`, equivalence `~1e-16`, robustness `3/3`, and gauge response on the
  cycle-bearing families. This is the first portability checkpoint, not a new
  canonical card.

## The core tension (still open)

The architectures that DERIVE the most physics (chiral walk: KG, light cone,
causal set, spin) have fundamentally broken gravity (coin mixing period). The
architecture with clean gravity (graph Laplacian scalar) doesn't derive spin
or light cone.

The session proved these are incompatible at the single-field level:
- Coin-based kinematics -> derived KG + broken gravity
- Potential-based gravity -> clean gravity + no derived spinor physics

A resolution might require:
1. **Multi-field theory**: scalar field for gravity, spinor field for matter,
   coupled through the graph structure. Like real physics (metric + matter).
2. **Emergent spinor**: the scalar field on a graph might develop effective
   spinor structure at large scales (analogous to emergent fermions in
   condensed matter).
3. **Different axioms**: axioms that produce the Dirac equation from graph
   structure without a coin, such as a discrete version of the vierbein
   formalism.

## Comparison with pre-session best

| Measure | Chiral 1+1D (pre) | Graph Laplacian (new) |
|---------|-------------------|----------------------|
| Core card | 10/10 (old card) | 16/16 (audited) |
| KG | exact (1D) | R^2=0.9998 (3D) |
| Gravity TOWARD | basin (oscillates) | 100% monotone |
| Achromatic | CV=2.66 | CV=0.002 |
| Equivalence | violated (56%) | CV=0.000 |
| N-stable | oscillates | all TOWARD |
| Spin | chirality | N/A |
| Light cone | v=1 exact | v < 1 |
| Born | 3.3e-16 | 4.5e-15 |
| Gauge | AB 88.5% | AB-proxy 43-79% |
| Topology | 1D lattice | cubic+random+growing |

## Honest assessment

**What's strong:**
- The gravity mechanism is the cleanest of any architecture tested.
- The topology independence is real and meaningful.
- The Born rule (Sorkin I3) is at machine zero.
- The axioms are minimal and physically motivated.

**What's still weak:**
- Scalar field can't do spin or strict light cone.
- C12 gauge is a proxy, not a genuine gauge coupling.
- The "derivation" of KG from the Laplacian is elementary (it's just the
  lattice discretization of the wave equation).
- No connection to the original axiom chain (events, links, delays, records).

**What's next:**
- Port the potential gravity insight back to a Dirac-on-graph architecture
  using the vierbein/connection formalism (not scalar potential on I4).
- Test on actual DAGs from the axiom growth rules.
- Develop a genuine gauge coupling (not slit-phase proxy).
- Write up the graph Laplacian axioms as a separate, self-contained result.

## Audit boundary (2026-04-28)

The earlier Status line read "historical synthesis note. The current
`proposed_retained` staggered status is..." which the audit-lane parser
classified as `proposed_retained` because the literal token appeared in
the Status string.

Audit verdict (`audited_failed`, leaf criticality):

> Issue: The row is a historical synthesis note whose declared runner
> is explicitly labeled a legacy proxy harness and prints 'Do not use
> this script as a current-main evidence surface.' Why this blocks: a
> 16/16 legacy proxy run cannot ratify the broad graph-axiom or
> current staggered `proposed_retained` claim, especially when the
> note says current status is tracked by successor cards with
> different semantics. Repair target: demote this file to historical
> synthesis/support and audit the current force-based staggered card,
> corrected graph-KG card, and any portability cards as separate
> runner-backed claims.

The note has been re-tiered to `support` per the verdict's repair
target.

## What this note does NOT claim

- A current staggered status assertion — the live status is on the
  force-based staggered card and corrected full-suite baseline, not
  here.
- That the legacy proxy harness is a current-main evidence surface
  (the script itself prints the opposite).
- A graph-axiom result strong enough to ratify a successor-card
  staggered claim by itself.

## What would close this lane (Path A future work)

If the broader graph-axiom synthesis is to be re-promoted, it would
require auditing the current force-based staggered card, the corrected
graph-KG card, and any portability cards as separate runner-backed
claims, with this note left as historical context.
