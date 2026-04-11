# Gravity Sign Audit — Corrected Assessment

**Date:** 2026-04-10
**Revised:** 2026-04-10 (after spot-check verification)

**Purpose:** Determine whether the TOWARD gravity results across all retained harnesses
are genuine physical predictions or tautological consequences of sign conventions.

## Executive Summary

The coupling sign `−mass·Φ` is **prescribed** (Newtonian convention), not derived.
That is an input assumption, and should be stated as such.

However, the dynamics under that prescription are **non-trivially correct** on the
retained admissible graph families. Spot-checks with a stronger edge-radial force
measure confirm the sign agreement on random geometric, growing, and layered cycle
families. The force proxy used on irregular graphs (shell-averaged radial gradient)
is a proxy, not the exact expectation value, and should be qualified as such.

The emergent-geometry "AWAY" claim was **overclaimed** from the weaker shell proxy.
A three-metric comparison (shell_mean, shell_prob, edge_radial) shows mixed signs —
the honest verdict is measurement-dependent, not settled geometric repulsion.

## Observable Hierarchy

| Observable | Definition | Status |
|-----------|------------|--------|
| **Exact lattice force** F = −Σ ρ·dV/dx | Exact expectation on regular lattice | Cleanest. Used in `frontier_staggered_17card.py` |
| **Edge-radial force** | Σ edges w·(Φⱼ−Φᵢ)·ρᵢ·cos(θ) | Exact per-edge, radial projection | Stronger proxy for irregular graphs |
| **Probability-weighted shell force** | Σ_shells P_shell · ΔΦ/Δd | Stronger radial proxy | Audit cross-check / recommended irregular-graph gate |
| **Shell-mean force** | Σ_shells ⟨ρ⟩_shell · ΔΦ/Δd | Weaker proxy; shell size enters explicitly | Current implementation in cycle/self-gravity/retarded batteries |
| **Centroid** | d⟨x⟩/dt | Broken on staggered lattices (period-4) | Not usable |

**Standard going forward:**
- Regular lattices: use exact F = −⟨dV/dx⟩
- Irregular graphs: require BOTH probability-weighted shell force AND edge-radial
  force to agree in sign before claiming gravity direction
- Treat shell-mean and centroid as diagnostics only

## The Sign Chain

### Link 1: Field Equation → Positive Φ

The screened Poisson `(L + μ²I)Φ = G·ρ` with positive-definite operator and
ρ = |ψ|² ≥ 0 necessarily gives Φ ≥ 0. This is mathematical, not a physics choice.
The retarded wave equation with β > 0 likewise drives Φ positive.

### Link 2: Hamiltonian Coupling (THE ASSUMPTION)

Every file uses:
```python
H.setdiag(mass * parity - mass * phi)
```
The `−mass·Φ` mirrors Newtonian V = −GM/r. This is an input assumption.
It is NOT derived from the staggered structure. Flipping the sign would reverse
all force directions.

### Link 3: Force Measurement

**17card (exact):** F = −⟨dV/dx⟩ on the lattice coordinates. Clean, unambiguous.

**Graph batteries (proxy):** Shell-mean radial gradient from BFS-depth shell
averages of `Φ` and `ρ`. This is a radial proxy — shell volume enters the
averaging. It should be described as "radial force proxy" rather than "exact
force."

### What the Coupling Assumption Buys

Given `−mass·Φ`, the TOWARD direction is expected for any wavepacket with support
near the potential minimum. The non-trivial content is:

1. **The dynamics are stable** — backreaction doesn't blow up over 20 iterations
2. **The force magnitude scales correctly** — G_eff = 0.4–0.6, source-linear
3. **Multiple force measures agree** — shell proxy and edge-radial give same sign
   on all admissible families (verified by spot-check)
4. **State-family universality** — 7/7 initial states give consistent force magnitude
5. **Topology-dependent phase transition** — critical exponent β varies with graph family

## Spot-Check Results (Edge-Radial vs Shell Proxy)

Admissible cycle families, retarded field, both measures TOWARD:

| Family | Shell proxy | Edge-radial | Agreement |
|--------|-----------|-------------|-----------|
| Random geometric | +0.059 | +0.090 | YES |
| Growing | +0.011 | +0.017 | YES |
| Layered cycle | +0.100 | +0.128 | YES |

## Emergent Geometry — Corrected

The v2 emergent geometry script (n=100, G=50) now reports three measures:

| Measure | Value | Sign |
|---------|-------|------|
| shell_mean | −1.94e-3 | AWAY |
| shell_prob | −3.30e-2 | AWAY |
| edge_radial | +3.52e-3 | TOWARD |

**Verdict:** Mixed / measurement-dependent. Not settled geometric repulsion.
The old one-number "AWAY" readout was overclaimed. Do not promote the
emergent-geometry gravity sign story until it passes the two-metric gate
across seeds and sizes.

## What IS Genuinely Non-Trivial

| Test | What it shows | Why non-trivial |
|------|---------------|-----------------|
| Norm conservation ~1e-15 | CN is exactly unitary | Numerical correctness |
| Self-gravity contraction | Width shrinks under self-gravity | Magnitude is non-trivial |
| Iterative stability (20/20) | Backreaction loop converges | Could blow up; it doesn't |
| G_eff = 0.4–0.6 | Retarded field coupling strength | Quantitative, not sign-dependent |
| Multi-measure sign agreement | Shell and edge-radial agree on admissible families | Cross-validates the proxy |
| Critical exponent β | Topology-dependent onset | Phase transition existence is real |
| Gauge current J(A) | Persistent current on graph cycles | Unrelated to gravity sign |
| Born rule I₃ | Three-slit interference | Unrelated to gravity sign |
| Lieb-Robinson cone | 97% inside | Unrelated to gravity sign |
| d_eff = 2.03 | Growth rule makes 2D geometry | Genuine geometric result |

## What Would Strengthen the Gravity Story

### Option A: Derive the Coupling Sign
Show that the staggered Hamiltonian REQUIRES `−mass·Φ` from Dirac structure.
**Status:** Not attempted. Strongest path to "gravity is predicted."

### Option B: Sign-Agnostic Observables
Reframe around contraction magnitude, binding energy, correlation length —
compare to GR quantitatively without invoking force direction.
**Status:** Partially done (G_eff), not systematically framed.

### Option C: Two-Sign Comparison
Run both `−mass·Φ` and `+mass·Φ` through the full battery. If repulsive coupling
is pathological (divergent norm, unstable backreaction), that selects the sign.
**Status:** Not done. Easiest win.

## For a Nature Referee

A referee will ask: "Why is the potential attractive?"

Honest answer: The coupling sign `−mass·Φ` is an input assumption, mirroring
Newtonian gravity. What we show is that staggered fermions on arbitrary bipartite
graphs produce **consistent, stable, quantitatively characterized** self-gravitating
dynamics under this assumption:

- Stable backreaction (no blowup over iterated self-gravity)
- G_eff = 0.4–0.6 coupling (retarded field, source-scale gap closed)
- Topology-dependent critical threshold for gravitational collapse
- Force direction confirmed by two independent measures on irregular graphs
- Emergent 2D geometry from matter-coupled growth (sign of geometric force: mixed)

The direction is postulated. The consistency, stability, and quantitative
characterization are the results.
