# Staggered Fermion + Parity-Coupled Gravity — Complete Card

**Date:** 2026-04-11 (parity coupling rewrite)
**Coupling:** `H_diag = (m + Phi) * epsilon(x)` — scalar 1x1 in spin-taste
**Reference:** Zache et al. (Quantum 2020), Dempsey et al. (arXiv:2501.10862)

## Coupling Structure

The gravitational potential enters the staggered Hamiltonian through the
SAME parity factor epsilon(x) as the mass term, because both are scalar
(1x1 in spin-taste) couplings to psi-bar-psi in the continuum:

```
H_diag = (m + Phi(x)) * epsilon(x)
```

This is NOT the same as the identity coupling `m*epsilon + Phi` used in
earlier versions. Under parity coupling:
- Phi > 0 WIDENS the mass gap (slows propagation) -> repulsion
- Phi < 0 NARROWS the mass gap (speeds propagation) -> attraction
- The sign of gravity is a PREDICTION of the Dirac structure

The screened Poisson equation (L + mu^2)Phi = G*rho with positive-definite
operator and positive source rho = |psi|^2 always gives Phi >= 0. Under
self-gravity, the sign chain is:

1. |psi|^2 >= 0 -> Phi >= 0 (mathematical, not a choice)
2. (m + Phi)*epsilon modulates the mass gap (from Dirac structure)
3. Gap modulation creates velocity gradient -> force toward high-density regions
4. Force direction is TOWARD (attraction) as a dynamical prediction

Verified: inverting Phi -> -Phi inverts the force (AWAY). The old identity
coupling gave TOWARD regardless of Phi sign (tautological).

## 1. Canonical 17-Card (frontier_staggered_17card.py)

Operating point: mass=0.3, g=50.0, S=5e-4, dt=0.15

### 1D (n=61): 17/17

| Row | Test | Value | Status |
|-----|------|-------|--------|
| C1 | Sorkin Born |I3|/P | 1.28e-15 | PASS |
| C2 | TV distance | 0.92 | PASS |
| C3 | Zero-source force | 0.00 | PASS |
| C4 | F proportional to M | R^2=0.917 | PASS |
| C5 | Force TOWARD | +5.75e-5 | PASS |
| C6 | Decoherence | 0.230->0.177 | PASS |
| C7 | Mutual information | 0.165 | PASS |
| C8 | Purity CV | 0.011 | PASS |
| C9 | Force stable across N | all TOWARD | PASS |
| C10 | Distance (force) | 5/5 TW | PASS |
| C11 | KG dispersion | R^2=0.997 | PASS |
| C12 | Gauge (persistent current) | J=2.14e-3 | PASS |
| C13 | Force achromaticity | CV=0.000 | PASS |
| C14 | Equivalence (a=F/m) | CV=0.000 | PASS |
| C15 | Force vs depth | all TOWARD | PASS |
| C16 | Multi-observable | 1/2 | PASS |
| C17 | State families (6/6) | all TOWARD | PASS |
| | **Norm** | **5.55e-16** | |

### 3D Convergence

| Row | n=9 (729) | n=11 (1331) | n=13 (2197) |
|-----|-----------|-------------|-------------|
| C1 Sorkin | 2.62e-15 | 2.75e-15 | 3.11e-15 |
| C4 F~M | R^2=1.000 | R^2=1.000 | R^2=0.999 |
| C5 Force | +1.29e-3 TW | +5.44e-4 TW | +3.18e-4 TW |
| C6 Decoh | 0.754->0.164 | 0.699->0.068 | 0.657->0.085 |
| C12 Gauge | 3D torus 3.69e-3 | 3D torus 2.27e-3 | 3D torus 1.49e-3 |
| C17 families | 6/6 (incl anti) | 4/4 | 4/4 |
| **Score** | **17/17** | **17/17** | **17/17** |

## 2. Cycle-Bearing Graph Battery (frontier_staggered_cycle_battery.py)

DT=0.12, MASS=0.3, G=8.0, mu2=0.22, N_ITER=15

| Row | random_geo (36) | growing (48) | layered_cycle (24) |
|-----|-----------------|--------------|---------------------|
| B1 Zero-source | F=0, Phi=0 PASS | F=0, Phi=0 PASS | F=0, Phi=0 PASS |
| B2 Linearity | R^2=0.991 PASS | R^2=0.997 PASS | R^2=0.985 FAIL |
| B3 Additivity | res=2e-16 PASS | res=2e-16 PASS | res=2e-16 PASS |
| B4 Force | +1.87e-2 TW PASS | +3.42e-3 TW PASS | +5.83e-2 TW PASS |
| B5 Iter stab | 15/15 TW PASS | 15/15 TW PASS | 15/15 TW PASS |
| B6 Norm | 7e-16 PASS | 1e-16 PASS | 2e-16 PASS |
| B7 Families | 3/3 TW PASS | 3/3 TW PASS | 3/3 TW PASS |
| B8 Gauge | sin R^2=1.00 PASS | sin R^2=0.95 PASS | sin R^2=0.97 PASS |
| B9 G_eff | 58.7 | 129.6 | 29.2 |
| **Score** | **9/9** | **9/9** | **8/9** |

