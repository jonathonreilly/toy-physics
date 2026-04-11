# Nature-Level Discovery Directions — Cross-Architecture Synthesis

**Date:** 2026-04-11
**Status:** Active brainstorm, ranked by leverage

## Current State After Parity Coupling Rewrite

The staggered fermion lane now has:
- B1: a **strong weak-coupling sign-sensitive regime** on irregular graphs,
  but not a full blocker closure
- B2: a standard lowest-order variational justification for screened Poisson
- B3: light cone framed as standard lattice QFT / Lieb-Robinson behavior
- B4: static lattice still acceptable for a first paper, but not a Nature
  breakthrough by itself

Full suite: 29/38 (1D), 28/38 (3D). Canonical card: 17/17.

## Top Discovery Directions (Ranked)

### 1. Geometry Superposition on Staggered Lattice
**HIGHEST PRIORITY — Never attempted, connects to quantum gravity**

The chiral 1+1D walk achieved geometry superposition: TV=0.039, real phase
differences dphi=0.25-0.66 rad between different graph geometries. A new
frontier script now shows a **path-sum DAG-ensemble** geometry-superposition
signal at about `4.4%` contrast, but that script is not staggered. So this
remains untested on the actual staggered architecture.

**The experiment:** Evolve a staggered fermion on a superposition of two
graph geometries (e.g., a graph with vs without a massive object). Measure
whether the detector state depends on which geometry was traversed. If the
states are distinguishable (TV > 0), this demonstrates that matter probes
geometry at the quantum level — a direct connection to quantum gravity.

**Why Nature cares:** This is the discrete analog of the BMV (Bose-Marletto-
Vedral) experiment for quantum gravity. If staggered fermions on a
superposition of geometries produce entanglement, it demonstrates that
gravity must be quantum in this model.

**Risk:** Medium. The chiral walk proved the concept; the question is whether
the staggered architecture preserves it. The staggered structure is more
rigid (no coin freedom) which could help or hinder.

### 2. Area-Law Entropy from Self-Gravity
**HIGH PRIORITY — Untested Nature backlog item**

The staggered lane now has self-gravity with real contraction (w=0.40-0.76)
on graphs. Compute von Neumann entropy of a bipartition of the self-
gravitating field. Does S scale with boundary area (area law) or volume?

The TM showed sub-area-law entropy (saturates at ln(2)). If the staggered
self-gravitating state shows area-law scaling, this is a direct connection
to holography and black hole thermodynamics.

**Why Nature cares:** Area-law entropy → holographic principle → the
information paradox. Demonstrating area-law scaling from a simple discrete
model with self-gravity would be a genuine breakthrough.

**Risk:** Medium-low. The measurement (von Neumann entropy of a bipartition)
is straightforward. The question is whether the staggered self-gravitating
dynamics produces the right scaling.

### 3. Sublattice Parity = Staggered γ₅: Decoherence Protection
**HIGH PRIORITY — Transfers mirror lane's strongest result**

The mirror/Z₂ lane proved that Z₂ symmetry breaks the CLT ceiling and
preserves rank-2 information channels (MI = 0.773, 6x random). The
staggered lattice has a built-in Z₂ structure: even/odd sublattice parity
= staggered γ₅.

**The test:** Does the staggered Z₂ provide the same decoherence protection
as the mirror Z₂? If the staggered sublattice parity preserves a rank-2
channel in a path-sum sense, the mirror program's strongest result transfers
directly to the current mainline.

**Why Nature cares:** It unifies two seemingly different programs (algebraic
symmetry constraints on DAGs vs. lattice field theory) under a single
principle: discrete parity symmetry preserves quantum coherence.

**Risk:** Low. The mirror measurement infrastructure exists; it just needs
to be applied to the staggered lattice.

### 4. Chirality-Gravity Coupling on Staggered Lattice
**MEDIUM PRIORITY — Testable spin-gravity prediction**

