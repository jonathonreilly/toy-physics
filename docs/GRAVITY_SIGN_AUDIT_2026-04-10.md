# Gravity Sign Audit — Corrected Assessment

**Date:** 2026-04-10
**Revised:** 2026-04-10 (after spot-check verification)

**Purpose:** Determine whether the TOWARD gravity results across all retained harnesses
are genuine physical predictions or tautological consequences of sign conventions.

## Executive Summary

The coupling sign `−mass·Φ` is **prescribed** (Newtonian convention), not derived.
That is an input assumption, and should be stated as such.

The later two-sign comparison makes the irregular-graph implication sharper:
the current shell-radial and edge-radial sign measures are **not sign-selective**.
They can stay inward under both attractive and repulsive coupling because they are
dominated by the source-centered `Φ` profile. The exact lattice force on the cubic
card remains a genuine dynamical-response observable; the irregular graph sign rows
do not.

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
2. **The force magnitude / source scale is non-trivial** — G_eff = 0.4–0.6,
   source-linear under the retarded law
3. **Multiple structural measures agree under the prescribed sign** — shell proxy
   and edge-radial can agree on admissible families, but this no longer counts as
   sign selection after Option C
4. **State-family structure is non-trivial** — retained families can share the same
   interaction profile without destabilizing the field law
5. **Topology-dependent phase transition** — critical exponent β varies with graph family

## Spot-Check Results (Edge-Radial vs Shell Proxy)

Admissible cycle families, retarded field, both measures inward under the
prescribed attractive sign:

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
| Multi-measure sign agreement | Shell and edge-radial agree on admissible families | Cross-validates proxy BUT see Option C caveat below |
| Critical exponent β | Topology-dependent onset | Phase transition existence is real |
| Gauge current J(A) | Persistent current on graph cycles | Unrelated to gravity sign |
| Born rule I₃ | Three-slit interference | Unrelated to gravity sign |
| Lieb-Robinson cone | 97% inside | Unrelated to gravity sign |
| d_eff = 2.03 | Growth rule makes 2D geometry | Genuine geometric result |

## What Would Strengthen the Gravity Story

### Option A: Derive the Coupling Sign ← DONE — BREAKTHROUGH

The literature (Zache et al. 2020, Dempsey et al. 2025) shows that a scalar
potential in the staggered Hamiltonian must couple through the SAME parity
factor ε(x) as the mass (both are 1⊗1 in spin-taste):

    CORRECT:  H_diag = (m + Φ) · ε(x)      ("parity coupling")
    WRONG:    H_diag = m·ε ± m·Φ            ("identity coupling" — all current scripts)

The full GR coupling via the lapse function gives:

    H_grav = √N · H_flat · √N,   N = 1 + Φ/m   ("lapse coupling")

**Result: Both correct couplings DISTINGUISH attractive from repulsive.**

| Coupling | Well (V<0) | Hill (V>0) | Distinguishes? |
|----------|-----------|-----------|----------------|
| identity (current) | TOWARD +0.61 | TOWARD +0.48 | NO |
| parity (correct) | TOWARD +2.08 | AWAY −0.78 | YES |
| lapse (full GR) | TOWARD +0.61 | AWAY −1.78 | YES |

Under parity coupling, V<0 narrows the mass gap locally → faster
propagation toward the potential minimum → TOWARD. V>0 widens the gap →
slower propagation → AWAY. This is a genuine dynamical prediction:
**the sign of gravity emerges from the Dirac mass-gap structure.**

Additionally, parity coupling CONTRACTS the wavepacket (w_f/w_0 = 0.94)
under self-gravity, while identity EXPANDS it (1.68). Gravity should
contract — the correct coupling gets the right physics.

**Script:** `frontier_correct_coupling.py`

**Action required:** All retained batteries must be updated to use parity
coupling `H_diag = (m + Φ)·ε` instead of `H_diag = m·ε − m·Φ`.

### Option B: Sign-Agnostic Observables
Reframe around contraction magnitude, binding energy, correlation length —
compare to GR quantitatively without invoking force direction.
**Status:** Partially done (G_eff), not systematically framed.

### Option C: Two-Sign Comparison ← DONE
Run both `−mass·Φ` and `+mass·Φ` through the full battery. If repulsive coupling
is pathological (divergent norm, unstable backreaction), that selects the sign.

**Result: BOTH SIGNS ARE COMPLETELY STABLE.**
- Norm drift: identical (machine epsilon)
- Width: both expand comparably (no contraction under either sign at G=50, N=20)
- Φ convergence: both stable
- Energy: bounded under both (attractive E<0, repulsive E>0 — just the diagonal shift)
- Spectral range: comparable
- **Force sign: BOTH give TOWARD on all three measures.**

The last point is the most damning: even repulsive coupling gives positive
shell/edge-radial force. The force observables are measuring the Φ profile
shape (positive, peaked at source), not the wavepacket's dynamical response
to the potential. The shell force `Σ ρ·∇Φ` is always positive because Φ
is always positive and peaked inward — regardless of whether Φ enters the
Hamiltonian with + or − sign.

**Conclusion:** Consistency does NOT select the coupling sign at these parameters.
The sign is a free parameter. The force observables do not distinguish the signs
because they measure the field shape, not the dynamical response.

**Script:** `frontier_two_sign_comparison.py`

## For a Nature Referee

A referee will ask: "Why is the potential attractive?"

Honest answer: The coupling sign `−mass·Φ` is an input assumption, mirroring
Newtonian gravity. The two-sign comparison (Option C) confirms this: both
`−mass·Φ` and `+mass·Φ` produce stable, norm-conserving dynamics with bounded
energy and convergent backreaction. Consistency does not select the sign.

Furthermore, the shell/edge-radial force observables give TOWARD under
BOTH signs — they measure the field profile shape, not the dynamical
response to the potential. This means the "force direction" rows in the
retained batteries are not testing gravity; they are testing that
(L+μ²)⁻¹ρ peaks at the source, which is guaranteed.

What we DID show (sign-agnostic, would survive this critique):
- Staggered fermions on bipartite graphs support consistent self-gravitating
  dynamics under EITHER coupling sign (stable backreaction, norm conservation)
- G_eff = 0.4–0.6 coupling magnitude (retarded field, source-scale gap closed)
- Topology-dependent critical threshold for gravitational collapse (β varies)
- Emergent 2D geometry from matter-coupled growth (d_eff = 2.03)
- Gauge invariance, Born rule, Lieb-Robinson causality on arbitrary graphs

The force DIRECTION is not among these results. The force MAGNITUDE and
the existence of a phase transition are.

The direction is postulated. The consistency, stability, and quantitative
characterization are the results.
