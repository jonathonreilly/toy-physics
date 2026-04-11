# Nature Backlog

**Date:** 2026-04-10
**Status:** Active

## Prerequisite (STRUCTURAL ONLY)

One canonical endogenous two-field harness that simultaneously closes
R1-R7 + R9 on both cycle-bearing and causal-DAG families.

**Current best sibling result:** `9/9`, `9/9`, `9/9` on the three retained
cycle-bearing families plus `8/9` on the causal DAG (`R8` gauge N/A). The
retarded family-closure sibling is now retained on the three cycle-bearing
families; the DAG stays structurally `N/A` for gauge.
**Script:** `frontier_two_field_retarded_family_closure.py`
**Caveat:** after the two-sign audit, this prerequisite should be read as a
structural interacting-field closure attempt, not as evidence that the
irregular graph families predict attractive gravity direction. On those
families the retained sign rows are audited radial proxies and are not
sign-selective.

## Tier 0: Direction / Observable Gap

### 0. Derive or Select the Coupling Sign
Show that the attractive sign is required by the staggered / Dirac structure,
or find one graph-native irregular observable that actually distinguishes
attractive from repulsive coupling.
**Status:** PARTIALLY CLOSED (2026-04-11).
- The identity coupling `m·ε − m·Φ` was wrong. Replaced with the
  literature-correct parity coupling `(m + Φ)·ε(x)` (Zache et al. 2020).
- On the **exact-lattice canonical card**, well/hill sign test now splits
  cleanly: TOWARD for V<0, AWAY for V>0. This is a genuine sign-selective
  result on the cubic lattice.
- On **irregular graph families**, the retained shell/edge-radial proxies
  are strong structural interacting-field results but do not yet constitute
  a clean directional-gravity claim. The new endogenous same-surface probe
  failed (`0/9`, `0/9`, `4/9`), so one frozen graph-native directional
  observable is still needed. See `IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md`.
- Self-gravity now contracts strongly (w=0.44-0.63) under parity coupling,
  vs expanding (w=1.68) under the old identity coupling.
**Scripts:** `frontier_correct_coupling.py`, `frontier_two_sign_parity.py`

## Tier 1: Emergent Geometry (Nature-level)

### 1. Graph Growth Rule → Emergent Dimensionality + Gravity
Start from a seed, grow a graph by a local rule (preferential attachment
to high-|ψ|² nodes), evolve staggered ψ on the grown graph, measure
whether the effective geometry matches curved spacetime.
**Status:** EXPLORATORY POSITIVE / PARTIAL REOPEN.
Single-seed growth gives `d_eff≈2.03` and strong matter clustering, and the
new `G` sweep reopens a narrow strong-coupling window (`G=100` robust TOWARD),
but node density does not track `Φ` cleanly, `d_eff` does not vary
systematically with coupling, and the gravity sign is mixed away from that
window.
This is not yet a Nature-ready geometry result.

### 2. Einstein Equations from Graph Backreaction
Compute Ollivier curvature before/after self-gravitating matter equilibrates.
Does the curvature change match Gμν = 8πG Tμν?
**Status:** NOT STARTED

## Tier 2: Qualitative Breakthroughs

### 3. Hawking-like Radiation from Collapse
At G slightly above G_crit, measure probability flux leaking from the
collapsed state. Is it thermal? Does T ∝ 1/G?
**Status:** NOT STARTED

### 4. Area-Entropy Law from Self-Gravity
Does the entanglement entropy of the collapsed region scale with
BOUNDARY (area law) rather than volume?
**Status:** NOT STARTED

## Tier 3: Strong Quantitative Results

### 5. Universal Critical Exponents
Does β depend on graph topology? Different β = new universality class.
**Status:** EXPLORATORY finite-size scout only. Current scans suggest
topology-dependent onset fits, but they are not yet a retained universality
claim and at least one DAG configuration is degenerate.

### 6. Gravitational Lensing
Deflection of test wavepacket by self-gravitating blob. Does α ∝ M/b?
**Status:** NOT STARTED (Schwarzschild probe failed due to no equilibrium)

## Tier 4: Methodological

### 7. Dynamic Growth + Self-Gravity
Add nodes during evolution (after record formation). Does staggered
physics survive on the grown graph?
**Status:** NOT STARTED

### 8. 3D Self-Gravity with 1/r Potential
Run self-gravity on 3D cubic staggered (n=9). Cleaner than 2D log(r).
**Status:** NOT STARTED

### 9. Causal One-Way Propagation
Build staggered evolution that's both unitary AND causal. Kähler-Dirac
exterior derivative on cell complex.
**Status:** DAG probe shows backward propagation not blocked by Hermitian H.

### 10. Information-Theoretic Axiom Derivation
Derive the axioms from a complexity-minimization principle.
**Status:** NOT STARTED

### 11. User's Breakthrough Target
One canonical endogenous two-field on cycle + DAG. All 9 rows.
**Status:** STRUCTURALLY CLOSED on the retained cycle-bearing families
(`9/9`, `9/9`, `9/9`) and `8/9` on the DAG operating point, but not yet a
directional-gravity closure because the irregular same-surface probe failed
and the sign rows are not sign-selective.