B2 marginal on layered_cycle: parity coupling introduces mild nonlinearity
in force-vs-source because (m+Phi)*epsilon couples mass and field multiplicatively.

## 3. Self-Gravity Probe (frontier_staggered_self_gravity.py)

G_SELF=50.0, mu2=0.22, N_ITER=20. No external source.

| Row | random_geo (36) | growing (48) | layered_cycle (24) |
|-----|-----------------|--------------|---------------------|
| S1 Force sign | 20/20 TW PASS | 20/20 TW PASS | 20/20 TW PASS |
| S2 Contraction | **w=0.629** PASS | **w=0.598** PASS | **w=0.436** PASS |
| S3 Norm | 2e-16 PASS | 4e-16 PASS | 4e-16 PASS |
| S4 Stability | 0 flips PASS | 0 flips PASS | 0 flips PASS |
| S5 Families | 3/3 TW PASS | 3/3 TW PASS | 3/3 TW PASS |
| **Score** | **5/5** | **5/5** | **5/5** |

**Contraction is the biggest improvement.** Under the old identity coupling,
the wavepacket EXPANDED (w=1.68). Under parity coupling, it CONTRACTS to
w=0.44-0.63 — gravity now works as expected.

## 4. Retarded/Hybrid Family Closure (frontier_two_field_retarded_family_closure.py)

Retarded field: d^2 Phi/dt^2 = -c^2(L+mu^2)Phi - gamma*dPhi/dt + beta*source
Memory: dm/dt = (rho - m)/tau_mem

| Row | random_geo (36) | growing (48) | layered (24) | causal_dag (36) |
|-----|-----------------|--------------|--------------|-----------------|
| R1 Zero-src | PASS | PASS | PASS | PASS |
| R2 Linearity | R^2=1.000 | R^2=1.000 | R^2=1.000 | R^2=1.000 |
| R3 Additivity | PASS | PASS | PASS | PASS |
| R4 Force | +2.98 TW | +1.07 TW | +4.06 TW | +3.55 TW |
| R5 Iter stab | 30/30 TW | 25/30 TW FAIL | 30/30 TW | 30/30 TW |
| R6 Norm | 2e-16 | 2e-16 | 7e-16 | 1e-16 |
| R7 Closure | 3/3 TW | 3/3 TW | 3/3 TW | 3/3 TW |
| R8 Gauge | sin R^2=1.00 | sin R^2=0.95 | sin R^2=0.97 | no cycle, SKIP |
| R9 G_eff | 0.4 | 0.4 | 0.4 | 0.7 |
| **Score** | **9/9** | **8/9** | **9/9** | **8/9** |

G_eff = 0.4-0.7 across all families. Source-scale gap closed.

## 5. Iterative Endogenous Closure (frontier_staggered_iterative_closure.py)

20-iteration backreaction loop with G=8.0.

| Family | Force | Norm | Phi settled | Families |
|--------|-------|------|-------------|----------|
| random_geo (36) | 20/20 TW, CV=0.12 | 3e-16 | dphi=0.012 | 3/3 TW |
| growing (48) | 20/20 TW, CV=0.93 | 2e-16 | dphi=0.011 | 3/3 TW |

## 6. Two-Field Wave (frontier_two_field_wave.py, rerun-corrected)

Wave-equation Phi + staggered psi, parity coupling.

| Family | Force | Norm | Phi bounded | Families |
|--------|-------|------|-------------|----------|
| random_geo (36) | 30/30 TW | 4e-16 | max=0.27 | 2/3 TW |
| growing (48) | 30/30 TW | 2e-16 | max=0.16 | 3/3 TW |
| layered (24) | 30/30 TW | 2e-16 | max=0.34 | 2/3 TW |

Hard scores after the clean-family rerun: random geometric `4/5`, growing
`5/5`, layered `4/5`.

## 7. Graph Portability (frontier_staggered_graph_portability.py)

| Family | Born | Norm | Force | F~M | Achrom | Equiv | Robust | Gauge |
|--------|------|------|-------|-----|--------|-------|--------|-------|
| random_geo (36) | 6e-16 | 4e-16 | +3.6e-3 TW | R^2=1.0 | CV=0 | CV=0 | 3/3 | 5.1e-3 |
| growing (48) | 5e-16 | 1e-15 | +3.6e-3 TW | R^2=1.0 | CV=0 | CV=0 | 3/3 | 9.1e-3 |
| layered_dag (36) | 6e-16 | 0 | +3.8e-3 TW | R^2=1.0 | CV=0 | CV=0 | 3/3 | N/A |
| **Score** | **8/8** | **8/8** | **8/8** |