The 3+1D chiral walk shows 117% chirality-gravity asymmetry: ψ+ deflects
3.8x more than ψ−. The staggered lattice has sublattice parity (staggered
γ₅) but nobody has tested whether gravity depends on the sublattice
composition of the initial state.

**The test:** Prepare states localized on even-only vs odd-only sublattice
sites. Evolve under self-gravity. Does the force differ? If so, this is a
testable prediction: matter on different sublattice parities couples to
gravity differently.

**Why Nature cares:** Spin-gravity coupling is an active experimental search.
A clean theoretical prediction from a discrete model would be directly
relevant to precision gravity experiments.

**Risk:** Medium. The effect might be too small to measure, or the sublattice
composition might not be a good analog of spin.

### 5. Causal Set Metric Recovery on Staggered DAG
**MEDIUM PRIORITY — Low-effort, high-value test**

The TM achieves causal set metric recovery r=0.997, the chiral walk r=0.956.
The staggered DAG probe shows forward propagation (frac=0.1266) but never
measures metric recovery. This is a standard causal-set-theory diagnostic
that takes ~20 lines of code.

**Why Nature cares:** Causal set theory is a major quantum gravity program.
Demonstrating that staggered fermions recover the causal set metric would
bridge lattice field theory and causal set theory.

**Risk:** Low. The measurement is well-defined. The question is whether
the staggered propagator on a DAG preserves enough causal structure.

### 6. 2+1D Chiral Achromatic Mystery
**MEDIUM PRIORITY — Design insight for fixing 3+1D**

The 2+1D chiral walk achieves broadband achromatic gravity while 1+1D has
CV=2.66. Why? The factorized coin in 2+1D has only one spatial pair, so the
mixing period interacts differently with the lattice. Understanding this
could unlock the 3+1D achromatic problem.

**Why Nature cares:** If the mechanism is understood, it could lead to a
coin-based architecture that has both strict v=1 light cone AND achromatic
gravity — escaping the impossible triangle.

**Risk:** High. This is a theoretical mystery, not a straightforward test.

### 7. Valley-Linear Action Constraint on Source Sector
**LOWER PRIORITY — Could fix G_eff mismatch**

The ordered lattice lane proved that valley-linear S=L(1-f) is the unique
action consistent with Lorentz + Newton at leading order. This action-
uniqueness theorem has NEVER been applied to the staggered lane's source
sector. Could narrow the admissible Φ law on graphs.

### 8. Weak-Coupling Full Battery
**IMMEDIATE — Needed to test whether the weak-coupling regime can be frozen**

Run the complete 17-card and supplementary batteries at G=10 (the sweet
spot for sign-sensitive irregular-graph behavior). Currently only tested with
the dedicated weak-coupling battery script, where the effect is strong but not
yet universal (`14/15`, not `15/15`).

## Cross-Architecture Table

| Feature | Chiral 1+1D | Mirror Z₂ | Staggered | TM |
|---------|-------------|-----------|-----------|-----|
| Born | 1e-16 | 3e-15 | 1e-15 | 4e-17 |
| KG | exact | N/A | exact | N/A |
| Light cone | strict v=1 | N/A | LR 97% | N/A |
| Gauge | AB 88.5% | N/A | pers. curr. | N/A |
| Geometry super. | TV=0.039 | N/A | **UNTESTED on staggered** | N/A |
| Causal metric | r=0.956 | N/A | **UNTESTED** | r=0.997 |
| Self-gravity | N/A | N/A | w=0.40-0.76 | N/A |
| MI | N/A | 0.773 | 0.164-0.615 | N/A |
| Decoherence | 82.8% (2+1D) | near-flat | 23%→18% | N/A |
| Area entropy | N/A | N/A | **UNTESTED** | sub-area |
| Spin-gravity | 117% asym | N/A | **UNTESTED** | N/A |
| Dynamic growth | N/A | N/A | partial | works |

The **UNTESTED** cells are the highest-leverage experiments in the repo.