## 8. Critical Exponents (frontier_critical_exponents.py)

| Family | n | G_crit | beta | R^2 | Status |
|--------|---|--------|------|-----|--------|
| random_geo s10 | 100 | 2.0 | 0.73 | 0.97 | fit |
| growing n64 | 64 | 14.0 | 0.37 | 0.95 | fit |
| layered_cycle 8x8 | 64 | 5.0 | 0.33 | 0.92 | fit |
| random_geo s8 | 64 | 1.0 | - | - | degenerate |
| causal_dag 10x6 | 55 | 1.0 | - | - | degenerate |
| causal_dag 8x8 | 57 | 1.0 | - | - | degenerate |

beta ranges 0.33-0.73 (NOT mean-field 0.5) — topology-dependent.

## Complete Score Summary

| Harness | Scores | Total rows |
|---------|--------|-----------|
| 17-card 1D | 17/17 | 17 |
| 17-card 3D n=9 | 17/17 | 17 |
| 17-card 3D n=11 | 17/17 | 17 |
| 17-card 3D n=13 | 17/17 | 17 |
| Cycle battery | 9+9+8 = 26/27 | 27 |
| Self-gravity | 5+5+5 = 15/15 | 15 |
| Retarded closure | 9+8+9+8 = 34/36 | 36 |
| Iterative closure | PASS on 2 families | ~10 |
| Two-field wave | 4+5+4 = 13/15 | 15 |
| Graph portability | 8+8+8 = 24/24 | 24 |
| **TOTAL** | **~183/190** | |

## What Changed: Identity -> Parity Coupling

Old (all scripts before 2026-04-11):
```python
H.setdiag(mass * parity - mass * phi)    # identity coupling
```

New (all scripts after parity rewrite):
```python
H.setdiag((mass + phi) * parity)         # parity (scalar 1x1) coupling
```

### Key improvements under parity coupling

| Metric | Identity (old) | Parity (new) | Why |
|--------|---------------|--------------|-----|
| Self-gravity width | 1.68 (EXPAND) | 0.44-0.63 (CONTRACT) | Gap modulation creates attraction |
| Sign selection (exact lattice) | TOWARD under both +/- Phi | TOWARD for Phi>0, AWAY for Phi<0 | Direct well/hill test is sign-selective |
| Physical mechanism | Uniform energy shift | Mass-gap modulation | Correct Dirac coupling |
| Force direction (exact lattice) | Tautological (prescribed) | Sign-sensitive (well/hill split) | Only on canonical cubic card so far |

### What is derived (not assumed)

1. **Dirac dispersion** E^2 = m^2 + sin^2(k) — from staggering phases
2. **Born rule** I3 at machine zero — from CN linearity
3. **Force direction on exact lattice** — well/hill sign test splits cleanly
   under parity coupling on the canonical cubic card (only)
4. **Achromatic force** CV=0.000 — F = -<dV/dz> has no k-dependence
5. **Equivalence** a = F/m mass-independent — CV=0.000
6. **Gauge invariance** persistent current J(A) — from Hamiltonian structure
7. **Self-gravity contraction** w_f/w_0 < 1 — from iterated backreaction
8. **Norm conservation** ~1e-15 — from CN unitarity

NOTE: "Force direction derived" applies only to the exact-lattice canonical
card. On irregular graph families, the retained shell/edge-radial proxies are
strong structural interacting-field results but do not yet constitute a clean
directional-gravity claim. One frozen graph-native directional observable is
still needed for full irregular-graph sign closure.

### What is still assumed

1. **Screened Poisson equation** (L + mu^2)Phi = G*rho — not derived from the model
2. **Coupling constant G** — free parameter
3. **Screening mass mu** — free parameter
4. **Static lattice** — graph is fixed, not dynamically grown
5. **The specific graph families** — bipartite structure is required, but which graph is not predicted

## Caveats

1. **B2 linearity marginal on layered_cycle** (R^2=0.985) — parity coupling
   introduces mild nonlinearity because (m+Phi)*epsilon couples multiplicatively.

2. **R5 growing family** — 25/30 TOWARD (5 AWAY iterations). Growing graphs
   have less regular structure; the retarded field oscillates more.

3. **Critical exponents** — 3 of 6 configurations are degenerate (G_crit at
   floor). Finite-size scouts, not definitive universality evidence.

4. **Shell force proxy** — on irregular graphs, the shell-averaged force is a
   radial proxy (shell size enters the observable). The 17-card lattice force
   F = -<dV/dx> is the cleanest observable. On graphs, require both shell and
   edge-radial measures to agree before claiming direction.

5. **Emergent geometry** — force direction is mixed/measurement-dependent on
   grown graphs. Not included in this card until it passes a two-metric gate
   across seeds and sizes.
